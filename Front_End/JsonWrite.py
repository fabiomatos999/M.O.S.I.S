import sqlite3
import json
import sys


class JsonSelectAll():
    # Connect to the SQLite database
    conn = sqlite3.connect("testing3.db")
    cursor = conn.cursor()

    # Selects data from both media entry and media metadata table using JOIN
    cursor.execute('''
        SELECT
            media_entry.entryId,
            media_entry.shotType,
            media_entry.time AS entryTime,
            media_entry.illuminationType,
            media_entry.gain,
            media_entry.saturation,
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
        (entry_id, shot_type, entry_time, illumination_type, gain, saturation,
         shutter_speed, white_balance, metadata_id, left_camera_media,
         right_camera_media, metadata_time, temperature, pressure, ph,
         dissolved_oxygen) = row

        entry_data = {
            "entryId": entry_id,
            "shotType": shot_type,
            "entryTime": entry_time,
            "illuminationType": illumination_type,
            "gain": gain,
            "saturation": saturation,
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

    # Checks if the media_entry and media_metadata tables are empty
    if not media_data:
        print("There is no data stored")
        sys.exit()

    # Serialize and save each entry to a separate JSON file
    for index, entry in enumerate(media_data):
        json_data = json.dumps(entry, indent=4)
        filename = f"entry_{index + 1}.json"
        with open(filename, 'w') as json_file:
            json_file.write(json_data)
        print(f"Saved JSON data to {filename}")

    # Close the database connection
    conn.close()


# Execute the class to run the code
JsonSelectAll()
