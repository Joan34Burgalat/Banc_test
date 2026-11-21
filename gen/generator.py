
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
