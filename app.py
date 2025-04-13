import random
import requests

from flask import Flask, render_template, redirect, request, Response, jsonify, make_response
from spotify_methods import SpotifyUser, client_id, redirect_uri

app = Flask(__name__)
error_responses = {
    500: {
        "status": 500,
        "name": "Internal Server Error",
        "message": "Something wrong happened on our end."
    },
    502: {
        "status": 502,
        "name": "Bad Gateway Error",
        "message": "We had trouble connecting. Please check your connection."
    },
    404: {
        "status": 404,
        "name": "Page Not Found",
        "message": "We couldn't find the page you were looking for."
    }
}

@app.route("/callback", methods=["GET"])
def callback():
    print("Completing callback...")
    redirect_path = request.args.get("redirect_path")

    auth_code = request.args.get("code")
    if not auth_code:
        return redirect("/", 302)
    print(auth_code)
    # Generate new auth and refresh token with authentication code
    spotify_client = SpotifyUser(auth_code=auth_code)

    response = redirect(f"/", 302)

    # Set user cookies
    response.set_cookie(key="access_token", value=spotify_client.access_token, max_age=3600)
    response.set_cookie(key="refresh_token", value=spotify_client.refresh_token)
    print(spotify_client.refresh_token)
    return response


@app.route("/oauth", methods=["GET"])
def auth():
    print("Redirecting for oauth...")
    oauth_redirect_location = f"https://accounts.spotify.com/en/authorize?" \
                              f"response_type=code&" \
                              f"client_id={client_id}&" \
                              f"redirect_uri={redirect_uri}&" \
                              f"scope=" \
                              f"streaming+" \
                              f"user-read-email+" \
                              f"user-modify-playback-state+" \
                              f"user-read-private+" \
                              f"user-read-playback-state&" \
                              f"show_dialog=true"
    return redirect(oauth_redirect_location, 302)


@app.route("/login", methods=["GET"])
def display_login():
    return render_template("login.html")


@app.route("/", methods=["GET"])
def display_home():
    # Check for refresh token.
    refresh_token = request.cookies.get("refresh_token")
    access_token = request.cookies.get("access_token")
    if not refresh_token:
        return redirect("/login", 302)

    spotify_client = SpotifyUser(refresh_token=refresh_token, access_token=access_token)  # refresh_token=refresh_token, auth_token=auth_token

    if refresh_token and not access_token:
        spotify_client.refresh_authorization_token()

    # Artists Category
    popular_heardles = [
        "0Y5tJX1MQlPlqiwlOH1tJY",  # Travis Scott
        "06HL4z0CvFAxyc27GXpf02",  # Taylor Swift
        "3TVXtAsR1Inumwj472S9r4",  # Drake
        "2h93pZq0e7k5yf4dywlkpM",  # Frank Ocean
        "1Xyo4u8uXC1ZmMpatF05PJ",  # The Weeknd
        "699OTQXzgjhIYAHMy9RyPD",  # Playboi Carti
        "4q3ewBCX7sLwd24euuV69X",  # Bad Bunny
        "6KImCVD70vtIoJWnq6nGn3",  # Harry Styles
        "66CXWjxzNUsdJxJ2JdwvnR",  # Ariana Grande

    ]
    artists_data = spotify_client.collect(
        path="/artists",
        ids=",".join(popular_heardles)
    ).json()['artists']

    user_profile = spotify_client.collect("/me").json()
    user_image = "https://icons.veryicon.com/png/o/miscellaneous/youyinzhibo/guest.png"
    if user_profile.get('images'):
        user_image = user_profile['images'][0]['url']
    user_display_name = user_profile['display_name']
    return render_template(
        "home.html",
        artists_data=artists_data,
        user_image=user_image,
        user_display_name=user_display_name,
        access_token=spotify_client.access_token
    )


