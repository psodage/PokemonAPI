const DEX_MIN = 1;
const DEX_MAX = 1025;

const form = document.getElementById("search-form");
const dexInput = document.getElementById("dex-input");
const resultPanel = document.getElementById("result");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const dexId = Number(dexInput.value);
    if (!Number.isInteger(dexId) || dexId < DEX_MIN || dexId > DEX_MAX) {
        showError("Please enter a valid number between 1 and 1025.");
        return;
    }

    showLoading();

    try {
        const res = await fetch("/pokemon", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ pokemon_number: dexId }),
        });

        const data = await res.json();

        if (data.error) {
            showError(data.error);
            return;
        }

        showPokemon(data.name, dexId, data.image_data);
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

function showPokemon(name, dexId, imageUrl) {
    const dexLabel = String(dexId).padStart(3, "0");
    showPanel(`
        <h2 class="result-name">${escapeHtml(name)}</h2>
        <p class="result-dex">#${dexLabel}</p>
        <img class="result-img" src="${escapeHtml(imageUrl)}" alt="${escapeHtml(name)}">
    `);
}

function escapeHtml(text) {
    const el = document.createElement("span");
    el.textContent = text;
    return el.innerHTML;
}
