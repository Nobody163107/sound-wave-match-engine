import numpy as np
from collections import defaultdict # to get an efficient dictionary rather than python native.
from src.preprocess import standardize_audio
from src.fingerprint import generate_hash, get_2d_peaks
from src.spectrogram import create_spectrogram
from src.database import get_db_conn


def find_matches(query_hashes): 
    '''
    This function takes the query hashes and generates a list with offsets to each of the matched hashes. 
    '''
    
    conn = get_db_conn()
    cursor = conn.cursor()
    
    # creating a dictionary of list to store the songs with offsets
    
    match_songs = defaultdict(list)
    # extract only the hashes.  
    hash_key = [h_key for h_key, _ in query_hashes]
    
    if not hash_key: 
        return match_songs
    
    
    # Create the SQL placeholder for lookups. 
    
    place_holder = ",".join(["?"] * len(hash_key))
    
    query = f"""
        SELECT hash , song_id, time_offset
        FROM fingerprints
        WHERE hash IN ({place_holder})    
    
    """    
    cursor.execute(query, hash_key)
    db_results = cursor.fetchall()
    conn.close()    
    # mapping the values for fast lookup. 
    query_time_map = {h_key: q_time for h_key, q_time in query_hashes}
    
    
    # storing the matches as per the hasehs found
    for h_key, song_id, db_off in db_results: 
        q_time = query_time_map[h_key]
        time_off = db_off - q_time
        match_songs[song_id].append(time_off)
        
    return match_songs


def score_matches(): 