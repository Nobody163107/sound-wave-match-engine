import numpy as np
import scipy.ndimage as ndimage
import matplotlib.pyplot as plt
from src.config import NEIGHBOURHOOD_SIZE, MIN_DELTA_TIME, MAX_DELTA_TIME, FAN_OUT
import hashlib


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


def generate_hash(times, freqs, time_ind, freq_ind): 
    """
    This function obtains the peaks we got and pairs them into anchor frequency and target frequency and then hashes them. 
    
    """
    hashes = []# to store the hashes. 
    
    num_peaks = len(time_ind) # total number of peaks contesting for being an anchor. 
    
    for i in range(num_peaks): 
        anchor_idx = time_ind[i] # gives the index of the anchor
        anchor_freq = freqs[freq_ind[i]]
        actual_tim = times[anchor_idx]
        
        pairs_form = 0
        for j in range(i + 1, num_peaks): 
            target_time_idx = time_ind[j]
            target_freq = freqs[freq_ind[j]]
            
            delta_t_idx = target_time_idx - anchor_idx


            # if this conditino satisfies then we can take that time, we dont want too close peaks nor too far peaks
            if MIN_DELTA_TIME <= delta_t_idx  <= MAX_DELTA_TIME:
                actual_delta_t = times[target_time_idx] - actual_tim
                
                hash_str = f"{int(anchor_freq)}|{int(target_freq)}|{actual_delta_t:.3f}"
                
                hashing = hashlib.sha1(hash_str.encode("utf-8")).hexdigest()[:20] # store only 20 characters which is enough for 80 bits
                
                hashes.append((hashing, actual_tim))
                
                pairs_form += 1
                
                if(pairs_form >= FAN_OUT): break
                
                
            elif delta_t_idx > MAX_DELTA_TIME:
                break
        
    print("[Phase- 4] Successfully Generated Unique hash values for the constellation maps. ")
    return hashes
    


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
        
        # visualize_constell(times, freqs, time_i, freq_i, os.path.basename(test_file))
        
        hashes = generate_hash(times, freqs, time_i, freq_i)
        
        print("Displaying the hash keys for the peaks: (hashkey -> time_offset)")
        for key, off in hashes[:10]: 
            print(f"THe hash value : {key} has a time offset {off}")
        
    
    
    except Exception as e: 
        print(f"Error: {e}")
    
    
    
    
    
    