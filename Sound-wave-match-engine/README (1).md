# Sound-Wave Match Engine (Acoustic Fingerprinting System)

A lightweight, highly optimized audio identification engine built from
scratch in Python. It implements the core concepts behind industrial
acoustic fingerprinting systems (such as **Shazam**) by converting audio
into sparse constellation maps, generating robust combinatorial hashes,
and matching unknown recordings using relative time-offset alignment.

------------------------------------------------------------------------

# System Architecture

``` text
                 Raw Audio
                     │
                     ▼
      Phase 1 ── Audio Preprocessing
                     │
                     ▼
      Phase 2 ── STFT Spectrogram
                     │
                     ▼
      Phase 3 ── 2D Peak Detection
                     │
                     ▼
      Phase 4 ── Combinatorial Hashing
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
Phase 5: Database         Phase 6: Matching
(SQLite Indexing)      (Offset Histogram)
         │
         ▼
Phase 7: CLI / Deployment
```

------------------------------------------------------------------------

# Phase Overview

## Phase 1 --- Audio Preprocessing

-   Load MP3/WAV files
-   Convert to mono
-   Resample to **22050 Hz**
-   Normalize signal

------------------------------------------------------------------------

## Phase 2 --- Spectrogram Generation

The audio signal is divided into overlapping windows and transformed
into the frequency domain using the Short-Time Fourier Transform (STFT).

Default parameters:

-   FFT Window: **4096**
-   Hop Length: **1024**

Output:

-   Frequency bins
-   Time bins
-   Spectrogram (dB)

------------------------------------------------------------------------

## Phase 3 --- Peak Detection

A 2D local-maximum filter is applied over the spectrogram to retain only
high-energy acoustic landmarks.

Processing includes:

-   Diamond-shaped neighborhood filtering
-   Binary erosion
-   Noise suppression

The output is a sparse **Constellation Map**.

------------------------------------------------------------------------

## Phase 4 --- Combinatorial Hashing

Each anchor peak is paired with future peaks inside a target zone.

Each pair stores:

-   Anchor Frequency
-   Target Frequency
-   Time Difference (Δt)

These values are converted into a SHA-1 fingerprint.

------------------------------------------------------------------------

## Phase 5 --- Database Storage

Fingerprints are stored inside SQLite using two relational tables.

### songs

  Column      Description
  ----------- ------------------------
  id          Unique song identifier
  title       Song title
  artist      Artist
  file_path   Original file path

### fingerprints

  Column        Description
  ------------- -------------------
  hash          SHA-1 fingerprint
  song_id       Foreign key
  time_offset   Timestamp

A **B-Tree index** is created on the `hash` column for efficient lookup.

------------------------------------------------------------------------

## Phase 6 --- Matching Engine

Unknown audio is processed through the exact same fingerprint pipeline.

For every matching hash:

ΔOffset = Database Offset − Query Offset

Correct matches produce a strong histogram peak, while incorrect matches
produce scattered offsets.

------------------------------------------------------------------------

## Phase 7 --- CLI & Deployment

The project exposes a unified command-line interface for:

-   Adding songs
-   Building the fingerprint database
-   Identifying unknown recordings

------------------------------------------------------------------------

# Hyperparameters (`src/config.py`)

``` python
TARGET_SAMPLING_RATE = 22050
CHANNELS = 1

FFT_WINDOW_SIZE = 4096
HOP_SIZE = 1024

NEIGHBOURHOOD_SIZE = 15
MIN_AMPLITUDE_DB = -60

MIN_DELTA_TIME = 1
MAX_DELTA_TIME = 10
FAN_OUT = 5
```

------------------------------------------------------------------------

# Installation

``` bash
git clone https://github.com/yourusername/Sound-wave-match-engine.git
cd Sound-wave-match-engine

python3 -m venv sndenv
source sndenv/bin/activate
# Windows:
# sndenv\Scripts\activate

pip install -r requirements.txt
```

------------------------------------------------------------------------

# Usage

## Add a song

``` bash
python main.py --add "data/raw/sample-20s.mp3" --artist "The Test Band"
```

## Identify a recording

``` bash
python main.py --identify "path/to/recorded_clip.mp3"
```

------------------------------------------------------------------------

# Production Roadmap

-   Replace SQLite with PostgreSQL + Redis
-   Expose a FastAPI REST API
-   Containerize using Docker
-   Deploy to cloud infrastructure

------------------------------------------------------------------------

# Project Structure

``` text
Sound-wave-match-engine/
│
├── data/
│   ├── database/
│   └── raw/
│
├── src/
│   ├── config.py
│   ├── preprocess.py
│   ├── spectrogram.py
│   ├── fingerprint.py
│   ├── database.py
│   └── search.py
│
├── main.py
├── Dockerfile
├── requirements.txt
└── README.md
```

------------------------------------------------------------------------

# Future Improvements

-   Real-time microphone recognition
-   GPU-accelerated spectrogram generation
-   Distributed fingerprint storage
-   Confidence scoring
-   Web dashboard
-   Mobile integration
