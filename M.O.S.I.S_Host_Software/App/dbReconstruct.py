import os
import db
from enums import shotType, illuminationType
import imageManipulation


class DBReconstruct:

    def __init__(self, rootPath: str):
        self.rootPath = rootPath
        self.folders = os.listdir(self.rootPath)
        self.folders = list(filter(lambda x: x != "lost+found", self.folders))
        self.query = db.DatabaseQuery()
        for folder in self.folders:
            self.insertMediaEntryFromFolderName(folder)
            self.insertMediaMetadataFromFolderName(folder)
        self.query.__del__()

    def insertMediaEntryFromFolderName(self, folder: str):
        def decodeShutterSpeed(shutterSpeed: str) -> str:
            fraction = shutterSpeed.split("_")
            if len(fraction) == 2:
                return "{}/{}".format(fraction[0], fraction[1])
            else:
                return fraction[0]
        fields = folder.split("-")
        entryId = fields[0]
        shottype = shotType[fields[1]]
        time = "{}-{}-{}-{}-{}".format(fields[2], fields[3], fields[4],
                                       fields[5], fields[6])
        illuminationtype = illuminationType[fields[7]]
        gain = fields[8]
        saturation = fields[9]
        shutterSpeed = decodeShutterSpeed(fields[10])
        whiteBalance = fields[11]
        self.query.insertMediaEntry(entryId, shottype, time, illuminationtype,
                                    gain, saturation, shutterSpeed,
                                    whiteBalance)

    def insertMediaMetadataFromFolderName(self, folder: str):

        imagePairs = imageManipulation.findImagePairs(
            os.path.join(self.rootPath, folder))
        entryId = None
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
            leftCameraMedia = (folder + "/" + pair[0])
            rightCameraMedia = (folder + "/" + pair[1])
            stereoMediaPath = \
                "static/Media/{}/{}-{}-{}-{}-{}-{}-{}-S.jpg".format(
                    folder, entryId, metadataId, time, temperature, pressure,
                    ph, dissolvedOxygen)
            if not os.path.exists(stereoMediaPath):
                imageManipulation.generateStereoscopicImage(
                    os.path.join(self.rootPath, leftCameraMedia),
                    os.path.join(self.rootPath, rightCameraMedia),
                    stereoMediaPath)
            thresholdLeftImagePath = \
                "static/Media/{}/{}-{}-{}-{}-{}-{}-{}-GL.jpg".format(
                    folder, entryId, metadataId, time, temperature, pressure,
                    ph, dissolvedOxygen)
            thresholdRightImagePath = \
                "static/Media/{}/{}-{}-{}-{}-{}-{}-{}-GR.jpg".format(
                    folder, entryId, metadataId, time, temperature, pressure,
                    ph, dissolvedOxygen)
            if not os.path.exists(thresholdLeftImagePath):
                imageManipulation.generateWhiteScaleImage(
                    os.path.join(self.rootPath, leftCameraMedia),
                    thresholdLeftImagePath)
            if not os.path.exists(thresholdRightImagePath):
                imageManipulation.generateWhiteScaleImage(
                    os.path.join(self.rootPath, rightCameraMedia),
                    thresholdRightImagePath)
            taggedStereoMediaPath = \
                "static/Media/{}/{}-{}-{}-{}-{}-{}-{}-T.jpg".format(
                    folder, entryId, metadataId, time, temperature, pressure,
                    ph, dissolvedOxygen)
            if not os.path.exists(taggedStereoMediaPath):
                imageManipulation.addMetadataBar(stereoMediaPath,
                                                 taggedStereoMediaPath, time,
                                                 float(temperature),
                                                 float(pressure), float(ph),
                                                 float(dissolvedOxygen))
            stereoMediaPath = "{}/{}".format(
                stereoMediaPath.split("/")[-2],
                stereoMediaPath.split("/")[-1])
            thresholdLeftImagePath = "{}/{}".format(
                thresholdLeftImagePath.split("/")[-2],
                thresholdLeftImagePath.split("/")[-1])
            thresholdRightImagePath = "{}/{}".format(
                thresholdRightImagePath.split("/")[-2],
                thresholdRightImagePath.split("/")[-1])
            thresholdRightImagePath = "{}/{}".format(
                thresholdRightImagePath.split("/")[-2],
                thresholdRightImagePath.split("/")[-1])
            taggedStereoMediaPath = "{}/{}".format(
                taggedStereoMediaPath.split("/")[-2],
                taggedStereoMediaPath.split("/")[-1])
            self.query.insertMediaMetadata(
                metadataId, entryId, leftCameraMedia, rightCameraMedia, time,
                temperature, pressure, ph, dissolvedOxygen,
                thresholdLeftImagePath, thresholdRightImagePath,
                stereoMediaPath, taggedStereoMediaPath)


        shottype = self.query.getMediaEntry(entryId).shotType
        if shottype == "BURST" or shottype == "TIMELAPSE":
            gifPath = os.path.join(os.path.join(self.rootPath, folder), "stereo.gif")
            if not os.path.exists(gifPath):
                imageManipulation.generateGif(
                "{}/{}".format(self.rootPath, folder), imagePairs)
        elif shottype == "TELESCOPIC":
            focusStackPathL = os.path.join(os.path.join(self.rootPath, folder), "focusStack-L.jpg")
            focusStackPathR = os.path.join(os.path.join(self.rootPath, folder), "focusStack-R.jpg")
            focusStackPathS = os.path.join(os.path.join(self.rootPath, folder), "focusStack-S.jpg")
            if not os.path.exists(focusStackPathL) and os.path.exists(focusStackPathR) and os.path.exists(focusStackPathS):
                imageManipulation.generateFocusStackImage(os.path.join(self.rootPath, folder))
        elif shottype == "VIDEO":
            videoPath = os.path.join(os.path.join(self.rootPath, folder), "stereoVideo.mp4")
            if not os.path.exists(videoPath):
                imageManipulation.generateStereoscopicVideo(os.path.join(self.rootPath, folder))


if __name__ == "__main__":
    dbr = DBReconstruct("static/Media")
