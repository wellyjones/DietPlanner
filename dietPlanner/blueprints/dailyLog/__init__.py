from flask import Blueprint

dailylog_bp = Blueprint(
    "dailylog",
    __name__,
    url_prefix="/dailyLog"
)

from . import routes