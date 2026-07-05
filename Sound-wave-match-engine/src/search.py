"""Matching utilities that compare generated fingerprints to stored ones."""

from collections import defaultdict

import numpy as np

from src.database import get_db_conn
from src.fingerprint import generate_hash, get_2d_peaks
from src.preprocess import standardize_audio
from src.spectrogram import create_spectrogram


def find_matches(query_hashes):
    """Return the songs and offsets that match the supplied query hashes."""
    conn = get_db_conn()
    cursor = conn.cursor()

    match_songs = defaultdict(list)
    hash_keys = [hash_value for hash_value, _ in query_hashes]

    if not hash_keys:
        return match_songs

    placeholder = ",".join(["?"] * len(hash_keys))
    query = f"""
        SELECT hash, song_id, time_offset
        FROM fingerprints
        WHERE hash IN ({placeholder})
    """
    cursor.execute(query, hash_keys)
    db_results = cursor.fetchall()

    print(f"Database returned {len(db_results)} matching fingerprint rows.")
    conn.close()

    query_time_map = {hash_value: query_time for hash_value, query_time in query_hashes}

    for hash_value, song_id, db_offset in db_results:
        query_time = query_time_map[hash_value]
        time_offset = db_offset - query_time
        match_songs[song_id].append(time_offset)

    return match_songs


def score_matches(match_songs, bin_size=0.5):
    """Rank candidate songs using a histogram of time-offset votes."""
    rank = []

    for song_id, offsets in match_songs.items():
        if not offsets:
            continue

        quantized_values = [np.round(x / bin_size) * bin_size for x in offsets]

        histogram = defaultdict(int)
        for bucket in quantized_values:
            histogram[bucket] += 1

        best_peak = max(histogram.values())
        rank.append((song_id, best_peak))

    rank.sort(key=lambda item: item[1], reverse=True)
    return rank


def identify_song(file_path):
    """Process a query clip and report the best matching song."""
    signal, sr = standardize_audio(file_path)
    freqs, times, spectro = create_spectrogram(signal)
    freq_ind, time_ind = get_2d_peaks(spectro)

    print(f"Constellation map generated with {len(time_ind)} peaks.")
    hashes = generate_hash(times, freqs, time_ind, freq_ind)

    print(f"Searching the database for {len(hashes)} query fingerprints...")
    match_songs = find_matches(hashes)
    print(f"Found {len(match_songs)} candidate songs.")
    score = score_matches(match_songs)

    print("Top 3 matches:")

    conn = get_db_conn()
    cursor = conn.cursor()

    for rank, (song_id, peak) in enumerate(score[:3], start=1):
        cursor.execute("SELECT title, artist FROM songs WHERE id = ?", (song_id,))
        title, artist = cursor.fetchone()
        print(f"{rank}. {title} by {artist} with {peak} aligned hits")

    if not score:
        print("No matches found.")
        conn.close()
        return None

    conn.close()
    return score[0]


if __name__ == "__main__":
    test_path = "/mnt/c/Users/Praneeth Tadi/Documents/Coding/Machine Learning/ML Projects/Sound-wave-match-engine/data/raw/sample-20s.mp3"
    identify_song(test_path)
