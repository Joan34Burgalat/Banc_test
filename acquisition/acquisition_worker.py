
import threading
from PyQt5.QtCore import QObject, pyqtSignal


class AcquisitionWorker(QObject):

    # Signal envoyé à l'interface graphique
    data_ready = pyqtSignal(float)

    def __init__(self, instrument, period_s=0.3):
        super().__init__()

        self.instrument = instrument
        self.period_s = period_s

        # Événement permettant d'arrêter le thread
        self._stop_event = threading.Event()

        # Thread d'acquisition
        self._thr = None

    @property
    def running(self):
        return (
            self._thr is not None
            and self._thr.is_alive()
        )

    def start(self):

        # Évite de lancer plusieurs threads
        if self.running:
            return

        self._stop_event.clear()

        self._thr = threading.Thread(
            target=self._loop,
            daemon=True
        )

        self._thr.start()

    def stop(self):

        # Demande l'arrêt du thread
        self._stop_event.set()

        if self._thr is not None:
            self._thr.join()

    def _loop(self):

        while not self._stop_event.is_set():

            try:
                # Lecture de l'instrument
                val = self.instrument.read_value()

                # Transmission vers l'interface Qt
                self.data_ready.emit(val)

            except Exception as e:
                print("[ACQ][ERR]", e)

            # Attente interruptible
            if self._stop_event.wait(self.period_s):
                break
