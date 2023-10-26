from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import QThread
from pixelinkWrapper import PxLApi
import time

class PreviewWindow(QWidget):

    def __init__(self, parent, cameraHandle: int):
        super().__init__(parent)
        self.mainWindow = parent
        self.cameraHandle = cameraHandle
        self.winId = int(self.winId())
        self.previewState = PxLApi.PreviewState.STOP
        self.previewThread = ControlPreview(self)

    def closeEvent(self, event):
        self.previewState = PxLApi.PreviewState.STOP
        time.sleep(0.05)
        PxLApi.setStreamState(self.cameraHandle, PxLApi.StreamState.STOP)
        PxLApi.uninitialize(self.cameraHandle)


class ControlPreview(QThread):

    def __init__(self, parent):
        super().__init__()
        self.previewWindow = parent

        def runPreview(self):
            PxLApi.setStreamState(self.previewWindow.cameraHandle,
                                  PxLApi.StreamState.START)
            PxLApi.setPreviewSettings(
                self.previewWindow.cameraHandle, "",
                PxLApi.WindowsPreview.WS_VISIBLE
                | PxLApi.WindowsPreview.WS_CHILD, 0, 0, 400, 400,

                self.previewWindow.winId)
            ret = PxLApi.setPreviewState(self.previewWindow.cameraHandle,
                                         PxLApi.PreviewState.START)
            while (PxLApi.PreviewState.START == self.previewWindow.previewState
                   and PxLApi.apiSuccess(ret[0])):
                pass
            PxLApi.setPreviewState(self.previewWindow.cameraHandle,
                                   PxLApi.PreviewState.STOP)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    form = QWidget()
    ui = PreviewWindow(form, [1])
    form.show()
    sys.exit(app.exec())
