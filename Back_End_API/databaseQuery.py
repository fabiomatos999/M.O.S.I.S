import sqlite3
import os
import DataClass


class DatabaseQuery():

    def __init__(self, db: str = "testing3.db"):
        """Given a database string, return a database cursor."""
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor()

    def selectMediaEntrybyId(self, entryId: int) -> DataClass.MediaEntry:
        """Given a Media Entry ID, return the row associated with the ID."""
        ret = self.cursor.execute(
            'SELECT * from media_entry WHERE entryId = ?',
            (entryId, )).fetchone()
        ret = DataClass.MediaEntry(ret[0], ret[1], ret[2], ret[3], ret[4],
                                   ret[5], ret[6], ret[7])
        return ret

    def getAllMediaMetadaByEntryId(self,
                                   entryId: int) -> DataClass.MediaMetadata:
        ret = self.cursor.execute(
            'SELECT * FROM media_metadata WHERE entryId = ?',
            (entryId, )).fetchall()
        ret = list(
            map(
                lambda x: DataClass.MediaMetadata(x[0], x[1], x[2], x[3], x[
                    4], x[5], x[6], x[7], x[8]), ret))
        return ret
