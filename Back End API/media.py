class media_Entry():
    # Defines the media entry class for the Media Entry table
    def __init__(self, entry_Id, shot_Type, time, illumination_Type, iso,
                 aperture_Size, shutter_Speed, white_Balance):
        self.entry_Id = entry_Id
        self.shot_Type = shot_Type
        self.time = time
        self.illumination_Type = illumination_Type
        self.iso = iso
        self.aperture_Size = aperture_Size
        self.shutter_Speed = shutter_Speed
        self.white_Balance = white_Balance


class media_Metadata():
    # Defines the media metadata class for the Media Metadata table
    def __init__(self, entry_Id, left_Camera_Media, right_Camera_Media, time, temperature,
                 pressure, ph, dissolved_Oxygen):
        self.entry_Id = entry_Id
        self.left_Camera_Media = left_Camera_Media
        self.right_Camera_Media = right_Camera_Media
        self.time = time
        self.temperature = temperature
        self.pressure = pressure
        self.ph = ph
        self.dissolved_Oxygen = dissolved_Oxygen
