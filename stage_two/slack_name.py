import requests

def handle_person_request(slack_name, data=None):
    base_url = "https://crud-api-0yn8.onrender.com/api"  # Updated API URL

    if data is None:
        # GET request to retrieve a person by Slack Name
        response = requests.get(f"{base_url}?slack_name={slack_name}")
        return response.json()
    elif not existing_person:
        # POST request to create a new person
        if slack_name == "Paul Clever":
            response = requests.post(base_url, json={"name": slack_name})
            return response.json()
        else:
            return {"error": "You can only create a person with Slack name 'Paul Clever'"}, 400
    else:
        # PUT request to update a person's name
        new_name = data.get("name")
        if new_name:
            response = requests.put(f"{base_url}?slack_name={slack_name}", json={"name": new_name})
            return response.json()
        else:
            return {"error": "Name is required for updating"}, 400

# DELETE request to delete a person by Slack Name
def delete_person(slack_name):
    base_url = "https://crud-api-0yn8.onrender.com/api"  # Updated API URL
    response = requests.delete(f"{base_url}?slack_name={slack_name}")
    return response.json()

if __name__ == "__main__":
    # Example usage of handle_person_request for different HTTP requests

    # GET request to retrieve a person by Slack Name
    slack_name = "Paul_Clever"  # Replace with the desired Slack Name
    print(handle_person_request(slack_name))

    # PUT request to update a person's name
    new_name = "New Name for Paul Clever"  # Replace with the desired new name
    print(handle_person_request(slack_name, {"name": new_name}))

    # DELETE request to delete a person by Slack Name
    print(delete_person(slack_name))

