
import numpy as np


def compute_fft(voltage, sample_rate, window="rectangular"):
    """
    Calcule le spectre d'amplitude d'un signal réel.

    Args:
        voltage : échantillons de tension (V)
        sample_rate : fréquence d'échantillonnage (Hz)
        window : "rectangular" ou "hann"

    Returns:
        frequencies : fréquences positives (Hz)
        amplitudes : amplitudes spectrales (V)
    """

    y = np.asarray(voltage, dtype=float)
    n = len(y)

    if n < 2:
        raise ValueError("Au moins deux échantillons sont nécessaires")

    if sample_rate <= 0 or not np.isfinite(sample_rate):
        raise ValueError("Fréquence d'échantillonnage invalide")

    if not np.all(np.isfinite(y)):
        raise ValueError("Échantillons invalides")

    # Sélection de la fenêtre
    if window == "rectangular":
        w = np.ones(n)

    elif window == "hann":
        w = np.hanning(n)

    else:
        raise ValueError("Fenêtre inconnue")

    # Application de la fenêtre au signal
    y_windowed = y * w

    # Calcul de la FFT
    spectrum = np.fft.rfft(y_windowed)

    frequencies = np.fft.rfftfreq(
        n,
        d=1 / sample_rate
    )

    # Correction du gain cohérent de la fenêtre
    amplitudes = np.abs(spectrum) / np.sum(w)

    # Correction du spectre unilatéral
    if n % 2 == 0:
        amplitudes[1:-1] *= 2
    else:
        amplitudes[1:] *= 2

    return frequencies, amplitudes
