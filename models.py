from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os
from datetime import datetime
from sqlalchemy.sql import func

database_path = os.environ["DATABASE_URL"]

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


"""
Chocolate
Food made with chocolate, type of chocolate, vendor(foreign key/join table)
"""


class Chocolate(db.Model):
    __tablename__ = "Chocolate"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    chocolate_type = Column(String, nullable=False)
    vendor = Column(String, nullable=False)
    vendor_id = db.Column(
        db.Integer, db.ForeignKey("Chocolatier.id", ondelete="CASCADE")
    )
    comments = Column(String)

    def __init__(self, name, chocolate_type, vendor, vendor_id, comments=""):
        self.name = name
        self.chocolate_type = chocolate_type
        self.vendor = vendor
        self.vendor_id = vendor_id
        self.comments = comments

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "chocolate_type": self.chocolate_type,
            "vendor": self.vendor,
            "vendor_id": self.vendor_id,
            "comments": self.comments,
        }

    def __repr__(self):
        return "<Chocolate " + str(self.id) + " " + str(self.name) + ">"


"""
Chocolatier
Chocolatier details: vendor/biz name, address, chef,
website, phone, reviews/comments
"""


class Chocolatier(db.Model):
    __tablename__ = "Chocolatier"

    id = Column(Integer().with_variant(Integer, "postgres"), primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    website = Column(String)
    facebook = Column(String)
    phone = Column(String, nullable=False)
    chef = Column(String)
    comments = Column(String)
    chocolates = db.relationship(
        "Chocolate", backref="chocolatier", passive_deletes=True
    )

    def __init__(self, name, address, website, facebook, phone, chef, comments=""):  # noqa
        self.name = name
        self.address = address
        self.website = website
        self.facebook = facebook
        self.phone = phone
        self.chef = chef
        self.comments = comments

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "website": self.website,
            "facebook": self.facebook,
            "phone": self.phone,
            "chef": self.chef,
            "comments": self.comments,
        }

    def __repr__(self):
        return "<Chocolatier " + str(self.id) + " " + str(self.name) + ">"
