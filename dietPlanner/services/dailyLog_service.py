from ..repositories.dailyLog_repo import (
    get_daily_log_for_date,
    insert_daily_log,
    update_daily_log,
)

USER_ID = 1  # temporary


def save_daily_log(form_data):
    log_date = form_data.get("log_date")

    existing = get_daily_log_for_date(USER_ID, log_date)

    data = {
        "weight": form_data.get("weight"),
        "sleep": form_data.get("sleep"),
        "steps": form_data.get("steps"),
    }

    if existing:
        update_daily_log(USER_ID, log_date, data)
    else:
        insert_daily_log(USER_ID, log_date, data)


def get_daily_log_for_form(log_date):
    return get_daily_log_for_date(USER_ID, log_date)


def get_daily_log_status(log_date):
    data = get_daily_log_for_date(USER_ID, log_date)

    if not data:
        return {
            "weight": False,
            "sleep": False,
            "steps": False,
            "exists": False,
        }

    return {
        "weight": bool(data["weight"]),
        "sleep": bool(data["sleep"]),
        "steps": bool(data["steps"]),
        "exists": True,
    }


# ✅ Alias for dashboard clarity
get_body_stats_status = get_daily_log_status
