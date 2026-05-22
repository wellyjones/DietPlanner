import os
import json

from ..services.aiPayload_service import build_daily_ai_payload
from ..services.dailyAIPrompt_service import build_daily_prompt, PROMPT_VERSION_DAILY
from ..repositories.dailyAIAnalysis_repo import (
    insert_ai_analysis_request,
    delete_ai_analysis_by_user_date_version,
    exists_ai_analysis,
    get_ai_analysis_for_date,
    get_latest_successful_analysis
)
from ..services.dailyAIAnalysis_runner import run_daily_ai_analysis

USER_ID = 1
MODEL_NAME = "gpt-4o-2024-08-06"
ENABLE_OPENAI = True #os.getenv("ENABLE_OPENAI", "false").lower() == "true"

def queue_daily_ai_analysis(log_date, user_id=USER_ID):

    prompt_version = PROMPT_VERSION_DAILY

    payload = build_daily_ai_payload(log_date, user_id=user_id)
    prompt_text = build_daily_prompt(payload)

    payload_json = json.dumps(payload, ensure_ascii=False)

    # ✅ Clean: ask repo if exists
    if exists_ai_analysis(user_id, log_date, prompt_version):
        delete_ai_analysis_by_user_date_version(user_id, log_date, prompt_version)

    # ✅ Clean insert
    ai_analysis_id = insert_ai_analysis_request(
        user_id=user_id,
        log_date=log_date,
        input_payload_json=payload_json,
        prompt_version=prompt_version,
        model_name="pending",
        status="PENDING",
        prompt_text=prompt_text
    )

    if ENABLE_OPENAI:
        run_daily_ai_analysis(ai_analysis_id, prompt_text, model_name=MODEL_NAME)

    return run_daily_ai_analysis

def get_ai_analysis_for_form(USER_ID, log_date):
    return get_ai_analysis_for_date(USER_ID, log_date)


def get_ai_assessment_for_date(user_id, log_date):
    print("DEBUG: user_id =", user_id)
    print("DEBUG: log_date =", log_date)

    record = get_latest_successful_analysis(user_id, log_date)

    print("DEBUG: DB record =", record)

    if not record:
        return None

    try:
        parsed = json.loads(record["ResponseJSON"])
        print("DEBUG: parsed =", parsed)
        return parsed
    except Exception as e:
        print("JSON ERROR:", e)
        return None

