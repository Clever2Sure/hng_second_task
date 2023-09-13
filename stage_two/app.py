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

# Create a route that listens to /api
@app.route('/api', methods=['GET', 'POST'])
def crud_operations():
    if request.method == 'POST':
        data = request.get_json()

        if 'name' in data and is_valid_name(data['name']):
            new_person = Person(name=data['name'])
            db.session.add(new_person)
            db.session.commit()
            return jsonify({"message": "Person created successfully"}), 201
        else:
            return jsonify({"error": "Invalid or missing name"}), 400

    elif request.method == 'GET':
        slack_name = request.args.get('slack_name')

        if slack_name:
            person = Person.query.filter_by(name=slack_name).first()
            if person:
                return jsonify({"id": person.id, "name": person.name})
            else:
                return jsonify({"error": "Person not found"}), 404
        else:
            return jsonify({"error": "Missing slack_name query parameter"}), 400

# Updating a person by Slack Name (PUT request)
@app.route('/api', methods=['PUT'])
def update_person():
    data = request.get_json()
    slack_name = request.args.get('slack_name')

    if slack_name:
        person = Person.query.filter_by(name=slack_name).first()
        if person:
            if 'name' in data:
                person.name = data['name']
                db.session.commit()
                return jsonify({"message": "Person updated successfully"}), 200
            else:
                return jsonify({"error": "Name is required"}), 400
        else:
            return jsonify({"error": "Person not found"}), 404
    else:
        return jsonify({"error": "Missing slack_name query parameter"}), 400

# Deleting a person by Slack Name (DELETE request)
@app.route('/api', methods=['DELETE'])
def delete_person():
    slack_name = request.args.get('slack_name')

    if slack_name:
        person = Person.query.filter_by(name=slack_name).first()
        if person:
            db.session.delete(person)
            db.session.commit()
            return jsonify({"message": "Person deleted successfully"}), 200
        else:
            return jsonify({"error": "Person not found"}), 404
    else:
        return jsonify({"error": "Missing slack_name query parameter"}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5003)

