import databaseQuery
import json
import os


class FolderStructureGenerator:

    def __init__(self, root_path: str = "/home/pi/Media_Storage"):
        self.root_path = root_path
        self.databaseQuery = databaseQuery.DatabaseQuery()

    def create_folder_structure(self, entryId: int):
        mediaEntry = self.databaseQuery.getMediaEntrybyId(entryId)
        folderPath = os.path.join(self.root_path, str(mediaEntry))
        os.makedirs(folderPath, exist_ok=True)

    def exportMetadata(self, entryId: int):
        metadata = self.databaseQuery.getAllMediaMetadaByEntryId(entryId)
        metadata = list(map(lambda x: x.__dict__, metadata))
        jsonContents = json.dumps(metadata, indent=4)
        entryFolder = os.path.join(
            self.root_path, str(self.databaseQuery.getMediaEntrybyId(entryId)))
        file = open(os.path.join(entryFolder, "metadata.json"), "w")
        file.write(jsonContents)
        file.close()

    def create_folder_structure_for_all(self):
        media_entries = self.databaseQuery.getAllMediaEntry()
        
        for mediaEntry in media_entries:
            folderPath = os.path.join(self.root_path, str(mediaEntry))
            os.makedirs(folderPath, exist_ok=True)

if __name__ == "__main__":

    fol = FolderStructureGenerator(os.path.join(os.getcwd(), "test"))

    fol.create_folder_structure_for_all()