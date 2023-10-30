"""PyQt6 Widget for displaying camera preview."""
from pixelinkWrapper import PxLApi
import time
import sys

from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget
from PyQt6.QtCore import QThread


class PreviewWidget(QWidget):
    """Main widget for spawning and starting PixeLink Camera preview."""

    def __init__(self, parent=None):
        """Initialize the parent window and starts the camera preview."""
        super().__init__(parent)
        self.previewWindow = PreviewWindow(self)
        self.vboxLayout = QVBoxLayout()
        self.vboxLayout.addWidget(self.previewWindow)
        self.setLayout(self.vboxLayout)
        self._startCamera()

    def _startCamera(self):
        # Set up the camera and start the stream
        ret = PxLApi.initialize(0)
        if PxLApi.apiSuccess(ret[0]):
            self.hCamera = ret[1]
            # Just use all of the camera's current settings.
            # Start the stream and preview
            ret = PxLApi.setStreamState(self.hCamera, PxLApi.StreamState.START)
            if PxLApi.apiSuccess(ret[0]):
                self._startPreview()

    def _startPreview(self):
        self.previewWindow.previewState = PxLApi.PreviewState.START
        self.previewWindow.previewThread.start()

    def _stopCamera(self):
        # The user has quit the appliation, shut down the preview and stream
        self.previewWindow.previewState = PxLApi.PreviewState.STOP
        # Give preview a bit of time to stop
        time.sleep(0.05)

        PxLApi.setStreamState(self.hCamera, PxLApi.StreamState.STOP)

        PxLApi.uninitialize(self.hCamera)

    def exitApp(self):
        """Call super class to close widget properly."""
        self.close()

    def closeEvent(self, event):
        """Once the user has quit the application, stop using the camera."""
        self._stopCamera()
        return super().closeEvent(event)


class PreviewWindow(QWidget):
    """Contain the windows ID and process thread object."""

    def __init__(self, parent=None):
        """Assign parent and create thread object for preview."""
        super().__init__(parent)
        self.mainWindow = parent
        self.winId = int(self.winId())
        self.previewState = PxLApi.PreviewState.STOP  # default preview state
        self.previewThread = ControlPreview(self)

    # Window resize handler
    def resizeEvent(self, event):
        """Set the preview size of the widget."""
        hCamera = self.mainWindow.hCamera
        width = event.size().width()
        height = event.size().height()
        previewHwnd = self.winId
        PxLApi.setPreviewSettings(
            hCamera, "",
            PxLApi.WindowsPreview.WS_VISIBLE | PxLApi.WindowsPreview.WS_CHILD,
            0, 0, width, height, previewHwnd)


"""
Preview control QThread -- starts and stops the preview of the preview window.
"""


class ControlPreview(QThread):
    """Process thread for previewing the camera."""

    def __init__(self, parent=None):
        """Assign parent and start QThread constructor."""
        super().__init__()
        self.previewWindow = parent

    def run(self):
        """Override of run method for QThread, ran when start method is run."""
        self._runPreview()

    def _runPreview(self):
        """Start preview for the camera in a process thread.

        Will run until previewState of the camera is not Stopped.
        """
        # Get the current dimensions of the Preview Window
        hCamera = self.previewWindow.mainWindow.hCamera
        width = self.previewWindow.size().width()
        height = self.previewWindow.size().height()
        previewHwnd = self.previewWindow.winId

        # Start the stream in case the camera is not streaming
        ret = PxLApi.setStreamState(hCamera, PxLApi.StreamState.START)
        assert PxLApi.apiSuccess(ret[0]), "%i" % ret[0]

        # Set preview settings
        ret = PxLApi.setPreviewSettings(
            hCamera, "",
            PxLApi.WindowsPreview.WS_VISIBLE | PxLApi.WindowsPreview.WS_CHILD,
            0, 0, width, height, previewHwnd)
        """Start the preview (NOTE: camera must be streaming).
        Keep looping until the previewState is Stopped."""
        ret = PxLApi.setPreviewState(hCamera, PxLApi.PreviewState.START)
        while (PxLApi.PreviewState.START == self.previewWindow.previewState
               and PxLApi.apiSuccess(ret[0])):
            #     user32.TranslateMessage(pMsg)
            #     user32.DispatchMessageW(pMsg)
            continue

        # User has exited -- Stop the preview
        ret = PxLApi.setPreviewState(hCamera, PxLApi.PreviewState.STOP)
        assert PxLApi.apiSuccess(ret[0]), "%i" % ret[0]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    parent = QWidget()
    mainWin = PreviewWidget()(parent=parent)
    parent.show()
    sys.exit(app.exec())
