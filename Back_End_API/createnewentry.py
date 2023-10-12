import sqlite3
from media import MediaEntry, MediaMetadata


class CreateNewEntry():
    conn = sqlite3.connect('my_database.db')
    # Create a cursor object to interact with the database.
    cursor = conn.cursor()
    # Create new media entry
    test_study_entry = MediaEntry.create_new_media_entry("Burst", "2023-10-09T10:18:35.200", "None", 9600, 0.23, 0.23, 5000)
    # Insert the media entry into media entry table
    cursor.execute("INSERT INTO media_entry (shotType, time, illuminationType, iso, apertureSize, shutterSpeed, "
                   "whiteBalance) VALUES (?, ?, ?, ?, ?, ?, ?)", test_study_entry)
    # Saves entry id of media entry to a variable
    entry_id = cursor.lastrowid
    # Create new media data entry with media entry id
    test_study_data = MediaMetadata.create_new_mediadata(entry_id, "leftcamera", "rightcamera", "2023-10-09T10:18:35.200", 100, 124, 9, 15)
    # Insert the media metadata entry to media metadata table
    cursor.execute("INSERT INTO media_metadata (entryId, leftCameraMedia, rightCameraMedia, time, temperature, pressure, ph, dissolvedOxygen) "
                   "Values (?, ?, ?, ?, ?, ?, ?, ?)", test_study_data)
    conn.commit()
    conn.close()
