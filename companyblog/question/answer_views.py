from datetime import datetime

from flask import Blueprint, request, redirect, url_for

from companyblog import db
from companyblog.models import Question, Answer

answer = Blueprint('answer', __name__)


@answer.route('/create/<int:question_id>', methods=("POST",))
def create(question_id):
    q = Question.query.get_or_404(question_id)

    content = request.form['content']

    a = Answer(content=content, create_date=datetime.now())

    q.answer_set.append(a)
    db.session.commit()

    return redirect(url_for('question.detail', question_id=question_id))
