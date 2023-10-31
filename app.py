from Raven.Raven import create_jsonApp
import os
from routes.user_routes import user_routes
from routes.routes_authentification import authenticate_routes
from models import db, User
from stravalib import Client
from flask import request, redirect
from flask_login import  LoginManager, login_required, current_user

app = create_jsonApp(blueprints=[user_routes, authenticate_routes], isJSon=False)
app.template_folder = f'{os.getcwd()}/templates'

# Setup  configs
app.config['STRAVA_CLIENT_ID'] = "115859"
app.config['STRAVA_CLIENT_SECRET'] = "0003488944ccd8d4a1c703b5dd49a6f9e778017c"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local2.sqlite'


# database creation
db.init_app(app)
with app.app_context():
    db.create_all()

# Authentification
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(user_id)
    if user is not None:
        user._authenticated = True
    return user


#-------------------3RD PARTY------------------------#
#Strava OAuth2 exchange
@app.route('/strava_auth')
@login_required
def r_strava_auth():
    code = request.args.get('code')
    client = Client()
    xc = client.exchange_code_for_token
    access_token = xc(client_id=app.config['STRAVA_CLIENT_ID'],
                      client_secret=app.config['STRAVA_CLIENT_SECRET'], code=code)
    current_user.strava_token = access_token['access_token']
    db.session.add(current_user)
    db.session.commit()
    return redirect('/')
#---------------END 3RD PARTY------------------------#

if __name__ == "__main__":
    app.run()
