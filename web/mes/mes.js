
// Références aux éléments HTML
const channel = document.getElementById("channel");
const connect = document.getElementById("connect");
const disconnect = document.getElementById("disconnect");
const status = document.getElementById("status");
const samples = document.getElementById("samples");
const fftWindow = document.getElementById("fftWindow");
const canvas = document.getElementById("signalChart");
const fftSize = document.getElementById("fftSize");

let lastFFTUpdate = 0;
let fftInProgress = false;
let fftBuffer = [];
let selectedFFTSize = Number(fftSize.value);

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


    // Initialisation de l'analyseur spectral
    const fftCanvas = document.getElementById("fftChart");

    const fftChart = new Chart(fftCanvas, {
    type: "line",

    data: {
        datasets: [{
            label: "Amplitude spectrale (V)",
            data: [],
            borderColor: "#f4a261",
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
                    text: "Fréquence (Hz)"
                },
                min: 0,
                max: 10000
            },

            y: {
                beginAtZero: true,
                title: {
                    display: true,
                    text: "Amplitude (V)"
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
        fftBuffer = [];
        lastFFTUpdate = 0;
        totalSamples = 0;
        samples.textContent = "Échantillons reçus : 0";
    };

    ws.onmessage = (event) => {

        const data = JSON.parse(event.data);
        fftBuffer.push(...data.voltage);

        // Conserver les N derniers échantillons
        if (fftBuffer.length > selectedFFTSize) {
            fftBuffer = fftBuffer.slice(-selectedFFTSize);
        }

        // Limiter uniquement la fréquence des calculs FFT
        const now = performance.now();

        if (
            fftBuffer.length === selectedFFTSize &&
            now - lastFFTUpdate >= 200 &&
            !fftInProgress
            ) 
        {
            lastFFTUpdate = now;
            console.log("FFT demandée :", fftBuffer.length);
            updateFFT([...fftBuffer]);
        }
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

fftSize.addEventListener("change", () => {

    selectedFFTSize = Number(fftSize.value);

    // Réinitialisation pour éviter de mélanger les acquisitions
    fftBuffer = [];

    console.log(
        `Nouvelle taille FFT : ${selectedFFTSize} échantillons`
    );
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


// Envoi des échantillons vers Python pour analyse FFT
async function updateFFT(voltage) {
    console.log("FFT demandée :", voltage.length);
    if (fftInProgress) {
        return;
    }

    fftInProgress = true;

    try {
        const response = await fetch("/mes/fft", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                voltage: voltage,
                sample_rate: 100000,
                window: fftWindow.value
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const result = await response.json();
        console.log("FFT reçue :", result.frequencies.length);

        // Construction des points du spectre
        const points = result.frequencies.map((frequency, i) => ({
            x: frequency,
            y: result.amplitudes[i]
        }));

        // Mise à jour de l'analyseur spectral
        fftChart.data.datasets[0].data = points;
        fftChart.update("none");

    } catch (error) {
        console.error("Erreur FFT :", error);
    }

    finally {
        fftInProgress = false;
    }
}
