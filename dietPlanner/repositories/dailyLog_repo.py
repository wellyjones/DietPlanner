from datetime import datetime 
from ..infrastructure.database import get_connection


def get_daily_log_for_date(user_id, log_date):
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT Weight_kg, PreviousNightSleepScore, Steps
            FROM DailyLog
            WHERE UserID = ? AND LogDate = ?
            """,
            (user_id, log_date),
        ).fetchone()

    if not row:
        return None

    return {
        "weight": row[0],
        "sleep": row[1],
        "steps": row[2],
    }

def insert_daily_log(user_id, log_date, data):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO DailyLog
            (UserID, LogDate, Weight_kg, PreviousNightSleepScore, Steps)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                user_id,
                log_date,
                data.get("weight"),
                data.get("sleep"),
                data.get("steps"),
            ),
        )
        conn.commit()

def update_daily_log(user_id, log_date, data):
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE DailyLog
            SET
                Weight_kg = ?,
                PreviousNightSleepScore = ?,
                Steps = ?
            WHERE UserID = ? AND LogDate = ?
            """,
            (
                data.get("weight"),
                data.get("sleep"),
                data.get("steps"),
                user_id,
                log_date,
            ),
        )
        conn.commit()

