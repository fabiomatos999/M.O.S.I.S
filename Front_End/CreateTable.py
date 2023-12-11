"""Create tables for the M.O.S.I.S UI database."""
import sqlite3

# Connect to or create an SQLite database file. If it doesn't exist,
# a new database will be created.
conn = sqlite3.connect('testing6.db')

# Create a cursor object to interact with the database.
cursor = conn.cursor()
# Creates the Media Entry Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS media_entry (
        entryId INTEGER PRIMARY KEY,
        shotType TEXT NOT NULL,
        time TEXT NOT NULL ,
        illuminationType TEXT NOT NULL,
        gain REAL NOT NULL,
        saturation INTEGER NOT NULL,
        shutterSpeed TEXT NOT NULL,
        whiteBalance INTEGER NOT NULL
    )
''')
# Creates the Media Metadata Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS media_metadata (
        metadataId INTEGER PRIMARY KEY,
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

# Commit the changes and close the database connection when done.
conn.commit()
conn.close()
