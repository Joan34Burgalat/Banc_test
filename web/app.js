
const channel = document.getElementById("channel");
const waveform = document.getElementById("waveform");
const frequency = document.getElementById("frequency");
const amplitude = document.getElementById("amplitude");

const button = document.getElementById("apply");
const status = document.getElementById("status");

button.addEventListener("click", function () {

    const configuration = {
        channel: Number(channel.value),
        waveform: waveform.value,
        frequency: Number(frequency.value),
        amplitude: Number(amplitude.value)
    };

    if (
        !Number.isFinite(configuration.frequency) ||
        !Number.isFinite(configuration.amplitude) ||
        configuration.frequency < 0 ||
        configuration.amplitude < 0
    ) {
        status.textContent = "Paramètres invalides.";
        return;
    }

    console.log(configuration);

    status.textContent =
        "CH" + configuration.channel +
        " : " + configuration.waveform +
        " | " + configuration.frequency + " Hz" +
        " | " + configuration.amplitude + " V";
});
