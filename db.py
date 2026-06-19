"""
SQLite database layer for ticket persistence.
"""
import sqlite3
import json
import os
from datetime import datetime

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "tickets.db")


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, timeout=15, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=15000")
    return conn


def init_db():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id               TEXT PRIMARY KEY,
            customer_message TEXT NOT NULL,
            order_id         TEXT,
            intent           TEXT,
            subtype          TEXT,
            risk             TEXT,
            decision_action  TEXT,
            refund_amount    REAL,
            response         TEXT,
            status           TEXT DEFAULT 'open',
            decision_reason  TEXT,
            review_action    TEXT,
            logs             TEXT,
            created_at       TIMESTAMP DEFAULT (datetime('now')),
            resolved_at      TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def insert_ticket(ticket: dict) -> str:
    conn = get_conn()
    logs_json = json.dumps(ticket.get("log", []), ensure_ascii=False)
    conn.execute("""
        INSERT INTO tickets
            (id, customer_message, order_id, intent, subtype, risk,
             decision_action, refund_amount, response, status,
             decision_reason, logs)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ticket["ticket_id"],
        ticket.get("customer_message", ""),
        ticket.get("order_id", ""),
        ticket.get("intent", ""),
        ticket.get("subtype", ""),
        ticket.get("risk", ""),
        ticket.get("decision_action", ""),
        ticket.get("refund_amount"),
        ticket.get("response", ""),
        ticket.get("status", "auto_processed"),
        ticket.get("decision_reason", ""),
        logs_json,
    ))
    conn.commit()
    conn.close()
    return ticket["ticket_id"]


def resolve_ticket(ticket_id: str, action: str, amount=None):
    conn = get_conn()
    if amount is not None:
        conn.execute("""
            UPDATE tickets
            SET status='resolved', review_action=?, refund_amount=?,
                resolved_at=datetime('now')
            WHERE id=?
        """, (action, amount, ticket_id))
    else:
        conn.execute("""
            UPDATE tickets
            SET status='resolved', review_action=?,
                resolved_at=datetime('now')
            WHERE id=?
        """, (action, ticket_id))
    conn.commit()
    conn.close()


def update_ticket_response(ticket_id: str, response_text: str):
    conn = get_conn()
    conn.execute("UPDATE tickets SET response=? WHERE id=?", (response_text, ticket_id))
    conn.commit()
    conn.close()


def get_pending_review() -> list[dict]:
    conn = get_conn()
    rows = conn.execute("""
        SELECT * FROM tickets
        WHERE status = 'pending_review'
        ORDER BY created_at DESC
    """).fetchall()
    conn.close()
    return [_row_to_dict(r) for r in rows]


def get_processed(limit: int = 50) -> list[dict]:
    conn = get_conn()
    rows = conn.execute("""
        SELECT * FROM tickets
        WHERE status IN ('auto_processed', 'resolved')
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,)).fetchall()
    conn.close()
    return [_row_to_dict(r) for r in rows]


def get_ticket(ticket_id: str) -> dict | None:
    conn = get_conn()
    row = conn.execute("SELECT * FROM tickets WHERE id=?", (ticket_id,)).fetchone()
    conn.close()
    return _row_to_dict(row) if row else None


def count_by_status() -> dict:
    conn = get_conn()
    rows = conn.execute("""
        SELECT status, COUNT(*) as cnt FROM tickets GROUP BY status
    """).fetchall()
    conn.close()
    return {r["status"]: r["cnt"] for r in rows}


def _row_to_dict(row: sqlite3.Row) -> dict:
    d = dict(row)
    if "id" in d:
        d["ticket_id"] = d.pop("id")
    if d.get("logs"):
        try:
            d["log"] = json.loads(d["logs"])
        except (json.JSONDecodeError, TypeError):
            d["log"] = []
    else:
        d["log"] = []
    d.pop("logs", None)
    return d

def get_max_ticket_id() -> str | None:
    conn = get_conn()
    row = conn.execute("SELECT id FROM tickets ORDER BY id DESC LIMIT 1").fetchone()
    conn.close()
    return row["id"] if row else None