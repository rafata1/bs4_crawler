import requests
import json

url = "http://43.207.168.118/?rest_route=/wp/v2/posts"

payload = json.dumps({
  "title": "Eastenders actor 'was run over by £70m Chelsea defender Wesley Fofana in 2022 incident with the dad-of-two suffering a broken collarbone after being catapulted into the air by player's Lamborghini'",
  "status": "publish",
  "content": "abc123"
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Basic ZHVuZ2NkYTp6NHk0IE9BMTYgSmNNcSBkNkVyIGh1ejkgSDFzTg=='
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
