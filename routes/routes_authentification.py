from flask import Blueprint, redirect, render_template, request
from models import db, User
from forms import LoginForm
from flask_login import login_user, logout_user, login_required
from htmx_reloader import htmx_template_selector

authenticate_routes = Blueprint("authenticate_routes", __name__)


@authenticate_routes.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email, password = form.data['email'], form.data['password']
        q = db.session.query(User).filter(User.email == email)
        user = q.first()
        if user is not None and user.authenticate(password):
            login_user(user)
            return redirect("/create_user")
    
    return htmx_template_selector(request, partial_html='login.html', full_html="login_f.html", context={"form":form})


@authenticate_routes.route('/logout')
def logout():
    logout_user()
    return redirect("/")
