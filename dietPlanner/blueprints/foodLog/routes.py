from flask import render_template, request, redirect, url_for
from . import foodlog_bp
from ...services.foodLog_service import (
    save_food_log,
    get_food_log_for_form
)

@foodlog_bp.get("/")
def food_log_form():
    log_date = request.args.get("date")

    existing_log = get_food_log_for_form(log_date)

    return render_template(
        "foodLog/form.html",
        log_date=log_date,
        food_log=existing_log  # None if no data
    )

@foodlog_bp.post("/new")
def create_or_update_food_log():
    save_food_log(request.form)
    return redirect(url_for("dashboard.dashboard", date=request.form.get("food_date")))

