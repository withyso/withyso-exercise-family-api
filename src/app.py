"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = members
    return jsonify(response_body), 200

@app.route('/member', methods=['POST'])
def add_member():
    body = request.get_json(silent=True)
    if body is None:
        return "Body of the request shouldn't be empty", 400
    if "first_name" not in body:
        return "first_name is mandatory", 400
    if "age" not in body:
        return "You need to add an age", 400
    if "lucky_numbers" not in body:
        return "You need to add at least one lucky number", 400
    new_member = {
        "first_name": body["first_name"],
        "id": jackson_family._generateId(),
        "age":  body["age"],
        "last_name": jackson_family.last_name,
        "lucky_numbers":    body["lucky_numbers"]
    }
    print(new_member)
    jackson_family.add_member(new_member)
    return jsonify({"msg":"New member added"}), 201
    


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
