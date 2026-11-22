import numpy as np

class SignalGenerator:

    def __init__(self):

        self.channels = {
            i: {
                "waveform": "sine",
                "frequency": 1000.0,
                "amplitude": 5.0,
                "offset": 0.0,
                "phase": 0.0,
                "enabled": False
            }
            for i in range(1, 5)
        }

    def configure_channel(self, channel, config):

        if channel not in self.channels:
            raise ValueError("Canal inexistant")

        self.channels[channel] = config.copy()

    def get_channel(self, channel):

        if channel not in self.channels:
            raise ValueError("Canal inexistant")

        return self.channels[channel].copy()


    def generate_signal(self, channel, duration=0.01, sample_rate=100000, start_time=0.0):
        """
        Génère les échantillons temporels d'un canal.

        channel : numéro du canal (1 à 4)
        duration : durée du signal en secondes
        sample_rate : fréquence d'échantillonnage en Hz
          
        Arg : 
            channel : numéro du canal d'émission
            duration : durée d'émition
            sample_rate : échantillonage 

        Retourne :
            t : tableau des instants
            y : tableau des tensions
        """

        config = self.get_channel(channel)
        nb_samples = int(duration * sample_rate)

        if nb_samples < 1:
            raise ValueError("La durée et la fréquence d'échantillonnage sont invalides")
        # Axe temporel continu entre les blocs
        t = start_time + np.arange(nb_samples) / sample_rate
        amplitude = config["amplitude"]
        frequency = config["frequency"]
        offset = config["offset"]
        phase = np.deg2rad(config["phase"])
        
        # Calcul de l'argument périodique
        theta = 2 * np.pi * frequency * t + phase

        # Génération selon la forme d'onde
        if not config["enabled"]:
            y = np.zeros(nb_samples)

        elif config["waveform"] == "sine":
            y = amplitude * np.sin(theta) + offset

        elif config["waveform"] == "square":
            y = amplitude * np.where(
                np.sin(theta) >= 0, 1.0, -1.0
            ) + offset

        elif config["waveform"] == "triangle":
            y = (2 * amplitude / np.pi) * np.arcsin(
                np.sin(theta)
            ) + offset

        elif config["waveform"] == "dc":
            y = np.full(nb_samples, offset)

        else:
            raise ValueError("Forme de signal inconnue")


        return t, y
