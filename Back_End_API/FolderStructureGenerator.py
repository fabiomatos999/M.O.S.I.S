import databaseQuery
import json
import os

class FolderStructureGenerator:

    def __init__(self, root_path: str = "/home/pi/Media_Storage"):
        self.root_path = root_path
        self.databaseQuery = databaseQuery.DatabaseQuery()

    def create_folder_structure(self, folders):
        for folder in folders:
            folder_path = os.path.join(self.root_path, folder)
            os.makedirs(folder_path, exist_ok=True)


if __name__ == "__main__":

    fol = FolderStructureGenerator(os.path.join(os.getcwd(), "test"))

    fol.create_folder_structure(fol.databaseQuery.getAllMediaEntry())

