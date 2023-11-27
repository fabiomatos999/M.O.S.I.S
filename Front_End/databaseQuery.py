"""Database query abstraction module for M.O.S.I.S microscope UI."""
import sqlite3
import os
import DataClass


class DatabaseQuery:
    """Create database and corrects to it."""

    def __init__(self, db: str = "M.O.S.I.S.db"):
        """Given a database string, return a database cursor."""
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
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

        # Create the media_metadata table
        self.cursor.execute('''
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
        self.conn.commit()

    def __del__(self):
        """Destructor for DatabaseQuery class."""
        self.conn.close()

    def getMediaEntrybyId(self, entryId: int) -> DataClass.MediaEntry:
        """Given a Media Entry ID, return the row associated with the ID.

        :param entryId ID for row in MediaEntry table
        """
        ret = self.cursor.execute(
            "SELECT * from media_entry WHERE entryId = ?",
            (entryId, )).fetchone()
        ret = DataClass.MediaEntry(ret[0], ret[1], ret[2], ret[3], ret[4],
                                   ret[5], ret[6], ret[7])
        return ret

    def getMediaMetadatabyId(self, metadataId: int) -> DataClass.MediaMetadata:
        """Given a Media Metadata ID, return the row associated with the ID.

        :param metadataId ID for row in MediaMetadata table.
        """
        ret = self.cursor.execute(
            "Select * from media_metadata WHERE metadataId = ?",
            (metadataId, )).fetchone()
        ret = DataClass.MediaMetadata(ret[0], ret[1], ret[2], ret[3], ret[4],
                                      ret[5], ret[6], ret[7], ret[8])
        return ret

    def getAllMediaMetadaByEntryId(self,
                                   entryId: int) -> [DataClass.MediaMetadata]:
        """Given an entryId, will return all associated MediaMetadata.

        :param entryId ID for row in MediaEntry table
        """
        ret = self.cursor.execute(
            "SELECT * FROM media_metadata WHERE entryId = ?",
            (entryId, )).fetchall()
        ret = list(
            map(
                lambda x: DataClass.MediaMetadata(x[0], x[1], x[2], x[3], x[4],
                                                  x[5], x[6], x[7], x[8]),
                ret,
            ))
        return ret

    def insertMediaEntry(
        self,
        shotType: str,
        time: str,
        illuminationType: str,
        gain: float,
        saturation: int,
        shutterSpeed: str,
        whiteBalance: int,
    ) -> int:
        """Insert MediaEntry table entry into database.

        :param shotType Shot Type for MediaEntry.
        Should be either: "SINGLE", "BURST", "TIMELAPSE", "TELESCOPIC" or
        "VIDEO".
        :param time Time stamp for the MediaMetadata Entry.
        :param illuminationType Illumination Type for MediaEntry
        Should be either "NONE", "WHITE", "RED", "ULTRAVIOLET".
        :param gain The gain value for the camera.
        Should be within camera parameters.
        :param shutterSpeed The shutter speed value for the camera.
        Should be within camera parameters.
        :param whiteBalance The white balance (or color temperature) value for
        the camera.
        Should be within camera parameters.

        :return The row id of the newly inserted MediaEntry.
        """
        self.cursor.execute(
            """INSERT INTO media_entry
            (shotType, time, illuminationType, gain, saturation, shutterSpeed,
            whiteBalance) VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                shotType,
                time,
                illuminationType,
                gain,
                saturation,
                shutterSpeed,
                whiteBalance,
            ),
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def insertMediaMetadata(
        self,
        entryId: int,
        path: str,
        extension: str,
        time: str,
        temperature: float,
        pressure: float,
        ph: float,
        dissolvedOxygen: float,
    ) -> int:
        """Insert MediaMetadata table entry into database.

        :param entryId The id for the MediaEntry table entry.
        This is associated with the MediaMetadata table as a foreign key.
        :param path Path to the folder where the Media Metadata
        will be created.
        :param extension The file extension for the created media
        :param time Time stamp for the MediaMetadata Entry
        :param temperature Temperature of the environment in Celsius
        :param pressure Pressure of the environment in mbar
        :param ph pH of the environment
        :param dissolvedOxygen Dissolved oxygen of the
        environment in mg/L

        :return The row id of the newly inserted MediaMetadata.
        """
        # Looks for the most recent metadataId from the table
        # and adds one to it
        self.cursor.execute("SELECT MAX(metadataId) FROM media_metadata")
        result = self.cursor.fetchone()
        if result[0] is not None:
            metadataId = result[0] + 1
        else:
            metadataId = 1
        # The recent most recent metadataId is then added to the string name of
        # the left and right camera media path
        leftCameraMedia = os.path.join(
            path,
            "{}-{}-{}-{}-{}-{}-{}-L.{}".format(entryId, metadataId, time,
                                               temperature, pressure, ph,
                                               dissolvedOxygen, extension),
        )
        rightCameraMedia = os.path.join(
            path,
            "{}-{}-{}-{}-{}-{}-{}-R.{}".format(entryId, metadataId, time,
                                               temperature, pressure, ph,
                                               dissolvedOxygen, extension),
        )
        self.cursor.execute(
            """INSERT INTO media_metadata
            (entryId, leftCameraMedia, rightCameraMedia, time, temperature,
            pressure, ph, dissolvedOxygen)
            Values (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                entryId,
                leftCameraMedia,
                rightCameraMedia,
                time,
                temperature,
                pressure,
                ph,
                dissolvedOxygen,
            ),
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def getAllMediaEntry(self) -> [str]:
        """Get all Media Entries from the media_entry table.

        :return A list of the string representation for
        all Media Entries in the database.
        """
        ret = self.conn.execute("Select * from media_entry").fetchall()
        ret = list(
            map(
                lambda x: DataClass.MediaEntry(x[0], x[1], x[2], x[3], x[4], x[
                    5], x[6], x[7]),
                ret,
            ))
        ret = list(map(lambda x: str(x), ret))
        return ret
