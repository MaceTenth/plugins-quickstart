
from flask import Flask, jsonify, request, abort, send_from_directory
from flask_cors import CORS
from shazamio import Shazam, GenreMusic
import asyncio
import os
from dotenv import load_dotenv
from functools import wraps

load_dotenv()
app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


API_KEY = os.getenv('API_KEY')



def run_asyncio(func):
    new_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    try:
        return new_loop.run_until_complete(func)
    finally:
        new_loop.close()

@app.route('/top_songs', methods=['GET'])

def top_songs():
    songs = run_asyncio(Shazam().top_world_tracks(limit=10))
    return jsonify(songs)

@app.route('/top_songs/<country>', methods=['GET'])

def top_songs_country(country):
    songs = run_asyncio(Shazam().top_country_tracks(country, 5))
    return jsonify(songs)

@app.route('/top_songs/<country>/<genre>', methods=['GET'])

def top_songs_country_genre(country, genre):
    songs = run_asyncio(Shazam().top_country_genre_tracks(country_code=country, genre=GenreMusic[genre.upper()], limit=4))
    return jsonify(songs)

@app.route('/top_songs/genre/<genre>', methods=['GET'])

def top_songs_genre(genre):
    songs = run_asyncio(Shazam().top_world_genre_tracks(genre=GenreMusic[genre.upper()], limit=10))
    return jsonify(songs)

@app.route('/.well-known/ai-plugin.json', methods=['GET'])
def manifest():
    return send_from_directory(os.getcwd(), '.well-known/ai-plugin.json')

@app.route('/openapi.yaml', methods=['GET'])
def getyamlfile():
    return send_from_directory(os.getcwd(), 'openapi.yaml')

@app.route('/logo.png', methods=['GET'])
def getlogo():
    return send_from_directory(os.getcwd(), 'logo.png')

@app.errorhandler(403)
def forbidden(e):
    return jsonify(error=str(e)), 403

@app.errorhandler(401)
def unauthorized(e):
    return jsonify(error=str(e)), 401

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()
