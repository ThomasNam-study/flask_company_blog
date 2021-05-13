from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for

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


@question.route('/create/', methods=('GET', 'POST'))
def create():
    form = QuestionForm()

    if form.validate_on_submit():
        q = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now())

        db.session.add(q)
        db.session.commit()

        return redirect(url_for('question.index'))

    return render_template('question/question_form.html', form=form)


@question.route('/detail/<int:question_id>/')
def detail(question_id):
    q = Question.query.get_or_404(question_id)

    form = AnswerForm()

    return render_template('question/question_detail.html', question=q, form=form)
