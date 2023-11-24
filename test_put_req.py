import requests
import json

url = 'http://localhost:8080/update_review'  # Adjust the URL if needed

payload = {
    'review_id': 4,
    'new_review_text': "Update: I added more cream cheese and it tasted better."
}

response = requests.put(url, json=payload)

print(response.status_code)
print(json.dumps(response.json()))