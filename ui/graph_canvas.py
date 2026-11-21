
import time
from collections import deque

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, max_points=200):

        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)

        super().__init__(self.fig)

        self.max_points = max_points
        self.t0 = time.perf_counter()

        self.x = deque(maxlen=max_points)
        self.y = deque(maxlen=max_points)

        (self.line,) = self.ax.plot([], [], lw=2)

        self.ax.set_xlabel("Temps (s)")
        self.ax.set_ylabel("Tension (V)")
        self.ax.set_title("Acquisition en temps réel")
        self.ax.grid(True)

        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 5)

    def push(self, value: float):

        t = time.perf_counter() - self.t0

        self.x.append(t)
        self.y.append(value)

        self.line.set_data(self.x, self.y)

        # Fenêtre temporelle glissante de 10 secondes
        self.ax.set_xlim(max(0, t - 10), max(10, t + 0.5))

        # Ajustement automatique de l'axe vertical
        ymin = min(self.y)
        ymax = max(self.y)

        margin = max(0.1, (ymax - ymin) * 0.1)

        self.ax.set_ylim(
            ymin - margin,
            ymax + margin
        )

        self.draw_idle()
