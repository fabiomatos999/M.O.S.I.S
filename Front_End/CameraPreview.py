import CameraPictureControl
import CameraControl
from pixelinkwrapper import PxLApi


def getPreviewImage(hCamera: [int], path: str) -> str:
    cpc = CameraPictureControl.CameraPictureControl()
    cc = CameraControl.CameraControl()
    cc.setRegionOfInterest(hCamera, 1096, 772, 400, 400)
    cpc.get_snapshot(hCamera, (path + str(hCamera[0])))
    cc.setRegionOfInterest(hCamera)
    return path
