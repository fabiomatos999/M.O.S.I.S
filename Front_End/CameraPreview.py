import CameraPictureControl
import CameraControl
from pixelinkwrapper import PxLApi


def getPreviewImage(hCamera: [int], path: str) -> str:
    cpc = CameraPictureControl.CameraPictureControl()
    cc = CameraControl.CameraControl()
    cc.setRegionOfInterest(hCamera, 1096, 772, 400, 400)
    cpc.get_snapshot(hCamera[0], (path + str(hCamera[0])))
    cpc.get_snapshot(hCamera[1], (path + str(hCamera[1])))
    cc.setRegionOfInterest(hCamera)
    return path
