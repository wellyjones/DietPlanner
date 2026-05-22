from flask import Blueprint

foodlog_bp = Blueprint(
    "foodlog",
    __name__,
    url_prefix="/foodLog"
)

from . import routes