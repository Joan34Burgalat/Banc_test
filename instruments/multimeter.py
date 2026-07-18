from .visa_instrument import VisaInstrument

class Multimeter(VisaInstrument):
    def read_value(self) -> float:
        resp = self.backend.query("MEAS:VOLT:DC?")
        try:
            return float(resp)
        except ValueError:
            return float(resp.strip().split()[0])
