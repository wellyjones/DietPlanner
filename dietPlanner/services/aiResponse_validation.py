def validate_daily_ai_response(obj: dict) -> list:
    """
    Returns a list of validation errors (empty list = valid)
    """

    errors = []

    required_keys = [
        "yesterday_summary",
        "score",
        "what_went_well",
        "what_needs_improving",
        "today_focus",
        "motivation",
        "confidence"
    ]

    # ✅ Check top-level keys
    for key in required_keys:
        if key not in obj:
            errors.append(f"Missing top-level key: {key}")

    # ✅ Validate types
    try:
        if not isinstance(obj.get("what_went_well"), list):
            errors.append("what_went_well must be a list")

        if not isinstance(obj.get("what_needs_improving"), list):
            errors.append("what_needs_improving must be a list")

        if not isinstance(obj.get("today_focus"), list):
            errors.append("today_focus must be a list")

        if not isinstance(obj.get("confidence"), (int, float)):
            errors.append("confidence must be a number")

    except Exception as ex:
        errors.append(f"Schema traversal error: {ex}")

    return errors
