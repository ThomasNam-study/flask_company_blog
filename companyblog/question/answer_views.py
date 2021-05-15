from datetime import datetime

from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import current_user, login_required

from companyblog import db
from companyblog.models import Question, Answer
from companyblog.question.forms import AnswerForm

answer = Blueprint('answer', __name__)


@answer.route('/create/<int:question_id>', methods=("POST",))
@login_required
def create(question_id):
    form = AnswerForm()

    q = Question.query.get_or_404(question_id)

    if form.validate_on_submit():
        content = form.content.data

        a = Answer(content=content, create_date=datetime.now(), user=current_user)

        q.answer_set.append(a)
        db.session.commit()

        return redirect(f"{url_for('question.detail', question_id=question_id)}#answer_{a.id}")

    return render_template('question/question_detail.html', question=q, form=form)


@answer.route('/modify/<int:answer_id>/', methods=('GET', 'POST'))
@login_required
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)

    if current_user != answer.user:
        flash("수정 권한이 없습니다.")
        return redirect(url_for('question.detail', question_id=answer.question.id))

    if request.method == 'POST':
        form = AnswerForm()

        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.modify_date = datetime.now()
            db.session.commit()

            return redirect(f"{url_for('question.detail', question_id=answer.question.id)}#answer_{answer.id}")
    else:
        form = AnswerForm(obj=answer)

    return render_template('answer/answer_form.html', form=form, answer=answer)


@answer.route('/delete/<int:answer_id>/')
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    q_id = answer.question.id

    if current_user != answer.user:
        flash("삭제 권한이 없습니다.")
    else:
        db.session.delete(answer)
        db.session.commit()

        flash("삭제 되었습니다.")

    return redirect(url_for('question.detail', question_id=q_id))
