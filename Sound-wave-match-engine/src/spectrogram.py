"""Spectrogram generation helpers for time-frequency feature extraction."""

import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as signal

from src.config import FFT_WINDOW_SIZE, HOP_SIZE, TARGET_SAMPLING_RATE


def create_spectrogram(audio_signal):
    """Create a logarithmic spectrogram from an audio signal."""
    print("[Phase 2] Computing the short-time Fourier transform...")

    frequencies, time, spectro = signal.spectrogram(
        audio_signal,
        fs=TARGET_SAMPLING_RATE,
        window="hamming",
        noverlap=FFT_WINDOW_SIZE - HOP_SIZE,
        nperseg=FFT_WINDOW_SIZE,
    )

    spectro_db = 10 * np.log10(spectro + 1e-10)

    print(f"Spectrogram created successfully. Shape: {spectro_db.shape}")
    print(f"Time bins: {len(time)}")
    print(f"Frequency bins: {len(frequencies)}")

    return frequencies, time, spectro_db


def visualize_spectro(frequencies, time, spectro, track_name):
    """Plot the spectrogram as a 2D heatmap."""
    plt.figure(figsize=(12, 5))
    plt.pcolormesh(time, frequencies, spectro, shading="gouraud", cmap="viridis")
    plt.title(f"Spectrogram for {track_name}", fontsize=10, fontweight="bold")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Frequency (Hz)")
    plt.ylim(0, 5000)
    plt.colorbar(label="Power (dB)")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    import os

    from src.preprocess import standardize_audio

    testfile = "/mnt/c/Users/Praneeth Tadi/Documents/Coding/Machine Learning/ML Projects/Sound-wave-match-engine/data/raw/sample-20s.mp3"
    try:
        raw_signal, src = standardize_audio(testfile)

        freqs, times, spec = create_spectrogram(raw_signal)

        visualize_spectro(freqs, times, spec, os.path.basename(testfile))
    except Exception as exc:
        print(f"Error: {exc}")
