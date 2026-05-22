from ..infrastructure.database import get_connection
from datetime import datetime

def create_user(email: str, password: str):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO users (email, password, createDate) VALUES (?, ?, ?)",
            (email, password, datetime.utcnow().isoformat())
        )
        conn.commit()