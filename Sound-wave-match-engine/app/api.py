import os
import shutil
from fastapi import FastAPI
from fastapi import UploadFile, File, HTTPException
from src.search import identify_song
from src.database import get_db_conn
app = FastAPI(title="SoundWave Matching Engine", version="1.0.0")


@app.get("/")
async def message(): 
    return {"Status": "Running", 
            "Message": "Welcome to SoundWave Matching Engine"}


@app.post("/identify")
async def identify_audio(file: UploadFile = File(...)): 
    """
    Takes a live recording or audio file blob,
    processes through the DSP pipeline and returns the top result
    """
    # extensions allowed
    ext = [".mp3", ]
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in ext and file.filename != "blob": 
        # sometimes raw buffer is names as blo
        pass
    
    
    temp_dir = "data/temp"
    os.makedirs(temp_dir, exist_ok=True)
    
    temp_file = os.path.join(temp_dir, file.filename)
    
    try: 
            

        with open(temp_file, "wb") as buffer: 
            shutil.copyfileobj(file.file, buffer)

        result = identify_song(temp_file)
        song_id, score = result
        conn = get_db_conn()
        cursor = conn.cursor()

        cursor.execute("SELECT title, artist FROM songs WHERE id = ?", (song_id, ))
        row = cursor.fetchone()

        if not row: 
            raise HTTPException(status_code=500, detail="Found the match but no registry metadata found.")
        title, artist = row
        conn.close()

        if not result: 
            return {
                "status": "404 not foound", 
                "Detail" : "Such a song doesnt exist"
            }

        return {
            "status": "success",
            "song": {
                "id": song_id, 
                "title": title,
                "aritist": artist,
                "match_score": score
                
            } 
}   
    except Exception as e:
        print(f"Error occured : {e}")
    finally: 
        if os.path.exists(temp_file):
            os.remove(temp_file)
            
@app.post("/health")
async def health_check():
    """Simple ping check to make sure the app is running. """
    return {"status": "Engine running", "health": "Healthy"}
            