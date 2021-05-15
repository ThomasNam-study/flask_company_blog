from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import func

from companyblog import db
from companyblog.models import Question, Answer, User, question_voter
from companyblog.question.forms import QuestionForm, AnswerForm

question = Blueprint('question', __name__)


@question.route('/')
def index():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    so = request.args.get('so', type=str, default='recent')

    # q_list = Question.query.order_by(Question.create_date.desc())
    if so == 'recommand':
        sub_query = db.session.query(
            question_voter.c.question.id, func.count('*').label('num_voter')).group_by(
            question_voter.c.question.id).subquery()

        q_list = Question.query.outerjoin(sub_query, Question.id == sub_query.c.question_id).order_by(sub_query.c.num_voter.desc(), Question.create_date.desc())
    elif so == 'popular':
        sub_query = db.session.query(
            Answer.question_id, func.count('*').label('num_answer')).group_by(
            Answer.question_id).subquery()

        q_list = Question.query.outerjoin(sub_query, Question.id == sub_query.c.question_id).order_by(
            sub_query.c.num_answer.desc(), Question.create_date.desc())
    else:
        q_list = Question.query.order_by(Question.create_date.desc())

    if kw:
        search = '%%{}%%'.format(kw)

        sub_query = db.session.query(
            Answer.question_id, Answer.content, User.username
        ).join(
            User, Answer.user_id == User.id
        ).subquery()

        q_list = q_list.join(User).outerjoin(sub_query, sub_query.c.question_id == Question.id).filter(
            Question.subject.ilike(search) | Question.content.ilike(search) | User.username.ilike(
                search) | sub_query.c.content.ilike(search)
            | sub_query.c.username.ilike(search)).distinct()

    q_list = q_list.paginate(page, per_page=10)

    return render_template('question/question_list.html', q_list=q_list, kw=kw, so=so)


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
