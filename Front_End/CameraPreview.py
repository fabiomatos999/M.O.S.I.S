"""Image manipulation module for preview screen."""
import CameraPictureControl
import cv2


def getPreviewImage(cameraHandles: [int], folderPath: str) -> str:
    """Generate preview screen images and resize images to 400x400.

    :param cameraHandles list of camera handles from the
    PxLApi initialize function
    :param folderPath folder where the preview screen images will
    be outputted
    """
    cpc = CameraPictureControl.CameraPictureControl()
    lCamName = folderPath + str(cameraHandles[0]) + ".jpeg"
    rCamName = folderPath + str(cameraHandles[1]) + ".jpeg"
    cpc.get_snapshot(cameraHandles[0], lCamName)
    cpc.get_snapshot(cameraHandles[1], rCamName)
    lImg = cv2.imread(lCamName)
    lImg = cv2.resize(lImg, (400, 400))
    cv2.imwrite(lCamName, lImg)
    rImg = cv2.imread(rCamName)
    rImg = cv2.resize(rImg, (400, 400))
    cv2.imwrite(rCamName, rImg)
    return folderPath
