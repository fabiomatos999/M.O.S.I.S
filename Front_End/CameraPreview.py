import CameraPictureControl
import CameraControl
import cv2


def getPreviewImage(hCamera: [int], path: str) -> str:
    cpc = CameraPictureControl.CameraPictureControl()
    cc = CameraControl.CameraControl()
    print(hCamera)
    #cc.setRegionOfInterest(hCamera, 1096, 772, 400, 400)
    lCamName = path + str(hCamera[0]) + ".jpeg"
    rCamName = path + str(hCamera[1]) + ".jpeg"
    cpc.get_snapshot(hCamera[0], lCamName)
    cpc.get_snapshot(hCamera[1], rCamName)
    lImg = cv2.imread(lCamName)
    lImg = cv2.resize(lImg, (400, 400))
    cv2.imwrite(lCamName, lImg)
    rImg = cv2.imread(rCamName)
    rImg = cv2.resize(rImg, (400, 400))
    cv2.imwrite(rCamName, rImg)
    return path
