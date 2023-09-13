import unittest
import json
from app import app, db
from app.models import Person  # Import your Person model

class TestCRUDOperations(unittest.TestCase):
    def setUp(self):
        # Create a test client
        self.app = self.app = app.test_client()

        # Create tables in the test database
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Drop tables after each test
        with app.app_context():
            db.drop_all()

    def test_create_person(self):
        response = self.app.post('/api', json={"name": "John Doe"})
        self.assertEqual(response.status_code, 201)

    def test_read_person(self):
        # Create a test person in the database
        test_person = Person(name="Test Person")
        with app.app_context():
            db.session.add(test_person)
            db.session.commit()

        response = self.app.get(f'/api/{test_person.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Test Person")

    def test_update_person(self):
        # Create a test person in the database
        test_person = Person(name="Test Person")
        with app.app_context():
            db.session.add(test_person)
            db.session.commit()

        response = self.app.put(f'/api/{test_person.id}', json={"name": "Updated Name"})
        self.assertEqual(response.status_code, 200)

        # Check if the name has been updated in the database
        with app.app_context():
            updated_person = Person.query.get(test_person.id)
            self.assertEqual(updated_person.name, "Updated Name")

    def test_delete_person(self):
        # Create a test person in the database
        test_person = Person(name="Test Person")
        with app.app_context():
            db.session.add(test_person)
            db.session.commit()

        response = self.app.delete(f'/api/{test_person.id}')
        self.assertEqual(response.status_code, 200)

        # Check if the person has been deleted from the database
        with app.app_context():
            deleted_person = Person.query.get(test_person.id)
            self.assertIsNone(deleted_person)

if __name__ == '__main__':
    unittest.main()
