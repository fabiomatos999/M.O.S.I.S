"""Folder structure generator for M.O.S.I.S UI.

Used to create MediaEntry folders and export MediaEntries into JSON.
"""
import databaseQuery
import json
import os


class FolderStructureGenerator:
    """Folder Structure Generator for Media Entries."""

    def __init__(self, root_path: str = "/home/pi/Media_Storage"):
        """Set root path of the folder structure.

        :param root_path The root directory of folder structure.
        By default uses the SSD mount point of the M.O.S.I.S
        microscope.
        """
        self.root_path = root_path
        self.databaseQuery = databaseQuery.DatabaseQuery()

    def create_folder_structure(self, entryId: int):
        """Create folder for a MediaEntry.

        :param entryId The id for the MediaEntry table entry.
        This is associated with the MediaMetadata table as a foreign key.
        """
        mediaEntry = self.databaseQuery.getMediaEntrybyId(entryId)
        folderPath = os.path.join(self.root_path, str(mediaEntry))
        os.makedirs(folderPath, exist_ok=True)

    def exportMetadata(self, entryId: int):
        """Export MediaEntry to a JSON file in the MediaEntry folder.

        :param entryId The id for the MediaEntry table entry.
        This is associated with the MediaMetadata table as a foreign key.
        """
        metadata = self.databaseQuery.getAllMediaMetadaByEntryId(entryId)
        metadata = list(map(lambda x: x.__dict__, metadata))
        jsonContents = json.dumps(metadata, indent=4)
        entryFolder = os.path.join(
            self.root_path, str(self.databaseQuery.getMediaEntrybyId(entryId)))
        file = open(os.path.join(entryFolder, "metadata.json"), "w")
        file.write(jsonContents)
        file.close()

    def create_folder_structure_for_all(self):
        """Create MediaEntries for all media entries."""
        media_entries = self.databaseQuery.getAllMediaEntry()

        for mediaEntry in media_entries:
            folderPath = os.path.join(self.root_path, str(mediaEntry))
            os.makedirs(folderPath, exist_ok=True)


if __name__ == "__main__":

    fol = FolderStructureGenerator(os.path.join(os.getcwd(), "test"))

    fol.create_folder_structure_for_all()
