from typing import List
import pyvisa as visa

class BackendError(Exception):
    pass

class VisaBackend:
    def __init__(self):
        self.rm = visa.ResourceManager()
        self.session = None

    def list_resources(self) -> List[str]:
        return list(self.rm.list_resources())

    def open(self, address: str) -> None:
        self.close()
        self.session = self.rm.open_resource(address)
        self.session.timeout = 3000
        try:
            self.session.write_termination = '\n'
            self.session.read_termination = '\n'
        except Exception:
            pass

    def close(self) -> None:
        if self.session is not None:
            try:
                self.session.close()
            finally:
                self.session = None

    def write(self, cmd: str) -> None:
        if self.session is None:
            raise BackendError("Session VISA non ouverte")
        self.session.write(cmd)

    def read(self) -> str:
        if self.session is None:
            raise BackendError("Session VISA non ouverte")
        return self.session.read()

    def query(self, cmd: str) -> str:
        if self.session is None:
            raise BackendError("Session VISA non ouverte")
        return self.session.query(cmd)
