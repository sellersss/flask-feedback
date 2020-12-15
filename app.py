from flask import Flask, request, render_template, flash, redirect, session
from forms import RegisterForm, LoginForm
from models import db, connect_db, Users

app = Flask(__name__)

app.config['SECRET_KEY'] = 'passw0rd'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()


@app.route('/')
def index():
    """Site home.

    Redirects user to registration page.
    """

    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register users.

    Displays a form that when submitted creates a user.
    """

    form = RegisterForm()

    if form.validate_on_submit():
        # Assigning submitted form data
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        # Registering a user
        user = Users.register(username, password, email, first_name, last_name)
        session["username"] = user.username
        db.session.add(user)
        db.session.commit()

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login users.

    Displays a form that when submitted allows a user to access logged in
    features.
    """

    form = LoginForm()

    if form.validate_on_submit():
        # Assigning submitted form data
        username = form.username.data
        password = form.password.data

        # Authenticating a user
        user = Users.authenticate(username, password)
        if user:
            session['username'] = user.username
            return redirect('/secret')
        flash('Bad username or password.', 'danger')

    return render_template('login.html', form=form)


@app.route('/secret')
def secret():
    """Secret page.

    Only for logged in users.
    """

    return 'You made it!'
