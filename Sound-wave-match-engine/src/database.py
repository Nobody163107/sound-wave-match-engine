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
    
    