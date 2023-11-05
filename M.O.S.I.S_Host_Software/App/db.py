"""Database interaction module."""
import sqlite3
from enums import illuminationType, shotType
from representations import MediaEntryInternalRepresentation, \
    MediaMetadataInternalRepresentation
import re
import os


class DatabaseQuery:
    """Database query class used to interact with the db and create tables."""

    def __init__(self, db: str = "test.db"):
        """Create db tables and gives a db connection and cursor."""
        self.conn = sqlite3.connect('test.db', check_same_thread=False)
        self.cursor = self.conn.cursor()
        # Create MediaEntry table if not exists
        self.cursor.execute('''
    CREATE TABLE IF NOT EXISTS MediaEntry (
        entryId INTEGER PRIMARY KEY UNIQUE,
        shotType TEXT NOT NULL,
        time TEXT NOT NULL ,
        illuminationType TEXT NOT NULL,
        gain REAL NOT NULL,
        saturation INTEGER NOT NULL,
        shutterSpeed TEXT NOT NULL,
        whiteBalance INTEGER NOT NULL
    )
''')
        # Create MediaMetadata table if not exists
        self.cursor.execute('''
    CREATE TABLE IF NOT EXISTS MediaMetadata (
        metadataId INTEGER PRIMARY KEY UNIQUE,
        entryId INTEGER,
        leftCameraMedia TEXT NOT NULL,
        rightCameraMedia TEXT NOT NULL,
        time TEXT NOT NULL,
        temperature REAL NOT NULL,
        pressure REAL NOT NULL,
        ph REAL NOT NULL,
        dissolvedOxygen REAL NOT NULL,
        grayscaleLeftMedia TEXT NOT NULL,
        grayscaleRightMedia TEXT NOT NULL,
        stereoMedia TEXT NOT NULL,
        taggedMedia TEXT NOT NULL,
        FOREIGN KEY (entryId) REFERENCES media_entry(entryId)
    )
''')
        self.conn.commit()

    def __del__(self):
        """Close db connection when object is destroyed."""
        self.conn.close()

    def insertMediaEntry(self, entryId: int, shottype: shotType, time: str,
                         illuminationtype: illuminationType, gain: float,
                         saturation: int, shutterSpeed: str,
                         whiteBalance: int):
        self.cursor.execute(
            """INSERT INTO MediaEntry
            (entryId, shotType, time,
            illuminationType, gain, saturation, shutterSpeed, whiteBalance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (entryId, shottype.name, time, illuminationtype.name, gain,
             saturation, shutterSpeed, whiteBalance))
        self.conn.commit()

    def getMediaEntry(self, entryId: int) -> MediaEntryInternalRepresentation:
        ret = self.cursor.execute("SELECT * FROM MediaEntry WHERE entryId = ?",
                                  (entryId, )).fetchone()
        return DatabaseQuery.mediaEntryTableToInternalRepresentation(ret)

    def getAllMediaEntryIDs(self) -> [int]:
        ret = self.cursor.execute("SELECT entryId FROM MediaEntry").fetchall()
        return list(map(lambda x: x[0], ret))

    def getMediaEntriesById(
            self, entryIDs: [int]) -> [MediaEntryInternalRepresentation]:
        """Get a list of media entries given a list of entry IDs."""
        returnMediaEntries = []
        for id in entryIDs:
            returnMediaEntries.append(self.getMediaEntry(id))
        return returnMediaEntries

    def getAllMediaEntry(self) -> [MediaEntryInternalRepresentation]:
        ret = self.cursor.execute("SELECT * FROM MediaEntry").fetchall()
        return list(
            map(
                lambda x: DatabaseQuery.
                mediaEntryTableToInternalRepresentation(x), ret))

    def insertMediaMetadata(self, metadataId: int, entryId: int,
                            leftCameraMedia: str, rightCameraMedia, time: str,
                            temperature: float, pressure: float, ph: float,
                            dissolvedOxygen: float, grayscaleLeftMedia: str,
                            grayscaleRightMedia: str, stereoMedia: str,
                            taggedMedia: str):
        self.cursor.execute(
            """INSERT INTO MediaMetadata
            (metadataId, entryId, leftCameraMedia,
            rightCameraMedia, time, temperature,
            pressure, ph, dissolvedOxygen,
            grayscaleLeftMedia, grayscaleRightMedia,
            stereoMedia, taggedMedia)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (metadataId, entryId, leftCameraMedia, rightCameraMedia, time,
             temperature, pressure, ph, dissolvedOxygen, grayscaleLeftMedia,
             grayscaleRightMedia, stereoMedia, taggedMedia))
        self.conn.commit()

    def getMediaMetadataByMetadataId(
            self, metadataId: int) -> MediaMetadataInternalRepresentation:
        ret = self.cursor.execute(
            "SELECT * FROM MediaMetadata WHERE metadataId = ?",
            (metadataId, )).fetchone()
        return DatabaseQuery.mediaMetadataTableToInternalRepresentation(ret)

    def getAllMediaMetadataId(
            self, entryId: int) -> [MediaMetadataInternalRepresentation]:
        ret = self.cursor.execute(
            "SELECT * FROM MediaMetadata WHERE entryId = ?",
            (entryId, )).fetchall()
        return list(
            map(
                lambda x: DatabaseQuery.
                mediaMetadataTableToInternalRepresentation(x), ret))

    def getAllMediaMetadata(self) -> [MediaMetadataInternalRepresentation]:
        ret = self.cursor.execute("SELECT * FROM MediaMetadata").fetchall()
        return list(
            map(
                lambda x: DatabaseQuery.
                mediaMetadataTableToInternalRepresentation(x), ret))

    def getFirstMediaEntry(self) -> int:
        ret = self.cursor.execute(
            """SELECT entryId FROM MediaEntry ORDER BY entryId ASC LIMIT 1"""
        ).fetchone()
        return int(ret[0])

    def getLastMediaEntry(self) -> int:
        ret = self.cursor.execute(
            """SELECT entryId FROM MediaEntry ORDER BY entryId DESC LIMIT 1"""
        ).fetchone()
        return int(ret[0])

    def getFirstMediaMetadata(self) -> int:
        ret = self.cursor.execute(
            """SELECT metadataId FROM MediaMetadata ORDER BY metadataId ASC LIMIT 1"""
        ).fetchone()
        return int(ret[0])

    def getLastMediaMetadata(self) -> int:
        ret = self.cursor.execute(
            """SELECT metadataId FROM MediaMetadata ORDER BY metadataId DESC LIMIT 1"""
        ).fetchone()
        return int(ret[0])

    def getMediaEntriesByShotType(
            self, shottype: str) -> [MediaEntryInternalRepresentation]:
        ret = self.cursor.execute(
            "SELECT * FROM MediaEntry WHERE shotType = ?", (shottype, ))
        return list(
            map(
                lambda x: DatabaseQuery.
                mediaEntryTableToInternalRepresentation(x), ret))

    def getMediaEntriesByTime(self,
                              time: str) -> [MediaEntryInternalRepresentation]:
        ret = self.cursor.execute(
            "SELECT * FROM MediaEntry WHERE time LIKE %?%", time)
        return list(
            map(
                lambda x: DatabaseQuery.
                mediaEntryTableToInternalRepresentation(x), ret))

    def getMediaEntriesByIlluminationType(
            self, illuminationtype: str) -> [MediaEntryInternalRepresentation]:
        ret = self.cursor.execute(
            "SELECT * FROM MediaEntry WHERE illuminationType = ?",
            (illuminationtype, ))
        return list(
            map(
                lambda x: DatabaseQuery.
                mediaEntryTableToInternalRepresentation(x), ret))

    @staticmethod
    def mediaEntryTableToInternalRepresentation(dbQuery: (
    )) -> MediaEntryInternalRepresentation:
        return MediaEntryInternalRepresentation(dbQuery[0], dbQuery[1],
                                                dbQuery[2], dbQuery[3],
                                                dbQuery[4], dbQuery[5],
                                                dbQuery[6], dbQuery[7])

    def mediaMetadataTableToInternalRepresentation(dbQuery: (
    )) -> MediaMetadataInternalRepresentation:
        return MediaMetadataInternalRepresentation(
            dbQuery[0], dbQuery[1], dbQuery[2], dbQuery[3], dbQuery[4],
            dbQuery[5], dbQuery[6], dbQuery[7], dbQuery[8], dbQuery[9],
            dbQuery[10], dbQuery[11], dbQuery[12])

    def parseIdRange(self, searchQuery: str) -> [int]:
        dualEndedRangeRegex = r'^\d+-\d+$'
        leftEndedRangeragex = r'^\d+-$'
        rightEndedRangeRegex = r'^-\d+$'
        commaSeparatedValueRegex = r'^(\d+,)+\d+$'
        singleValueRagex = r'^\d+$'
        dbMin = self.getFirstMediaEntry()
        dbMax = self.getLastMediaEntry()
        entries = set()
        left = int()
        right = int()

        def returnRange(left: int, right: int, dbMin: int,
                        dbMax: int) -> [int]:
            if left > right:
                temp = left
                left = right
                right = temp
                if left < dbMin:
                    left = dbMin
                    if right > dbMax:
                        right = dbMax
            return list(range(left, right + 1, 1))

        for query in searchQuery.split(" "):
            if bool(re.search(dualEndedRangeRegex, query)):
                left = int(query.split('-')[0])
                right = int(query.split('-')[-1])
                for i in returnRange(left, right, dbMin, dbMax):
                    entries.add(int(i))
            elif bool(re.search(leftEndedRangeragex, query)):
                left = int(query.split('-')[0])
                right = dbMax
                for i in returnRange(left, right, dbMin, dbMax):
                    entries.add(int(i))
            elif bool(re.search(rightEndedRangeRegex, query)):
                left = dbMin
                right = int(query.split('-')[-1])
                for i in returnRange(left, right, dbMin, dbMax):
                    entries.add(int(i))
            elif bool(re.search(commaSeparatedValueRegex, query)):
                values = query.split(',')
                for i in values:
                    entries.add(int(i))
            elif bool(re.search(singleValueRagex, query)):
                entries.add(int(query))
                entries = list(
                    filter(lambda x: x >= dbMin and x <= dbMax, entries))
                entries.sort()
            entryIds = self.getAllMediaEntryIDs()
            entries = list(filter(lambda x: entryIds.__contains__(x) , entries))
            return entries
