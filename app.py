import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Chocolate, Chocolatier
from auth import AuthError, requires_auth

def create_app(test_config=None):
  # creates and configures the app, using the Flask class to create an instance of "app"
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, PUT, DELETE, OPTIONS')
    return response

  #INDEX route--authentication should be requested for endpoints
  @app.route('/')
  def index():
    greeting="Welcome to The Chocolatier Electric!!!"
    return greeting

  #GET route for all chocolates, available to customers and managers
  @app.route('/chocolates')
  @requires_auth("get:chocolates")
  def get_chocolates(payload):
    recipe=[c.format() for c in Chocolate.query.all()]
    return jsonify({"success":True, "Chocolates":recipe}),200

  #POST route for all chocolates, available to customers and managers
  @app.route('/chocolates', methods=['POST'])
  @requires_auth("post:chocolates")
  def create_chocolate(payload):
    body = request.get_json()
    try:
      name=body.get('name', None)
      chocolate_type=body.get('chocolate_type', None)
      vendor=body.get('vendor', None)
      vendor_id=body.get('vendor_id', None)
      comments=body.get('comments',None)
      try:
        chocolate=Chocolate(name=name, chocolate_type=chocolate_type, vendor=vendor, vendor_id=vendor_id, comments=comments)
        chocolate.insert()
        return jsonify({'success':True, 'created': chocolate.id, 'name':chocolate.name, 'total_chocolates':len(Chocolate.query.all())}),200
        
      except Exception as e:
        print("Exception is ", e)
        abort(422)
    except Exception as e:
      print("Exception is ", e)
      abort(422)

  @app.route('/chocolates/search', methods=['POST'])
  @requires_auth("post:chocolates")
  def search(payload):
    body=request.get_json()
    searchTerm=body.get('searchTerm','')
    try:
      results = Chocolate.query.filter(Chocolate.name.ilike('%{}%'.format(searchTerm))).all()
      chocolate=[result.format() for result in results]
      return jsonify({ 'success':True, 'chocolates':chocolate}),200
    
    except Exception as e:
      print("Exception is ", e)
      abort(404)

  #PATCH route for all chocolates, available to customers and managers
  @app.route('/chocolates/<id>', methods=['PATCH'])
  @requires_auth("patch:chocolates")
  def edit_chocolates(payload, id):
    body = request.get_json()
    name=body.get('name', None)
    chocolate_type=body.get('chocolate_type', None)
    vendor=body.get('vendor', None)
    vendor_id=body.get('vendor_id', None)
    comments=body.get('comments',None)
    try:
        chocolate = Chocolate.query.filter(Chocolate.id == id).one_or_none()
        if chocolate is None:
            abort(404)
        chocolate.name = name
        chocolate.chocolate_type = chocolate_type
        chocolate.vendor = vendor
        chocolate.vendor_id = vendor_id
        chocolate.comments = comments
        chocolate.update()
        chocolate=list(chocolate.format())
        return jsonify({'success':True, 'chocolate':chocolate}), 200
    except Exception as e:
        print("Exception is ", e)
        abort(422)

  #DELETE route for all chocolates, available to managers only
  @app.route('/chocolates/<id>', methods=['DELETE'])
  @requires_auth("delete:chocolates")
  def delete_chocolates(payload, id):
    try:
        chocolate=Chocolate.query.filter(Chocolate.id == id).one_or_none()
        if chocolate is None:
            abort(404)
        chocolate.delete()
        return jsonify({'success':True, 'deleted': chocolate.id}), 200
    except Exception as e:
      abort(422)

  #GET route for chocolatiers, available to customers and managers
  @app.route('/chocolatiers')
  @requires_auth("get:chocolatiers")
  def get_chocolatiers(payload):
    recipe=[c.format() for c in Chocolatier.query.all()]
    return jsonify({"success":True, "Chocolatiers":recipe}),200

  #POST route for chocolatiers, available to managers only
  @app.route('/chocolatiers', methods=['POST'])
  @requires_auth("post:chocolatiers")
  def create_chocolatier(payload):
    body = request.get_json()
    try:
      name=body.get('name', None)
      address=body.get('address', None)
      website=body.get('website', None)
      facebook=body.get('facebook', None)
      phone=body.get('phone', None)
      chef=body.get('chef', None)
      comments=body.get('comments',None)

      try:
          chocolatier=Chocolatier(name=name, address=address, website=website, facebook=facebook, phone=phone, chef=chef, comments=comments)
          chocolatier.insert()
          return jsonify({'success':True, 'created': chocolatier.id, 'name':chocolatier.name, 'total_chocolatiers':len(Chocolatier.query.all())}),200
      except Exception as e:
        print("Exception is ", e)
        abort(422)
    except Exception as e:
      print("Exception is ", e)
      abort(422)

  #PATCH route for chocolatiers, available to managers only
  @app.route('/chocolatiers/<id>', methods=['PATCH'])
  @requires_auth("patch:chocolatiers")
  def edit_chocolatiers(payload, id):
    body = request.get_json()
    name=body.get('name', None)
    address=body.get('address', None)
    website=body.get('website', None)
    facebook=body.get('facebook', None)
    phone=body.get('phone', None)
    comments=body.get('comments',None)
    try:
        chocolatier = Chocolatier.query.filter(Chocolatier.id == id).one_or_none()
        if chocolatier is None:
            abort(404)
        chocolatier.name = name
        chocolatier.address = address
        chocolatier.website = website
        chocolatier.facebook = facebook
        chocolatier.phone = phone
        chocolatier.comments = comments
        chocolatier.update()
        edited_chocolatier=list(chocolatier.format())
        return jsonify({'success':True, 'chocolatier':edited_chocolatier}), 200
    except Exception as e:
        print("Exception is ", e)
        abort(422)

  #DELETE route for chocolatiers, available to managers only
  @app.route('/chocolatiers/<id>', methods=['DELETE'])
  @requires_auth("delete:chocolatiers")
  def delete_chocolatiers(payload, id):
    try:
      chocolatier=Chocolatier.query.filter(Chocolatier.id == id).one_or_none()
      if chocolatier is None:
        abort(404)
      chocolatier.delete()
      return jsonify({'success':True, 'deleted': chocolatier.id}), 200
    except Exception as e:
      abort(422)
#ERROR HANDLING

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
          "success": False,
          "error": 400,
          "message": "Bad Request. Please check your data and try again."
      }), 400
    
  @app.errorhandler(404)
  def not_found(error):
     return jsonify({
         "success": False,
         "error": 404,
         "message": "Resource Not Found. Sorry!"
     }), 404

  @app.errorhandler(405)
  def not_allowed(error):
      return jsonify({
          "success": False,
          "error": 405,
          "message": "That method is not allowed for this endpoint."
      }), 405
    
  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "Unprocessable. This request was formatted well, but may have semantic errors."
      }), 422

  @app.errorhandler(500)
  def server_error(error):
      return jsonify({
          "success": False,
          "error": 500,
          "message": "There was a problem with the server. Please try again later."
      }), 500

  @app.errorhandler(AuthError)
  def auth_error(error):
    return jsonify({
        "success":False,
        "error": 401,
        "message":"authentication failed"
    }), 401

  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)