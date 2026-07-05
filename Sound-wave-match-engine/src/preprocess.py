"""Audio loading and normalization utilities for the fingerprinting pipeline."""

import os

import librosa as lb
import matplotlib.pyplot as plt
import numpy as np

from src.config import TARGET_SAMPLING_RATE


def standardize_audio(filepath):
    """Load an audio file, resample it, convert it to mono, and normalize it."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Could not find the audio file: {filepath}")

    print(f"Processing audio file: {filepath}")

    signal, sr = lb.load(filepath, sr=TARGET_SAMPLING_RATE, mono=True)

    print("Audio file loaded and converted to a NumPy array.")
    print(f"Sampling rate: {sr}")
    print(f"Estimated duration: {len(signal) / sr:.2f} seconds")

    max_amplitude = np.max(np.abs(signal))
    if max_amplitude:
        signal = signal / max_amplitude

    return signal, sr


def visualise_audio(signal, sr, track_name):
    """Plot the waveform of an audio signal for inspection."""
    time_axis = np.linspace(0, len(signal) / sr, len(signal))

    plt.figure(figsize=(12, 4))
    plt.plot(time_axis, signal, color="blue", alpha=0.7, linewidth=0.4)
    plt.title(f"Waveform for {track_name}", fontsize=12, fontweight="bold")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude (-1 to 1)")
    plt.show()


if __name__ == "__main__":
    test_file = "/mnt/c/Users/Praneeth Tadi/Documents/Coding/Machine Learning/ML Projects/Sound-wave-match-engine/sample-20s.mp3"

    try:
        audio, samp = standardize_audio(test_file)

        print("Preview of the first 5 samples:")
        print(audio[:5])

        visualise_audio(audio, samp, "sample track")
    except Exception as exc:
        print(f"Error: {exc}")
