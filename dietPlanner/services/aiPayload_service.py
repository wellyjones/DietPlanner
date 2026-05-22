from datetime import datetime
import json

from ..repositories.dailyLog_repo import get_daily_log_for_date
from ..repositories.foodLog_repo import get_food_log_for_date
from ..repositories.workoutLog_repo import get_workouts_for_date
from ..repositories.selfAssessment_repo import get_self_assessment_for_date

USER_ID = 1  # temporary until auth exists


def build_daily_ai_payload(log_date, user_id=USER_ID):
    """
    Builds the canonical daily payload dict for AI analysis.
    No OpenAI call here.
    """
    daily_log = get_daily_log_for_date(user_id, log_date)
    food_log = get_food_log_for_date(user_id, log_date)
    workouts = get_workouts_for_date(user_id, log_date)
    self_assessment = get_self_assessment_for_date(user_id, log_date)

    payload = {
        "meta": {
            "user_id": user_id,
            "date": log_date,
            "timezone": "Europe/London",
            "source": "DietPlanner v1",
            "generated_at": datetime.utcnow().isoformat() + "Z",
        },
        "daily_log": daily_log,               # dict or None
        "food_log": food_log,                 # dict or None
        "workouts": workouts or [],            # list
        "self_assessment": self_assessment,   # dict or None
    }

    return payload


def build_daily_ai_payload_json(log_date, user_id=USER_ID):
    """
    Convenience wrapper: returns JSON string for storage.
    """
    payload = build_daily_ai_payload(log_date, user_id=user_id)
    return json.dumps(payload, ensure_ascii=False)
