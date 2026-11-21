
from abc import ABC, abstractmethod


class VisaInstrument(ABC):

    def __init__(self, backend, address: str = ""):
        self.backend = backend
        self.address = address
        self.connected = False

    def connect(self):
        if self.backend is None or not self.address:
            raise ValueError("Backend ou adresse VISA manquant")

        self.backend.open(self.address)
        self.connected = True

    def disconnect(self):
        if self.backend:
            self.backend.close()

        self.connected = False

    def idn(self) -> str:
        if self.backend is None:
            return "SIMULATOR"

        return self.backend.query("*IDN?")

    def reset(self):
        if self.backend:
            self.backend.write("*RST")
            self.backend.write("*CLS")

    @abstractmethod
    def read_value(self) -> float:
        """Lecture d'une mesure."""
        pass
