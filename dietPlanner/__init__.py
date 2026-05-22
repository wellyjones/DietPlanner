from flask import Flask
from .infrastructure.database import init_db
from .blueprints.dailyLog import dailylog_bp
from .blueprints.workoutLog import workoutlog_bp
from .blueprints.foodLog import foodlog_bp
from .blueprints.selfAssessment import selfassessment_bp
from .blueprints.dashboard import dashboard_bp

def create_app():
    app = Flask(__name__)

    # Initialise database at startup
    init_db()

    # Register blueprints AFTER app is created
    app.register_blueprint(dailylog_bp)
    app.register_blueprint(workoutlog_bp)
    app.register_blueprint(foodlog_bp)
    app.register_blueprint(selfassessment_bp)
    app.register_blueprint(dashboard_bp)
    app.secret_key = "development-secret-key"  # change later
    
    @app.route("/ping")
    def ping():
        return "OK"
    
    return app