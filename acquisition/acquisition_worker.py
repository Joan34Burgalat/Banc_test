import threading, time
from PyQt5.QtCore import QObject, pyqtSignal

class AcquisitionWorker(QObject):
    data_ready = pyqtSignal(float)

    def __init__(self, instrument, period_s=0.3):
        super().__init__()
        self.instrument = instrument
        self.period_s = period_s
        self._running = False
        self._thr = None

    def start(self):
        if self._running: return
        self._running = True
        self._thr = threading.Thread(target=self._loop, daemon=True)
        self._thr.start()

    def stop(self):
        self._running = False
        if self._thr:
            self._thr.join(timeout=1)

    def _loop(self):
        while self._running:
            try:
                val = self.instrument.read_value()
                self.data_ready.emit(val)
            except Exception as e:
                print("[ACQ][ERR]", e)
            time.sleep(self.period_s)
