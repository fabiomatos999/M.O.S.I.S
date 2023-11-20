"""Camera Picture Control Module for M.O.S.I.S microscope."""
from pixelinkWrapper import PxLApi
from ctypes import create_string_buffer
import time
import databaseQuery
from MainMenu import MainMenu
import sensor

SUCCESS = 0
FAILURE = 1


class CameraPictureControl():
    """Camera Picture Control for M.O.S.I.S microscope.

    Allows to get snapshots in JPEG and raw format, do single, burst
    and interval (time lapse), telescopic and video.
    """

    def __init__(self,
                 picFormat: PxLApi.ImageFormat = PxLApi.ImageFormat.JPEG):
        """Initialize with a default image format of JPEG.

        :param picFormat Image format enum from PxLApi ImageFormat.
        """
        self.imageFormat = picFormat
        self.stopStudy = False

    def get_snapshot(self, cameraHandle: int, fileName: str):
        """Get a snapshot from the camera, and save to a file.

        :param cameraHandle camera handle from the
         PxLApi initialize function
        :param fileName complete file path to saved image file.
        """
        assert 0 != cameraHandle
        assert fileName

        # Determine the size of buffer needed to hold an image from the camera
        rawImageSize = self.determine_raw_image_size(cameraHandle)
        if 0 == rawImageSize:
            return FAILURE

        # Create a buffer to hold the raw image
        rawImage = create_string_buffer(rawImageSize)

        if 0 != len(rawImage):

            # Capture a raw image.
            # The raw image buffer will contain image data on success.
            ret = self.get_raw_image(cameraHandle, rawImage)
            print("Captured Image")
            if PxLApi.apiSuccess(ret[0]):
                frameDescriptor = ret[1]

                print("took picture")

                assert 0 != len(rawImage)
                assert frameDescriptor
                #
                # Do any image processing here
                #

                print("format picture")

                # Encode the raw image into something displayable
                ret = PxLApi.formatImage(rawImage, frameDescriptor,
                                         self.imageFormat)
                print("formatted picture")

                if SUCCESS == ret[0]:
                    formatedImage = ret[1]
                    # Save formatted image into a file

                    print("saving picture")
                    name = fileName

                    if self.save_image_to_file(name, formatedImage) != SUCCESS:
                        return FAILURE
            ret = PxLApi.setStreamState(cameraHandle, PxLApi.StreamState.STOP)
            return SUCCESS

    def getBurstSnapshot(self,
                         burstNumber: int,
                         hCamera: int,
                         fileName: str,
                         burstInterval: int = 0) -> int:
        """Get burst image from a camera.

        Return SUCCESS or FAILURE.
        """
        counter = 0

        try:
            while counter < burstNumber:
                self.get_snapshot(hCamera, fileName)
                counter += 1
            return SUCCESS
        except Exception:
            return FAILURE

    def getIntervalSnapshot(self, cameraHandles: [int],
                            total_interval_min: float, amountOfPictures: int,
                            entryId: int, path: str):
        """Take a (time lapse) snapshot using total time and pictures.

        :param cameraHandles list of camera handles from the
         PxLApi initialize function
        :param total_interval_min Total amount time for
        the time lapse capture in  minutes.
        :param amountOfPictures Total amount of pictures
        to be taken in the time lapse.
        :param entryId The id for the MediaEntry table entry.
        This is associated with the MediaMetadata table as a foreign key.
        :param path Directory where the MediaMetadata will the stored.
        """
        dq = databaseQuery.DatabaseQuery()
        counter = 0
        stepInterval = (total_interval_min * 60) / amountOfPictures
        stepTime = time.time() + stepInterval

        sensorHub = sensor.sensorHub()
        while counter < amountOfPictures:
            if self.stopStudy:
                return
            if time.time() > stepTime or counter == 0:
                sensorData = sensorHub.Read()
                media_metadata = dq.insertMediaMetadata(
                    entryId, path, "jpg", MainMenu.getCurrentTime(),
                    sensorData.tempReading, sensorData.baroReading,
                    sensorData.phReading, sensorData.DOreading)
                media_metadata = dq.getMediaMetadatabyId(media_metadata)
                self.get_snapshot(cameraHandles[0],
                                  media_metadata.left_Camera_Media)
                self.get_snapshot(cameraHandles[1],
                                  media_metadata.right_Camera_Media)
                stepTime = time.time() + stepInterval
                counter += 1
            else:
                time.sleep(0.1)

    def getTelescopicSnapshot(self, cameraHandles: [int], minFocus: float,
                              maxFocus: float, numShots: int, entry_id: int,
                              path: str):
        """Take a telescopic image given shots and min and max focus values.

        :param cameraHandles list of camera handles from the
         PxLApi initialize function
        :param minFocus The minimum focus value where the telescopic image
        capture will start
        :param maxFocus The maximum focus value where the telescopic image
        capture will stop
        :param numShots The number of images to be taken in a telescopic image.
        :param entry_id MediaEntry entry_id associated with this image
        :param path Directory where media will be written to.
        NOTE: Min and Max focus values have to be between 1 and 46,000.
        """
        dq = databaseQuery.DatabaseQuery()
        sensorHub = sensor.sensorHub()
        if minFocus > maxFocus:
            temp = minFocus
            minFocus = maxFocus
            maxFocus = temp
        for focus in range(minFocus, maxFocus, numShots):
            self.setExposure(cameraHandles, focus, "")
            sensorData = sensorHub.Read()
            media_metadata = dq.insertMediaMetadata(entry_id, path, "jpg",
                                                    MainMenu.getCurrentTime(),
                                                    sensorData.tempReading,
                                                    sensorData.baroReading,
                                                    sensorData.phReading,
                                                    sensorData.DOreading)
            media_metadata = dq.getMediaMetadatabyId(media_metadata)
            self.get_snapshot(self.previewScreen.cameraHandles[0],
                              media_metadata.left_Camera_Media)
            self.get_snapshot(self.previewScreen.cameraHandles[1],
                              media_metadata.right_Camera_Media)

    def getVideo(self,
                 cameraHandles: [int],
                 entryId: int,
                 path: str,
                 recordTime: int = 60):
        """Capture sterioscopic images as fast as the camera sensors allows.

        :param cameraHandles list of camera handles from the
         PxLApi initialize function
        :param entryId The id for the MediaEntry table entry.
        This is associated with the MediaMetadata table as a foreign key.
        :param path Directory where the MediaMetadata will the stored.
        :param recordTime Recording time for the video in seconds.

        The images will be converted into a video file by the host software.
        """
        dq = databaseQuery.DatabaseQuery()
        now = time.time()
        sensorHub = sensor.sensorHub()
        while time.time() < now + recordTime:
            if self.stopStudy:
                return
            sensorData = sensorHub.Read()
            metadata = dq.insertMediaMetadata(entryId, path, "jpg",
                                              MainMenu.getCurrentTime(),
                                              sensorData.tempReading,
                                              sensorData.baroReading,
                                              sensorData.phReading,
                                              sensorData.DOreading)
            metadata = dq.getMediaMetadatabyId(metadata)
            self.get_snapshot(cameraHandles[0], metadata.left_Camera_Media)
            self.get_snapshot(cameraHandles[1], metadata.right_Camera_Media)

    def determine_raw_image_size(self, hCamera):
        """
        Query the region of interest (ROI), decimation, and pixel format.

        Using this information, we can calculate the size of a raw image
        Returns 0 on failure
        """
        assert 0 != hCamera

        # Get region of interest (ROI)
        ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.ROI)
        params = ret[2]
        roiWidth = params[PxLApi.RoiParams.WIDTH]
        roiHeight = params[PxLApi.RoiParams.HEIGHT]

        # Query pixel addressing
        # assume no pixel addressing (in case it is not supported)
        pixelAddressingValueX = 1
        pixelAddressingValueY = 1

        ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.PIXEL_ADDRESSING)
        if PxLApi.apiSuccess(ret[0]):
            params = ret[2]
            if PxLApi.PixelAddressingParams.NUM_PARAMS == len(params):
                # Camera supports symmetric and asymmetric pixel addressing
                pixelAddressingValueX = params[
                    PxLApi.PixelAddressingParams.X_VALUE]
                pixelAddressingValueY = params[
                    PxLApi.PixelAddressingParams.Y_VALUE]
            else:
                # Camera supports only symmetric pixel addressing
                pixelAddressingValueX = params[
                    PxLApi.PixelAddressingParams.VALUE]
                pixelAddressingValueY = params[
                    PxLApi.PixelAddressingParams.VALUE]

        # We can calculate the number of pixels now.
        numPixels = (roiWidth / pixelAddressingValueX) * (
            roiHeight / pixelAddressingValueY)
        ret = PxLApi.getFeature(hCamera, PxLApi.FeatureId.PIXEL_FORMAT)

        # Knowing pixel format means we can determine how many bytes per pixel.
        params = ret[2]
        pixelFormat = int(params[0])

        # And now the size of the frame
        pixelSize = PxLApi.getBytesPerPixel(pixelFormat)

        return int(numPixels * pixelSize)

    def get_raw_image(self, hCamera, rawImage):
        """
        Capture an image from the camera.

        NOTE: PxLApi.getNextFrame is a blocking call.
        i.e. PxLApi.getNextFrame won't return until an image is captured.
        So, if you're using hardware triggering,
        it won't return until the camera is triggered.
        Returns a return code with success and frame descriptor
        information or API error
        """
        assert 0 != hCamera
        assert 0 != len(rawImage)

        MAX_NUM_TRIES = 4

        # Put camera into streaming state so we can capture an image
        ret = PxLApi.setStreamState(hCamera, PxLApi.StreamState.START)
        # if not PxLApi.apiSuccess(ret[0]):
        #    return FAILURE

        # Get an image
        # NOTE: PxLApi.getNextFrame can return ApiCameraTimeoutError sometimes.
        # How you handle this depends on your situation and
        # how you use your camera.
        # For this sample app, we'll just retry a few times.
        ret = (PxLApi.ReturnCode.ApiUnknownError, )

        for i in range(MAX_NUM_TRIES):
            ret = PxLApi.getNextFrame(hCamera, rawImage)
            if PxLApi.apiSuccess(ret[0]):
                break

        return ret

    def save_image_to_file(self, fileName, formatedImage):
        """
        Save the encoded image buffer to a file.

        This overwrites any existing file
        Returns SUCCESS or FAILURE
        """
        assert fileName
        assert 0 != len(formatedImage)

        # Create a folder to save snapshots if it does not exist

        # Open a file for binary write
        print(fileName)
        file = open(fileName, "wb")
        if file is None:
            return FAILURE
        numBytesWritten = file.write(formatedImage)
        file.close()
        print("picture saved")

        if numBytesWritten == len(formatedImage):
            return SUCCESS

        return FAILURE


def main():
    """Camera Control Module Main Function.

    Takes a screenshot, then stops the stream.
    """
    picControl = CameraPictureControl()

    filenameJpeg = "snapshot.jpg"

    ret = PxLApi.initialize(0)
    if not PxLApi.apiSuccess(ret[0]):
        return 1
    hCamera = ret[1]

    # Get a snapshot and save it to a folder as a file
    retVal = picControl.get_snapshot(hCamera, filenameJpeg)

    # Done capturing, so no longer need the camera streaming images.
    # Note: If ret is used for this call, it will lose frame descriptor
    # information.
    PxLApi.setStreamState(hCamera, PxLApi.StreamState.STOP)

    # Tell the camera we're done with it.
    PxLApi.uninitialize(hCamera)

    if SUCCESS != retVal:
        print("ERROR: Unable to capture an image")
        return FAILURE

    return SUCCESS


if __name__ == "__main__":
    main()
