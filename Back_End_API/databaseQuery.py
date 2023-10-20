import sqlite3
import os
import DataClass


class DatabaseQuery:
    def __init__(self, db: str = "testing3.db"):
        """Given a database string, return a database cursor."""
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def getMediaEntrybyId(self, entryId: int) -> DataClass.MediaEntry:
        """Given a Media Entry ID, return the row associated with the ID."""
        ret = self.cursor.execute(
            "SELECT * from media_entry WHERE entryId = ?", (entryId,)
        ).fetchone()
        ret = DataClass.MediaEntry(
            ret[0], ret[1], ret[2], ret[3], ret[4], ret[5], ret[6], ret[7]
        )
        return ret

    def getAllMediaMetadaByEntryId(self, entryId: int) -> DataClass.MediaMetadata:
        ret = self.cursor.execute(
            "SELECT * FROM media_metadata WHERE entryId = ?", (entryId,)
        ).fetchall()
        ret = list(
            map(
                lambda x: DataClass.MediaMetadata(
                    x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8]
                ),
                ret,
            )
        )
        return ret

    def insertMediaEntry(
        self,
        shotType: str,
        time: str,
        illuminationType: str,
        gain: float,
        saturation: int,
        shutterSpeed: float,
        whiteBalance: int,
    ) -> int:
        self.cursor.execute(
            "INSERT INTO media_entry (shotType, time, illuminationType, gain, saturation, shutterSpeed, "
            "whiteBalance) VALUES (?, ?, ?, ?, ?, ?, ?)",
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
        mediaEntry = self.getMediaEntrybyId(entryId)
        leftCameraMedia = os.path.join(
            path,
            str(mediaEntry),
            "{}-{}-{}-{}-{}-{}-L.{}".format(
                entryId, time, temperature, pressure, ph, dissolvedOxygen, extension
            ),
        )
        rightCameraMedia = os.path.join(
            path,
            str(mediaEntry),
            "{}-{}-{}-{}-{}-{}-R.{}".format(
                entryId, time, temperature, pressure, ph, dissolvedOxygen, extension
            ),
        )
        self.cursor.execute(
            "INSERT INTO media_metadata (entryId, leftCameraMedia, rightCameraMedia, time, temperature, pressure, ph, dissolvedOxygen) "
            "Values (?, ?, ?, ?, ?, ?, ?, ?)",
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
