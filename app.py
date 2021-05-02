"""Flask app for Feedback site where users can login, post/edit feedback, and logout."""

from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, EditFeedbackForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "1492ColumbusBlue"

toolbar = DebugToolbarExtension(app)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)


@app.route("/")
def redirect_to_registration():
    """Redirects user back to registration page."""

    return redirect('/register')


@app.route("/register")
def show_registration_form():
    "Display form for user registration."

    form = RegisterForm()

    return render_template("register.html", form=form)


@app.route("/register", methods=["POST"])
def handle_registration():
    """Upon submission, register/create a user."""

    form = RegisterForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(name, pwd, email, first_name, last_name)
        db.session.add(user)
        db.session.commit()

        session["user_name"] = user.username

        # on successful login, redirect to secret page
        return redirect(f"/users/{user.username}")

    else:
        flash("Sorry! Something went wrong with your registration. Please try again.")
        return render_template("register.html", form=form)

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET","POST"])
def login():
    """Produce login form or handle login."""

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(name, pwd)

        if user:
            session["user_name"] = user.username  # keep logged in
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)


@app.route("/users/<username>")
def show_user_info(username):
    """Hidden page that displays info about logged-in user."""

    if "user_name" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

    else:
        user = User.query.get_or_404(username)
        feedbacks = Feedback.query.all()
        return render_template("users.html", user=user, feedbacks=feedbacks)


@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    session.pop("user_name")

    return redirect("/")


@app.route("/users/<username>/delete", methods=["GET", "POST"])
def delete_user(username):
    """Remove the user from the database and delete their feedback."""

    if "user_name" not in session:
        flash("You must be logged in to view!")
        return redirect(f"/")

    else:
        user = User.query.get_or_404(username)
        Feedback.query.filter(Feedback.username == username).delete()
        User.query.filter(User.username == username).delete()
        db.session.commit()
        return redirect("/")


@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    """Display and handle form to add feedback."""

    

    if "user_name" not in session:
        flash("You must be logged in to view!")
        return redirect(f"/")

    else:
        form = FeedbackForm()

        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data

            feedback = Feedback.add(title=title, content=content, username=username)
            db.session.add(feedback)
            db.session.commit()
            return redirect(f"/users/{username}")

        else:
            flash("Sorry! Something went wrong with your feedback. Please try again.")
            return render_template("feedback.html", form=form)
    
        return render_template("feedback.html", form=form)


@app.route("/users/<username>/feedback/<feedback_id>/update", methods=["GET", "POST"])
def edit_feedback(username, feedback_id):
    """Display a form to edit feedback and submit updates."""

    if "user_name" not in session:
        flash("You must be logged in to view!")
        return redirect(f"/")

    else:
        feedback = Feedback.query.get(feedback_id)
        form = EditFeedbackForm(obj=feedback)

        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data

            feedback.title = title
            feedback.content = content
            db.session.commit()
            return redirect(f"/users/{username}")

        else:
            flash("Sorry! Something went wrong with your feedback. Please try again.")
            return render_template("edit_feedback.html", form=form)
    
        return render_template("edit_feedback.html", form=form, feedback=feedback, username=username)