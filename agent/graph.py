"""LangGraph workflow orchestration.

Pipeline: classifier -> api_query -> decision -> refund_exec -> response_gen
                                       |-> rpa_fallback -> decision (if API fails)
                                       |-> human_review (if high risk)
"""
from typing import TypedDict, Optional
import config
from langgraph.graph import StateGraph, END

from models.intent import IntentResult
from models.order import Order
from models.tracking import TrackingInfo
from agent.classifier import classify, extract_order_id
from agent.api_query import query_order, QueryResult
from agent.decision import decide, Decision
from agent.refund_exec import execute_refund, RefundResult
from agent.response_gen import generate_response
from agent.rpa_executor import get_default_mock_data, execute_rpa
import asyncio

def _run_async(coro):
    try:
        asyncio.get_running_loop()
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as pool:
            return pool.submit(asyncio.run, coro).result()
    except RuntimeError:
        return asyncio.run(coro)


class AgentState(TypedDict):
    customer_message: str
    order_id: Optional[str]
    intent_result: Optional[IntentResult]
    order: Optional[Order]
    tracking: Optional[TrackingInfo]
    api_available: bool
    api_error: str
    decision_result: Optional[Decision]
    refund_result: Optional[RefundResult]
    response: str
    log: list[str]


def node_classify(state: AgentState) -> dict:
    msg = state["customer_message"]
    oid = state.get("order_id") or extract_order_id(msg) or "ORD-001"
    intent = classify(msg, llm_provider=config.LLM_PROVIDER)
    return {
        "order_id": oid,
        "intent_result": intent,
        "log": state["log"] + [f"[classifier] -> {intent.summary} (risk={intent.risk.value})"],
    }


def node_api_query(state: AgentState) -> dict:
    oid = state.get("order_id", "")
    result: QueryResult = query_order(oid)
    log_line = (
        f"[api_query] order={'found' if result.order else 'not_found'} "
        f"tracking={'found' if result.tracking else 'n/a'} "
        f"api_available={result.api_available}"
    )
    return {
        "order": result.order,
        "tracking": result.tracking,
        "api_available": result.api_available,
        "api_error": result.error,
        "log": state["log"] + [log_line],
    }


def node_rpa_fallback(state: AgentState) -> dict:
    oid = state.get("order_id", "ORD-004")
    note = ""
    if False:  # RPA disabled in pipeline
        note = " (Playwright available - visit /api/rpa/test to trigger)"
    mock = get_default_mock_data(oid)
    return {
        "api_available": True,
        "api_error": "",
        "log": state["log"] + [f"[rpa] pipeline mock for {oid}{note}: {mock.extracted_data}"],
    }


def node_decision(state: AgentState) -> dict:
    intent = state.get("intent_result")
    order = state.get("order")
    tracking = state.get("tracking")
    dec = decide(intent, order, tracking)
    return {
        "decision_result": dec,
        "log": state["log"] + [f"[decision] action={dec.action} amount={dec.amount} risk={dec.risk.value}"],
    }


def node_refund_exec(state: AgentState) -> dict:
    dec = state.get("decision_result")
    oid = state.get("order_id", "")
    if dec and dec.amount and dec.amount > 0:
        result = execute_refund(oid, dec.amount, dec.reason)
    else:
        result = RefundResult()
        result.success = True
    return {
        "refund_result": result,
        "log": state["log"] + [f"[refund] success={result.success} error={result.error}"],
    }


def node_response_gen(state: AgentState) -> dict:
    order = state.get("order")
    oid = state.get("order_id", "")
    name = order.customer_name if order else "Customer"
    dec = state.get("decision_result")
    amount = dec.amount if dec else 0
    action = dec.action if dec else "no_action"
    resp = generate_response(name, oid, amount or 0, action)
    return {
        "response": resp,
        "log": state["log"] + [f"[response] generated ({action})"],
    }


def node_human_review(state: AgentState) -> dict:
    resp = "Your case has been escalated for manual review. We will respond within 24-48 hours."
    return {
        "response": resp,
        "log": state["log"] + ["[human_review] case escalated"],
    }


def route_after_api(state: AgentState) -> str:
    if state.get("api_available"):
        return "decision"
    return "rpa_fallback"


def route_after_decision(state: AgentState) -> str:
    dec = state.get("decision_result")
    if dec and dec.action == "human_review":
        return "human_review"
    return "refund_exec"


def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("classifier", node_classify)
    graph.add_node("api_query", node_api_query)
    graph.add_node("rpa_fallback", node_rpa_fallback)
    graph.add_node("decision", node_decision)
    graph.add_node("refund_exec", node_refund_exec)
    graph.add_node("response_gen", node_response_gen)
    graph.add_node("human_review", node_human_review)

    graph.set_entry_point("classifier")
    graph.add_edge("classifier", "api_query")

    graph.add_conditional_edges(
        "api_query",
        route_after_api,
        {"decision": "decision", "rpa_fallback": "rpa_fallback"},
    )
    graph.add_edge("rpa_fallback", "decision")

    graph.add_conditional_edges(
        "decision",
        route_after_decision,
        {"refund_exec": "refund_exec", "human_review": "human_review"},
    )
    graph.add_edge("refund_exec", "response_gen")
    graph.add_edge("response_gen", END)
    graph.add_edge("human_review", END)

    return graph.compile()


app = build_graph()


def run_pipeline(customer_message: str, order_id: str | None = None) -> dict:
    initial = {
        "customer_message": customer_message,
        "order_id": order_id,
        "intent_result": None,
        "order": None,
        "tracking": None,
        "api_available": False,
        "api_error": "",
        "decision_result": None,
        "refund_result": None,
        "response": "",
        "log": [],
    }
    return app.invoke(initial)



