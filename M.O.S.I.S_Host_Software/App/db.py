"""Database interaction module."""
import sqlite3
from enums import illuminationType, shotType


class DatabaseQuery:
    """Database query class used to interact with the db and create tables."""

    def __init__(self, db: str = "test.db"):
        """Create db tables and gives a db connection and cursor."""
        self.conn = sqlite3.connect('test.db')
        self.cursor = self.conn.cursor()
        # Create MediaEntry table if not exists
        self.cursor.execute('''
    CREATE TABLE IF NOT EXISTS MediaEntry (
        entryId INTEGER PRIMARY KEY UNIQUE,
        shotType TEXT NOT NULL,
        time TEXT NOT NULL ,
        illuminationType TEXT NOT NULL,
        gain REAL NOT NULL,
        saturation INTEGER NOT NULL,
        shutterSpeed TEXT NOT NULL,
        whiteBalance INTEGER NOT NULL
    )
''')
        # Create MediaMetadata table if not exists
        self.cursor.execute('''
    CREATE TABLE IF NOT EXISTS MediaMetadata (
        metadataId INTEGER PRIMARY KEY UNIQUE,
        entryId INTEGER,
        leftCameraMedia TEXT NOT NULL,
        rightCameraMedia TEXT NOT NULL,
        time TEXT NOT NULL,
        temperature REAL NOT NULL,
        pressure REAL NOT NULL,
        ph REAL NOT NULL,
        dissolvedOxygen REAL NOT NULL,
        FOREIGN KEY (entryId) REFERENCES media_entry(entryId)
    )
''')
        self.conn.commit()

    def __del__(self):
        """Close db connection when object is destroyed."""
        self.conn.close()

    def insertMediaEntry(self, entryId: int, shottype: shotType,
                         illuminationtype: illuminationType, saturation: int,
                         gain: float, shutterSpeed: str, whiteBalance: int):
        self.cursor.execute(
            """INSERT INTO MediaEntry
            (entryId, shotType, time,
            illuminationType, gain, saturation, whiteBalance)
            VALUES (?, ?,?,?,?,?,?)""",
            (entryId, shottype, illuminationtype, gain, saturation,
             shutterSpeed, whiteBalance))
        self.conn.commit()
