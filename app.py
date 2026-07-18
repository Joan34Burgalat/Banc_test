from PyQt5.QtWidgets import QApplication
import sys

from instruments.simulator_dmm import SimulatorDMM
from acquisition.acquisition_worker import AcquisitionWorker
from ui.main_window import MainWindow

def main():
    # instrument (simulateur pour l’instant)
    instr = SimulatorDMM()
    worker = AcquisitionWorker(instr, period_s=0.3)

    app = QApplication(sys.argv)
    win = MainWindow(worker)  # la fenêtre contrôle start/stop et affiche le graphe
    win.resize(900, 600)
    win.show()

    # démarrer direct si tu veux
    worker.start()

    try:
        sys.exit(app.exec_())
    finally:
        worker.stop()

if __name__ == "__main__":
    main()
