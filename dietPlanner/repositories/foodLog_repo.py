from ..infrastructure.database import get_connection

def insert_food_log(
    food_date,
    breakfast,
    lunch,
    dinner,
    snacks,
    liquid
):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO FoodLog
            (UserID, FoodLogDate, Breakfast, Lunch, Dinner, Snacks, Liquid)
            VALUES (1, ?, ?, ?, ?, ?, ?)
            """,
            (
                food_date,
                breakfast,
                lunch,
                dinner,
                snacks,
                liquid
            )
        )
        conn.commit()

def get_food_log_for_date(user_id, log_date):
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT Breakfast, Lunch, Dinner, Snacks, Liquid
            FROM FoodLog
            WHERE UserID = ? AND FoodLogDate = ?
            """,
            (user_id, log_date)
        ).fetchone()

    if not row:
        return None

    return {
        "breakfast": row[0],
        "lunch": row[1],
        "dinner": row[2],
        "snacks": row[3],
        "liquid": row[4],
    }

def update_food_log(user_id, log_date, data):
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE FoodLog
            SET
                Breakfast = ?,
                Lunch = ?,
                Dinner = ?,
                Snacks = ?,
                Liquid = ?
            WHERE UserID = ?
              AND FoodLogDate = ?
            """,
            (
                data.get("breakfast"),
                data.get("lunch"),
                data.get("dinner"),
                data.get("snacks"),
                data.get("liquid"),
                user_id,
                log_date,
            )
        )
        conn.commit()
