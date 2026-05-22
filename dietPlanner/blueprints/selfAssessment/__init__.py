from flask import Blueprint

selfassessment_bp = Blueprint(
    "selfassessment",
    __name__,
    url_prefix="/selfAssessment"
)

from . import routes