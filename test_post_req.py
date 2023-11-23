import requests
import json

url = 'http://localhost:8080/post_review'  # Adjust the URL if needed

# JSON payload for the POST request
payload = {
    "recipe_id": 12,
    "user_id": "sarah_m",
    "date": "2023-11-23T19:27:51.987Z",
    "rating": 4,
    "text": "The recipe was great!",
}

# Send the POST request
response = requests.post(url, json=payload)

# Print the response
print(response.status_code)
print(json.dumps(response.json()))