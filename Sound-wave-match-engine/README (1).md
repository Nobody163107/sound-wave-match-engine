# SoundWave Match Engine

SoundWave is a lightweight audio identification project inspired by acoustic fingerprinting systems such as Shazam. It converts audio into compact fingerprint hashes, stores them in SQLite, and later uses them to recognize unknown recordings.

## Overview

The pipeline is organized into a small set of stages:

1. Audio preprocessing and normalization
2. Spectrogram generation using STFT
3. Peak detection to build a sparse constellation map
4. Combinatorial hashing for robust matching
5. SQLite-based lookup and offset voting

## Project structure

```text
soundwave-match-engine/
├── data/
│   ├── database/
│   ├── queries/
│   └── raw/
├── src/
│   ├── config.py
│   ├── preprocess.py
│   ├── spectrogram.py
│   ├── fingerprint.py
│   ├── database.py
│   └── search.py
├── requirements.txt
└── readme.md
```

## Installation

```bash
python3 -m venv sndenv
source sndenv/bin/activate
pip install -r requirements.txt
```

## Usage

Add a song to the database:

```bash
python -m src.main --add "data/raw/sample-20s.mp3" --artist "Example Artist"
```

Identify a recording:

```bash
python -m src.main --identify "data/queries/your_query.mp3"
```

## Notes

- The project currently uses a local SQLite database for fingerprint storage.
- The matching logic is based on relative time offsets between peaks, which helps handle clips that start at different positions.
- The implementation is intentionally simple and easy to follow for learning and experimentation.
