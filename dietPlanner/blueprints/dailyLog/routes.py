from flask import render_template, request, redirect, url_for
from . import dailylog_bp
from ...services.dailyLog_service import (
    save_daily_log,
    get_daily_log_for_form,
)


@dailylog_bp.get("/")
def daily_log_form():
    log_date = request.args.get("date")

    existing_log = get_daily_log_for_form(log_date)

    return render_template(
        "dailyLog/form.html",
        log_date=log_date,
        daily_log=existing_log,
    )

@dailylog_bp.post("/new")
def create_or_update_daily_log():
    log_date = request.form.get("log_date")

    save_daily_log(request.form)

    return redirect(
        url_for("dashboard.dashboard", date=log_date)
    )
