Flask API Documentation
Overview
This Flask API project simplifies managing person data with CRUD operations (Create, Read, Update, Delete). It offers the following features:

Create a person record.
Read details about a person by Slack name.
Update a person's information by Slack name.
Delete a person from the database by Slack name.

Endpoints
Read a Person by Slack Name
HTTP Method: GET

Endpoint: /api

Query Parameter: slack_name (e.g., /api?slack_name=Paul_Clever)

Response Format: JSON

Response Example:

{
  "id": 1,
  "name": "Paul Clever"
}


Create a Person
HTTP Method: POST

Endpoint: /api

Request Format: JSON

Request Body Example:

{
  "name": "Paul Clever"
}


Response Format: JSON

Response Example:

{
  "name": "Paul Clever"
}


Update a Person by Slack Name
HTTP Method: PUT

Endpoint: /api

Query Parameter: slack_name (e.g., /api?slack_name=Paul_Clever)

Request Format: JSON

Request Body Example:

{
  "name": "Updated Name"
}


Response Format: JSON

Response Example:

{
  "name": "Updated Name"
}

Delete a Person by Slack Name
HTTP Method: DELETE

Endpoint: /api

Query Parameter: slack_name (e.g., /api?slack_name=Paul_Clever)

Response Format: JSON

Response Example:

{
  "message": "Person deleted successfully"
}


Testing
To ensure the API's functionality, run the following command:

python -m unittest tests/test_app.py


Deployment
You can easily deploy this Flask API project on Render.com by following these steps:

Fork the Example Repository:

Fork the example repository on GitHub by clicking the "Fork" button.
Create a New Web Service on Render:

Log in to your Render.com account.

Connect Your Forked Repository:

In the Render dashboard, create a new web service.
Choose your forked repository.
Configure Deployment Settings:

Specify the runtime as Python.
Set the build command to pip install -r requirements.txt.
Use the start command: gunicorn app:app.
Add Environment Variables (if needed):

Set any required environment variables.
Choose a Plan:
Select a suitable plan.
Deploy Your Application:

Click "Create Web Service."
Your Flask API will be automatically deployed and accessible via the provided URL.
For more detailed deployment and configuration information, refer to the Render documentation.

Conclusion
This Flask API project simplifies managing person data with robust CRUD operations, proper error handling, and easy deployment options. Feel free to explore and adapt it for your specific needs!
