"""
SQLite 数据库查询教学脚本
运行方式: python query_db.py
"""
import sqlite3
from datetime import datetime

DB_PATH = r"C:\Users\winni\Aftersale_system\tickets.db"


def print_sep(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


# 1. 查看有哪些表
print_sep("1. 数据库中有哪些表")
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
for t in cur.fetchall():
    print(f"  表名: {t['name']}")
    cur.execute(f"PRAGMA table_info({t['name']})")
    cols = cur.fetchall()
    for c in cols:
        print(f"    ├ {c['name']:20s}  {c['type']:12s}  {'PK' if c['pk'] else ''}  {'NOT NULL' if c['notnull'] else ''}")
    print()

# 2. 工单总数
print_sep("2. 工单总数")
cur.execute("SELECT COUNT(*) AS cnt FROM tickets")
row = cur.fetchone()
print(f"  总工单数: {row['cnt']}")

# 3. 按状态统计
print_sep("3. 按状态统计")
cur.execute("SELECT status, COUNT(*) AS cnt FROM tickets GROUP BY status ORDER BY cnt DESC")
for r in cur.fetchall():
    print(f"  {r['status']:20s}  {r['cnt']} 条")

# 4. 按意图分类统计
print_sep("4. 按意图分类统计")
cur.execute("SELECT intent, COUNT(*) AS cnt FROM tickets GROUP BY intent ORDER BY cnt DESC")
for r in cur.fetchall():
    print(f"  {r['intent']:15s}  {r['cnt']} 条")

# 5. 最近 10 条工单
print_sep("5. 最近 10 条工单")
cur.execute("""
    SELECT id, customer_message, intent, status, created_at
    FROM tickets
    ORDER BY created_at DESC
    LIMIT 10
""")
for r in cur.fetchall():
    msg = r['customer_message'][:30] + "..." if len(r['customer_message']) > 30 else r['customer_message']
    print(f"  {r['id']:12s} | {msg:32s} | {r['intent']:10s} | {r['status']:15s} | {r['created_at']}")

# 6. 待人工审核
print_sep("6. 待人工审核的工单")
cur.execute("SELECT id, customer_message, decision_action, refund_amount, created_at FROM tickets WHERE status='pending_review'")
rows = cur.fetchall()
if rows:
    for r in rows:
        msg = r['customer_message'][:30] + "..." if len(r['customer_message']) > 30 else r['customer_message']
        print(f"  {r['id']:12s} | {msg:32s} | 决策: {r['decision_action']:10s} | 金额: {r['refund_amount']} | {r['created_at']}")
else:
    print("  (无待审核工单)")

# 7. 高风险工单
print_sep("7. 高风险工单")
cur.execute("""
    SELECT id, customer_message, risk, decision_action, refund_amount
    FROM tickets
    WHERE risk IN ('high', 'medium')
    ORDER BY CASE risk WHEN 'high' THEN 0 WHEN 'medium' THEN 1 END
    LIMIT 10
""")
rows = cur.fetchall()
if rows:
    for r in rows:
        msg = r['customer_message'][:30] + "..." if len(r['customer_message']) > 30 else r['customer_message']
        print(f"  {r['id']:12s} | {msg:30s} | 风险: {r['risk']:6s} | 决策: {r['decision_action']:10s} | 金额: {r['refund_amount']}")
else:
    print("  (无高风险工单)")

conn.close()
print(f"\n{'='*60}")
print(f"  查询完成")
print(f"{'='*60}")
