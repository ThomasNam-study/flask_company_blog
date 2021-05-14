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
from companyblog.blog_posts.views import blog_posts
from companyblog.question.views import question
from companyblog.question.answer_views import answer
from companyblog.question.filter import format_datetime
from companyblog.question.comment_views import comment_view

app.jinja_env.filters['datetime'] = format_datetime

app.register_blueprint(core)
app.register_blueprint(error_pages)
app.register_blueprint(users)
app.register_blueprint(blog_posts)
app.register_blueprint(question, url_prefix='/question')
app.register_blueprint(answer, url_prefix='/answer')
app.register_blueprint(comment_view, url_prefix='/comment')
