from enums import illuminationType, shotType


class MediaEntryInternalRepresentation():
    """Internal representation for MediaEntry."""

    def __init__(self, entryId: int, shotType: shotType, time: str,
                 illuminationType: illuminationType, saturation: int,
                 gain: float, shutterSpeed: float, whiteBalance: int):
        """Construct w."""
        self.entryId = entryId
        self.shotType = shotType
        self.time = time
        self.illuminationType = illuminationType
        self.saturation = saturation
        self.gain = gain
        self.shutterSpeed = shutterSpeed
        self.whiteBalance = whiteBalance

    def __str__(self):
        """Text representation for MediaEntry."""
        return "{}-{}-{}-{}-{}-{}-{}-{}".format(
            self.entryId, self.shotType, self.time, self.illuminationType,
            self.saturation, self.gain, self.shutterSpeed, self.whiteBalance)


class MediaMetadataInternalRepresentation:
    """Internal representation for a MediaMetadata entry."""

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

    def __str__(self):
        return "{}-{}-{}-{}-{}-{}-{}-{}-{}".format(
            self.metadataId,
            self.entryId,
            self.leftCameraMedia,
            self.rightCameraMedia,
            self.time,
            self.temperature,
            self.pressure,
            self.ph,
            self.dissolvedOxygen,
        )
