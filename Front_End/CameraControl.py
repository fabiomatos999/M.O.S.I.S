"""Camera control module for PixeLINK PL-D755 Camera."""
from pixelinkWrapper import PxLApi
import threading
import time


class CameraControl():
    """Control class for both of PixeLINK PL-D755 on M.O.S.I.S microscope."""

    def __init__(self):
        """Construct CameraControl class."""
        self.hCamera_list = []
        self.stream_height = None
        self.stream_width = None
        self.previewState = False
        self.focusValue = 46000

        self.minFocusValue = None
        self.maxFocusValue = None
        self.minMaxParams = []
        self.customFocus = [1]

        self.minExposureValue = None
        self.maxExposureValue = None
        self.exposureValue = None

        self.minSaturationValue = None
        self.maxSaturationValue = None
        self.saturationValue = None

        self.minGainValue = None
        self.maxGainValue = None
        self.gainValue = None

    def setUpStreamSize(self, width, height):
        """
        Set the global stream width and height.

        :param width: width of the preview stream
        :param height: height of the preview height
        :return:
        """
        self.stream_width = width
        self.stream_height = height

    def setUpMaxMinFeatureValues(self, hCamera: int):
        """
        Set the camera features min and max values for automatic mode.

        Also make sure new values are within an acceptable range.
        :param hCamera Camera handler from the
         PxLApi initialize function
        :return:
        """
        # Get Focus Feature Min and Max values
        ret = PxLApi.getCameraFeatures(hCamera, PxLApi.FeatureId.FOCUS)
        if (PxLApi.apiSuccess(ret[0])):
            if (ret[1] is not None):
                cameraFeatures = ret[1]
                assert 1 == cameraFeatures.uNumberOfFeatures, \
                    "Unexpected number of features"
                assert cameraFeatures.Features[
                    0].uFeatureId == PxLApi.FeatureId.FOCUS, \
                    "Unexpected returned featureId"

                # Sets max and min focus value of camera
                self.minFocusValue = cameraFeatures.Features[0].Params[
                    0].fMinValue  # Min focus value
                self.maxFocusValue = cameraFeatures.Features[0].Params[
                    1].fMaxValue  # Max focus value
                self.minMaxParams.insert(0, self.minFocusValue)
                self.minMaxParams.insert(1, self.maxFocusValue)

                print("min focus value: ", self.minFocusValue)
                print("max focus value: ", self.maxFocusValue)

        # Get Exposure Feature Min and Max value
        ret = PxLApi.getCameraFeatures(hCamera, PxLApi.FeatureId.EXPOSURE)
        if (PxLApi.apiSuccess(ret[0])):
            if (ret[1] is not None):
                cameraFeatures = ret[1]
                assert 1 == cameraFeatures.uNumberOfFeatures, \
                    "Unexpected number of features"
                assert cameraFeatures.Features[
                    0].uFeatureId == PxLApi.FeatureId.EXPOSURE, \
                    "Unexpected returned featureId"

                self.minExposureValue = cameraFeatures.Features[0].Params[
                    0].fMinValue  # Min focus value
                self.maxExposureValue = cameraFeatures.Features[0].Params[
                    1].fMaxValue  # Max focus value

                print("min exposure value: ", self.minExposureValue)
                print("max exposure value: ", self.maxExposureValue)

        # Get Saturation Feature Min and Max value
        ret = PxLApi.getCameraFeatures(hCamera, PxLApi.FeatureId.SATURATION)
        if (PxLApi.apiSuccess(ret[0])):
            if (ret[1] is not None):
                cameraFeatures = ret[1]
                assert 1 == cameraFeatures.uNumberOfFeatures, \
                    "Unexpected number of features"
                assert cameraFeatures.Features[
                    0].uFeatureId == PxLApi.FeatureId.SATURATION, \
                    "Unexpected returned featureId"

                self.minSaturationValue = cameraFeatures.Features[0].Params[
                    0].fMinValue  # Min focus value
                self.maxSaturationValue = cameraFeatures.Features[0].Params[
                    0].fMaxValue  # Max focus value

                print("min saturation value: ", self.minSaturationValue)
                print("max saturation value: ", self.maxSaturationValue)

        # Get Saturation Feature Min and Max value
        ret = PxLApi.getCameraFeatures(hCamera, PxLApi.FeatureId.GAIN)
        if (PxLApi.apiSuccess(ret[0])):
            if (ret[1] is not None):
                cameraFeatures = ret[1]
                assert 1 == cameraFeatures.uNumberOfFeatures, \
                    "Unexpected number of features"
                assert cameraFeatures.Features[
                    0].uFeatureId == PxLApi.FeatureId.GAIN, \
                    "Unexpected returned featureId"

                self.minGainValue = cameraFeatures.Features[0].Params[
                    0].fMinValue  # Min focus value
                self.maxGainValue = cameraFeatures.Features[0].Params[
                    0].fMaxValue  # Max focus value

                print("min Gain value: ", self.minGainValue)
                print("max Gain value: ", self.maxGainValue)

    def setUpCamera(self, num_cameras: int = 1) -> [int]:
        """Initialize both cameras for M.O.S.I.S microscope.

        :return List of Camera handlers from the
         PxLApi initialize function
        """
        main_hCameras = []
        "# First: Determine how many cameras are connected and are available"
        ret = PxLApi.getNumberCameras()
        print(ret)
        if PxLApi.apiSuccess(ret[0]):
            cameraIdInfo = ret[1]
            numCameras = len(cameraIdInfo)
            print(numCameras)
            if 0 < numCameras:
                # One-by-one, get the camera info for each camera
                for i in range(numCameras):
                    serialNumber = cameraIdInfo[i].CameraSerialNum
                    print(serialNumber)
                    # Connect to the camera
                    ret = PxLApi.initialize(serialNumber)
                    if PxLApi.apiSuccess(ret[0]):
                        hCamera = ret[1]
                        main_hCameras.append(hCamera)
                        if serialNumber == 775002722:
                            params = [1, 1]
                            ret2 = PxLApi.setFeature(
                                hCamera, PxLApi.FeatureId.FLIP,
                                PxLApi.FeatureFlags.MANUAL, params)
                            if not PxLApi.apiSuccess(ret2[0]):
                                print(
                                    "  Could not flip camera image, ret: %d!" %
                                    ret2[0])
                                return

                        # And get the info
                        ret = PxLApi.getCameraInfo(hCamera)
                        print(ret)

        self.setUpMaxMinFeatureValues(main_hCameras[0])
        return main_hCameras

    def control_preview_thread(self,
                               hCamera,
                               topHwnd,
                               title="",
                               leftOffset=-10):
        """
        Thread  function in charge of showing the camera preview.

        :param topHwnd: integer number that corresponds to the parent window
        the stream will be showed in
        :return: an assertion that the stream was successfully stopped,
        once the user exits the preview
        """
        width = 400
        height = 400

        ret = PxLApi.setPreviewSettings(
            hCamera, title,
            PxLApi.WindowsPreview.WS_VISIBLE | PxLApi.WindowsPreview.WS_CHILD,
            leftOffset, -70, width, height, topHwnd)

        ret = PxLApi.setPreviewState(hCamera, PxLApi.PreviewState.START)

        assert PxLApi.apiSuccess(ret[0]), "%i" % ret[0]

    def create_new_preview_thread(self, hCamera, topHwnd):
        """Create a new preview thread for each preview run."""
        return threading.Thread(target=self.control_preview_thread,
                                args=(hCamera, topHwnd),
                                daemon=True)

    def start_preview(self, stream_width: int, stream_height: int,
                      hCamera: int, topHwnd: int):
        """
        Start the preview (with message pump).

        :param stream_width Preview window size in pixels
        :param stream_height Preview window size in pixels
        :param hCamera Camera handler from the
         PxLApi initialize function
        :param topHwnd: integer number that corresponds to the parent window
        the stream will be showed in
        Preview gets stopped when the top level window is closed.
        """
        self.setUpStreamSize(stream_width, stream_height)

        # Declare control preview thread that can control preview and poll the
        # message pump on Windows
        self.previewState = PxLApi.PreviewState.START
        previewThread = self.create_new_preview_thread(hCamera, topHwnd)
        previewThread.start()

    def cleanUpCameras(self, hCamera: [int]):
        """Set Preview State for both cameras to Stop.

        :param hCamera List of Camera handlers from the
         PxLApi initialize function
        """
        for i in range(len(hCamera)):
            PxLApi.setStreamState(hCamera[i], PxLApi.StreamState.STOP)
            # ret =\
            #     PxLApi.setPreviewState(hCamera[i], PxLApi.PreviewState.STOP)
            PxLApi.uninitialize(hCamera[i])

    def setRegionOfInterest(self,
                            hCamera: [int],
                            fleft: int = 0,
                            ftop: int = 0,
                            fwidth: int = 2592,
                            fheight: int = 1944):
        """Set the region of interest for both cameras.

        :param hCamera List of Camera handlers from the
         PxLApi initialize function
        :param fleft Has to be between 0 and 1928
        :param ftop Has to be between 0 and 2560
        :param fwidth Has to be between 0 and 2592
        :param fheight Has to be between 0 and 1944
        Note: If none if the optional parameters are passed in,
        it will default to the maximum resolution of the
        PL-D755 Camera.
        """
        for cameraHandle in hCamera:
            PxLApi.setStreamState(cameraHandle, PxLApi.StreamState().STOP)
            PxLApi.setFeature(cameraHandle, PxLApi.FeatureId.ROI,
                              PxLApi.FeatureFlags.MANUAL,
                              [fleft, ftop, fwidth, fheight])

    def setWhiteBalance(self, hCamera: [int], temp: int = 3200):
        """Set the color temperature for both cameras.

        :param hCamera List of Camera handlers from the
         PxLApi initialize function
        :param temp Has to be between 3200 and 6500.
        """
        if 3200 < temp < 6500:

            for camera in hCamera:
                ret = PxLApi.setFeature(camera, PxLApi.FeatureId.WHITE_BALANCE,
                                        PxLApi.FeatureFlags.MANUAL, [temp])
                if (PxLApi.apiSuccess(ret[0])):
                    print("UwU")
                else:
                    raise ValueError("Invalid Temperature Inputted.")

    def autoWhiteBalance(self, hCamera: [int]):
        """Auto white balance for both cameras.

        :param hcamera List of camera handlers from the
         PxLApi initialize function
        """
        cameraColors = [0, 0, 0]

        for camera in hCamera:
            ret = PxLApi.setFeature(camera, PxLApi.FeatureId.WHITE_SHADING,
                                    PxLApi.FeatureFlags.ONEPUSH, cameraColors)
            for _ in range(10):
                ret = PxLApi.getFeature(camera, PxLApi.FeatureId.WHITE_SHADING)
                flags = ret[1]
                if not (flags & PxLApi.FeatureFlags.ONEPUSH):
                    break
                time.sleep(1)

    def setFocus(self,
                 hCamera: [int],
                 newfocusValue: float = 2,
                 mode: str = "auto"):
        """
        Prompt the camera to perform autofocus.

        :param hCamera List of Camera handlers from the
         PxLApi initialize function
        :param newFocusValue Has to be between 1 and 46,000
        :param mode If "auto" then will perform autofocus, else
        will use newFocusValue
        :return
        """
        params = []
        print(self.maxFocusValue, self.minFocusValue)
        if mode == "auto":
            params.insert(0, self.minFocusValue)
            params.insert(1, self.maxFocusValue)

            for handle in hCamera:
                print(handle)
                ret = PxLApi.setFeature(handle, PxLApi.FeatureId.FOCUS,
                                        PxLApi.FeatureFlags.MANUAL, params)
                if not PxLApi.apiSuccess(ret[0]):
                    print("  Could not set Focus Feature, ret: %d!" % ret[0])
                    PxLApi.uninitialize(handle)
                    return

        else:
            if not self.minFocusValue < newfocusValue < self.maxFocusValue:
                print("focus value not in acceptable range")
                return

            # self.params.insert(0, newfocusValue)
            self.customFocus[0] = newfocusValue

            for handle in range(len(hCamera)):
                ret = PxLApi.setFeature(hCamera[handle],
                                        PxLApi.FeatureId.FOCUS,
                                        PxLApi.FeatureFlags.MANUAL,
                                        self.customFocus)
                if not PxLApi.apiSuccess(ret[0]):
                    print("  Could not set Focus Feature, ret: %d!" % ret[0])
                    PxLApi.uninitialize(hCamera[handle])
                    return
            self.focusValue = newfocusValue

    def setExposure(self,
                    hCamera: [int],
                    newExposureValue: float = 0.0001078958302969113,
                    mode: str = "auto"):
        """
        Set exposure for a camera.

        :param hCamera List of Camera handlers from the
         PxLApi initialize function
        :param newExposureValue Has to be between 0.00010699999984353781 and 2
        :param mode If "auto" then will perform auto-exposure, else
        will use newExposureValue
        :return
        """
        if not\
           self.minExposureValue <= newExposureValue <= self.maxExposureValue:
            print("focus value not in acceptable range", newExposureValue)
            return

        params = []

        if mode == "auto":
            params = []
            params.insert(0, self.minExposureValue)
            params.insert(1, self.minExposureValue)
            params.insert(2, self.maxExposureValue)

            for i in range(len(hCamera)):
                ret = PxLApi.setFeature(hCamera[i], PxLApi.FeatureId.EXPOSURE,
                                        PxLApi.FeatureFlags.AUTO, params)
                if not PxLApi.apiSuccess(ret[0]):
                    print("  Could not set Focus Feature, ret: %d!" % ret[0])
                    PxLApi.uninitialize(hCamera[i])
                    return
        else:
            params.insert(0, newExposureValue)

            for i in range(len(hCamera)):
                ret = PxLApi.setFeature(hCamera[i], PxLApi.FeatureId.EXPOSURE,
                                        PxLApi.FeatureFlags.MANUAL, params)
                if not PxLApi.apiSuccess(ret[0]):
                    print("  Could not set Focus Feature, ret: %d!" % ret[0])
                    PxLApi.uninitialize(hCamera[i])
                    return
            self.exposureValue = newExposureValue

    def setSaturation(self,
                      hCamera: [int],
                      newSaturationValue: int = 100,
                      mode: int = "auto"):
        """
        Set exposure value for a camera.

        :param hCamera List of Camera handlers from the
         PxLApi initialize function
        :param newExposureValue Has to be between 0 and 200
        :param mode If "auto" then will perform auto-exposure, else
        will use newExposureValue
        :return
        """
        if not self.minSaturationValue <=\
           newSaturationValue <= self.maxSaturationValue:
            print("focus value not in acceptable range", newSaturationValue)
            return

        params = []

        if mode == "auto":
            params = []
            params.insert(0, self.minSaturationValue)
            params.insert(1, self.maxSaturationValue)

            for i in range(len(hCamera)):
                ret = PxLApi.setFeature(hCamera[i],
                                        PxLApi.FeatureId.SATURATION,
                                        PxLApi.FeatureFlags.AUTO, params)
                if not PxLApi.apiSuccess(ret[0]):
                    print("  Could not set Saturation Feature, ret: %d!" %
                          ret[0])
                    PxLApi.uninitialize(hCamera[i])
                    return
        else:
            params.insert(0, newSaturationValue)

            for i in range(len(hCamera)):
                ret = PxLApi.setFeature(hCamera[i],
                                        PxLApi.FeatureId.SATURATION,
                                        PxLApi.FeatureFlags.MANUAL, params)
                if not PxLApi.apiSuccess(ret[0]):
                    print("  Could not set Saturation Feature, ret: %d!" %
                          ret[0])
                    PxLApi.uninitialize(hCamera[i])
                    return
            self.saturationValue = newSaturationValue

    def setGain(self,
                hCamera: [int],
                newGainValue: float = 0,
                mode: str = "auto"):
        """
        Set the gain value for a camera.

        :param hCamera List of Camera handlers from the
         PxLApi initialize function
        :param newGainValue Has to be between 0 and 24
        :param mode If "auto" then will perform auto-gain, else
        will use newGainValue
        :return
        """
        if not self.minGainValue <= newGainValue <= self.maxGainValue:
            print("focus value not in acceptable range", newGainValue)
            return

        params = []

        if mode == "auto":
            params = []
            params.insert(0, self.minGainValue)
            params.insert(1, self.maxGainValue)

            for i in range(len(hCamera)):
                ret = PxLApi.setFeature(hCamera[i], PxLApi.FeatureId.GAIN,
                                        PxLApi.FeatureFlags.AUTO, params)
                if not PxLApi.apiSuccess(ret[0]):
                    print("  Could not set Gain Feature, ret: %d!" % ret[0])
                    PxLApi.uninitialize(hCamera[i])
                    return
        else:
            params.insert(0, newGainValue)

            for i in range(len(hCamera)):
                ret = PxLApi.setFeature(hCamera[i], PxLApi.FeatureId.GAIN,
                                        PxLApi.FeatureFlags.MANUAL, params)
                if not PxLApi.apiSuccess(ret[0]):
                    print("  Could not set Gain Feature, ret: %d!" % ret[0])
                    PxLApi.uninitialize(hCamera[i])
                    return
            self.gainValue = newGainValue
