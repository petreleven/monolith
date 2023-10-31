from flask_wtf import FlaskForm
import wtforms as f
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    email = f.StringField('email', validators=[DataRequired()])
    firstname = f.StringField('firstname')
    password = f.PasswordField('password')
    age = f.IntegerField('age')
    weight = f.FloatField('weight')
    max_hr = f.IntegerField('max_hr')
    rest_hr = f.IntegerField('rest_hr')
    vo2max = f.IntegerField('vo2max')

    display = ['email', 'firstname', 'password',
               'age', 'weight', 'max_hr', 'rest_hr', 'vo2max']


class LoginForm(FlaskForm):
    email = f.StringField('email', validators=[DataRequired()])
    password = f.PasswordField('password')
    display = ['email', 'password']
