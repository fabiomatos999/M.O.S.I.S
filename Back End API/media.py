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

    #Creates a new media entry
    @staticmethod
    def create_new_media_entry(shot_Type, time, illumination_Type, iso,
                 aperture_Size, shutter_Speed, white_Balance):
        shot_Type = shot_Type
        time = time
        illumination_Type = illumination_Type
        iso = iso
        aperture_Size = aperture_Size
        shutter_Speed = shutter_Speed
        white_Balance = white_Balance

class media_Metadata():
    # Defines the media metadata class for the Media Metadata table
    def __init__(self, media_Id, entry_Id, left_Camera_Media, right_Camera_Media, time, temperature,
                 pressure, ph, dissolved_Oxygen):
        self.media_Id = media_Id
        self.entry_Id = entry_Id
        self.left_Camera_Media = left_Camera_Media
        self.right_Camera_Media = right_Camera_Media
        self.time = time
        self.temperature = temperature
        self.pressure = pressure
        self.ph = ph
        self.dissolved_Oxygen = dissolved_Oxygen

    #Creates new mediadata entry
    @staticmethod
    def create_new_mediadata( entry_Id, left_Camera_Media, right_Camera_Media, time, temperature,
                 pressure, ph, dissolved_Oxygen):
        entry_Id = entry_Id
        left_Camera_Media = left_Camera_Media
        right_Camera_Media = right_Camera_Media
        time = time
        temperature = temperature
        pressure = pressure
        ph = ph
        dissolved_Oxygen = dissolved_Oxygen