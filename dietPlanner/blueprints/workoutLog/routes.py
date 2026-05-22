from flask import render_template, request, redirect, url_for
from datetime import date
from . import workoutlog_bp
from ...services.workoutLog_service import (
    get_workouts_for_list,
    get_workout_for_edit,
    save_workout_edit,
    save_workout,
    save_workout_new,
)

@workoutlog_bp.get("/new")
def new_workout_form():
    log_date = request.args.get("date")

    return render_template(
        "workoutLog/form.html",
        workout=None,
        log_date=log_date,
        form_action=url_for("workoutlog.save_new_workout"),
    )

@workoutlog_bp.post("/new")
def save_new_workout():
    log_date = request.form.get("log_date")

    save_workout_new(request.form)

    return redirect(
        url_for("workoutlog.list_workouts", date=log_date)
    )


@workoutlog_bp.get("/list")
def list_workouts():
    log_date = request.args.get("date") or date.today().isoformat()

    workouts = get_workouts_for_list(log_date)

    return render_template(
        "workoutLog/list.html",
        log_date=log_date,
        workouts=workouts,
    )

@workoutlog_bp.get("/edit/<int:workout_id>")
def edit_workout_form(workout_id):
    log_date = request.args.get("date")
    workout = get_workout_for_edit(workout_id)

    return render_template(
        "workoutLog/form.html",
        workout=workout,
        log_date=log_date,
        form_action=url_for("workoutlog.update_workout", workout_id=workout_id),
    )

@workoutlog_bp.post("/edit/<int:workout_id>")
def update_workout(workout_id):
    log_date = request.form.get("log_date")

    save_workout_edit(workout_id, request.form)

    return redirect(
        url_for("workoutlog.list_workouts", date=log_date)
    )
