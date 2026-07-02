import sqlite3
import os

db_path = "data/database/fingerprints.db"

def get_db_conn(): 
    """
    Establishes the connection to the database and returns the connection
    """
    conn = sqlite3.connect(db_path)

    
    conn.execute("PRAGMA foreign_keys = ON;")
    
    return conn


def init_db(): 
    """
    Creates database schema and sets up the tables and structure for fast lookups. 
    """
    # 
    print("[PHase - 5] Setting up the Relational Database Schema: ")
    
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = get_db_conn()
    cursor = conn.cursor()
    
    # 1. Creating the first table or registry. 
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS songs (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       title TEXT NOT NULL,
                       artist TEXT DEFAULT 'unknown',
                       file_path TEXT NOT NULL UNIQUE
                       
                       
                   )
                   
                   
                   
                   """)
    
    cursor.execute(
        """
            CREATE TABLE IF NOT EXISTS fingerprints(
                hash TEXT NOT NULL, 
                song_id INTEGER NOT NULL, 
                time_offset REAL NOT NULL, 
                FOREIGN KEY (song_id) REFERENCES songs(id) ON DELETE CASCADE
                
                
            )
        
        
        """
        
    )
    
    conn.execute("CREATE INDEX IF NOT EXISTS idx_hash ON fingerprints(hash)")
    conn.commit()
    conn.close()
    print("Succesfully completed Setting up the relational schema. ")
    
def store_song_fingerprints(title, file_path, hashes, arist = 'unknown'): 
    '''
    This function takes the processed fingerprints of a song and inserts all of them at once. 
    '''
    # initialise the connection
    conn = get_db_conn()
    cursor = conn.cursor()
    
    try: 
        # get the row number to check if it exists. 
        cursor.execute("SELECT id FROM songs WHERE file_path = ?", (file_path, ))
        row = cursor.fetchone()
        if row: 
            # skip if exists
            print(f"The song {title} already exists, so skipping")
            conn.close()
            return row[0];
        
        # insert the song metadata
        cursor.execute("INSERT INTO songs (title, artist, file_path) VALUES (?, ?, ?)", (title, arist, file_path))
        
        song_id = cursor.lastrowid
        
        # inserting all the hashes
        # getting the data with exact format as per the schema: 
        fingerprint_data = [(has, song_id, offset) for has, offset in hashes]
        
        print(f"Inserting the data of {len(fingerprint_data)} hashes into the database: ")
        cursor.executemany("INSERT INTO fingerprints (hash, song_id, time_offset) VALUES (?, ?, ?)", fingerprint_data)
        
        
        
        conn.commit()
        print(f"Success ! successfully inserted the fingerprints for {title}")
        # conn.close()
        return song_id
        
    except Exception as e:
        print("Unknown error occured ! rolling back the changes")
        conn.rollback()
        # conn.close()
        raise e
    finally: 
        conn.close()
        
    
    
    
    