from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class Visit(db.Model):
    __tablename__ = 'Visit'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    day = db.Column(db.Text, nullable=False)
    month = db.Column(db.Text, nullable=False)
    year = db.Column(db.Text, nullable=False)

class Mention(db.Model):
    __tablename__='Mention'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #format Jul 8 2020
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

    @classmethod
    def register(cls, username, password):
        """Register an admin for admin web portal access

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        admin = Admin(
            username=username,
            password=hashed_pwd
        )

        db.session.add(admin)
        return admin

    @classmethod
    def authenticate(cls, username, password):
        """Find admin with `username` and `password`.

        This is a class method (call it on the class, not an individual admin.)
        It searches for a admin whose password hash matches this password
        and, if it finds such a admin, returns that admin object.

        If can't find matching admin (or if password is wrong), returns False.
        """

        admin = cls.query.filter_by(username=username).first()

        if admin:
            is_auth = bcrypt.check_password_hash(admin.password, password)
            if is_auth:
                return admin.username
            else:
                return False
        return False

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
