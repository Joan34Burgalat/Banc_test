
import numpy as np
from mes.signal_processing import compute_fft , interpolate_fft_peak


# Paramètres du signal
sample_rate = 100000
frequency = 1000
amplitude = 3
duration = 0.01

# Génération d'un sinus de référence
n = int(sample_rate * duration)
t = np.arange(n) / sample_rate

voltage = amplitude * np.sin(
    2 * np.pi * frequency * t
)

# Calcul de la FFT
frequencies, amplitudes = compute_fft(
    voltage,
    sample_rate
)

# Recherche du pic spectral hors composante continue
peak_index = np.argmax(amplitudes[1:]) + 1

print("Nombre d'échantillons :", n)
print("Résolution FFT :", sample_rate / n, "Hz")
print("Fréquence dominante :", frequencies[peak_index], "Hz")
print("Amplitude dominante :", amplitudes[peak_index], "V")

# Vérifications automatiques
assert np.isclose(frequencies[peak_index], frequency)
assert np.isclose(amplitudes[peak_index], amplitude)

print("Test FFT validé")



# Test de la fenêtre de Hann sur un sinus à 1050 Hz
frequency = 1050

voltage = 3 * np.sin(
    2 * np.pi * frequency * t
)

freq_rect, amp_rect = compute_fft(
    voltage,
    sample_rate,
    window="rectangular"
)

freq_hann, amp_hann = compute_fft(
    voltage,
    sample_rate,
    window="hann"
)

print("\nComparaison des fenêtres à 1050 Hz")
print("Pic rectangulaire :", max(amp_rect), "V")
print("Pic Hann :", max(amp_hann), "V")

# Comparaison de la fuite à une fréquence éloignée
index_3000 = np.argmin(np.abs(freq_rect - 3000))

print("Amplitude à 3000 Hz (rectangulaire) :",amp_rect[index_3000])

print("Amplitude à 3000 Hz (Hann) :",amp_hann[index_3000])

# Génération d'un sinus de 1055 Hz
fs = 100000
N = 10000
f_signal = 1055

t = np.arange(N) / fs
signal = 3 * np.sin(2 * np.pi * f_signal * t)

# Application de la fenêtre Hann
window = np.hanning(N)
spectrum = np.abs(np.fft.rfft(signal * window))

# Normalisation de l'amplitude
spectrum *= 2 / np.sum(window)

frequencies = np.fft.rfftfreq(N, 1 / fs)

# Appel de notre fonction d'interpolation
f_estimated, a_estimated = interpolate_fft_peak(
    frequencies, spectrum
)

print("Fréquence réelle :", f_signal, "Hz")
print("Fréquence estimée :", f_estimated, "Hz")
print("Erreur fréquentielle :", abs(f_estimated - f_signal), "Hz")
print("Amplitude interpolée :", a_estimated, "V")
