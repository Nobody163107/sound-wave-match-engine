"""SQLite persistence helpers for storing and retrieving audio fingerprints."""

import os
import sqlite3


db_path = "data/database/fingerprints.db"


def get_db_conn():
    """Create and return a connection to the SQLite database."""
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    """Create the SQLite schema used by the fingerprinting pipeline."""
    print("[Phase 5] Initializing the SQLite schema...")

    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = get_db_conn()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS songs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            artist TEXT DEFAULT 'unknown',
            file_path TEXT NOT NULL UNIQUE
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS fingerprints (
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
    print("Database schema setup completed successfully.")


def store_song_fingerprints(title, file_path, hashes, artist='unknown'):
    """Store a song and its generated fingerprints in the database."""
    conn = get_db_conn()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id FROM songs WHERE file_path = ?", (file_path,))
        row = cursor.fetchone()
        if row:
            print(f"Song '{title}' already exists. Skipping insertion.")
            conn.close()
            return row[0]

        cursor.execute(
            "INSERT INTO songs (title, artist, file_path) VALUES (?, ?, ?)",
            (title, artist, file_path),
        )

        song_id = cursor.lastrowid
        fingerprint_data = [(hash_value, song_id, offset) for hash_value, offset in hashes]

        print(f"Inserting {len(fingerprint_data)} fingerprint entries for '{title}'.")
        cursor.executemany(
            "INSERT INTO fingerprints (hash, song_id, time_offset) VALUES (?, ?, ?)",
            fingerprint_data,
        )

        conn.commit()
        print(f"Successfully stored fingerprints for '{title}'.")
        return song_id

    except Exception as exc:
        print("An unexpected error occurred. Rolling back the transaction.")
        conn.rollback()
        raise exc
    finally:
        conn.close()
    