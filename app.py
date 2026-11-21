
import sys

from PyQt5.QtWidgets import QApplication

from instruments.simulator_dmm import SimulatorDMM
from acquisition.acquisition_worker import AcquisitionWorker
from ui.main_window import MainWindow


def main():

    # 1. Initialisation de l'application Qt
    app = QApplication(sys.argv)

    # 2. Création de l'instrument simulé
    instrument = SimulatorDMM()

    # 3. Création du worker d'acquisition
    worker = AcquisitionWorker(
        instrument=instrument,
        period_s=0.3
    )

    # 4. Création de la fenêtre principale
    window = MainWindow(worker)
    window.resize(900, 600)
    window.show()

    # 5. Lancement de l'application
    try:
        return app.exec_()

    finally:
        # Arrêt de sécurité du worker
        worker.stop()


if __name__ == "__main__":
    sys.exit(main())
