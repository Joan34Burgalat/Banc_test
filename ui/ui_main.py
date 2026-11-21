# ui_main.py
#import sys
#from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton
#from PyQt5.QtCore import Qt

#class MainWindow(QWidget):
#    def __init__(self):
#        super().__init__()
#        self.setWindowTitle("Supervision Instrument - PyQt5")
#        self.resize(900, 600)

#        self.label = QLabel("Mesure : -- V", alignment=Qt.AlignCenter)
#        self.btn_start = QPushButton("▶ Démarrer")
#        self.btn_stop  = QPushButton("⏸ Arrêter")
#        self.btn_quit  = QPushButton("❌ Quitter")

#        layout = QVBoxLayout()
#        layout.addWidget(self.label)
#        layout.addWidget(self.btn_start)
#        layout.addWidget(self.btn_stop)
#        layout.addWidget(self.btn_quit)
#        self.setLayout(layout)

if __name__ == "__main__":
   sys.exit(app.exec_())
   app = QApplication(sys.argv)
   w = MainWindow()
   w.show()
