from flask import Blueprint, request, jsonify
from flask_cors import cross_origin 
from backend.models.mysql_book_model import BookModel

book_blueprint = Blueprint('book_blueprint', __name__)
model = BookModel()

@book_blueprint.route('/book', methods=['POST'])
@cross_origin()
def create_book():
    content = model.create_book(request.json['book_title'], request.json['book_description'], request.json['author_id'], request.json['publication_year'], request.json['genre'])    
    return jsonify(content)

@book_blueprint.route('/book', methods=['PUT'])
@cross_origin()
def update_book():
    content = model.update_book(request.json['book_id'], request.json['book_title'], request.json['book_description'], request.json['author_id'], request.json['publication_year'], request.json['genre'])    
    return jsonify(content)

@book_blueprint.route('/book', methods=['DELETE'])
@cross_origin()
def delete_book():
    return jsonify(model.delete_book(int(request.json['book_id'])))

@book_blueprint.route('/book', methods=['GET'])
@cross_origin()
def book():
    return jsonify(model.get_book(int(request.json['book_id'])))

@book_blueprint.route('/books', methods=['GET'])
@cross_origin()
def books():
    return jsonify(model.get_books())