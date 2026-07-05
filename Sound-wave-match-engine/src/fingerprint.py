"""Peak extraction and fingerprint hashing utilities for the audio pipeline."""

import hashlib

import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage as ndimage

from src.config import FAN_OUT, MAX_DELTA_TIME, MIN_DELTA_TIME, NEIGHBOURHOOD_SIZE


def get_2d_peaks(spect_db, min_ampl=-50):
    """Return prominent spectrogram peaks as a sparse constellation map."""
    struct = ndimage.generate_binary_structure(2, 1)
    nbd = ndimage.iterate_structure(struct, NEIGHBOURHOOD_SIZE)

    localmax = (ndimage.maximum_filter(spect_db, footprint=nbd) == spect_db)
    background = spect_db < min_ampl
    erode_background = ndimage.binary_erosion(background, structure=nbd, border_value=1)

    detect_peak = localmax & ~erode_background

    freq_ind, time_ind = np.where(detect_peak)
    order = np.argsort(time_ind)

    time_ind = time_ind[order]
    freq_ind = freq_ind[order]

    return freq_ind, time_ind


def generate_hash(times, freqs, time_ind, freq_ind):
    """Create combinatorial fingerprint hashes from detected peak pairs."""
    hashes = []

    num_peaks = len(time_ind)

    for i in range(num_peaks):
        anchor_idx = time_ind[i]
        anchor_freq = freqs[freq_ind[i]]
        actual_time = times[anchor_idx]

        pairs_form = 0
        for j in range(i + 1, num_peaks):
            target_time_idx = time_ind[j]
            target_freq = freqs[freq_ind[j]]

            delta_t_idx = target_time_idx - anchor_idx

            if MIN_DELTA_TIME <= delta_t_idx <= MAX_DELTA_TIME:
                actual_delta_t = times[target_time_idx] - actual_time
                hash_str = f"{int(anchor_freq)}|{int(target_freq)}|{actual_delta_t:.3f}"
                hash_value = hashlib.sha1(hash_str.encode("utf-8")).hexdigest()[:20]

                hashes.append((hash_value, actual_time))
                pairs_form += 1

                if pairs_form >= FAN_OUT:
                    break

            elif delta_t_idx > MAX_DELTA_TIME:
                break

    print("[Phase 4] Fingerprints generated successfully.")
    return hashes


def visualize_constell(times, freqs, time_ind, freq_ind, track_name):
    """Plot the sparse constellation map for a track."""
    peak_times = times[time_ind]
    peak_freq = freqs[freq_ind]

    plt.figure(figsize=(12, 5))
    plt.scatter(peak_times, peak_freq, color='red', marker='o', s=5, alpha=0.7)
    plt.title(f"Peak constellation map of {track_name}")
    plt.xlabel("Time")
    plt.ylabel("Frequency")
    plt.ylim(0, 5000)
    plt.show()


if __name__ == "__main__":
    from src.database import *
    import os

    from src.preprocess import standardize_audio
    from src.spectrogram import create_spectrogram

    test_file = "/mnt/c/Users/Praneeth Tadi/Documents/Coding/Machine Learning/ML Projects/Sound-wave-match-engine/data/raw/sample-20s.mp3"

    try:
        init_db()

        audio, sr = standardize_audio(test_file)
        freqs, times, spect = create_spectrogram(audio)
        freq_i, time_i = get_2d_peaks(spect)

        hashes = generate_hash(times, freqs, time_i, freq_i)

        song_title = os.path.splitext(os.path.basename(test_file))[0]

        print("Connecting to the database...")
        song_id = store_song_fingerprints(
            title=song_title,
            artist="Test artist, Mango",
            hashes=hashes,
            file_path=test_file,
        )

        print(f"Successfully added the song to the database with reference id: {song_id}")

    except Exception as exc:
        print(f"Error: {exc}")
    