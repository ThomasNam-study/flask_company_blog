from datetime import datetime

from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import current_user, login_required

from companyblog import db
from companyblog.models import Question, Answer, Comment
from companyblog.question.forms import AnswerForm, CommentForm

comment_view = Blueprint('comment', __name__)


@comment_view.route('/create/question/<int:question_id>', methods=("GET", "POST",))
@login_required
def create_question(question_id):
    form = CommentForm()

    q = Question.query.get_or_404(question_id)

    if request.method == 'POST' and form.validate_on_submit():
        content = form.content.data

        c = Comment(content=content, create_date=datetime.now(), user=current_user, question=q)

        db.session.add(c)
        db.session.commit()

        return redirect(url_for('question.detail', question_id=question_id))

    return render_template('comment/comment_form.html', question=q, form=form)


@comment_view.route('/modify/question/<int:comment_id>/', methods=('GET', 'POST'))
@login_required
def modify_question(comment_id):
    comment = Comment.query.get_or_404(comment_id)

    if current_user != comment.user:
        flash("수정 권한이 없습니다.")
        return redirect(url_for('question.detail', question_id=comment.question.id))

    if request.method == 'POST':
        form = AnswerForm()

        if form.validate_on_submit():
            form.populate_obj(comment)
            comment.modify_date = datetime.now()
            db.session.commit()

            return redirect(url_for('question.detail', question_id=comment.question.id))
    else:
        form = CommentForm(obj=comment)

    return render_template('comment/comment_form.html', form=form, comment=comment)


@comment_view.route('/delete/question/<int:comment_id>/')
def delete_question(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    q_id = comment.question.id

    if current_user != comment.user:
        flash("삭제 권한이 없습니다.")
    else:
        db.session.delete(comment)
        db.session.commit()

        flash("삭제 되었습니다.")

    return redirect(url_for('question.detail', question_id=q_id))


@comment_view.route('/create/answer/<int:answer_id>', methods=("GET", "POST",))
@login_required
def create_answer(answer_id):
    form = CommentForm()

    answer = Answer.query.get_or_404(answer_id)

    if request.method == 'POST' and form.validate_on_submit():
        content = form.content.data

        c = Comment(content=content, create_date=datetime.now(), user=current_user, answer=answer)

        db.session.add(c)
        db.session.commit()

        return redirect(url_for('question.detail', question_id=answer.question.id))

    return render_template('comment/comment_form.html', form=form)


@comment_view.route('/modify/answer/<int:comment_id>/', methods=('GET', 'POST'))
@login_required
def modify_answer(comment_id):
    comment = Comment.query.get_or_404(comment_id)

    if current_user != comment.user:
        flash("수정 권한이 없습니다.")
        return redirect(url_for('question.detail', question_id=comment.answer.question.id))

    if request.method == 'POST':
        form = AnswerForm()

        if form.validate_on_submit():
            form.populate_obj(comment)
            comment.modify_date = datetime.now()
            db.session.commit()

            return redirect(url_for('question.detail', question_id=comment.answer.question.id))
    else:
        form = CommentForm(obj=comment)

    return render_template('comment/comment_form.html', form=form, comment=comment)


@comment_view.route('/delete/answer/<int:comment_id>/')
def delete_answer(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    q_id = comment.answer.question.id

    if current_user != comment.user:
        flash("삭제 권한이 없습니다.")
    else:
        db.session.delete(comment)
        db.session.commit()

        flash("삭제 되었습니다.")

    return redirect(url_for('question.detail', question_id=q_id))
