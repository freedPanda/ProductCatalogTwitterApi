class Visit(db.Model):
    __tablename__ = 'Visit'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    day = db.Column(db.Text, nullable=False)
    month = db.Column(db.Text, nullable=False)
    year = db.Column(db.Text, nullable=False)

class Mention(db.Model):
    __tablename__='Mention'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Text, nullable=False)
    tweetid = db.Column(db.Text, nullable=False)
    #when entering hashtags, should enter all as one string, seperated by commas
    hashtags = db.Column(db.Text, nullable=True)
    screenname = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=True)