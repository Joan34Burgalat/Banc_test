
from gen.generator import SignalGenerator

# Instanciation du générateur
generator = SignalGenerator()

# Configuration du canal 1
generator.configure_channel(1, {
    "waveform": "sine",
    "frequency": 1000,
    "amplitude": 5,
    "offset": 0,
    "phase": 0,
    "enabled": True
})

# Génération numérique
t, y = generator.generate_signal(1)

print("Nombre d'échantillons :", len(y))
print("Premiers instants :", t[:5])
print("Premières tensions :", y[:5])
print("Tension maximale :", max(y))
print("Tension minimale :", min(y))
