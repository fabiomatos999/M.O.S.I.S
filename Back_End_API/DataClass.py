import json


class MediaEntry():
    # Defines the media entry class for the Media Entry table
    def __init__(self, entry_Id: int, shot_Type: str, time: str,
                 illumination_Type: str, gain: int, saturation: float,
                 shutter_Speed: float, white_Balance: int):
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
    def media_entry(shot_Type: str, time: str, illumination_Type: str,
                    gain: float, saturation: int, shutter_Speed: float,
                    white_Balance: int):
        shot_Type = shot_Type
        time = time
        illumination_Type = illumination_Type
        gain = gain
        saturation = saturation
        shutter_Speed = shutter_Speed
        white_Balance = white_Balance
        return shot_Type, time, illumination_Type, saturation, gain, shutter_Speed, white_Balance

    def __str__(self):
        return "{}-{}-{}-{}-{}-{}-{}-{}".format(
            self.entry_Id, self.shot_Type, self.time, self.illumination_Type,
            self.gain, self.saturation, self.shutter_Speed, self.white_Balance)

    def intoJSON(self) -> str:
        return json.dumps(self.__dict__, indent=4)


class MediaMetadata():
    # Defines the media metadata class for the Media Metadata table
    def __init__(self, media_Id: int, entry_Id: int, left_Camera_Media: str,
                 right_Camera_Media: str, time: str, temperature: float,
                 pressure: float, ph: float, dissolved_Oxygen: float):
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
    def mediadata(left_Camera_Media: str, right_Camera_Media: str, time: str,
                  temperature: float, pressure: float, ph: float,
                  dissolved_Oxygen: float):
        left_Camera_Media = left_Camera_Media
        right_Camera_Media = right_Camera_Media
        time = time
        temperature = temperature
        pressure = pressure
        ph = ph
        dissolved_Oxygen = dissolved_Oxygen
        return left_Camera_Media, right_Camera_Media, time, temperature, pressure, ph, dissolved_Oxygen

    def __str__(self):
        return "{}-{}-{}-{}-{}-{}-{}-{}-{}".format(
            self.media_Id, self.entry_Id, self.left_Camera_Media,
            self.right_Camera_Media, self.time, self.temperature,
            self.pressure, self.ph, self.dissolved_Oxygen)

    def intoJSON(self) -> str:
        return json.dumps(self.__dict__, indent=4)
