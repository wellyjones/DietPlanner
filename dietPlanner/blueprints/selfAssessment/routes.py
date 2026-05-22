from datetime import date
from flask import render_template, request, redirect, url_for
from datetime import date
from . import selfassessment_bp
from ...services.selfAssessment_service import (
    save_self_assessment,
    get_self_assessment_for_form,
)

@selfassessment_bp.get("/")
def self_assessment_form():
    log_date = request.args.get("date") or date.today().isoformat()

    existing = get_self_assessment_for_form(log_date)

    return render_template(
        "selfAssessment/form.html",
        log_date=log_date,
        self_assessment=existing,  # None or {"notes": "..."}
    )

@selfassessment_bp.post("/new")
def create_self_assessment():
    save_self_assessment(request.form)
    return redirect(url_for("dashboard.dashboard", date=request.form.get("self_assessment")))

