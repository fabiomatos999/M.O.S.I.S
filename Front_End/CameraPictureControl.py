"""Camera Picture Control Module for M.O.S.I.S microscope."""
from pixelinkWrapper import PxLApi
import os
from ctypes import create_string_buffer
from datetime import datetime
import time
import databaseQuery
from MainMenu import MainMenu
import databaseQuery

SUCCESS = 0
FAILURE = 1


class CameraPictureControl():
    """Camera Picture Control for M.O.S.I.S microscope.

    Allows to get snapshots in JPEG and raw format, do single, burst
    and interval (time lapse).
    """

    def __init__(self, picFormat=PxLApi.ImageFormat.JPEG):
        """Initialize with a default image format of JPEG."""
        self.imageFormat = picFormat

    def get_snapshot(self, hCamera: int, fileName: str):
        """Get a snapshot from the camera, and save to a file."""
        assert 0 != hCamera
        assert fileName

        # Determine the size of buffer needed to hold an image from the camera
        rawImageSize = self.determine_raw_image_size(hCamera)
        if 0 == rawImageSize:
            return FAILURE

        # Create a buffer to hold the raw image
        rawImage = create_string_buffer(rawImageSize)

        if 0 != len(rawImage):

            # Capture a raw image.
            # The raw image buffer will contain image data on success.
            ret = self.get_raw_image(hCamera, rawImage)
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
            ret = PxLApi.setStreamState(hCamera, PxLApi.StreamState.STOP)
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

    def getIntervalSnapshot(self, hCamera: [int], total_interval_min: float,
                            steps: int, entryId: int, path: str):
        """Take a (time lapse) snapshot using total time and pictures."""
        counter = 0
        dq = databaseQuery.DatabaseQuery
        media_metadata = dq.insertMediaMetadata(
                    entryId, path, "jpg", MainMenu.getCurrentTime(), 95.5,
                    100, 8, 0.5)
        interval_seconds = 60 * total_interval_min
        start_time = time.time()
        start_step = time.time()
        media_metadata = dq.getMediaMetadatabyId(media_metadata)

        print("start interval snapshot")
        total_pictures = interval_seconds / steps

        print("start time: ", start_time)

        try:
            while time.time(
            ) - start_time <= interval_seconds or counter < total_pictures:
                # print("time difference: ", time.time() - start_time)
                if time.time() - start_step >= steps:

                    MainMenu.cameraPictureControl.get_snapshot(
                    MainMenu.previewScreen.cameraHandles[0],
                    media_metadata.left_Camera_Media)
                    MainMenu.cameraPictureControl.get_snapshot(
                    MainMenu.previewScreen.cameraHandles[1],
                    media_metadata.right_Camera_Media)
                    counter += 1
                    start_step = time.time()
            return SUCCESS
        except Exception:
            return FAILURE

    def getTelescopicSnapshot(self, hCamera: [int], minFocus: float,
                              maxFocus: float, numShots: int):
        """Take a telescopic image given shots and min and max focus values.

        :param hcamera list of camera handlers from the
         PxLApi initialize function
        :param minFocus The minimum focus value where the telescopic image
        capture will start
        :param maxFocus The maximum focus value where the telescopic image
        capture will stop
        NOTE: Min and Max focus values have to be between 1 and 46,000.
        """
        if not (1 < minFocus < 46, 000 and 1 < minFocus < 46000):
            raise ValueError(
                "Min and Max Focus Have to be between 1 and 46,000")
        if minFocus > maxFocus:
            temp = minFocus
            minFocus = maxFocus
            maxFocus = temp
        step = (maxFocus - minFocus) / numShots
        for focusValue in range(minFocus, maxFocus + step, step):
            for camera in hCamera:
                PxLApi.setFeature(camera, PxLApi.FeatureId.FOCUS,
                                  PxLApi.FeatureFlags.ONEPUSH, focusValue)
                self.get_snapshot(camera, "formatted-filename")

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

    def getVideo(self,
                 cameraHandles: [int],
                 recordTime: int = 60,
                 videoFPS: int = 24,
                 decimation: int = PxLApi.ClipPlaybackDefaults.DECIMATION_NONE,
                 bitrate: int = PxLApi.ClipPlaybackDefaults.BITRATE_DEFAULT,
                 encoding: int = PxLApi.ClipEncodingFormat.H264,
                 filePath: str = str(),
                 fileName: str = str()):
        pass



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
