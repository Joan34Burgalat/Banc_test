import time
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, max_points=200):
        self.fig, self.ax = plt.subplots()
        super().__init__(self.fig)
        self.max_points = max_points
        self.t0 = time.time()
        self.x = deque(maxlen=max_points)
        self.y = deque(maxlen=max_points)
        (self.line,) = self.ax.plot([], [], lw=2)
        self.ax.set_xlabel("Temps (s)")
        self.ax.set_ylabel("Tension (V)")
        self.ax.set_ylim(0, 5)

    def push(self, value: float):
        t = time.time() - self.t0
        self.x.append(t); self.y.append(value)
        self.line.set_data(self.x, self.y)
        self.ax.set_xlim(max(0, t-10), t+0.5)
        self.ax.figure.canvas.draw_idle()
