import os

import requests
from flask import Flask, jsonify, render_template, request
from requests import RequestException

POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon"
DEX_MIN = 1
DEX_MAX = 1025
API_TIMEOUT = 10

app = Flask(__name__)


def error_response(message, status_code):
    return jsonify({"error": message}), status_code


def parse_dex_number(body):
    if body is None:
        body = {}

    try:
        dex_id = int(body.get("pokemon_number", 0))
    except (TypeError, ValueError):
        return None, "Invalid input. Pokémon number must be an integer."

    if not DEX_MIN <= dex_id <= DEX_MAX:
        return None, "Invalid Pokémon number. Please provide a number between 1 and 1025."

    return dex_id, None


def fetch_pokemon(dex_id):
    try:
        res = requests.get(f"{POKEAPI_URL}/{dex_id}", timeout=API_TIMEOUT)
    except RequestException:
        return None

    if res.status_code != 200:
        return None

    data = res.json()
    return {
        "pokemon_number": dex_id,
        "name": data["name"].capitalize(),
        "image_data": data["sprites"]["front_default"],
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/pokemon", methods=["POST"])
def pokemon_lookup():
    body = request.get_json(silent=True)
    dex_id, err = parse_dex_number(body)
    if err:
        return error_response(err, 400)

    pokemon = fetch_pokemon(dex_id)
    if pokemon is None:
        return error_response("Failed to fetch Pokémon details from the API.", 500)

    return jsonify(pokemon)


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "").lower() in ("1", "true", "yes")
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=debug, host="0.0.0.0", port=port)
