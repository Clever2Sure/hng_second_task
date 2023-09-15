from flask import Blueprint, request, jsonify
from models import Person, db

api_bp = Blueprint('api', __name__)

@api_bp.route('/persons', methods=['GET'])
def get_all_persons():
    persons = Person.query.all()
    return jsonify([{'id': person.id, 'name': person.name} for person in persons]), 200

@api_bp.route('/persons/<int:person_id>', methods=['GET'])
def get_person(person_id):
    person = Person.query.get(person_id)
    if person:
        return jsonify({'id': person.id, 'name': person.name}), 200
    else:
        return jsonify({'error': 'Person not found'}), 404

@api_bp.route('/persons', methods=['POST'])
def create_person():
    data = request.get_json()
    if 'name' in data:
        new_person = Person(name=data['name'])
        db.session.add(new_person)
        db.session.commit()
        return jsonify({'message': 'Person created successfully'}), 201
    else:
        return jsonify({'error': 'Invalid or missing name'}), 400

@api_bp.route('/persons/<int:person_id>', methods=['PUT'])
def update_person(person_id):
    data = request.get_json()
    person = Person.query.get(person_id)
    if person:
        if 'name' in data:
            person.name = data['name']
            db.session.commit()
            return jsonify({'message': 'Person updated successfully'}), 200
        else:
            return jsonify({'error': 'Name is required'}), 400
    else:
        return jsonify({'error': 'Person not found'}), 404

@api_bp.route('/persons/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    person = Person.query.get(person_id)
    if person:
        db.session.delete(person)
        db.session.commit()
        return jsonify({'message': 'Person deleted successfully'}), 200
    else:
        return jsonify({'error': 'Person not found'}), 404