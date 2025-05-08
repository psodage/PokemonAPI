import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pokemon', methods=['POST'])
def get_pokemon_details():
    data = request.get_json(force=True)

    try:
        pokemon_number = int(data.get('pokemon_number', 0))
    except ValueError:
        return jsonify({"error": "Invalid input. Pokémon number must be an integer."}), 400

    if not (1 <= pokemon_number <= 1025):
        return jsonify({"error": "Invalid Pokémon number. Please provide a number between 1 and 1025."}), 400

    pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_number}"
    response = requests.get(pokemon_url)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch Pokémon details from the API."}), 500

    pokemon_data = response.json()

    return jsonify({
        "pokemon_number": pokemon_number,
        "name": pokemon_data['name'].capitalize(),
        "image_data": pokemon_data['sprites']['front_default']
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
