from flask import Blueprint, request, jsonify
from flask_cors import cross_origin 
from backend.models.mysql_author_model import AuthorModel

author_blueprint = Blueprint('author_blueprint', __name__)
model = AuthorModel()

@author_blueprint.route('/author', methods=['POST'])
@cross_origin()
def create_author():
    content = model.create_author(request.json['author_name'], request.json['author_bio'], request.json['author_photo'])    
    return jsonify(content)

@author_blueprint.route('/author', methods=['PUT'])
@cross_origin()
def update_author():
    content = model.update_author(request.json['author_id'], request.json['author_name'], request.json['author_bio'], request.json['author_photo'])    
    return jsonify(content)

@author_blueprint.route('/author', methods=['DELETE'])
@cross_origin()
def delete_author():
    return jsonify(model.delete_author(int(request.json['author_id'])))

@author_blueprint.route('/author', methods=['GET'])
@cross_origin()
def author():
    return jsonify(model.get_author(int(request.json['author_id'])))

@author_blueprint.route('/authors', methods=['GET'])
@cross_origin()
def authors():
    return jsonify(model.get_authors())