@app.route("/infinity-heardle", methods=["GET"])
def display_infinity_heardle():
    # Check for refresh token.
    refresh_token = request.cookies.get("refresh_token")
    access_token = request.cookies.get("access_token")
    if not refresh_token:
        return redirect(f"/oauth?redirect_path={request.path}", 302)

    spotify_client = SpotifyUser(refresh_token=refresh_token, access_token=access_token)  # refresh_token=refresh_token, auth_token=auth_token

    if refresh_token and not access_token:
        spotify_client.refresh_authorization_token()

    artist_id = request.args.get("artist")

    artist_request = spotify_client.collect(
        path=f"/artists/{artist_id}"
    )
    if artist_request.json().get("error"):
        print(artist_request.json())
        return redirect("/", 302)

    artist_data = artist_request.json()

    artist_releases_request = spotify_client.collect(
        path=f"/artists/{artist_id}/albums",
        limit=50,
        include_groups="single,album"
    )

    if artist_releases_request.json().get("error"):
        return redirect("/", 302)

    artist_releases_data = artist_releases_request.json()
    release_ids = [release['id'] for release in artist_releases_data['items']]
    while len(release_ids) > 20:
        release_ids.pop()

    # Collect all tracks
    releases_tracks_request = spotify_client.collect(
        path="/albums",
        ids=",".join(release_ids)
    )

    if releases_tracks_request.json().get("error"):
        print("Failed...")
        return redirect("/", 302)

    all_releases = []
    for release_data in releases_tracks_request.json()['albums']:
        cover_url = release_data['images'][0]['url']
        for track_data in release_data['tracks']['items']:
            track_data['cover_url'] = cover_url
            all_releases.append(track_data)
    random_track = random.choice(all_releases)
    print(random_track)

    # spotify_client.toggle_playback(random_track['id'])

    user_profile = spotify_client.collect("/me").json()
    user_image = "https://icons.veryicon.com/png/o/miscellaneous/youyinzhibo/guest.png"
    if user_profile.get('images'):
        user_image = user_profile['images'][0]['url']
    user_display_name = user_profile['display_name']

    response = make_response(render_template(
        "heardle.html",
        access_token=spotify_client.access_token,
        artist=artist_data,
        track=random_track,
        all_tracks=all_releases,
        user_image=user_image,
        user_display_name=user_display_name,
        hidden_mode=True
    ))

    response.set_cookie(key="access_token", value=spotify_client.access_token, max_age=3600)
    response.set_cookie(key="refresh_token", value=spotify_client.refresh_token)

    return response


@app.route("/logout", methods=["GET"])
def logout():
    response = Response("You have been logged out")
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response


@app.route("/test", methods=["GET"])
def test():
    def printy(string):
        print(string)
    return render_template("test.html", func=printy)


# API

@app.route("/api/connect_player", methods=["POST"])
def process_connect_player():
    # Check for refresh token.
    refresh_token = request.cookies.get("refresh_token")
    access_token = request.cookies.get("access_token")
    device_id = request.args.get("device_id")

    if not refresh_token or not device_id:
        return redirect(f"/login", 302)

    spotify_client = SpotifyUser(access_token=access_token, refresh_token=refresh_token)
    connectPlayerPUT = requests.put(
        "https://api.spotify.com/v1/me/player",
        json={
            "device_ids": [
                device_id
            ]
        },
        headers=spotify_client.api_auth_headers
    )

    error_response = error_responses.get(connectPlayerPUT.status_code)
    if error_response:
        return error_response

    return jsonify({"success": True})


@app.route("/api/play_track", methods=["POST"])
def process_play_track():
    # Check for refresh token.
    refresh_token = request.cookies.get("refresh_token")
    access_token = request.cookies.get("access_token")
    track_id = request.args.get("track_id")

    if not refresh_token or not track_id:
        return redirect(f"/", 302)

    spotify_client = SpotifyUser(access_token=access_token, refresh_token=refresh_token)

    playTrackPUT = requests.put(
        "https://api.spotify.com/v1/me/player/play",
        json={
            "uris": [
                f"spotify:track:{track_id}"
            ]
        },
        headers=spotify_client.api_auth_headers
    )

    error_response = error_responses.get(playTrackPUT.status_code)
    if error_response:
        return error_response

    return jsonify({"success": True})


@app.route("/api/pause_track", methods=["POST"])
def process_pause_track():
    # Check for refresh token.
    refresh_token = request.cookies.get("refresh_token")
    access_token = request.cookies.get("access_token")

    if not refresh_token:
        return redirect(f"/", 302)

    spotify_client = SpotifyUser(access_token=access_token, refresh_token=refresh_token)

    pauseTrackPUT = requests.put(
        "https://api.spotify.com/v1/me/player/pause",
        headers=spotify_client.api_auth_headers
    )

    error_response = error_responses.get(pauseTrackPUT.status_code)
    if error_response:
        return error_response

    return jsonify({"success": True})


if __name__ == '__main__':
    app.run(debug=True, port=5000)

# TODO: PROFILES
# TODO: RANKING
# TODO: POPULARITY
# TODO: DAILY AND GUESSING HEARDLES
