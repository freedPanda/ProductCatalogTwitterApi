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

#admin table so products can be added or deleted
class Admin(db.Model):
    __tablename__ = 'Admin'

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False, unique=False)

#Products table for storing information about products
class Product(db.Model):
    __tablename__ = 'Product'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    price = db.Column(db.Integer, nullable=False, unique=False)
    image = db.Column(db.LargeBinary, nullable=False, unique=False)
    image1 = db.Column(db.LargeBinary, nullable=True, unique=False)
    image2 = db.Column(db.LargeBinary, nullable=True, unique=False)
    image3 = db.Column(db.LargeBinary, nullable=True, unique=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=False)
    available = db.Column(db.Boolean, nullable=False)
    #size = db.Column(db.Text, nullable=True, default=None)

    request = db.relationship('Request', backref='Product', lazy=True,
    passive_deletes=True)
    Sale = db.relationship('Sale', backref='Product', lazy=True,
    passive_deletes=True)

#customer can request to purchase a product via email
class Request(db.Model):
    __tablename__ = 'Request'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Text, nullable=False)
    firstname = db.Column(db.Text, nullable=False)
    lastname = db.Column(db.Text, nullable=False)
    message = db.Column(db.Text, nullable=False)
    product = db.Column(db.Integer, db.ForeignKey('Product.id', ondelete='CASCADE'), nullable=False)
    
#requests can be converted into sales
class Sale(db.Model):
    __tablename__ = 'Sale'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.Text, nullable=False)
    firstname = db.Column(db.Text, nullable=False)
    lastname = db.Column(db.Text, nullable=False)
    product = db.Column(db.Integer, db.ForeignKey('Product.id', ondelete='CASCADE'), nullable=False)
