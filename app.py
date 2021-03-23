import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Chocolate, Chocolatier

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.route('/')
  def index():
    greeting="Welcome to The Chocolatier Electric!!!"
    return greeting

  @app.route('/chocolates')
  def get_chocolates():
    recipe=[c.format() for c in Chocolate.query.all()]
    return jsonify({"Success":True, "Chocolates":recipe})


  @app.route('/chocolatiers')
  def get_chocolatiers():
    recipe=[c.format() for c in Chocolatier.query.all()]
    return jsonify({"Success":True, "Chocolatiers":recipe})


  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)