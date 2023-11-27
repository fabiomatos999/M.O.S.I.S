"""Internal representation of MediaEntry and MediaMetadata tables."""
import json


class MediaEntry:
    """Internal representation for MediaEntry database table."""

    def __init__(
        self,
        entry_Id: int,
        shot_Type: str,
        time: str,
        illumination_Type: str,
        gain: float,
        saturation: int,
        shutter_Speed: str,
        white_Balance: int,
    ):
        """Create MediaEntry object.

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
        """
        self.entry_Id = entry_Id
        self.shot_Type = shot_Type
        self.time = time
        self.illumination_Type = illumination_Type
        self.gain = gain
        self.saturation = saturation
        self.shutter_Speed = shutter_Speed
        self.white_Balance = white_Balance

    # Creates a new media entry
    @staticmethod
    def media_entry(
        shot_Type: str,
        time: str,
        illumination_Type: str,
        gain: float,
        saturation: int,
        shutter_Speed: str,
        white_Balance: int,
    ) -> (str, str, str, float, int, str, int):
        """Create a tuple from a MediaEntry fields.

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
        """
        return (
            shot_Type,
            time,
            illumination_Type,
            saturation,
            gain,
            shutter_Speed,
            white_Balance,
        )

    def __str__(self):
        """Str representation of a MediaEntry."""
        return "{}-{}-{}-{}-{}-{}-{}-{}".format(
            self.entry_Id,
            self.shot_Type,
            self.time,
            self.illumination_Type,
            self.gain,
            self.saturation,
            self.shutter_Speed,
            self.white_Balance,
        )

    def intoJSON(self) -> str:
        """Convert MediaEntry into JSON."""
        return json.dumps(self.__dict__, indent=4)


class MediaMetadata:
    """Internal representation for MediaMetadata database table."""

    def __init__(
        self,
        media_Id: int,
        entry_Id: int,
        left_Camera_Media: str,
        right_Camera_Media: str,
        time: str,
        temperature: float,
        pressure: float,
        ph: float,
        dissolved_Oxygen: float,
    ):
        """
        Define the media metadata class for the Media Metadata table.

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
        """
        self.media_Id = media_Id
        self.entry_Id = entry_Id
        self.left_Camera_Media = left_Camera_Media
        self.right_Camera_Media = right_Camera_Media
        self.time = time
        self.temperature = temperature
        self.pressure = pressure
        self.ph = ph
        self.dissolved_Oxygen = dissolved_Oxygen

    # Creates new media metadata entry
    @staticmethod
    def mediadata(
        left_Camera_Media: str,
        right_Camera_Media: str,
        time: str,
        temperature: float,
        pressure: float,
        ph: float,
        dissolved_Oxygen: float,
    ) -> (str, str, str, float, float, float, float):
        """Str representation of a MediaEntry.

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
        """
        left_Camera_Media = left_Camera_Media
        right_Camera_Media = right_Camera_Media
        time = time
        temperature = temperature
        pressure = pressure
        ph = ph
        dissolved_Oxygen = dissolved_Oxygen
        return (
            left_Camera_Media,
            right_Camera_Media,
            time,
            temperature,
            pressure,
            ph,
            dissolved_Oxygen,
        )

    def __str__(self):
        """Str representation of a MediaMetadata."""
        return "{}-{}-{}-{}-{}-{}-{}-{}-{}".format(
            self.media_Id,
            self.entry_Id,
            self.left_Camera_Media,
            self.right_Camera_Media,
            self.time,
            self.temperature,
            self.pressure,
            self.ph,
            self.dissolved_Oxygen,
        )

    def intoJSON(self) -> str:
        """Convert MediaMetadata into JSON."""
        return json.dumps(self.__dict__, indent=4)
