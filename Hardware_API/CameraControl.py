"""Camera control module for PixeLINK PL-D755 Camera."""
from pixelinkWrapper import PxLApi
import threading


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

    def setUpMaxMinFeatureValues(self, hCamera):
        """
        Set the camera features min and max values for automatic mode.

        Also make sure new values are within an acceptable range.
        :param hCamera:
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

    def setUpCamera(self, num_cameras=1):
        """Initialize both cameras for M.O.S.I.S microscope."""
        main_hCameras = []
        "# First: Determine how many cameras are connected and are available"
        ret = PxLApi.getNumberCameras()
        "print(ret)"
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
                        if i == 0:
                            params = [0, 1]
                            # params dictate that horizontal flip will be off
                            # (0) while vertical flip is on (1)

                            # flips image of the left camera
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

    def start_preview(self, stream_width, stream_height, hCamera, topHwnd):
        """
        Start the preview (with message pump).

        Preview gets stopped when the top level window is closed.
        """
        self.setUpStreamSize(stream_width, stream_height)

        # Declare control preview thread that can control preview and poll the
        # message pump on Windows
        self.previewState = PxLApi.PreviewState.START
        previewThread = self.create_new_preview_thread(hCamera, topHwnd)
        previewThread.start()

    def cleanUpCameras(self, hCamera):
        """Set Preview State for both cameras to Stop."""
        for i in range(len(hCamera)):
            PxLApi.setStreamState(hCamera[i], PxLApi.StreamState.STOP)
            # ret =\
            #     PxLApi.setPreviewState(hCamera[i], PxLApi.PreviewState.STOP)
            PxLApi.uninitialize(hCamera[i])

    def setFocus(self, hCamera, newfocusValue=2, mode="auto"):
        """
        Prompt the camera to perform autofocus.

        :param hCamera: the camera to perform autofocus
        :return:
        """
        # params = []
        if mode == "auto":
            # params.insert(0, self.minFocusValue)
            #             params.insert(1, self.maxFocusValue)

            for i in range(len(hCamera)):
                ret = PxLApi.setFeature(hCamera[i], PxLApi.FeatureId.FOCUS,
                                        PxLApi.FeatureFlags.ONEPUSH,
                                        self.minMaxParams)
                if not PxLApi.apiSuccess(ret[0]):
                    print("  Could not set Focus Feature, ret: %d!" % ret[0])
                    PxLApi.uninitialize(hCamera[i])
                    return

        else:
            if not self.minFocusValue < newfocusValue < self.maxFocusValue:
                print("focus value not in acceptable range")
                return

            # self.params.insert(0, newfocusValue)
            self.customFocus[0] = newfocusValue

            for i in range(len(hCamera)):
                ret = PxLApi.setFeature(hCamera[i], PxLApi.FeatureId.FOCUS,
                                        PxLApi.FeatureFlags.MANUAL,
                                        self.customFocus)
                if not PxLApi.apiSuccess(ret[0]):
                    print("  Could not set Focus Feature, ret: %d!" % ret[0])
                    PxLApi.uninitialize(hCamera[i])
                    return
            self.focusValue = newfocusValue

    def setExposure(self, hCamera, newExposureValue, mode="auto"):
        """
        Set exposure for a camera.

        :param hCamera: the camera to change exposure
        :return:
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

    def setSaturation(self, hCamera, newSaturationValue, mode="auto"):
        """
        Set exposure value for a camera.

        :param hCamera: the camera to change saturation
        :return:
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

    def setGain(self, hCamera, newGainValue, mode="auto"):
        """
        Set the gain value for a camera.

        :param hCamera: the camera to set gain
        :return:
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
