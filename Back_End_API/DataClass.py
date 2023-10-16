class MediaEntry():
    # Defines the media entry class for the Media Entry table
    def __init__(self, entry_Id: int, shot_Type: str, time: str, illumination_Type: str, iso: int,
                 aperture_Size: float, shutter_Speed: float, white_Balance: int):
        self.entry_Id = entry_Id
        self.shot_Type = shot_Type
        self.time = time
        self.illumination_Type = illumination_Type
        self.iso = iso
        self.aperture_Size = aperture_Size
        self.shutter_Speed = shutter_Speed
        self.white_Balance = white_Balance

    # Creates a new media entry
    @staticmethod
    def media_entry(shot_Type: str, time: str, illumination_Type: str, iso: int,
                    aperture_Size: float, shutter_Speed: float, white_Balance: int):
        shot_Type = shot_Type
        time = time
        illumination_Type = illumination_Type
        iso = iso
        aperture_Size = aperture_Size
        shutter_Speed = shutter_Speed
        white_Balance = white_Balance
        return shot_Type, time, illumination_Type, aperture_Size, iso, shutter_Speed, white_Balance


class MediaMetadata():
    # Defines the media metadata class for the Media Metadata table
    def __init__(self, media_Id: int, entry_Id: int, left_Camera_Media: str, right_Camera_Media: str, time: str,
                 temperature: float,
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
    def mediadata( left_Camera_Media: str, right_Camera_Media: str, time: str,
                  temperature: float,
                  pressure: float, ph: float, dissolved_Oxygen: float):
        left_Camera_Media = left_Camera_Media
        right_Camera_Media = right_Camera_Media
        time = time
        temperature = temperature
        pressure = pressure
        ph = ph
        dissolved_Oxygen = dissolved_Oxygen
        return left_Camera_Media, right_Camera_Media, time, temperature, pressure, ph, dissolved_Oxygen
