from flask import Blueprint, render_template

from companyblog.models import Question

pybo = Blueprint('pybo', __name__)


@pybo.route('/')
def index():
    q_list = Question.query.order_by(Question.create_date.desc())

    return render_template('question/question_list.html', q_list=q_list)
