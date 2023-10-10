import sqlite3

import cursor as cursor

from media import media_Entry, media_Metadata
class create_new_entry():
    conn = sqlite3.connect('my_database.db')
    # Create a cursor object to interact with the database.
    cursor = conn.cursor()
    # Create new media entry
    test_study_entry = media_Entry.create_new_media_entry("Burst", "2023-10-09T10:18:35.200", "None", 9600, 0.23, 0.23, 5000)
    cursor.execute("INSERT INTO media_entry (shotType, time, illuminationType, iso, apertureSize, shutterSpeed, "
                   "whiteBalance) VALUES (?, ?, ?, ?, ?, ?, ?)", test_study_entry)
    entry_id = cursor.lastrowid
    test_study_data = media_Metadata.create_new_mediadata(entry_id, "leftcamera", "rightcamera", "2023-10-09T10:18:35.200", 98, 124, 9, 15)
    cursor.execute("INSERT INTO media_metadata (entryId, leftCameraMedia, rightCameraMedia, time, temperature, pressure, ph, dissolvedOxygen) "
                   "Values (?, ?, ?, ?, ?, ?, ?, ?)", test_study_data)
    conn.commit()
    conn.close()
