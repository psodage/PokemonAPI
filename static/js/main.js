const DEX_MIN = 1;
const DEX_MAX = 1025;

const form = document.getElementById("search-form");
const queryInput = document.getElementById("query-input");
const resultPanel = document.getElementById("result");

const TYPE_COLORS = {
    normal: "#a8a878",
    fire: "#f08030",
    water: "#6890f0",
    electric: "#f8d030",
    grass: "#78c850",
    ice: "#98d8d8",
    fighting: "#c03028",
    poison: "#a040a0",
    ground: "#e0c068",
    flying: "#a890f0",
    psychic: "#f85888",
    bug: "#a8b820",
    rock: "#b8a038",
    ghost: "#705898",
    dragon: "#7038f8",
    dark: "#705848",
    steel: "#b8b8d0",
    fairy: "#ee99ac",
};

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const query = queryInput.value.trim();
    if (!query) {
        showError("Please enter a Pokédex number or Pokémon name.");
        return;
    }

    if (/^\d+$/.test(query)) {
        const dexId = Number(query);
        if (!Number.isInteger(dexId) || dexId < DEX_MIN || dexId > DEX_MAX) {
            showError("Please enter a valid number between 1 and 1025.");
            return;
        }
    }

    showLoading();

    try {
        const res = await fetch("/pokemon", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query }),
        });

        const data = await res.json();

        if (data.error) {
            showError(data.error);
            return;
        }

        showPokemon(data);
    } catch {
        showError("Something went wrong. Check your connection and try again.");
    }
});

function showPanel(html) {
    resultPanel.hidden = false;
    resultPanel.classList.add("is-visible");
    resultPanel.innerHTML = html;
}

function showLoading() {
    showPanel('<div class="spinner" role="status" aria-label="Loading"></div>');
}

function showError(message) {
    showPanel(`<p class="alert">${escapeHtml(message)}</p>`);
}

function typeBadgeClass(typeName) {
    return typeName.toLowerCase().replace(/\s+/g, "-");
}

function renderTypes(types) {
    return types
        .map((type) => {
            const slug = typeBadgeClass(type);
            const color = TYPE_COLORS[slug] || "var(--blue)";
            return `<span class="type-badge" style="background:${color}">${escapeHtml(type)}</span>`;
        })
        .join("");
}

function renderAbilities(abilities) {
    return abilities
        .map((ab) => {
            const hidden = ab.hidden ? ' <span class="ability-hidden">(hidden)</span>' : "";
            return `<li>${escapeHtml(ab.name)}${hidden}</li>`;
        })
        .join("");
}

function renderStats(stats) {
    const maxBase = 255;
    return stats
        .map((stat) => {
            const pct = Math.min(100, Math.round((stat.base / maxBase) * 100));
            return `
                <div class="stat-row">
                    <span class="stat-label">${escapeHtml(stat.name)}</span>
                    <div class="stat-bar-track">
                        <div class="stat-bar-fill" style="width:${pct}%"></div>
                    </div>
                    <span class="stat-value">${stat.base}</span>
                </div>
            `;
        })
        .join("");
}

function showPokemon(data) {
    const dexLabel = String(data.id).padStart(3, "0");
    const imageUrl = data.official_artwork || data.sprite || "";
    const imageHtml = imageUrl
        ? `<img class="result-img" src="${escapeHtml(imageUrl)}" alt="${escapeHtml(data.name)}">`
        : "";

    const baseExp =
        data.base_experience != null
            ? `<dt>Base exp.</dt><dd>${data.base_experience}</dd>`
            : "";

    showPanel(`
        <header class="result-header">
            <div class="result-title">
                <h2 class="result-name">${escapeHtml(data.name)}</h2>
                <p class="result-dex">#${dexLabel}</p>
                <div class="type-list">${renderTypes(data.types)}</div>
            </div>
            <div class="result-image">${imageHtml}</div>
        </header>

        <dl class="detail-grid">
            <dt>Height</dt>
            <dd>${data.height_m} m</dd>
            <dt>Weight</dt>
            <dd>${data.weight_kg} kg</dd>
            ${baseExp}
        </dl>

        <section class="detail-section">
            <h3 class="detail-heading">Abilities</h3>
            <ul class="ability-list">${renderAbilities(data.abilities)}</ul>
        </section>

        <section class="detail-section">
            <h3 class="detail-heading">Base stats</h3>
            <div class="stats-list">${renderStats(data.stats)}</div>
        </section>
    `);
}

function escapeHtml(text) {
    const el = document.createElement("span");
    el.textContent = text;
    return el.innerHTML;
}
