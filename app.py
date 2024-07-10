#!usr/bin/python3   
from flask import Flask, session, redirect, url_for, request, jsonify, render_template
import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)
#client id fron spotify app called remo-radio
client_id = '46fba58c09644bb7b75af484504761cf'
#client secret key from the same app
client_secret = 'da97eb9f3f8e46aea1f32ad3ddf60994'
# the redirect adress on the app
redirect_uri = 'http://127.0.0.1:5500/callback'
# the scope which is all the things the app is going to be able to access on spotify
scope = 'playlist-read-private'


cache_handler = FlaskSessionCacheHandler(session)
sp_auth = SpotifyOAuth(

    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_handler=cache_handler,
    show_dialog=True
)

sp = Spotify(auth_manager=sp_auth)
@app.route('/')
@app.route('/home')
def home():
    if not sp_auth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_auth.get_authorize_url()
        return redirect(auth_url)
    print()
    print('valid token')
    #return render_template('index.html')
    return render_template('index.html')

@app.route('/callback')
def callback():
    print()
    print("callback")
    print()
    sp_auth.get_access_token(request.args['code'])
    print()
    print("callback success")
    print()
    return redirect(url_for('get_playlists'))
    #return redirect(url_for('index.html'))



@app.route('/get_playlists', methods=['POST', 'GET'])
def get_playlists():
    if not sp_auth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_auth.get_authorize_url()
        return redirect(auth_url)
    playlists = sp.current_user_playlists()
    playlists_info = [(pl['name'], pl['external_urls']['spotify']) for pl in playlists['items']]
    playlists_dict = {name: url for name, url in playlists_info}
    print(playlists_dict)
    #return jsonify(playlists_dict)
    return render_template('index.html', playlists=playlists_dict)
    #playlists_html = '<br>'.join([f"{name}{url}" for name, url in playlists_info])
   # return playlists_html

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)