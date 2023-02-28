
from FarmerMarketLocator.config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from flask_mail import Mail

bcrypt = Bcrypt()
db = SQLAlchemy()
admin = Admin()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category ='danger'
login_manager.session_protection = 'strong'


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    admin.init_app(app)
    mail.init_app(app)
    
    from FarmerMarketLocator.users.verify import verify
    from FarmerMarketLocator.users.routes import users
    from FarmerMarketLocator.main.routes import main
    from FarmerMarketLocator.markets.routes import markets
    from FarmerMarketLocator.comments.routes import comments
    from FarmerMarketLocator.errors import errors

    app.register_blueprint(verify)
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(markets)
    app.register_blueprint(comments)
    app.register_blueprint(errors)
  
    return app

def create_db(app):
    with app.app_context():
        db.create_all()
