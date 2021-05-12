from datetime import datetime

from flask import Blueprint, request, redirect, url_for, render_template

from companyblog import db
from companyblog.models import Question, Answer
from companyblog.question.forms import AnswerForm

answer = Blueprint('answer', __name__)


@answer.route('/create/<int:question_id>', methods=("POST",))
def create(question_id):

    form = AnswerForm()

    q = Question.query.get_or_404(question_id)

    if form.validate_on_submit():

        content = form.content.data

        a = Answer(content=content, create_date=datetime.now())

        q.answer_set.append(a)
        db.session.commit()

        return redirect(url_for('question.detail', question_id=question_id))

    return render_template('question/question_detail.html', question=q, form=form)
