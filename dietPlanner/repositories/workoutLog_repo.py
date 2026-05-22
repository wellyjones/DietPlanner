from ..infrastructure.database import get_connection

def insert_workout(
    workout_date,
    workout_type,
    duration_min,
    calories,
    distance_miles,
    pace
):
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO WorkoutLog
            (UserID, WorkoutDate, WorkoutType, Duration_min, CaloriesBurned,
             RunDistance_miles, RunPace)
            VALUES (1, ?, ?, ?, ?, ?, ?)
            """,
            (
                workout_date,
                workout_type,
                duration_min,
                calories,
                distance_miles,
                pace
            )
        )
        conn.commit()

def get_workout_count_for_date(user_id, workout_date):
    with get_connection() as conn:
        result = conn.execute(
            """
            SELECT COUNT(*)
            FROM WorkoutLog
            WHERE UserID = ?
              AND WorkoutDate = ?
            """,
            (user_id, workout_date)
        ).fetchone()

    return result[0] if result else 0

def get_workouts_for_date(user_id, workout_date):
    """
    Returns a list of workouts for a given date.
    """
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT
                WorkoutLogID,
                WorkoutDate,
                WorkoutType,
                Duration_min,
                CaloriesBurned,
                RunDistance_miles,
                RunPace
            FROM WorkoutLog
            WHERE UserID = ?
              AND WorkoutDate = ?
            ORDER BY WorkoutLogID DESC
            """,
            (user_id, workout_date),
        ).fetchall()

    workouts = []
    for r in rows:
        workouts.append({
            "id": r[0],
            "date": r[1],
            "type": r[2],
            "duration": r[3],
            "calories": r[4],
            "distance": r[5],
            "pace": r[6],
        })

    return workouts


def get_workout_by_id(user_id, workout_id):
    """
    Returns a single workout dict, or None.
    """
    with get_connection() as conn:
        row = conn.execute(
            """
            SELECT
                WorkoutLogID,
                WorkoutDate,
                WorkoutType,
                Duration_min,
                CaloriesBurned,
                RunDistance_miles,
                RunPace
            FROM WorkoutLog
            WHERE UserID = ?
              AND WorkoutLogID = ?
            """,
            (user_id, workout_id),
        ).fetchone()

    if not row:
        return None

    return {
        "id": row[0],
        "date": row[1],
        "type": row[2],
        "duration": row[3],
        "calories": row[4],
        "distance": row[5],
        "pace": row[6],
    }


def update_workout(user_id, workout_id, data):
    """
    Updates a workout by ID.
    """
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE WorkoutLog
            SET
                WorkoutType = ?,
                Duration_min = ?,
                CaloriesBurned = ?,
                RunDistance_miles = ?,
                RunPace = ?
            WHERE UserID = ?
              AND WorkoutLogID = ?
            """,
            (
                data.get("workout_type"),
                data.get("duration_min"),
                data.get("calories"),
                data.get("distance_miles"),
                data.get("pace"),
                user_id,
                workout_id,
            ),
        )
        conn.commit()