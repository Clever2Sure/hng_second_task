from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables from .env file into os.environ
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # Replace with your database URL
db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# Define a function to validate the name
def is_valid_name(name):
    return isinstance(name, str) and len(name.strip()) > 0

# Create a person record
@app.route('/api', methods=['POST'])
def create_person():
    if request.method == 'POST':
        data = request.get_json()

        if 'name' in data and is_valid_name(data['name']):
            new_person = Person(name=data['name'])
            db.session.add(new_person)
            db.session.commit()
            
            # Adjust the response format here to match your documentation
            response_data = {"name": data['name']}
            
            return jsonify(response_data), 201
        else:
            return jsonify({"error": "Invalid or missing name"}), 400

# Read details about a person
@app.route('/api/<int:person_id>', methods=['GET'])
def read_person(person_id):
    if request.method == 'GET':
        person = Person.query.get(person_id)
        if person:
            # Adjust the response format here to match your documentation
            response_data = {
                "id": person.id,
                "name": person.name  # Adjust the name format if needed
            }
            return jsonify(response_data), 200
        else:
            return jsonify({"error": "Person not found"}), 404

# Update a person's information
@app.route('/api/<int:person_id>', methods=['PUT'])
def update_person(person_id):
    if request.method == 'PUT':
        data = request.get_json()
        person = Person.query.get(person_id)

        if person:
            if 'name' in data and is_valid_name(data['name']):
                person.name = data['name']
                db.session.commit()
                
                # Adjust the response format here to match your documentation
                response_data = {"name": data['name']}
                
                return jsonify(response_data), 200
            else:
                return jsonify({"error": "Invalid or missing name"}), 400
        else:
            return jsonify({"error": "Person not found"}), 404

# Delete a person from the database
@app.route('/api/<int:person_id>', methods=['DELETE'])
def delete_person(person_id):
    if request.method == 'DELETE':
        person = Person.query.get(person_id)

        if person:
            db.session.delete(person)
            db.session.commit()
            
            # Adjust the response format here to match your documentation
            response_data = {"message": "Person deleted successfully"}
            
            return jsonify(response_data), 200
        else:
            return jsonify({"error": "Person not found"}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Initialize the database with your name
        paul_clever = Person(name="Paul Clever")
        db.session.add(paul_clever)
        db.session.commit()

    app.run(host='0.0.0.0', port=5004)