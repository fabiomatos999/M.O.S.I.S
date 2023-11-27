"""Image manipulation module for preview screen."""
import CameraPictureControl
import cv2
import numpy
from PyQt6.QtGui import QImage, QPixmap
import CameraControl
from ctypes import create_string_buffer
from pixelinkwrapper import PxLApi
from PIL import Image
import io


def getPreviewImage(cameraHandles: [int]) -> (QPixmap, QPixmap):
    """Generate preview screen images and resize images to 400x400.

    :param cameraHandles list of camera handles from the
    PxLApi initialize function
    :param folderPath folder where the preview screen images will
    be outputted
    """
    cpc = CameraPictureControl.CameraPictureControl()
    cc = CameraControl.CameraControl()
    cc.setRegionOfInterest(cameraHandles)
    pixmaps = []
    for handle in cameraHandles:
        rawImageSize = cpc.determine_raw_image_size(handle)
        rawImage = create_string_buffer(rawImageSize)
        rawImageRet = cpc.get_raw_image(handle, rawImage)
        ret = PxLApi.formatImage(rawImage, rawImageRet[1],
                                 cpc.imageFormat)
        image = Image.open(io.BytesIO(ret[1]))
        imageArray = numpy.asarray(image)
        imageOpenCv = cv2.cvtColor(imageArray, cv2.COLOR_RGB2BGR)
        imageOpenCv = cv2.resize(imageOpenCv, (400,400))
        convert = QImage(imageOpenCv, imageOpenCv.shape[0], imageOpenCv.shape[1], imageOpenCv.strides[0], QImage.Format.Format_BGR888)
        pixmaps.append(convert)
    return (pixmaps[0], pixmaps[1])