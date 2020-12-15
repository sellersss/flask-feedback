from flask import Flask, redirect, render_template, flash, session
from forms import RegisterForm, LoginForm, FeedbackForm
from models import Feedback, db, connect_db, Users
from sqlalchemy.exc import IntegrityError

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
        db.session.add(user)

        # Handle non-unique username
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append(
                'Username already exists, please choose another one.')
            return render_template('register.html', form=form)

        return redirect(f'/users/{username}')

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

            return redirect(f'/users/{user.username}')
        else:
            flash('Incorrect username or password. Please try again.', 'danger')

    return render_template('login.html', form=form)


@app.route('/users/<username>')
def user_info(username):
    """User info page.

    Only for logged in users and displays all user details but their password.
    """

    current_username = session.get('username', None)
    if current_username and current_username == username:
        current_user = Users.query.filter_by(username=current_username).one()

        return render_template('user.html', user=current_user)
    return redirect('/')


@app.route('/users/<username>/delete', methods=['POST'])
def user_delete(username):
    """Removes a users.

    First removes a user and then logs the user out.
    """

    current_username = session.get('username', None)
    if current_username and current_username == username:
        current_user = Users.query.filter_by(username=current_username).one()

        db.session.delete(current_user)
        db.session.commit()

        return redirect('logout')
    return redirect(f'/users/{username}')


@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def feedback_add(username):
    """Add feedback.

    Displays the add feedback form and posts it to the database on submit.
    """

    current_username = session.get('username', None)
    if current_username and current_username == username:
        form = FeedbackForm()
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            feedback = Feedback(title=title,
                                content=content,
                                username=current_username)

            db.session.add(feedback)
            db.session.commit()

            return redirect(f'/users/{username}')
        return render_template('feedback_add.html', form=form, user=current_username)


@app.route('/feedback/<int:feedback_id>/feedback/update', methods=['GET', 'POST'])
def feedback_update(feedback_id):
    """"""

    current_username = session.get('username', None)
    feedback = Feedback.query.get_or_404(feedback_id)
    if current_username and current_username == feedback.username:
        form = FeedbackForm(obj=feedback)
        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data

            db.session.add(feedback)
            db.session.commit()

            return redirect(f'/users/{current_username}')
        return render_template('feedback_edit.html', form=form, user=current_username, feedback=feedback)


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback.

    Removes a feedback object from database through a post request.
    """

    current_username = session.get("username", None)
    feedback = Feedback.query.get_or_404(feedback_id)
    if current_username and current_username == feedback.username:
        db.session.delete(feedback)
        db.session.commit()

        return redirect(f"/users/{current_username}")


@app.route('/logout')
def logout():
    """Logout a user.

    Logs user out, disabling access to /secret.
    """

    session.pop('username')
    return redirect('/')
