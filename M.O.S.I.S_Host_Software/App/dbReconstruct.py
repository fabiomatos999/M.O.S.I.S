import os
import db
from enums import shotType, illuminationType
import re
import imageManipulation


class DBReconstruct:

    def __init__(self, rootPath: str):
        self.rootPath = rootPath
        self.folders = os.listdir(self.rootPath)
        self.query = db.DatabaseQuery()
        for folder in self.folders:
            self.insertMediaEntryFromFolderName(folder)
            self.insertMediaMetadataFromFolderName(folder)

    def insertMediaEntryFromFolderName(self, folder: str):
        fields = folder.split("-")
        entryId = fields[0]
        shottype = shotType[fields[1]]
        time = "{}-{}-{}-{}-{}".format(fields[2], fields[3], fields[4],
                                       fields[5], fields[6])
        illuminationtype = illuminationType[fields[7]]
        gain = fields[8]
        saturation = fields[9]
        shutterSpeed = fields[10]
        whiteBalance = fields[11]
        self.query.insertMediaEntry(entryId, shottype, time, illuminationtype,
                                    gain, saturation, shutterSpeed,
                                    whiteBalance)

    def insertMediaMetadataFromFolderName(self, folder: str):

        def findImagePairs(self, folder: str) -> [(str, str)]:
            files = os.listdir(os.path.join(self.rootPath, folder))
            files = list(
                filter(lambda x: not re.match(r"^.*\.json$", x), files))
            leftImages = list(
                filter(lambda x: re.match(r".*-L\..*$", x), files))
            rightImages = list(
                filter(lambda x: re.match(r".*-R\..*$", x), files))
            leftImages.sort()
            rightImages.sort()
            return list(zip(leftImages, rightImages))

        imagePairs = findImagePairs(self, folder)
        for pair in imagePairs:
            fields = pair[0].split('-')
            entryId = fields[0]
            metadataId = fields[1]
            time = "{}-{}-{}-{}-{}".format(fields[2], fields[3], fields[4],
                                           fields[5], fields[6])
            temperature = fields[7]
            pressure = fields[8]
            ph = fields[9]
            dissolvedOxygen = fields[10]
            leftCameraMedia = os.path.join(folder, pair[0])
            rightCameraMedia = os.path.join(folder, pair[1])
            self.query.insertMediaMetadata(metadataId, entryId,
                                           leftCameraMedia, rightCameraMedia,
                                           time, temperature, pressure, ph,
                                           dissolvedOxygen)
            mediaMetadata = self.query.getMediaMetadataByMetadataId(
                int(metadataId))
            mediaEntry = self.query.getMediaEntry(int(entryId))
            print(folder)
            stereoMediaPath = "static/Media/{}/{}-{}-{}-{}-{}-{}-{}-S.jpg".format(
                folder, entryId, metadataId, time, temperature, pressure, ph,
                dissolvedOxygen)
            if not os.path.exists(stereoMediaPath):
                imageManipulation.generateStereoscopicImage(
                    os.path.join(self.rootPath, leftCameraMedia),
                    os.path.join(self.rootPath, rightCameraMedia),
                    stereoMediaPath)
        shottype = self.query.getMediaEntry(entryId).shotType
        if shottype == "BURST" or shottype == "TIMELAPSE":
            imageManipulation.generateGif(
                "{}/{}".format(self.rootPath, folder), imagePairs)


if __name__ == "__main__":
    os.remove("test.db")
    dbr = DBReconstruct("static/Media")
