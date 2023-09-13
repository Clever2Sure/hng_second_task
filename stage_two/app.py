from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv  # Import load_dotenv

# Load environment variables from .env file into os.environ
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # Replace with your database URL
db = SQLAlchemy(app)

# Define the Person model
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Define a function to validate the name
def is_valid_name(name):
    # Validate that the name is a non-empty string
    return isinstance(name, str) and len(name.strip()) > 0

# Define your routes after the Person model

# Creating a new person (POST request)
@app.route('/api', methods=['POST'])
def create_person():
    data = request.get_json()
    
    if 'name' in data and is_valid_name(data['name']):
        new_person = Person(name=data['name'])
        db.session.add(new_person)
        db.session.commit()
        return jsonify({"message": "Person created successfully"}), 201
    else:
        return jsonify({"error": "Invalid or missing name"}), 400

# Retrieving a person by ID (GET request)
@app.route('/api/<int:person_id>', methods=['GET'])
def get_person(person_id):
    try:
        person = Person.query.get(person_id)
        if person:
            return jsonify({"id": person.id, "name": person.name})
        else:
            return jsonify({"error": "Person not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Retrieving a person by name (GET request)
@app.route('/api/<string:person_name>', methods=['GET'])
def get_person_by_name(person_name):
    try:
        person = Person.query.filter_by(name=person_name).first()
        if person:
            return jsonify({"id": person.id, "name": person.name})
        else:
            return jsonify({"error": "Person not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Updating a person by ID (PUT request)
@app.route('/api/<int:person_id>', methods=['PUT'])
def update_person(person_id):
    person = Person.query.get(person_id)
    if person:
        data = request.get_json()
        if 'name' in data:
            person.name = data['name']
            db.session.commit()
            return jsonify({"message": "Person updated successfully"}), 200
        else:
            return jsonify({"error": "Name is required"}), 400
    else:
        return jsonify({"error": "Person not found"}), 404

# Deleting a person by ID (DELETE request)
@app.route('/api/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    person = Person.query.get(person_id)
    if person:
        db.session.delete(person)
        db.session.commit()
        return jsonify({"message": "Person deleted successfully"}), 200
    else:
        return jsonify({"error": "Person not found"}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5003)  # Run the app on port 5003