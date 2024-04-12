import requests
endpoint = "https://speakmentor-django.onrender.com"

get_response = requests.get(endpoint)

print(get_response.json())