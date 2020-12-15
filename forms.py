from flask_wtf import FlaskForm
from wtforms import validators as v
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField


class RegisterForm(FlaskForm):
    """"""

    username = StringField('Username *',
                           validators=[v.InputRequired()])
    password = PasswordField('Password *', validators=[v.InputRequired()])
    email = StringField('Email *', validators=[v.InputRequired()])
    first_name = StringField('First name *', validators=[v.InputRequired()])
    last_name = StringField('Last name *', validators=[v.InputRequired()])


class LoginForm(FlaskForm):
    """"""

    username = StringField('Username *', validators=[v.InputRequired()])
    password = PasswordField('Password *', validators=[v.InputRequired()])
