
import numpy as np

from mes.signal_processing import compute_fft


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
