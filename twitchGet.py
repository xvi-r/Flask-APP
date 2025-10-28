import requests
import os

TWITCH_CLIENT_ID = os.environ.get("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = os.environ.get("TWITCH_CLIENT_SECRET")

def get_twitch_token():
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": TWITCH_CLIENT_ID,
        "client_secret": TWITCH_CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    response = requests.post(url, params=params)
    data = response.json()
    return data.get("access_token")


def is_streamer_live(username):
    if username == "":
        return
    token = get_twitch_token()
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(
        "https://api.twitch.tv/helix/streams",
        headers=headers,
        params={"user_login": username}
    )
    data = response.json()
    if data.get("data"):
        stream = data["data"][0]
        return f"🟢LIVE<br> Title: {stream["title"]}<br> Viewers: {stream["viewer_count"]}<br> Game: {stream["game_name"]}"
        
    else:
        return "🔴 NOT LIVE"

