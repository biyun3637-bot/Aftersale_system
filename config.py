"""
绯荤粺閰嶇疆銆?

DEMO_MODE = True  鈫?浣跨敤 Mock 鏁版嵁锛岄浂澶栭儴渚濊禆璺戦€氬叏閾捐矾
DEMO_MODE = False 鈫?浣跨敤鐪熷疄 API + LLM
"""
import os
from dotenv import load_dotenv

load_dotenv()

# 鈹€鈹€ 杩愯妯″紡 鈹€鈹€
DEMO_MODE = os.getenv("DEMO_MODE", "true").strip().lower() == "true"

# 鈹€鈹€ LLM 鈹€鈹€
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY", "")
ZHIPU_MODEL = os.getenv("ZHIPU_MODEL", "glm-4-flash")

# 鈹€鈹€ 閫€娆捐鍒欓槇鍊?鈹€鈹€
AUTO_REFUND_MAX = 20
PARTIAL_REFUND_DAYS = 10
PARTIAL_REFUND_PERCENT = 0.5
HUMAN_REVIEW_MIN = 100

# 鈹€鈹€ 鏈嶅姟鍣?鈹€鈹€
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))


# ── RPA ──
RPA_ENABLED = os.getenv("RPA_ENABLED", "false").strip().lower() == "true"
