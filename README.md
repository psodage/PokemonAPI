# Pokémon Finder

A small full-stack web app that looks up Pokémon by Pokédex number (1–1025). The Flask backend proxies [PokéAPI](https://pokeapi.co/), and the frontend is a single-page UI built with HTML, CSS, and JavaScript.

## Project structure

Place every file in the **repository root** (same folder as `app.py`):

```
pokemon/
├── app.py
├── templates/
│   └── index.html
├── static/
│   ├── css/style.css
│   └── js/main.js
├── requirements.txt
├── Procfile
├── runtime.txt
├── render.yaml
├── .gitignore
├── .env.example
└── README.md
```

| File | Purpose |
|------|---------|
| `app.py` | Flask app and `POST /pokemon` API |
| `templates/index.html` | Page markup |
| `static/css/style.css` | Styles |
| `static/js/main.js` | Form handling and API calls |
| `requirements.txt` | `Flask`, `requests`, `gunicorn` for install on Render |
| `Procfile` | Tells Render how to start the web process |
| `runtime.txt` | Pins Python version on Render |
| `render.yaml` | Optional one-click / Blueprint deploy on Render |

## Tech stack

- **Backend:** Flask (Python)
- **Frontend:** HTML, CSS, JavaScript (`templates/`, `static/`)
- **Production server:** Gunicorn
- **API:** [PokéAPI](https://pokeapi.co/api/v2/pokemon/)

## Prerequisites

- Python 3.12+
- Git
- A [GitHub](https://github.com) account
- A [Render](https://render.com) account (free tier works)

## Run locally

### 1. Clone and enter the project

```bash
git clone https://github.com/YOUR_USERNAME/pokemon.git
cd pokemon
```

### 2. Create a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the app

**Development (Flask built-in server):**

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000).

**Production-like (Gunicorn, same as Render):**

```bash
gunicorn app:app --bind 0.0.0.0:5000
```

Optional: copy `.env.example` to `.env` and set `FLASK_DEBUG=1` for auto-reload when using `python app.py`.

## Push to GitHub

From the project root:

```bash
git init
git add .
git commit -m "Add Pokémon Finder with Render deployment config"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/pokemon.git
git push -u origin main
```

Replace `YOUR_USERNAME` and `pokemon` with your GitHub username and repository name.

## Deploy on Render

### Option A — Connect GitHub (recommended)

1. Sign in at [render.com](https://render.com).
2. Click **New +** → **Web Service**.
3. Connect your GitHub account and select the `pokemon` repository.
4. Configure the service:
   - **Name:** `pokemon-finder` (or any name)
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`  
     (Render also reads this from the `Procfile` if you leave Start Command empty.)
   - **Instance type:** Free (if available)
5. Click **Create Web Service**.
6. Wait for the build to finish. Render will assign a URL like `https://pokemon-finder.onrender.com`.

Render uses `runtime.txt` for the Python version and `Procfile` for the process command.

### Option B — Blueprint (`render.yaml`)

1. Push this repo to GitHub (including `render.yaml`).
2. On Render: **New +** → **Blueprint**.
3. Select the repository and apply the blueprint.
4. Render creates a web service from `render.yaml` with build and start commands preconfigured.

### After deploy

- Visit your Render URL (e.g. `https://your-service.onrender.com`).
- Enter a Pokédex number (1–1025) and click **Find Pokémon**.

**Note:** Free-tier services may sleep after inactivity; the first request can take 30–60 seconds to wake up.

## API

| Method | Path | Body | Description |
|--------|------|------|-------------|
| `GET` | `/` | — | Serves the frontend |
| `POST` | `/pokemon` | `{"pokemon_number": 25}` | Returns name and sprite URL |

Example response:

```json
{
  "pokemon_number": 25,
  "name": "Pikachu",
  "image_data": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png"
}
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Build fails on Render | Confirm `requirements.txt` and `runtime.txt` are in the repo root |
| 502 / app won’t start | Ensure `Procfile` is `web: gunicorn app:app` and `app.py` defines `app = Flask(...)` |
| Module not found | Run `pip install -r requirements.txt` locally to verify dependencies |
| PokéAPI errors | Check network access; PokéAPI must be reachable from Render |

## License

MIT — use and modify freely.
