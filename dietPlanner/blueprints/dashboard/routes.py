from flask import render_template, request, redirect, url_for, flash
from datetime import date, timedelta
from . import dashboard_bp
from ...services.dailyLog_service import get_body_stats_status
from ...services.foodLog_service import get_food_log_status
from ...services.workoutLog_service import get_workout_status
from ...services.selfAssessment_service import get_self_assessment_status
from ...services.dailyAIAnalysis_service import queue_daily_ai_analysis, get_ai_analysis_for_form, get_ai_assessment_for_date

USER_ID = 1

@dashboard_bp.get("/")
def dashboard():
    today = date.today()

    selected_date = request.args.get("date")

    if selected_date:
        current_date = date.fromisoformat(selected_date)
    else:
        current_date = today

    # ✅ HARD LOCK: clamp future dates to today
    if current_date > today:
        current_date = today

    current_date_str = current_date.isoformat()

    prev_date = (current_date - timedelta(days=1)).isoformat()

    # ✅ Only allow next_date if not in the future
    next_date = (
        (current_date + timedelta(days=1)).isoformat()
        if current_date < today
        else None
    )

    body_stats = get_body_stats_status(current_date_str)
    food_log = get_food_log_status(current_date_str)
    workouts = get_workout_status(current_date_str)
    self_assessment = get_self_assessment_status(current_date_str)
    ai_record = get_ai_analysis_for_form(1, current_date_str)
    ai_assessment = get_ai_assessment_for_date(1, current_date_str)

    has_ai_result = (
        ai_record is not None and
        ai_record["Status"] == "SUCCESS"
    )

    return render_template(
        "dashboard.html",
        current_date=current_date_str,
        prev_date=prev_date,
        next_date=next_date,
        body_stats=body_stats,
        food_log=food_log,
        workouts=workouts,
        self_assessment=self_assessment,
        has_ai_result=has_ai_result,
        ai_assessment=ai_assessment

    )

@dashboard_bp.post("/submit")
def submit_todays_logs():
    log_date = request.form.get("log_date")
    print("DEBUG FORM DATA:", request.form, " --- ", log_date)
    queue_daily_ai_analysis(log_date)
    flash("✅ Daily logs submitted for AI analysis.", "success")

    return redirect(
        url_for("dashboard.dashboard", date=log_date)
    )

@dashboard_bp.get("/assessment")
def view_assessment():
    log_date = request.args.get("date")

    ai_record = get_ai_analysis_for_form(USER_ID, log_date)
    ai_assessment = get_ai_assessment_for_date(USER_ID, log_date)

    if not ai_record or ai_record["Status"] != "SUCCESS":
        flash("No assessment available yet.", "warning")
        return redirect(url_for("dashboard.dashboard", date=log_date))

    return render_template(
        "aiAssessment/form.html",
        log_date=log_date,
        ai_assessment=ai_assessment
    )

