import numpy as np
import scipy.ndimage as ndimage
import matplotlib.pyplot as plt
from src.config import NEIGHBOURHOOD_SIZE



def get_2d_peaks(spect_db, min_ampl = -50): 
    """
    THis function goes thro the spectrogram matrix. and collects the peaks using a 2D local maxima diamond-shaped filter and returns them as constellation. 
    """
    
    struct = ndimage.generate_binary_structure(2, 1) # the first argument tells about the dimensionalliyt, the second tells about teh connectivity, which is manhattan distance. 
    # scaling / iterating the structure till size 15 as per the config. 
    nbd = ndimage.iterate_structure(struct, NEIGHBOURHOOD_SIZE)
    
    # now we create the mappin of the local maxima values.. 
    localmax = (ndimage.maximum_filter(spect_db, footprint=nbd) == spect_db)
    
    # we create anotehr boolean mask to filter out the quieter noises. 
    background = (spect_db < min_ampl)
    # we relax the boundary a little to allow some of the cells to survive the local maxima. 
    erode_background = ndimage.binary_erosion(background, structure= nbd, border_value=1)
    
    detect_peak = localmax &  ~erode_background
    
    freq_ind, time_ind = np.where(detect_peak)
    
    return freq_ind, time_ind

def visualize_constell(times, freqs, time_ind, freq_ind, track_name): 
    """
    Helps visualise the sparse constellation maps. 
    
    """
    peak_times = times[time_ind]
    peak_freq = freqs[freq_ind]
    
    plt.figure(figsize=(12, 5))
    plt.scatter(peak_times, peak_freq, color = 'red', marker='o', s = 5, alpha = 0.7)
    plt.title(f"Peak constellation map of {track_name}")
    plt.xlabel("Time: ")
    plt.ylabel("frequency: ")
    plt.ylim(0, 5000)
    plt.show()
    


if __name__ == "__main__": 
    from src.preprocess import standardize_audio
    from src.spectrogram import create_spectrogram
    import os
    
    test_file = "/mnt/c/Users/Praneeth Tadi/Documents/Coding/Machine Learning/ML Projects/Sound-wave-match-engine/data/raw/sample-20s.mp3"
    
    try: 
        audio, sr = standardize_audio(test_file)
        freqs, times, spect = create_spectrogram(audio)
        freq_i, time_i = get_2d_peaks(spect)
        
        visualize_constell(times, freqs, time_i, freq_i, os.path.basename(test_file))
        
        
    
    
    except Exception as e: 
        print(f"Error: {e}")
    
    
    
    
    
    