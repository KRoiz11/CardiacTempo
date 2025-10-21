from flask import Flask, redirect, jsonify, request
import spotify, recco
import json
import os

client_id = os.getenv("CLIENT_ID")
redirect_uri = os.getenv("REDIRECT_URI")
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, CardiacTempo!"

@app.route("/login")
def login():
    scope = "user-read-playback-state user-modify-playback-state user-read-currently-playing playlist-read-private"
    auth_url = (
        "https://accounts.spotify.com/authorize"
        "?response_type=code"
        f"&client_id={client_id}"
        f"&scope={scope}"
        f"&redirect_uri={redirect_uri}"
    )
    return redirect(auth_url)

@app.route("/callback")
def callback():
    error = request.args.get("error")
    if error:
        return jsonify({"Error": error, "Reason": "User denied access permissions to the app."}), 400
    
    code = request.args.get("code")
    if not code:
        return jsonify({"Error": "no_code", "Reason": "No authorization code recieved."}), 400
    
    try:
        token = spotify.get_token(code=code)

        name = "..."
        playlist_id = spotify.get_current_user_playlist(token, name)
        playlist_length = spotify.get_playlist_length(token, playlist_id)

        print(playlist_length)
        recco_track_ids = []
        for offset in range(0, 401, 40):
            spotify_track_ids_set = spotify.get_playlist_items(token, playlist_id, offset)
            recco_track_ids_set = recco.get_recco_track_ids(spotify_track_ids_set)
            recco_track_ids.extend(recco_track_ids_set)
        print(len(recco_track_ids))
        return "Success"
        # return jsonify({"access_token": token}) # shows access_token on web browser for testing purposes
    except Exception as e:
        return jsonify({"Error": "token_exchange failed", "Reason": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)