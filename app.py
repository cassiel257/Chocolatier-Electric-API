import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)

  @app.route('/')
  def index():
    greeting="Welcome to The Chocolatier Electric!!!"
    return greeting

  @app.route('/chocolates')
  def get_chocolates():
    recipe=Chocolate.query.all()
    return recipe

  @app.route('/chocolatiers')
  def get_chocolatiers():
    recipe=Chocolatier.query.all()
    return recipe

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)