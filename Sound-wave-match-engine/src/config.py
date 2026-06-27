# this file consists all of the global parameters we apply to any of the audio files ingested into the pipeline. 


# PHASE -1 parameters.
TARGET_SAMPLING_RATE = 22050 # according to the nquiest theorem this is enougth to properly process audio files without losing much information
CHANNELS = 1 # we dont need spatial information so mono audio is self-sufficient. 

# PHASE -2 parameters. 
FFT_WINDOW_SIZE = 4096 # Size of the window which is going to slide
HOP_SIZE = 1024 # the distance each window slides.. with time. 

# Phase -3 Maxpooling
NEIGHBOURHOOD_SIZE = 15


