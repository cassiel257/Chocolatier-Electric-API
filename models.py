from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
Chocolate
Food made with chocolate, type of chocolate, vendor(foreign key/join table)
'''
class Chocolate(db.Model):
  __tablename__ = 'Chocolate'

  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  chocolate_type = Column(String, nullable=False)
  vendor = Column(String, nullable=False)
  vendor_id = db.Column(db.Integer, db.ForeignKey('Chocolatier.id', ondelete='CASCADE'))
  comments = Column(String)

  def __init__(self, name, chocolate_type=""):
    self.name = name
    self.chocolate_type = chocolate_type
    self.vendor = vendor
    self.comments = comments

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'chocolate_type': self.chocolate_type,
      'vendor': self.vendor,
      'comments': self.comments}

'''
Chocolatier
Chocolatier details: vendor/biz name, address, chef, website, phone, reviews/comments
'''
class Chocolatier(db.Model):
  __tablename__ = 'Chocolatier'

  id = Column(Integer, primary_key=True)
  name = Column(String, unique=True, nullable=False)
  address = Column(String, nullable=False)
  website = Column(String)
  facebook = Column(String, default='https://facebook.com')
  phone = Column(String, nullable=False)
  chef = Column(String)
  comments = Column(String)
  chocolates = db.relationship('Chocolate', backref='chocolatier', passive_deletes=True)


  def __init__(self, name, address, website, phone, chef, comments=""):
    self.name = name
    self.address = address
    self.website = website
    self.phone = phone
    self.chef = chef
    self.comments = comments

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'address': self.address,
      'website': self.website,
      'phone': self.phone,
      'chef': self.chef,
      'comments': self.comments}