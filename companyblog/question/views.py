from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from companyblog import db
from companyblog.models import Question
from companyblog.question.forms import QuestionForm, AnswerForm

question = Blueprint('question', __name__)


@question.route('/')
def index():
    page = request.args.get('page', type=int, default=1)

    q_list = Question.query.order_by(Question.create_date.desc())
    q_list = q_list.paginate(page, per_page=10)

    return render_template('question/question_list.html', q_list=q_list)


@question.route('/modify/<int:question_id>/', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    q = Question.query.get_or_404(question_id)

    if current_user != q.user:
        flash("수정 권한이 없습니다.")
        return redirect(url_for('question.detail', question_id=question_id))

    if request.method == 'POST':
        form = QuestionForm()

        if form.validate_on_submit():
            form.populate_obj(q)
            q.modify_date = datetime.now()
            db.session.commit()

            return redirect(url_for('question.detail', question_id=question_id))
    else:
        form = QuestionForm(obj=q)

    return render_template('question/question_form.html', form=form)


@question.route('/delete/<int:question_id>/', methods=('GET', 'POST'))
@login_required
def delete(question_id):
    q = Question.query.get_or_404(question_id)

    if current_user != q.user:
        flash("삭제 권한이 없습니다.")
        return redirect(url_for('question.detail', question_id=question_id))

    db.session.delete(q)
    db.session.commit()

    flash("삭제 되었습니다.")
    return redirect(url_for('question.index'))


@question.route('/create/', methods=('GET', 'POST'))
@login_required
def create():
    form = QuestionForm()

    if form.validate_on_submit():
        q = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now(),
                     user=current_user)

        db.session.add(q)
        db.session.commit()

        return redirect(url_for('question.index'))

    return render_template('question/question_form.html', form=form)


@question.route('/detail/<int:question_id>/')
def detail(question_id):
    q = Question.query.get_or_404(question_id)

    form = AnswerForm()

    return render_template('question/question_detail.html', question=q, form=form)
