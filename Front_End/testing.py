import sqlite3
import os
import DataClass  


from databaseQuery import DatabaseQuery

# Create a database connection
db = DatabaseQuery("testing3.db")

# Test the getMediaEntrybyId method
entry_id = 1  
media_entry = db.getMediaEntrybyId(entry_id)
print("Media Entry by ID:")
print(media_entry)

# Test the getMediaMetadatabyId method
metadata_id = 1  
media_metadata = db.getMediaMetadatabyId(metadata_id)
print("Media Metadata by ID:")
print(media_metadata)

# Test the getAllMediaMetadaByEntryId method
entry_id = 1  
metadata_list = db.getAllMediaMetadaByEntryId(entry_id)
print("All Media Metadata for Entry ID:")
for metadata in metadata_list:
    print(metadata)

# Test the insertMediaEntry method
new_entry_id = db.insertMediaEntry(
    shotType="Test Shot",
    time="2023-11-05",
    illuminationType="LED",
    gain=1.5,
    saturation=100,
    shutterSpeed=1/50.0,
    whiteBalance=5000
)
print(f"Inserted Media Entry with ID: {new_entry_id}")

# Test the insertMediaMetadata method
entry_id = 1  
path = "/path/to/media"
extension = "jpg"
time = "2023-11-05"
temperature = 25.0
pressure = 1013.25
ph = 7.0
dissolved_oxygen = 8.0
new_metadata_id = db.insertMediaMetadata(
    entry_id, path, extension, time, temperature, pressure, ph, dissolved_oxygen
)
print(f"Inserted Media Metadata with ID: {new_metadata_id}")

# Test the getAllMediaEntry method
media_entries = db.getAllMediaEntry()
print("All Media Entries:")
for entry in media_entries:
    print(entry)
