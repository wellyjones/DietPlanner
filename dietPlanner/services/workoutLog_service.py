def save_workout(form_data):
    from ..repositories.workoutLog_repo import insert_workout

    insert_workout(
        workout_date=form_data.get("log_date"),
        workout_type=form_data.get("workout_type"),
        duration_min=form_data.get("duration_min") or None,
        calories=form_data.get("calories") or None,
        distance_miles=form_data.get("distance_miles") or None,
        pace=form_data.get("pace") or None
    )

def save_workout_new(form_data):
    from ..repositories.workoutLog_repo import insert_workout

    insert_workout(
        workout_date=form_data.get("log_date"),
        workout_type=form_data.get("workout_type"),
        duration_min=form_data.get("duration_min") or None,
        calories=form_data.get("calories") or None,
        distance_miles=form_data.get("distance_miles") or None,
        pace=form_data.get("pace") or None
    )

def get_workout_status(log_date):
    from ..repositories.workoutLog_repo import get_workout_count_for_date

    count = get_workout_count_for_date(user_id=1, workout_date=log_date)

    return {
        "count": count,
        "has_workout": count > 0
    }

from ..repositories.workoutLog_repo import (
    get_workouts_for_date,
    get_workout_by_id,
    update_workout,
)

USER_ID = 1  # temporary until auth exists


def get_workouts_for_list(log_date):
    return get_workouts_for_date(USER_ID, log_date)


def get_workout_for_edit(workout_id):
    return get_workout_by_id(USER_ID, workout_id)


def save_workout_edit(workout_id, form_data):
    data = {
        "workout_type": form_data.get("workout_type"),
        "duration_min": form_data.get("duration_min") or None,
        "calories": form_data.get("calories") or None,
        "distance_miles": form_data.get("distance_miles") or None,
        "pace": form_data.get("pace") or None,
    }
    update_workout(USER_ID, workout_id, data)