import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from src.config import FFT_WINDOW_SIZE, HOP_SIZE, TARGET_SAMPLING_RATE

def create_spectrogram(audio_signal): 
    '''
    Generates the STFT of the audio signal and is converted to loudness decibels and returns the spectrogram. 
    '''
    print("[Phase-2] Initialising Short-Time Fourier Transform of the signal : ")
    
    frequencies, time, spectro = signal.spectrogram(
        audio_signal, fs = TARGET_SAMPLING_RATE, window="hamming", noverlap=FFT_WINDOW_SIZE - HOP_SIZE, nperseg=FFT_WINDOW_SIZE
    )
    
    # converts to loudness which is a better metric for comparision. 
    spectro_db = 10 * np.log10(spectro + 1e-10) # adding the small value to prevent runtime errors. 
    
    print(f"Spectrogram extracted successfully: Shape of the spectrogram: {spectro_db.shape}")
    print(f"Time stamps: {len(time)}")
    print(f"Frequency bins: {len(frequencies)}")
    
    return frequencies, time, spectro_db

def visualize_spectro(frequencies, time, spectro, track_name): 
    '''
    Plots the 2D heatmap of the spectrogram
    '''
    plt.figure(figsize=(12, 5))
    plt.pcolormesh(time, frequencies, spectro, shading='gouraud', cmap='viridis')
    plt.title(f"Spectrogram for signal -{track_name}", fontsize = 10, fontweight = 'bold')
    plt.xlabel("Time: ")
    plt.ylabel("Frequency: ")
    plt.ylim(0, 5000)
    plt.colorbar(label = "Power(DB)")
    plt.tight_layout()
    plt.show()

if __name__  == "__main__": 
    from src.preprocess import standardize_audio
    import os 
    testfile = "/mnt/c/Users/Praneeth Tadi/Documents/Coding/Machine Learning/ML Projects/Sound-wave-match-engine/data/raw/sample-20s.mp3"
    try: 
        raw_signal, src = standardize_audio(testfile)
        
        freqs, times, spec = create_spectrogram(raw_signal)
        
        visualize_spectro(freqs, times, spec, os.path.basename(testfile))
    except Exception as e: 
        print(f"Error: {e}")