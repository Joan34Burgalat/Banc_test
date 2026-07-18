from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from .graph_canvas import MplCanvas

class MainWindow(QWidget):
    def __init__(self, worker):
        super().__init__()
        self.setWindowTitle("Supervision Instrument")
        self.worker = worker

        self.canvas = MplCanvas()
        self.label = QLabel("Mesure : -- V", alignment=Qt.AlignCenter)
        self.btn_start = QPushButton("▶ Démarrer")
        self.btn_stop  = QPushButton("⏸ Arrêter")
        self.btn_quit  = QPushButton("❌ Quitter")

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.label)
        layout.addWidget(self.btn_start)
        layout.addWidget(self.btn_stop)
        layout.addWidget(self.btn_quit)
        self.setLayout(layout)

        # connexions
        self.worker.data_ready.connect(self.on_data)
        self.btn_start.clicked.connect(self.on_start)
        self.btn_stop.clicked.connect(self.on_stop)
        self.btn_quit.clicked.connect(self.close)
        self.btn_stop.setEnabled(False)

    def on_start(self):
        self.worker.start()
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)

    def on_stop(self):
        self.worker.stop()
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)

    def on_data(self, v: float):
        self.label.setText(f"Mesure : {v:.3f} V")
        self.canvas.push(v)

    def closeEvent(self, e):
        try:
            self.worker.stop()
        finally:
            return super().closeEvent(e)
