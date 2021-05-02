from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length, Optional


class RegisterForm(FlaskForm):
    """Form for registering a user."""

    username = StringField("Username", validators=[InputRequired(),
                                                    Length(min=6, max=20)])
    password = PasswordField("Password", validators=[InputRequired(),
                                                        Length(min=6, max=20)])
    email = StringField("Email", validators=[InputRequired(),
                                                Length(min=6, max=50)])
    first_name = StringField("First Name", validators=[InputRequired(),
                                                        Length(min=3, max=30)])
    last_name = StringField("Last Name", validators=[InputRequired(),
                                                        Length(min=6, max=30)])
    

class LoginForm(FlaskForm):
    """Form for logging a user in."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])


class FeedbackForm(FlaskForm):
    """Form for adding feedback as a user."""

    title = StringField("Title", validators=[InputRequired(),
                                                    Length(min=6, max=20)])
    content = TextAreaField("Content", validators=[InputRequired(),
                                                        Length(min=6, max=500)])


class EditFeedbackForm(FlaskForm):
    """Form for editing feedback as a user."""

    title = StringField("Title", validators=[Optional(),
                                                    Length(min=6, max=20)])
    content = TextAreaField("Content", validators=[Optional(),
                                                        Length(min=6, max=500)])