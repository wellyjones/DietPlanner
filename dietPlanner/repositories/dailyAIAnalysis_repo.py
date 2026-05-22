from ..infrastructure.database import get_connection

def insert_ai_analysis_request(
    user_id,
    log_date,
    input_payload_json,
    prompt_version,
    model_name,
    status,
    prompt_text
):
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO DailyAIAnalysis
            (UserID, LogDate, InputPayloadJSON, PromptVersion, ModelName, Status, PromptText)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                log_date,
                input_payload_json,
                prompt_version,
                model_name,
                status,
                prompt_text,
            ),
        )
        conn.commit()

        return cursor.lastrowid  # ✅ THIS replaces your MAX() hack

def update_ai_analysis_result(ai_analysis_id, status, model_name=None, response_json=None, response_raw=None, error_message=None):
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE DailyAIAnalysis
            SET Status = ?,
                ModelName = COALESCE(?, ModelName),
                ResponseJSON = ?,
                ResponseRaw = ?,
                ErrorMessage = ?
            WHERE AIAnalysisID = ?
            """,
            (status, model_name, response_json, response_raw, error_message, ai_analysis_id),
        )
        conn.commit()


def update_ai_analysis_payload(ai_analysis_id, input_payload_json, prompt_text):
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE DailyAIAnalysis
            SET InputPayloadJSON = ?,
                PromptText = ?,
                Status = 'PENDING'
            WHERE AIAnalysisID = ?
            """,
            (input_payload_json, prompt_text, ai_analysis_id)
        )
        conn.commit()

def get_ai_analysis_by_user_date_version(user_id, log_date, prompt_version):
    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT AIAnalysisID
            FROM DailyAIAnalysis
            WHERE UserID = ? AND LogDate = ? AND PromptVersion = ?
            """,
            (user_id, log_date, prompt_version)
        )
        return cursor.fetchone()

def delete_ai_analysis_by_user_date_version(user_id, log_date, prompt_version):
    with get_connection() as conn:
        conn.execute(
            """
            DELETE FROM DailyAIAnalysis
            WHERE UserID = ? AND LogDate = ? AND PromptVersion = ?
            """,
            (user_id, log_date, prompt_version)
        )
        conn.commit()

def exists_ai_analysis(user_id, log_date, prompt_version):
    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT 1
            FROM DailyAIAnalysis
            WHERE UserID = ? AND LogDate = ? AND PromptVersion = ?
            """,
            (user_id, log_date, prompt_version)
        )
        return cursor.fetchone() is not None

def get_ai_analysis_for_date(user_id, log_date):
    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT *
            FROM DailyAIAnalysis
            WHERE UserID = ? AND LogDate = ?
            ORDER BY AIAnalysisID DESC
            LIMIT 1
            """,
            (user_id, log_date)
        )
        return cursor.fetchone()


def get_latest_successful_analysis(user_id, log_date):
    with get_connection() as conn:
        cursor = conn.execute(
            """
            SELECT *
            FROM DailyAIAnalysis
            WHERE UserID = ?
              AND LogDate = ?
              AND Status = 'SUCCESS'
            ORDER BY CreatedAt DESC
            LIMIT 1
            """,
            (user_id, log_date)
        )
        return cursor.fetchone()
