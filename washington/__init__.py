from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
#from flask_redis import FlaskRedis


# Globally accessible libraries
db = SQLAlchemy()
login_manager = LoginManager()
USER_ID = None
USER = None
#r = FlaskRedis()

def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)
    #r.init_app(app)

    with app.app_context():
        # Include our Routes
        from . import auth
        from .control import control
        db.create_all()

        # Register Blueprints
        app.register_blueprint(control.control_bp)
        app.register_blueprint(auth.auth_bp)
        #app.register_blueprint(admin.admin_bp)

        return app
