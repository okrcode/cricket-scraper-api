# app/utils/common.py
from datetime import datetime

def now_iso():
    return datetime.utcnow().isoformat() + 'Z'
