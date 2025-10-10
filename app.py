from flask import Flask, redirect, request, jsonify
import main
import requests
import os

client_id = os.getenv("CLIENT_ID")
redirect_uri = os.getenv("REDIRECT_URI")
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, CardiacTempo!"

@app.route("/login")
def login():
    scope = "user-read-playback-state user-modify-playback-state user-read-currently-playing"
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
    code = request.args.get("code")
    token = main.get_token(code=code)
    return jsonify({"access_token": token})

if __name__ == "__main__":
    app.run(debug=True)