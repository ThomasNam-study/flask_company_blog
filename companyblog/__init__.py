import os

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

#############################
### 데이터 베이스
#############################

basedir = os.path.abspath(os.path.dirname(__file__))

app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

Migrate(app, db)

login_manage = LoginManager()

login_manage.init_app(app)
login_manage.login_view = 'users.login'


from companyblog.core.views import core
from companyblog.error_pages.handlers import error_pages
from companyblog.users.views import users

app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(users)
