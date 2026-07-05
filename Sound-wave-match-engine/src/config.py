"""Global configuration values used throughout the audio fingerprinting pipeline."""

# Phase 1: audio loading and normalization
TARGET_SAMPLING_RATE = 22050
CHANNELS = 1

# Phase 2: spectrogram generation
FFT_WINDOW_SIZE = 4096
HOP_SIZE = 1024

# Phase 3: peak detection and suppression
NEIGHBOURHOOD_SIZE = 15
MIN_AMPLITUDE = -60

# Phase 4: combinatorial hashing
FAN_OUT = 5
MIN_DELTA_TIME = 1
MAX_DELTA_TIME = 10


