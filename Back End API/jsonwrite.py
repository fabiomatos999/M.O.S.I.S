import sqlite3
import json
import sys

# Connect to the SQLite database
conn = sqlite3.connect("MOSIS.db")
cursor = conn.cursor()

# Selects data from both media entry and media metadata table using JOIN
cursor.execute('''
    SELECT
        media_entry.entryId,
        media_entry.shotType,
        media_entry.time AS entryTime,
        media_entry.illuminationType,
        media_entry.iso,
        media_entry.apertureSize,
        media_entry.shutterSpeed,
        media_entry.whiteBalance,
        media_metadata.metadataId,
        media_metadata.leftCameraMedia,
        media_metadata.rightCameraMedia,
        media_metadata.time AS metadataTime,
        media_metadata.temperature,
        media_metadata.pressure,
        media_metadata.ph,
        media_metadata.dissolvedOxygen
    FROM media_entry
    JOIN media_metadata ON media_entry.entryId = media_metadata.entryId
''')

rows = cursor.fetchall()
# Define a list to store the data
media_data = []

# Convert the fetched data into a list of dictionaries
for row in rows:
    (
        entry_id,
        shot_type,
        entry_time,
        illumination_type,
        iso,
        aperture_size,
        shutter_speed,
        white_balance,
        metadata_id,
        left_camera_media,
        right_camera_media,
        metadata_time,
        temperature,
        pressure,
        ph,
        dissolved_oxygen
    ) = row

    entry_data = {
        "entryId": entry_id,
        "shotType": shot_type,
        "entryTime": entry_time,
        "illuminationType": illumination_type,
        "iso": iso,
        "apertureSize": aperture_size,
        "shutterSpeed": shutter_speed,
        "whiteBalance": white_balance,
        "metadataId": metadata_id,
        "leftCameraMedia": left_camera_media,
        "rightCameraMedia": right_camera_media,
        "metadataTime": metadata_time,
        "temperature": temperature,
        "pressure": pressure,
        "ph": ph,
        "dissolvedOxygen": dissolved_oxygen
    }

    media_data.append(entry_data)

#Checks if the media_entry and media_metadata tables are empty
if not media_data:
    print("There is no data stored")
    sys.exit()

# Serialize the list of dictionaries to JSON format
json_data = json.dumps(media_data, indent=4)

# Print the JSON data or save it to a file
print(json_data)

# Close the database connection
conn.close()
