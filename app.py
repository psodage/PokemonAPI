import os
import re

import requests
from flask import Flask, jsonify, render_template, request
from requests import RequestException

POKEAPI_URL = "https://pokeapi.co/api/v2/pokemon"
DEX_MIN = 1
DEX_MAX = 1025
API_TIMEOUT = 10

STAT_LABELS = {
    "hp": "HP",
    "attack": "Attack",
    "defense": "Defense",
    "special-attack": "Sp. Atk",
    "special-defense": "Sp. Def",
    "speed": "Speed",
}
STAT_ORDER = list(STAT_LABELS.keys())

app = Flask(__name__)


def error_response(message, status_code):
    return jsonify({"error": message}), status_code


def normalize_raw_query(raw):
    if raw is None:
        return None, "Please enter a Pokédex number or Pokémon name."

    if isinstance(raw, (int, float)):
        raw = str(int(raw))
    else:
        raw = str(raw).strip()

    if not raw:
        return None, "Please enter a Pokédex number or Pokémon name."

    return raw, None


def name_to_slug(name):
    slug = name.lower()
    slug = re.sub(r"['.]", "", slug)
    slug = re.sub(r"\s+", "-", slug)
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


def parse_query(body):
    if body is None:
        body = {}

    raw = body.get("query")
    if raw is None and "pokemon_number" in body:
        raw = body.get("pokemon_number")

    query, err = normalize_raw_query(raw)
    if err:
        return None, err

    if query.isdigit():
        dex_id = int(query)
        if not DEX_MIN <= dex_id <= DEX_MAX:
            return (
                None,
                "Invalid Pokémon number. Please provide a number between 1 and 1025.",
            )
        return str(dex_id), None

    slug = name_to_slug(query)
    if not slug:
        return None, "Invalid Pokémon name."

    return slug, None


def format_pokemon(data):
    sprites = data.get("sprites") or {}
    other = sprites.get("other") or {}
    official = (other.get("official-artwork") or {}).get("front_default")

    types = sorted(data.get("types", []), key=lambda t: t["slot"])
    type_names = [t["type"]["name"].replace("-", " ").title() for t in types]

    abilities = []
    for entry in data.get("abilities", []):
        ability = entry.get("ability") or {}
        name = ability.get("name", "").replace("-", " ").title()
        abilities.append({"name": name, "hidden": entry.get("is_hidden", False)})

    stats_by_key = {}
    for entry in data.get("stats", []):
        stat = entry.get("stat") or {}
        key = stat.get("name")
        if key in STAT_LABELS:
            stats_by_key[key] = {
                "name": STAT_LABELS[key],
                "key": key,
                "base": entry.get("base_stat", 0),
            }

    stats = [stats_by_key[key] for key in STAT_ORDER if key in stats_by_key]

    return {
        "id": data["id"],
        "name": data["name"].replace("-", " ").title(),
        "sprite": sprites.get("front_default"),
        "official_artwork": official,
        "types": type_names,
        "abilities": abilities,
        "stats": stats,
        "height_m": round(data.get("height", 0) / 10, 1),
        "weight_kg": round(data.get("weight", 0) / 10, 1),
        "base_experience": data.get("base_experience"),
    }


def fetch_pokemon(identifier):
    try:
        res = requests.get(f"{POKEAPI_URL}/{identifier}", timeout=API_TIMEOUT)
    except RequestException:
        return None, "api_error"

    if res.status_code == 404:
        return None, "not_found"
    if res.status_code != 200:
        return None, "api_error"

    return format_pokemon(res.json()), None


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/pokemon", methods=["POST"])
def pokemon_lookup():
    body = request.get_json(silent=True)
    identifier, err = parse_query(body)
    if err:
        return error_response(err, 400)

    pokemon, fail = fetch_pokemon(identifier)
    if fail == "not_found":
        return error_response(
            "No Pokémon found. Check the number or name and try again.", 404
        )
    if fail == "api_error":
        return error_response("Failed to fetch Pokémon details from the API.", 500)

    return jsonify(pokemon)


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "").lower() in ("1", "true", "yes")
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=debug, host="0.0.0.0", port=port)
