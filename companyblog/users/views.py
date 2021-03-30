from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import logout_user, login_user

from companyblog import db
from companyblog.models import User
from companyblog.users.forms import RegistrationForm, LoginForm

users = Blueprint('user', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('Thanks for registration!')

        return redirect(url_for('users.login'))

    return render_template('register.html', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash("Login Success!")

            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next = url_for('core.index')

            return redirect(next)

    return render_template('login.html', form=form)


@users.route("/logout")
def logout():
    logout_user()

    return redirect(url_for('core.index'))
