class VisaInstrument:
    def __init__(self, backend, address: str = ""):
        self.backend = backend
        self.address = address
        self.connected = False

    def connect(self):
        if self.backend and self.address:
            self.backend.open(self.address)
            self.connected = True

    def disconnect(self):
        if self.backend:
            self.backend.close()
        self.connected = False

    def idn(self) -> str:
        return self.backend.query("*IDN?") if self.backend else "SIMULATOR"

    def reset(self):
        if self.backend:
            self.backend.write("*RST"); self.backend.write("*CLS")

    def read_value(self) -> float:
        raise NotImplementedError
