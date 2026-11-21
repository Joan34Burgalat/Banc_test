
from typing import List
import pyvisa as visa


class BackendError(Exception):
    """Erreur de communication avec un instrument VISA."""
    pass


class VisaBackend:

    def __init__(self):

        try:
            self.rm = visa.ResourceManager()
        except visa.errors.VisaIOError as e:
            raise BackendError(
                f"Impossible d'initialiser VISA : {e}"
            ) from e

        self.session = None

    def list_resources(self) -> List[str]:
        """Liste les instruments VISA disponibles."""

        try:
            return list(self.rm.list_resources())

        except visa.errors.VisaIOError as e:
            raise BackendError(
                f"Erreur de détection des instruments : {e}"
            ) from e

    def open(self, address: str) -> None:
        """Ouvre une connexion vers un instrument."""

        self.close()

        try:
            session = self.rm.open_resource(address)
            session.timeout = 3000

            session.write_termination = "\n"
            session.read_termination = "\n"

            self.session = session

        except visa.errors.VisaIOError as e:
            raise BackendError(
                f"Impossible de se connecter à {address} : {e}"
            ) from e

    def close(self) -> None:
        """Ferme la connexion active."""

        if self.session is not None:

            try:
                self.session.close()

            finally:
                self.session = None

    def write(self, cmd: str) -> None:
        """Envoie une commande à l'instrument."""

        if self.session is None:
            raise BackendError("Session VISA non ouverte")

        try:
            self.session.write(cmd)

        except visa.errors.VisaIOError as e:
            raise BackendError(
                f"Erreur d'écriture VISA : {e}"
            ) from e

    def read(self) -> str:
        """Lit une réponse de l'instrument."""

        if self.session is None:
            raise BackendError("Session VISA non ouverte")

        try:
            return self.session.read()

        except visa.errors.VisaIOError as e:
            raise BackendError(
                f"Erreur de lecture VISA : {e}"
            ) from e

    def query(self, cmd: str) -> str:
        """Envoie une commande et récupère la réponse."""

        if self.session is None:
            raise BackendError("Session VISA non ouverte")

        try:
            return self.session.query(cmd)

        except visa.errors.VisaIOError as e:
            raise BackendError(
                f"Erreur de requête VISA : {e}"
            ) from e

    def shutdown(self):
        """Libère les ressources VISA."""

        self.close()
        self.rm.close()
