class MediaEntryInternalRepresentation():
    """Internal representation for MediaEntry."""

    entryId = int()
    shotType = None
    time = str()
    illuminationType = None
    iso = int()
    apertureSize = float()
    shutterSpeed = float()
    whiteBalance = float()

    def __init__(self, entryId: int, shotType: shotType, time: str,
                 illuminationType: illuminationType, iso: int,
                 apertureSize: float, shutterSpeed: float, whiteBalance: int):
        """Construct MediaEntryInternalRepesentation."""
        self.entryId = entryId
        self.shotType = shotType
        self.time = time
        self.illuminationType = illuminationType
        self.iso = iso
        self.apertureSize = apertureSize
        self.shutterSpeed = shutterSpeed
        self.whiteBalance = whiteBalance


class MediaMetadataInternalRepresentation:
    """Internal representation for a MediaMetadata entry."""

    metadataId = int()
    entryId = int()
    leftCameraMedia = str()
    rightCameraMedia = str()
    time = str()
    temperature = float()
    pressure = float()
    ph = float()
    dissolvedOxygen = float()

    def __init__(self, metadataId: int, entryId: int, leftCameraMedia: str,
                 rightCameraMedia: str, time: str, temperature: float,
                 ph: float, dissolvedOxygen: float, pressure: float):
        """Construct MediaMetadataInternalRepresentation."""
        self.metadataId = metadataId
        self.entryId = entryId
        self.leftCameraMedia = leftCameraMedia
        self.rightCameraMedia = rightCameraMedia
        self.time = time
        self.temperature = temperature
        self.ph = ph
        self.dissolvedOxygen = dissolvedOxygen
        self.pressure = pressure
