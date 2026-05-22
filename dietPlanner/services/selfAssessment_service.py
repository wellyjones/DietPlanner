from ..repositories.selfAssessment_repo import (
    get_self_assessment_for_date,
    insert_self_assessment,
    update_self_assessment,
)

USER_ID = 1  # temporary until auth exists


def save_self_assessment(form_data):
    """
    Insert or update self assessment notes for the given date.
    """
    log_date = form_data.get("log_date")
    notes = form_data.get("notes") or None

    existing = get_self_assessment_for_date(USER_ID, log_date)

    if existing:
        update_self_assessment(USER_ID, log_date, notes)
    else:
        insert_self_assessment(USER_ID, log_date, notes)


def get_self_assessment_for_form(log_date):
    """
    Returns dict {"notes": "..."} or None if no record exists for that date.
    """
    return get_self_assessment_for_date(USER_ID, log_date)


def get_self_assessment_status(log_date):
    """
    Dashboard status only: completed or not.
    """
    data = get_self_assessment_for_date(USER_ID, log_date)
    return {"exists": data is not None}
