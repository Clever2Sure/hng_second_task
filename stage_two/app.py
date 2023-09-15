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
def read_person():
    slack_name = request.args.get('slack_name')
    
    if slack_name:
        person = Person.query.filter_by(name=slack_name).first()
        if person:
            return jsonify({"id": person.id, "name": person.name}), 200
        else:
            return jsonify({"error": "Person not found"}), 404
    else:
        return jsonify({"error": "Missing slack_name query parameter"}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Initialize the database with your name
        paul_clever = Person(name="Paul Clever")
        db.session.add(paul_clever)
        db.session.commit()

    app.run(host='0.0.0.0', port=5004)