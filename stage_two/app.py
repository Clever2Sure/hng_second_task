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

# Read details about a person by Slack name
@app.route('/api', methods=['GET'])
def read_person_by_slack_name():
    slack_name = request.args.get('slack_name')

    if slack_name:
        person = Person.query.filter_by(name=slack_name).first()
        if person:
            # Format the name as "Paul Clever"
            formatted_name = ' '.join(map(lambda x: x.capitalize(), person.name.split('_')))
            response_data = {
                "id": person.id,
                "name": formatted_name
            }
            return jsonify(response_data), 200
        else:
            return jsonify({"error": "Person not found"}), 404
    else:
        return jsonify({"error": "Missing 'slack_name' query parameter"}), 400

# Create a person record
@app.route('/api', methods=['POST'])
def create_person():
    if request.method == 'POST':
        data = request.get_json()

        if 'name' in data and is_valid_name(data['name']):
            new_person = Person(name=data['name'])
            db.session.add(new_person)
            db.session.commit()

            response_data = {"name": data['name']}

            return jsonify(response_data), 201
        else:
            return jsonify({"error": "Invalid or missing name"}), 400

# Update a person's information
@app.route('/api', methods=['PUT'])
def update_person():
    slack_name = request.args.get('slack_name')
    data = request.get_json()
    person = Person.query.filter_by(name=slack_name).first()

    if person:
        if 'name' in data and is_valid_name(data['name']):
            person.name = data['name']
            db.session.commit()

            response_data = {"name": data['name']}

            return jsonify(response_data), 200
        else:
            return jsonify({"error": "Invalid or missing name"}), 400
    else:
        return jsonify({"error": "Person not found"}), 404

# Delete a person from the database
@app.route('/api', methods=['DELETE'])
def delete_person():
    slack_name = request.args.get('slack_name')
    person = Person.query.filter_by(name=slack_name).first()

    if person:
        db.session.delete(person)
        db.session.commit()

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

