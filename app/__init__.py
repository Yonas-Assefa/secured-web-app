from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
        
    # Import and register blueprints
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # Rest of your code...
    
    return app