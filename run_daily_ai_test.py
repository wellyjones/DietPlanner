import json
from dietplanner.services.aiPayload_service import build_daily_ai_payload
from dietplanner.repositories.dailyAIAnalysis_repo import insert_ai_analysis_request
from dietplanner.services.dailyAIAnalysis_runner import run_daily_ai_analysis
from dietplanner.services.dailyAIPrompt_service import PROMPT_VERSION_DAILY

USER_ID = 1
LOG_DATE = "2026-04-25"
MODEL = "gpt-4o-2024-08-06"  # example model that supports structured outputs

def main():
    payload = build_daily_ai_payload(LOG_DATE, user_id=USER_ID)
    payload_json = json.dumps(payload, ensure_ascii=False)

    # Insert a PENDING row first
    insert_ai_analysis_request(
        user_id=USER_ID,
        log_date=LOG_DATE,
        input_payload_json=payload_json,
        prompt_version=PROMPT_VERSION_DAILY,
        model_name=MODEL,
        status="PENDING",
        prompt_text="daily_v1"  # or store full prompt later
    )

    # You may want to query back the AIAnalysisID you just inserted.
    # Simplest approach: manually look up latest row or add a "return id" insert function.
    # For now, run analysis on the latest row id:
    import sqlite3
    conn = sqlite3.connect("instance/dietplanner.db")
    ai_analysis_id = conn.execute("SELECT MAX(AIAnalysisID) FROM DailyAIAnalysis").fetchone()[0]
    conn.close()

    run_daily_ai_analysis(ai_analysis_id, payload, MODEL)
    print("Done. Check DailyAIAnalysis table for results.")

if __name__ == "__main__":
    main()
``