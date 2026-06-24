import librosa as lb
import numpy as np
import os
import matplotlib.pyplot as plt

from src.config import TARGET_SAMPLING_RATE

def standardize_audio(filepath):
    '''
    Takes in the audio file processes into mono audio with the targeted sampling rate and also normalises it. 
    '''
    
    
    # hanlding the exception.  
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Could not find the audio file {filepath}")
    
    print(f"Processing the audio file {filepath}")
    
    # ingestion of the file
    signal, sr = lb.load(filepath, sr= TARGET_SAMPLING_RATE, mono=True)
    
    print(f"Obtaine the audio file and converted to the Numpy array")
    print(f"Sampling rate = {sr}")
    print(f"The duration of the song as detected is {len(signal) / sr:.2f} seconds")
    
    # additional processing to maintain -1 to 1 range: 
    max = np.max(np.abs(signal))
    if(max): 
        signal = signal / max
    
    
    return signal, sr

def visualise_audio(signal, sr, track_name): 
    '''
    obtains the audio file and represents it visually on a graph with amplitude vs time relationship. 
    '''

    # creating the time axis till the duration of the song for samples equal to the number of array elements
    
    time_axis = np.linspace(0, len(signal)/ sr, len(signal) )
    
    plt.figure(figsize=(12, 4))
    plt.plot(time_axis, signal, color = "blue", alpha = 0.7, linewidth = 0.4)
    plt.title(f"Visualising the audio {track_name} : ", fontsize = 12, fontweight = 'bold')
    plt.xlabel("Time (in seconds): ")
    plt.ylabel("Amplitude (-1 to 1): ")
    plt.show()


if __name__ == "__main__": 
    # Testing the file 
    Test_file = "/mnt/c/Users/Praneeth Tadi/Documents/Coding/Machine Learning/ML Projects/Sound-wave-match-engine/sample-20s.mp3"
    
    try: 
        audio, samp = standardize_audio(Test_file)
        
        print("Checking the first 5 values: ")
        print(audio[:5])
        
        visualise_audio(audio, samp, "Some song.. ")
    except Exception as e: 
        print(f"Error: {e}")
        
                
    