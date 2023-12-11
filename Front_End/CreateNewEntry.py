import sqlite3
from DataClass import MediaEntry, MediaMetadata
from RandomEntryGenerator import RandomEntry

class CreateNewEntry():
    conn = sqlite3.connect('testing6.db')
    # Create a cursor object to interact with the database.
    cursor = conn.cursor()
    # Create new media entry
    test_study_entry = RandomEntry.rand_media_entry()
    # Insert the media entry into media entry table
    cursor.execute("INSERT INTO media_entry (shotType, time, illuminationType, gain, saturation, shutterSpeed, "
                   "whiteBalance) VALUES (?, ?, ?, ?, ?, ?, ?)", test_study_entry)
    # Saves entry id of media entry to a variable
    entry_id = cursor.lastrowid
    # Create new media data entry with media entry id
    test_study_data = RandomEntry.rand_media_metadata()
    study_data = (entry_id,) + test_study_data
    # Insert the media metadata entry to media metadata table
    cursor.execute("INSERT INTO media_metadata (entryId, leftCameraMedia, rightCameraMedia, time, temperature, pressure, ph, dissolvedOxygen) "
                   "Values (?, ?, ?, ?, ?, ?, ?, ?)",  study_data)
    conn.commit()
    conn.close()
