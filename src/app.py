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

#Miembros iniciales ------------------------

Jhon = {
    "first name" : 'Jhon',
    "age" : 33,
    "lucky number" : [7, 13, 22]
}

Jane = {
    "first name" : 'Jane',
    "age" : 35,
    "lucky number" : [10, 14, 3]
}

Jimmy = {
    "first name" : 'Jimmy',
    "age" : 5,
    "lucky number" : [1]
}

Pepe = {
    "first name" : 'Pepe',
    "age" : 32,
    "lucky number" : [4,5,6]
}

#añadir miembros a la familia Jackson ------------------

jackson_family.add_member(Jhon)
jackson_family.add_member(Jane)
jackson_family.add_member(Jimmy)

print('Jackson---->', jackson_family.get_all_members())

#Obtener miembros de la familia ------------------------

@app.route('/members', methods=['GET'])
def get_all_members():
        members = jackson_family.get_all_members()
        return jsonify(members), 200

#subir miembros ----------------------------------------

@app.route('/members', methods=['POST'])
def add_member():
    data = request.json
    jackson_family.addmember(data)
    return jsonify(data), 200

#eliminar miembros ----------------------------------------

@app.route('/members/<int:id>', methods =['DELETE'])
def delete_member(id):
     member = jackson_family.delete_member(id)
     if member:
        jackson_family.delete_member(id)
        return jsonify({"message": "Member delete"}), 200
     else:
        return jsonify({"message": "Member not found"}), 404
     



#-------------------------------------------------------

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
    response_body = {
        "hello": "world",
        "Jackson": members
    }


    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
