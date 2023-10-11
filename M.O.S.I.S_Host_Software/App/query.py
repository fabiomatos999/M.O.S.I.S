"""Query Abstraction functions for SQLite database."""
from representations import MediaEntryInternalRepresentation
from representations import MediaMetadataInternalRepresentation
from models import MediaEntry, MediaMetadata
from sqlalchemy import select, desc, asc
from datetime import datetime
from enums import shotType, illuminationType


def getCurrentTime() -> str:
    """Return current time in 'yyyy-MM-ddTHH:mm:ss.zzz' format."""
    date = datetime.now()
    return date.strftime('%Y-%m-%-dT%H:%M:%S.%f')


def insertMediaEntry(db, shotType, illuminationType, iso, apertureSize,
                     shutterSpeed, whiteBalance):
    """Insert a MediaEntry into the database."""
    new_entry = MediaEntry(shotType=str(shotType),
                           time=getCurrentTime(),
                           illuminationType=str(illuminationType),
                           iso=iso,
                           apertureSize=apertureSize,
                           shutterSpeed=shutterSpeed,
                           whiteBalance=whiteBalance)
    db.session.add(new_entry)
    db.session.commit()


def getMediaEntry(db, id: int) -> MediaEntryInternalRepresentation:
    """Get MediaEntry where entryId == id."""
    ret = db.session.execute(
        select(MediaEntry).where(MediaEntry.entryId == id)).first()
    return MediaEntryInternalRepresentation(ret[0].entryId, ret[0].shotType,
                                            ret[0].time,
                                            ret[0].illuminationType,
                                            ret[0].iso, ret[0].apertureSize,
                                            ret[0].shutterSpeed,
                                            ret[0].whiteBalance)


def getAllMediaEntryIDs(db):
    """Get all entryId from database."""
    dbReturn = list(db.session.execute(select(MediaEntry.entryId)))
    return list(map(lambda x: x[0], dbReturn))


def getAllMediaEntry(db) -> list[MediaEntryInternalRepresentation]:
    """Get all Media Entries from a database."""
    ret = list(db.session.execute(select(MediaEntry)))
    ret = list(
        map(
            lambda x: MediaEntryInternalRepresentation(x[0].entryId, x[
                0].shotType, x[0].time, x[0].illuminationType, x[0].iso, x[
                    0].apertureSize, x[0].shutterSpeed, x[0].whiteBalance),
            ret))
    return ret


def insertMediaMetadata(db, entryId, leftCameraMedia, rightCameraMedia,
                        temperature, pressure, ph, dissolvedOxygen):
    """Insert MediaMetadata entry into database."""
    new_metadata = MediaMetadata(entryId=entryId,
                                 leftCameraMedia=leftCameraMedia,
                                 rightCameraMedia=rightCameraMedia,
                                 time=getCurrentTime(),
                                 temperature=temperature,
                                 pressure=pressure,
                                 ph=ph,
                                 dissolvedOxygen=dissolvedOxygen)
    db.session.add(new_metadata)
    db.session.commit()


def getAllMediaMetadataId(
        db, entryId: int) -> list[MediaMetadataInternalRepresentation]:
    """Get all MediaMetadata with a specific entry ID from a database."""
    ret = list(
        db.session.execute(
            select(MediaMetadata).where(MediaMetadata.entryId == entryId)))
    ret = list(
        map(
            lambda x: MediaMetadataInternalRepresentation(
                x[0].metadataId, x[0].entryId, x[0].leftCameraMedia, x[0].
                rightCameraMedia, x[0].time, x[0].temperature, x[0].ph, x[
                    0].dissolvedOxygen, x[0].pressure), ret))
    return ret


def getAllMediaMetadata(db) -> list[MediaMetadataInternalRepresentation]:
    """Get all MediaMetadata entries from a database."""
    ret = list(db.session.execute(select(MediaMetadata)))
    ret = list(
        map(
            lambda x: MediaMetadataInternalRepresentation(
                x[0].metadataId, x[0].entryId, x[0].leftCameraMedia, x[0].
                rightCameraMedia, x[0].time, x[0].temperature, x[0].ph, x[
                    0].dissolvedOxygen, x[0].pressure), ret))
    return ret


def getFirstMediaEntry(db) -> int:
    """Get the minimum entryId from a database."""
    ret = db.session.execute(
        select(MediaEntry.entryId).order_by(asc(
            MediaEntry.entryId)).limit(1)).first()
    return int(ret[0])


def getLastMediaEntry(db) -> int:
    """Get the maximum entryId from a database."""
    ret = db.session.execute(
        select(MediaEntry.entryId).order_by(desc(
            MediaEntry.entryId)).limit(1)).first()
    return int(ret[0])


def getMediaEntriesById(db,
                        entryIDs: [int]) -> [MediaEntryInternalRepresentation]:
    """Get a list of media entries given a list of entry IDs."""
    returnMediaEntries = []
    for id in entryIDs:
        returnMediaEntries.append(getMediaEntry(db, id))
    return returnMediaEntries


def getMediaEntriesByShotType(
        db, shotType: shotType) -> [MediaEntryInternalRepresentation]:
    """Get a list of media entries given a shot type."""
    ret = db.session.execute(
        select(MediaEntry).where(MediaEntry.shotType == shotType.name))
    ret = list(
        map(
            lambda x: MediaEntryInternalRepresentation(x[0].entryId, x[
                0].shotType, x[0].time, x[0].illuminationType, x[0].iso, x[
                    0].apertureSize, x[0].shutterSpeed, x[0].whiteBalance),
            ret))
    return ret


def getMediaEntriesByTime(db, time: str) -> [MediaEntryInternalRepresentation]:
    """Get a list of media entries by Time stamp."""
    ret = db.session.execute(
        select(MediaEntry).where(MediaEntry.time.like("%{}%".format(time))))
    ret = list(
        map(
            lambda x: MediaEntryInternalRepresentation(x[0].entryId, x[
                0].shotType, x[0].time, x[0].illuminationType, x[0].iso, x[
                    0].apertureSize, x[0].shutterSpeed, x[0].whiteBalance),
            ret))
    return ret


def getMediaEntriesByIlluminationType(
        db, illuminationType: illuminationType
) -> [MediaEntryInternalRepresentation]:
    """Get a list of media entries given a illumination type."""
    ret = db.session.execute(
        select(MediaEntry).where(
            MediaEntry.illuminationType == illuminationType.name))
    ret = list(
        map(
            lambda x: MediaEntryInternalRepresentation(x[0].entryId, x[
                0].shotType, x[0].time, x[0].illuminationType, x[0].iso, x[
                    0].apertureSize, x[0].shutterSpeed, x[0].whiteBalance),
            ret))
    return ret
