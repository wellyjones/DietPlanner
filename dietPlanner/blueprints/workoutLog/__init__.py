from flask import Blueprint

workoutlog_bp = Blueprint(
    "workoutlog",
    __name__,
    url_prefix="/workoutLog"
)

from . import routes
