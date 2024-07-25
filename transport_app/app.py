from flask import Flask
from config import Config
from models import db, User, KPIFile
from routes import main as main_blueprint
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Registrar el blueprint de las rutas principales
app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
