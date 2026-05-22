from ..infrastructure.database import get_connection

def has_self_assessment_for_date(user_id, log_date):
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT 1
            FROM DailySelfAssessment
            WHERE UserID = ?
              AND LogDate = ?
            LIMIT 1
            """,
            (user_id, log_date)
        ).fetchone()

    return row is not None

from ..infrastructure.database import get_connection

def get_self_assessment_for_date(user_id, log_date):
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT Notes
            FROM DailySelfAssessment
            WHERE UserID = ? AND LogDate = ?
            """,
            (user_id, log_date),
        ).fetchone()

    if not row:
        return None

    return {
        "notes": row[0],
    }

def insert_self_assessment(user_id, log_date, notes):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO DailySelfAssessment (UserID, LogDate, Notes)
            VALUES (?, ?, ?)
            """,
            (user_id, log_date, notes),
        )
        conn.commit()


def update_self_assessment(user_id, log_date, notes):
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE DailySelfAssessment
            SET Notes = ?
            WHERE UserID = ? AND LogDate = ?
            """,
            (notes, user_id, log_date),
        )
        conn.commit()