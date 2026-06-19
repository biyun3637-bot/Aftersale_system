"""FastAPI routing layer."""
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from agent.graph import run_pipeline
from agent.response_gen import generate_review_response
from agent.refund_exec import execute_refund
from api_adapters.mock_data import DEMO_SCENARIOS, MOCK_ORDERS
import db as database

router = APIRouter()

# Initialize ticket counter from existing DB to avoid ID conflicts after restart
_ticket_counter = 0
try:
    max_id = database.get_max_ticket_id()
    if max_id:
        _ticket_counter = int(max_id.split("-")[1])
except Exception:
    _ticket_counter = 0


def _next_ticket_id() -> str:
    global _ticket_counter
    _ticket_counter += 1
    return f"TKT-{_ticket_counter:04d}"


class ProcessRequest(BaseModel):
    message: str
    order_id: Optional[str] = None

class ProcessResponse(BaseModel):
    ticket_id: str
    intent: str
    subtype: str
    risk: str
    decision_action: str
    refund_amount: Optional[float] = None
    response: str
    log: list[str]
    status: str

class ReviewAction(BaseModel):
    ticket_id: str
    action: str
    amount: Optional[float] = None


@router.post("/process", response_model=ProcessResponse)
def process_ticket(req: ProcessRequest):
    result = run_pipeline(req.message, req.order_id)

    intent_r = result.get("intent_result")
    dec = result.get("decision_result")
    ticket_id = _next_ticket_id()

    decision_action = dec.action if dec else "no_action"
    risk = intent_r.risk.value if intent_r else ""
    status = "pending_review" if decision_action == "human_review" else "auto_processed"

    ticket = {
        "ticket_id": ticket_id,
        "customer_message": req.message,
        "order_id": result.get("order_id", ""),
        "intent": intent_r.intent.value if intent_r else "",
        "subtype": intent_r.subtype if intent_r else "",
        "risk": risk,
        "decision_action": decision_action,
        "refund_amount": dec.amount if dec else None,
        "response": result.get("response", ""),
        "log": result.get("log", []),
        "decision_reason": dec.reason if dec else "",
        "status": status,
    }

    # Execute refund automatically for auto_processed decisions
    if decision_action in ("auto_full_refund", "auto_partial_refund") and dec and dec.amount:
        refund_result = execute_refund(
            order_id=ticket["order_id"],
            amount=dec.amount,
            reason=dec.reason or "Auto refund",
        )
        print(f"[refund] auto: order={ticket['order_id']} amount=${dec.amount} success={refund_result.success}")
        ticket["log"].append(f"[refund] auto: amount=${dec.amount} success={refund_result.success}")

    database.insert_ticket(ticket)

    return ProcessResponse(
        ticket_id=ticket_id,
        intent=ticket["intent"],
        subtype=ticket["subtype"],
        risk=risk,
        decision_action=decision_action,
        refund_amount=ticket["refund_amount"],
        response=ticket["response"],
        log=ticket["log"],
        status=status,
    )


@router.get("/scenarios")
def list_scenarios():
    return {"scenarios": DEMO_SCENARIOS}


@router.get("/review")
def get_review_queue():
    pending = database.get_pending_review()
    processed = database.get_processed(limit=20)
    return {"pending": pending, "processed": processed}


@router.post("/review")
def process_review(action: ReviewAction):
    ticket = database.get_ticket(action.ticket_id)
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")

    # Resolve effective refund amount before any operation
    order_id = ticket.get("order_id", "")
    refund_amount = action.amount
    if action.action == "approve" and (not refund_amount or refund_amount <= 0):
        from api_adapters.mock_data import MOCK_ORDERS
        order = MOCK_ORDERS.get(order_id)
        if order:
            refund_amount = order.amount

    database.resolve_ticket(
        ticket_id=action.ticket_id,
        action=action.action,
        amount=refund_amount,
    )

    # Execute refund when human approves
    if action.action == "approve":
        reason = ticket.get("decision_reason", "Human approved refund")
        if refund_amount and refund_amount > 0:
            refund_result = execute_refund(order_id, refund_amount, reason)
            print(f"[refund] human review approve: order={order_id} amount=${refund_amount} success={refund_result.success}")
        else:
            print(f"[refund] human review approve: order={order_id} skipped (no valid amount)")

    ticket_meta = database.get_ticket(action.ticket_id)
    if ticket_meta:
        response_text = generate_review_response(
            action=action.action,
            name=ticket_meta.get("customer_message", "Valued Customer").split()[0] if ticket_meta.get("customer_message") else "Valued Customer",
            order_id=ticket_meta.get("order_id", ""),
            amount=refund_amount or 0,
        )
        database.update_ticket_response(action.ticket_id, response_text)
    updated = database.get_ticket(action.ticket_id)
    return {"status": "ok", "ticket": updated}


@router.get("/tickets")
def list_tickets():
    stats = database.count_by_status()
    recent = database.get_processed(limit=10)
    return {"stats": stats, "recent": recent}


@router.get("/orders")
def list_orders():
    orders = []
    for oid, order in MOCK_ORDERS.items():
        orders.append({
            "id": order.id,
            "customer": order.customer_name,
            "amount": order.amount,
            "status": order.status.value,
            "delivery": order.delivery_status.value,
        })
    return {"orders": orders}


@router.get("/rpa/test")
def test_rpa():
    import asyncio
    from agent.rpa_executor import execute_rpa
    async def _run():
        result = await execute_rpa("TEST")
        return result
    try:
        loop = asyncio.new_event_loop()
        result = loop.run_until_complete(_run())
        loop.close()
        if result.success:
            return {
                "status": "ok",
                "data": result.extracted_data,
                "screenshot": result.screenshot_path,
            }
        else:
            return {"status": "error", "error": result.error}
    except Exception as e:
        return {"status": "error", "error": str(e)}