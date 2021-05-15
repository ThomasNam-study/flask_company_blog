from flask import Blueprint, flash, redirect, url_for
from flask_login import login_required, current_user

from companyblog import db
from companyblog.models import Question, Answer

vote_view = Blueprint('vote', __name__)


@vote_view.route('/question/<int:question_id>/')
@login_required
def question(question_id):
    _question = Question.query.get_or_404(question_id)

    if current_user == _question.user:
        flash("본인이 작성한 글은 추천할수 없습니다.")
    else:
        _question.voter.append(current_user)
        db.session.commit()

    return redirect(url_for('question.detail', question_id=question_id))


@vote_view.route('/answer/<int:answer_id>/')
@login_required
def answer(answer_id):
    _answer = Answer.query.get_or_404(answer_id)

    if current_user == _answer.user:
        flash("본인이 작성한 글은 추천할수 없습니다.")
    else:
        _answer.voter.append(current_user)
        db.session.commit()

    return redirect(url_for('question.detail', question_id=_answer.question.id))
