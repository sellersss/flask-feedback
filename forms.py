from flask_wtf import FlaskForm
from wtforms import validators as v
from wtforms import StringField, PasswordField


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


class FeedbackForm(FlaskForm):
    """"""

    title = StringField('Title',
                        validators=[
                            v.InputRequired(),
                            v.Length(max=100)])
    content = StringField('Content', validators=[v.InputRequired()])
