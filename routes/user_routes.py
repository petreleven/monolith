from flask import Blueprint, jsonify
from flask import render_template, request, redirect
from models import User, db
from forms import UserForm
from flask_login import login_required
from stravalib import Client


user_routes = Blueprint('user_routes', __name__)


@user_routes.route("/")
def home():
    return render_template("home.html")


@user_routes.route("/users")
def users():
    users = db.session.query(User)
    return render_template("users.html", users=users)


@user_routes.route("/create_user", methods=['GET', 'POST'])
@login_required
def create_user():
    form = UserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_user = User()
            form.populate_obj(new_user)
            new_user.set_password(new_user.password)
            db.session.add(new_user)
            db.session.commit()
            return redirect("/users")
    
    return render_template("create_user.html", form=form, strava_uri = get_strava_auth_url())


@user_routes.route("/fetch")
def fetch_runs():
    from background import fetch_all_runs
    res = fetch_all_runs.delay()
    res.wait()
    return jsonify(res.result)


# Strava url setup
def get_strava_auth_url():
    client = Client()
    client_id = '115859'
    redirect = 'http://127.0.0.1:5000/strava_auth'
    url = client.authorization_url(client_id=client_id, redirect_uri=redirect)
    return url