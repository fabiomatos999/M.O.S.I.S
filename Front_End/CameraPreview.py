import CameraPictureControl
import cv2
import time


def getPreviewImage(hCamera, path: str, cameraNumber: int) -> str:
    cpc = CameraPictureControl.CameraPictureControl()
    cpc.get_snapshot(hCamera, (path + str(cameraNumber)))
    img = cv2.imread("Media/Images/" + (path + str(cameraNumber)) + ".jpeg")
    img = cv2.resize(img, (400, 400))
    cv2.imwrite((path + str(cameraNumber) + ".jpeg"), img)
    return path
