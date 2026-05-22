from ..repositories.foodLog_repo import (
    insert_food_log,
    update_food_log,
    get_food_log_for_date,
)

USER_ID = 1  # temporary until auth exists


def save_food_log(form_data):
    """
    Insert or update a FoodLog entry for a given date.
    """
    log_date = form_data.get("food_date")

    existing = get_food_log_for_date(USER_ID, log_date)

    if existing:
        update_food_log(USER_ID, log_date, form_data)
    else:
        insert_food_log(
            food_date=log_date,
            breakfast=form_data.get("breakfast"),
            lunch=form_data.get("lunch"),
            dinner=form_data.get("dinner"),
            snacks=form_data.get("snacks"),
            liquid=form_data.get("liquid"),
        )


def get_food_log_for_form(log_date):
    """
    Return the full food log record for pre-populating the form,
    or None if no record exists.
    """
    return get_food_log_for_date(USER_ID, log_date)


def get_food_log_status(log_date):
    """
    Return boolean status values for the dashboard.
    """
    data = get_food_log_for_date(USER_ID, log_date)

    if not data:
        return {
            "breakfast": False,
            "lunch": False,
            "dinner": False,
            "snacks": False,
            "liquid": False,
            "exists": False,
        }

    return {
        "breakfast": bool(data["breakfast"]),
        "lunch": bool(data["lunch"]),
        "dinner": bool(data["dinner"]),
        "snacks": bool(data["snacks"]),
        "liquid": bool(data["liquid"]),
        "exists": True,
    }