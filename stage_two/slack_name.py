from app import app, db, Person  # Import necessary modules and classes from your Flask app

# Create an application context to interact with your database
with app.app_context():
    slack_name = 'Paul_Clever'  # Updated name to "Paul_Clever" (case-sensitive)

    # Check if a person record with the Slack name 'Paul_Clever' exists
    existing_person = Person.query.filter_by(name=slack_name).first()

    # Insert a new record if it doesn't exist
    if not existing_person:
        new_person = Person(name=slack_name)
        db.session.add(new_person)
        db.session.commit()

    # Print messages to indicate the results
    if existing_person:
        print("Person with Slack name 'Paul_Clever' already exists.")
    else:
        print("New person record with Slack name 'Paul_Clever' inserted successfully.")

