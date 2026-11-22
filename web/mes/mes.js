
// Références aux éléments HTML
const channel = document.getElementById("channel");
const connect = document.getElementById("connect");
const disconnect = document.getElementById("disconnect");
const status = document.getElementById("status");
const samples = document.getElementById("samples");

// Récupération du canvas
const canvas = document.getElementById("signalChart");

// Création de l'oscilloscope
const signalChart = new Chart(canvas, {

    type: "line",

    data: {
        datasets: [{
            label: "Tension (V)",
            data: [],
            borderColor: "#45b8ed",
            borderWidth: 2,
            pointRadius: 0
        }]
    },

    options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: false,

        scales: {
            x: {
                type: "linear",
                title: {
                    display: true,
                    text: "Temps (ms)"
                }
            },

            y: {
                title: {
                    display: true,
                    text: "Tension (V)"
                }
            }
        }
    }
});

console.log("Oscilloscope MES initialisé");


// Connexion WebSocket de l'oscilloscope
let ws = null;
let totalSamples = 0;

// Bouton Connecter
connect.addEventListener("click", () => {

    if (ws !== null) {
        return;
    }

    const selectedChannel = channel.value;

    connect.disabled = true;
    status.textContent = "Connexion en cours...";

    // Utilise automatiquement l'adresse du serveur FastAPI
    const protocol = location.protocol === "https:" ? "wss:" : "ws:";

    ws = new WebSocket(
        `${protocol}//${location.host}/ws/signals/${selectedChannel}`
    );

    ws.onopen = () => {
        status.textContent = `CH${selectedChannel} connecté`;
        disconnect.disabled = false;
    };

    ws.onmessage = (event) => {

        const data = JSON.parse(event.data);
        // Calculer les mesures sur le bloc reçu
        calculateMeasurements(data.voltage);
        // Conversion des secondes en millisecondes
        const points = data.time.map((t, i) => ({
            x: t * 1000,
            y: data.voltage[i]
        }));

        // Afficher le dernier bloc reçu
        signalChart.data.datasets[0].data = points;

        // Mettre à jour le graphique
        signalChart.update("none");

        // Compteur d'échantillons
        totalSamples += data.voltage.length;
        samples.textContent =
            `Échantillons reçus : ${totalSamples}`;
    };

    ws.onerror = (error) => {
        console.error("Erreur WebSocket :", error);
        status.textContent = "Erreur WebSocket";
    };

    ws.onclose = (event) => {
        status.textContent = `Déconnecté (code ${event.code})`;

        ws = null;
        connect.disabled = false;
        disconnect.disabled = true;
    };
});

// Bouton Déconnecter
disconnect.addEventListener("click", () => {

    if (ws !== null) {
        ws.close(1000, "Déconnexion utilisateur");
    }
});


function calculateMeasurements(voltage) {

    const n = voltage.length;

    if (n === 0) {
        return;
    }

    const vmin = Math.min(...voltage);
    const vmax = Math.max(...voltage);

    const vpp = vmax - vmin;

    const sum = voltage.reduce(
        (total, value) => total + value, 0
    );

    const mean = sum / n;

    const sumSquares = voltage.reduce(
        (total, value) => total + value ** 2, 0
    );

    const rms = Math.sqrt(sumSquares / n);

    document.getElementById("vmin").textContent = vmin.toFixed(3);
    document.getElementById("vmax").textContent = vmax.toFixed(3);
    document.getElementById("vpp").textContent = vpp.toFixed(3);
    document.getElementById("vmean").textContent = mean.toFixed(3);
    document.getElementById("vrms").textContent = rms.toFixed(3);
}

