import requests
import json

url = 'http://localhost:8080/delete_review/9'

response = requests.delete(url)

print(response.status_code)
print(json.dumps(response.json()))