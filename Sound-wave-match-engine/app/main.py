import argparse
import os

from src.database import init_db, store_song_fingerprints
from src.fingerprint import generate_hash, get_2d_peaks
from src.preprocess import standardize_audio
from src.search import identify_song
from src.spectrogram import create_spectrogram


def add_song(file_path, artist):
    """Register a song with the fingerprint database."""
    if not os.path.exists(file_path):
        print("No such file exists at the provided path.")
        return

    song_title = os.path.splitext(os.path.basename(file_path))[0]
    print(f"[CLI] Registering '{song_title}' by {artist}.")

    signal, sr = standardize_audio(file_path)
    freqs, times, spectro = create_spectrogram(signal)
    freq_idx, time_idx = get_2d_peaks(spectro)
    song_hashes = generate_hash(times, freqs, time_idx, freq_idx)

    song_id = store_song_fingerprints(
        title=song_title,
        file_path=file_path,
        hashes=song_hashes,
        artist=artist,
    )

    print(f"Successfully added the song to the database with id: {song_id}")


def main():
    parser = argparse.ArgumentParser(description="SoundWave matching engine")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--add", type=str, help="Path to the song to add to the database.")
    group.add_argument("--identify", type=str, help="Path to the song to identify.")
    parser.add_argument("--artist", type=str, default="unknown", help="Artist or composer name.")

    args = parser.parse_args()

    init_db()

    if args.add:
        add_song(args.add, args.artist)
    elif args.identify:
        if not os.path.exists(args.identify):
            print(f"Could not find a file at {args.identify}")
            return

        identify_song(args.identify)


if __name__ == "__main__":
    main()
