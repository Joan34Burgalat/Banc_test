import time, math
from .multimeter import Multimeter

class SimulatorDMM(Multimeter):
    def __init__(self):
        super().__init__(backend=None, address="")
        self.t0 = time.time()
        self.connected = True

    def connect(self): pass
    def disconnect(self): pass
    def idn(self) -> str: return "SIMULATOR,DMM,0,1.0"
    def reset(self): pass

    def read_value(self) -> float:
        t = time.time() - self.t0
        return 2.5 + 2.5 * math.sin(2 * math.pi * 0.2 * t)
