
from gen.generator import SignalGenerator

generator = SignalGenerator()


for waveform in ["sine", "square", "triangle", "dc"]:

    generator.configure_channel(1, {
        "waveform": waveform,
        "frequency": 1000,
        "amplitude": 5,
        "offset": 1,
        "phase": 0,
        "enabled": True
        })

# Génération numérique
    t, y = generator.generate_signal(1)

#print("Nombre d'échantillons :", len(y))
#print("Premiers instants :", t[:5])
#print("Premières tensions :", y[:5])
#print("Tension maximale :", max(y))
#print("Tension minimale :", min(y))

    print(f"\nSignal : {waveform}")
    print("Échantillons :", len(y))
    print("Minimum :", round(float(min(y)), 3))
    print("Maximum :", round(float(max(y)), 3))
