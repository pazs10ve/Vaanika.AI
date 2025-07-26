import requests
import json

url = "http://127.0.0.1:8000/video/generate-custom"
payload = {
    "script": "This is a more advanced test video with a blue background and some music.",
    "title": "Advanced Python Test Video",
    "background_color": "#0000FF",
    "music_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"
}
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, data=json.dumps(payload), headers=headers)

print(response.status_code)
try:
    print(response.json())
except json.JSONDecodeError:
    print(response.text)