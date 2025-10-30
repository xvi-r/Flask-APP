import requests
import os
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode
import json
import xmltodict

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

#Get Current Streamer's Stream info
def is_streamer_live(username, db = True):
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
        if db == True:
            return stream #If we are calling the function for our data base we return the dictionary to initialize the entity easier
        else:
            return f"🟢LIVE<br> Title: {stream["title"]}<br> Viewers: {stream["viewer_count"]}<br> Game: {stream["game_name"]}"
        
    else:
        return "🔴 NOT LIVE"


#Get Streamer Channel Info
def getStreamerData(username): 
    if username == "":
        return
    token = get_twitch_token()
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(
        f"https://api.twitch.tv/helix/users?login={username}",
        headers=headers,
        params={"user_login": username}
    )
    data = response.json()
    
    return data


def getTitanfallNetwork(id):

    url = "https://R2-pc.stryder.respawn.com/communities.php"

    # Query string parameters
    params = {
        "qt": "communities-getsettings",
        "hardware": "PC",
        "uid": "1009397012783",
        "language": "english",
        "getsettings": "1",
        "id": id,
        "cprot": "7",
        "timezoneOffset": "1"
    }

    headers = {
        "Host": "R2-pc.stryder.respawn.com",
        "User-Agent": "Respawn HTTPS/1.0",
        "Accept": "*/*",
        "X-Respawn-Handle": "1507350",
        "X-Respawn-Key": "LABj38NWSTxHUhdYaP62ZU6HtutCas3L"
    }

    data = {
        "env": "production",
        "3pToken": "PC_PLACEHOLDER_3P_TOKEN",
        "NucleusToken": "*0a1iWNjXVpg34WKx8NW2wQkjzBORVtsPlQrV28spdvsjPwvIID9zhKtb00w6TRjewISMBjdFJfi5H3Y1Bq8PPfHavyGMvW9sRGF-uY-uAy4bWB3niWF_KLhT4lv4l9DaGxhR8KucCw-IS9zZb0ZOwFRfRAZkxuIHl0z166pPW0oNeRkw63RMjpZkoc-gpJtpPLoInqKVs8X_fQBPr0qFFj7V1wddMcwUOiZGcLpNxBvC-2sXqnd6LX4oY_xgklrZuEGSX-MeA6C7z_4wKETwXmL5Gu80bFXenXypUtAYYH260uE8Q2rVeeArjZFeM0g0A5FPQeBbB8MT9r1dY1JuIhC93ROXxey_qaGgA0f28t9UsdSC9azI9B8Fo0jxvo1svZXwLRc8Zi8uDbvCRwrAudesiWN8uRbBNtt9hnguW19B8QAJOyFPqT10aIBfGiheuKOhewntsFVliOFN9Qn7uvtoG3tqcWsv63A4fmRfbO1aAeWaEY6h3YZ6A0IUti-bKTca9CHlhM0qh8vHoqwHAl7K3nObwVW8Z6SaRSoW9ur79haUMypzatwdf2nUxWVS9VvoNRY6yTPBmRfCGefPfC4Q8Aa5aYNhGVr1ERgwyQRkz_mzd-HwL38dzQABiVh-3",
        "securityToken": "HZSKrcn1uxDYjSlhQV58v2Bbn4sdeB8EWhqpgSoZfuqRjF6n9I7o6pgymJxrF1Ag8u17DdB5LaMTYr86Pu5GLuj6lfVp+hNSvPDYvHuFaI7ALTE1nMHIhe9hmQL91542"
    }

  
    response = requests.post(url, headers=headers, params=params, data=data, verify=False)
    xml_text = response.text.strip()


    json_string = f"{{{xml_text}}}" #Convert to actual json
    data = json.loads(json_string)
    
    if not data:
        return None #This happens if the community is unlisted
    
    return data["communitySettings"] #Return as dict


