from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_mail import Mail

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
login_manager = LoginManager(app)
mail = Mail(app)

login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

from app.routes import auth_routes, post_routes, comment_routes, admin_routes, messages_routes  # הוספתי את messages_routes
from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# רישום ה-Blueprints של כל הנתיבים
app.register_blueprint(auth_routes.bp)
app.register_blueprint(post_routes.bp)
app.register_blueprint(comment_routes.bp)
app.register_blueprint(admin_routes.bp)
app.register_blueprint(messages_routes.bp)  # רישום ה-Blueprint של הודעות
