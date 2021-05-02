"""Seed file to populate the Feedback app with dummy users."""

from models import User, Feedback
from app import db

# Create all tables
db.drop_all()
db.create_all()

# If tables aren't empty, empty them
User.query.delete()
Feedback.query.delete()

# Create mock users with User class
harry = User(username="ChosenOne23",
                password="potter",
                email="hp23@gmail.com",
                first_name="Harry",
                last_name="Potter"
)

ron = User(username="BestFriend16",
                password="weasley",
                email="ronaldmcdonald16@yahoo.com",
                first_name="Ron",
                last_name="Weasley"
)

hermoine = User(username="GirlPower15",
                password="granger",
                email="grangerdanger15@aol.com",
                first_name="Hermoine",
                last_name="Granger"
)

new_harry = harry.register(harry.username, 
                harry.password,
                harry.email,
                harry.first_name,
                harry.last_name)
new_ron = ron.register(ron.username, 
                ron.password,
                ron.email,
                ron.first_name,
                ron.last_name)
new_hermoine = hermoine.register(hermoine.username, 
                    hermoine.password,
                    hermoine.email,
                    hermoine.first_name,
                    hermoine.last_name)

db.session.add(new_harry)
db.session.add(new_ron)
db.session.add(new_hermoine)
db.session.commit()

harry_fb = Feedback(title="Potter Poetry II",
                    content="Scar on my head like I'm Harry P... Oh wait ,that's me! #bars",
                    username=harry.username)

ron_fb = Feedback(title="Being a Brother",
                    content="Being a young brotha is hard, bro!",
                    username=ron.username)

hermoine_fb = Feedback(title="Spell Game Crazy like Bellatrix",
                    content="Y'all need to step ya spell game up! #MudbloodBaller",
                    username=hermoine.username)

db.session.add(harry_fb)
db.session.add(ron_fb)
db.session.add(hermoine_fb)
db.session.commit()