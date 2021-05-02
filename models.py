"""Models for Feedback app, including User & Feedback."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """Feedback site user."""

    __tablename__ = "user"

    username = db.Column(db.String(20), 
                        primary_key=True, 
                        nullable=False, 
                        unique=True)

    password = db.Column(db.Text, 
                        nullable=False)
    
    email = db.Column(db.String(50), 
                        nullable=False)

    first_name = db.Column(db.String(30), 
                        nullable=False)
    
    last_name = db.Column(db.String(30), 
                        nullable=False)
    
    def __repr__(self):
        """Shows info about User SQLAlchemy object."""

        u = self
        return f"<User {u.username} {u.password} {u.email} {u.first_name} {u.last_name}>"

    # start_register
    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        """Register user w/ hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        # return instance of user w/username and hashed pwd
        return cls(username=username, 
                    password=hashed_utf8, 
                    email=email, 
                    first_name=first_name, 
                    last_name=last_name)
    # end_register

    # start_authenticate
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.get(username)

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False
    # end_authenticate    


class Feedback(db.Model):
    """Feedback for a user on the Feedback site."""

    __tablename__ = "feedback"

    id = db.Column(db.Integer, 
                        primary_key=True, 
                        auto_increment=True)

    title = db.Column(db.String(100),
                        nullable=False)
    
    content = db.Column(db.Text,
                        nullable=False)
    
    username = db.Column(db.Text,
                        db.ForeignKey('user.username'))
    
    user = db.relationship('User', backref='feedback')

    def __repr__(self):
        """Shows info for Feedback object."""

        f = self
        return f"<Feedback {f.id} {f.title} {f.content} {f.username} {f.user}"
    
    @classmethod
    def add(cls, title, content, username):
        """Add feedback for user once form is submitted."""

        return cls(title=title, 
                    content=content, 
                    username=username)