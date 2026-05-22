import json
from ..repositories.dailyAIAnalysis_repo import update_ai_analysis_result
from ..services.aiResponse_validation import validate_daily_ai_response
from ..services.openaiClient_service import call_openai_daily
from ..services.dailyAIPrompt_service import build_daily_prompt, DAILY_SCHEMA

def run_daily_ai_analysis(ai_analysis_id: int, payload_dict: dict, model_name: str) -> None:
    """
    Calls OpenAI, validates response JSON, stores results.
    """
    prompt_text = build_daily_prompt(payload_dict)

    try:
        raw, parsed = call_openai_daily(prompt_text, DAILY_SCHEMA, model_name)
        errors = validate_daily_ai_response(parsed)

        if errors:
            update_ai_analysis_result(
                ai_analysis_id,
                status="FAILED",
                model_name=model_name,
                response_json=None,
                response_raw=raw,
                error_message="; ".join(errors)
            )
            return

        update_ai_analysis_result(
            ai_analysis_id,
            status="SUCCESS",
            model_name=model_name,
            response_json=json.dumps(parsed, ensure_ascii=False),
            response_raw=raw,
            error_message=None
        )

    except Exception as ex:
        update_ai_analysis_result(
            ai_analysis_id,
            status="FAILED",
            model_name=model_name,
            response_json=None,
            response_raw=None,
            error_message=str(ex)
        )