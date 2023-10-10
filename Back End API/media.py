class media_entry():
  # Defines the media entry class for the Media Entry table
    def __init__(self, entry_id, shot_type, time, illumination_type, iso, aperture_size, shutter_speed, white_balance):
        self.entry_id = entry_id
        self.shot_type = shot_type
        self.time = time
        self.illumination_type = illumination_type
        self.iso = iso
        self.aperture_size = aperture_size
        self.shutter_speed = shutter_speed
        self.white_balance = white_balance

class media_metadata():
    #Defines the media metadata class for the Media Metadata table
    def __init__(self, meta_dataid, entry_id, leftcameramedia, rightcameramedia, time, temperature, pressure, ph):
        self.meta_dataid = meta_dataid
        self.entry_id = entry_id
        self.leftcameramedia = leftcameramedia
        self.rightcameramedia = rightcameramedia
        self.time = time
        self.temperature = temperature
        self.pressure = pressure
        self.ph = ph
