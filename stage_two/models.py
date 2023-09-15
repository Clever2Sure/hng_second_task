from run_app import db  # Assuming your run_app.py is in the same directory as models.py

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)