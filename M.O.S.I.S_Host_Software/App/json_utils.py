import json
from models import db
from query import getMediaEntry, getAllMediaMetadataId


class MediaEntryJSONRepresentation():
    """Class to convert MediaEntry with metadata to JSON."""

    def __init__(self, id: int):
        """Construct MediaEntry JSON representation."""
        self.MediaEntry = getMediaEntry(db, id).__dict__
        self.MediaMetadata = list(
            map(lambda x: x.__dict__, getAllMediaMetadataId(db, id)))

    def intoJSON(self) -> str:
        """Return JSON representation of self."""
        return json.dumps(self.__dict__, indent=4)


def fromJSON(path: str) -> MediaEntryJSONRepresentation:
    jf = openMediaEntryJSON(path)
    jf = json.loads(jf)
    return MediaEntryJSONRepresentation(jf["MediaEntry"]["entryId"])


def writeMediaEntryJSON(json: str, path: str):
    f = open(path, "w")
    f.write(json)
    f.close()


def openMediaEntryJSON(path: str) -> str:
    f = open(path, "r")
    ret = f.read()
    f.close()
    return ret
