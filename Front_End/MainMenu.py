from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6 import QtCore
import PreviewScreen
import StudyProfileSelectionMenu
import ShutterSpeedConfigurationMenu
import SaturationConfigurationMenu
import GainConfigurationMenu
import WhiteBalanceCalibrationMenu
import DissolvedOxygenCalibrationMenu
import phSensorCalibrationMenu
import sys
import CameraPictureControl
import databaseQuery
from datetime import datetime
import FolderStructureGenerator
import re
import os


class BaseMenuWidget(QtWidgets.QWidget):
    #Allows the button to be hightlighted when changing into it
    def showEvent(self, event):
        first_button = self.findChild(QtWidgets.QPushButton)
        if first_button:
            first_button.setFocus()


class MainMenu(object):

    def __init__(self, form):
        form.resize(800, 480)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 149, 1))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active,
                         QtGui.QPalette.ColorRole.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 110, 128))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active,
                         QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active,
                         QtGui.QPalette.ColorRole.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active,
                         QtGui.QPalette.ColorRole.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active,
                         QtGui.QPalette.ColorRole.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active,
                         QtGui.QPalette.ColorRole.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 149, 1))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active,
                         QtGui.QPalette.ColorRole.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active,
                         QtGui.QPalette.ColorRole.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(89, 239, 150))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active,
                         QtGui.QPalette.ColorRole.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active,
                         QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active,
                         QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active,
                         QtGui.QPalette.ColorRole.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active,
                         QtGui.QPalette.ColorRole.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 149, 1))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active,
                         QtGui.QPalette.ColorRole.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active,
                         QtGui.QPalette.ColorRole.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active,
                         QtGui.QPalette.ColorRole.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active,
                         QtGui.QPalette.ColorRole.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 127))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active,
                         QtGui.QPalette.ColorRole.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 149, 1))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive,
                         QtGui.QPalette.ColorRole.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 110, 128))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive,
                         QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive,
                         QtGui.QPalette.ColorRole.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive,
                         QtGui.QPalette.ColorRole.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive,
                         QtGui.QPalette.ColorRole.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive,
                         QtGui.QPalette.ColorRole.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 149, 1))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive,
                         QtGui.QPalette.ColorRole.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive,
                         QtGui.QPalette.ColorRole.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(89, 239, 150))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive,
                         QtGui.QPalette.ColorRole.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive,
                         QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive,
                         QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive,
                         QtGui.QPalette.ColorRole.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive,
                         QtGui.QPalette.ColorRole.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 149, 1))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive,
                         QtGui.QPalette.ColorRole.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive,
                         QtGui.QPalette.ColorRole.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive,
                         QtGui.QPalette.ColorRole.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive,
                         QtGui.QPalette.ColorRole.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 127))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive,
                         QtGui.QPalette.ColorRole.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled,
                         QtGui.QPalette.ColorRole.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 110, 128))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled,
                         QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled,
                         QtGui.QPalette.ColorRole.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled,
                         QtGui.QPalette.ColorRole.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled,
                         QtGui.QPalette.ColorRole.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled,
                         QtGui.QPalette.ColorRole.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled,
                         QtGui.QPalette.ColorRole.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled,
                         QtGui.QPalette.ColorRole.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled,
                         QtGui.QPalette.ColorRole.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled,
                         QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled,
                         QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled,
                         QtGui.QPalette.ColorRole.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 149, 1))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled,
                         QtGui.QPalette.ColorRole.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled,
                         QtGui.QPalette.ColorRole.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled,
                         QtGui.QPalette.ColorRole.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled,
                         QtGui.QPalette.ColorRole.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0, 127))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled,
                         QtGui.QPalette.ColorRole.PlaceholderText, brush)
        form.setPalette(palette)
        self.stackedLayout = QtWidgets.QStackedLayout()
        self.previewScreen = PreviewScreen.Ui_Form()
        self.previewScreenForm = BaseMenuWidget()
        self.previewScreen.setupUi(self.previewScreenForm)
        self.stackedLayout.addWidget(self.previewScreenForm)
        self.studyProfileSelectionMenu = StudyProfileSelectionMenu.Ui_Form()
        self.studyProfileSelectionMenuForm = BaseMenuWidget()
        self.studyProfileSelectionMenu.setupUi(
            self.studyProfileSelectionMenuForm)
        self.stackedLayout.addWidget(self.studyProfileSelectionMenuForm)
        self.shutterSpeedSelectionMenu = ShutterSpeedConfigurationMenu.Ui_Form(
        )
        self.shutterSpeedSelectionMenuForm = BaseMenuWidget()
        self.shutterSpeedSelectionMenu.setupUi(
            self.shutterSpeedSelectionMenuForm)
        self.stackedLayout.addWidget(self.shutterSpeedSelectionMenuForm)
        self.saturationConfigurationMenu = SaturationConfigurationMenu.Ui_SaturationConfigurationMenu(
        )
        self.saturationConfigurationMenuForm = BaseMenuWidget()
        self.saturationConfigurationMenu.setupUi(
            self.saturationConfigurationMenuForm)
        self.stackedLayout.addWidget(self.saturationConfigurationMenuForm)
        self.gainConfigurationMenu = GainConfigurationMenu.Ui_GainConfigurationMenu(
        )
        self.gainConfigurationMenuForm = BaseMenuWidget()
        self.gainConfigurationMenu.setupUi(self.gainConfigurationMenuForm)
        self.stackedLayout.addWidget(self.gainConfigurationMenuForm)
        self.whiteBalanceCalibrationMenu = WhiteBalanceCalibrationMenu.Ui_Form(
        )
        self.whiteBalanceCalibrationMenuForm = BaseMenuWidget()
        self.whiteBalanceCalibrationMenu.setupUi(
            self.whiteBalanceCalibrationMenuForm)
        self.stackedLayout.addWidget(self.whiteBalanceCalibrationMenuForm)
        self.dissolvedOxygenCalibrationMenu = \
            DissolvedOxygenCalibrationMenu.Ui_Form()
        self.dissolvedOxygenCalibrationMenuForm = BaseMenuWidget()
        self.dissolvedOxygenCalibrationMenu.setupUi(
            self.dissolvedOxygenCalibrationMenuForm)
        self.stackedLayout.addWidget(self.dissolvedOxygenCalibrationMenuForm)
        self.phSensorCalibrationMenu = \
            phSensorCalibrationMenu.Ui_phSensorCalibrationMenu()
        self.phSensorCalibrationMenuForm = BaseMenuWidget()
        self.phSensorCalibrationMenu.setupUi(self.phSensorCalibrationMenuForm)
        self.stackedLayout.addWidget(self.phSensorCalibrationMenuForm)
        self.stackedLayout.setCurrentIndex(0)
        self.stackedLayout.currentChanged.connect(self.changePreviewWindow)
        form.setLayout(self.stackedLayout)
        form.keyPressEvent = self.keyPressEvent
        self.studyProfileSelectionMenu.listWidget.currentItemChanged.connect(self.studyProfileSettings)
        self.cameraPictureControl = CameraPictureControl.CameraPictureControl()

    def changePreviewWindow(self):
        if self.stackedLayout.currentIndex() == 0:
            self.previewScreen.active = True
        else:
            self.previewScreen.active = False
        self.stackedLayout.setCurrentIndex(self.stackedLayout.currentIndex())

    #When a StudyProfile is chosen changes the default settings to the one on the StudyProfile
    def studyProfileSettings(self):
        studyProfile = self.studyProfileSelectionMenu.studyProfileContents[
            self.studyProfileSelectionMenu.currentStudyProfileIndex]
        self.whiteBalanceCalibrationMenu.CurrentWB.setText("White Balance: " + studyProfile["whiteBalance"])
        self.gainConfigurationMenu.CurrentGainLabel.setText("Gain: " + studyProfile["gain"])
        self.saturationConfigurationMenu.CurrentSaturationLabel.setText("Saturation: " + studyProfile["saturation"])
        self.shutterSpeedSelectionMenu.CurrentShutterSpeedLabel.setText("ShutterSpeed: " + studyProfile["shutterSpeed"])

    # When pressing F1 or F2 cycles through the menu
    def keyPressEvent(self, event):
        currentIndex = self.stackedLayout.currentIndex()
        if event.key() == Qt.Key.Key_F1:
            if currentIndex == 7:
                self.stackedLayout.setCurrentIndex(0)

            else:
                self.stackedLayout.setCurrentIndex(currentIndex + 1)

        elif event.key() == Qt.Key.Key_F2:
            if currentIndex == 0:
                self.stackedLayout.setCurrentIndex(7)
            else:
                self.stackedLayout.setCurrentIndex(currentIndex - 1)
        elif event.key(
        ) == Qt.Key.Key_Return and self.stackedLayout.currentIndex() == 0:
            self.executeStudyProfile()

        # When the menu cycles to the corresponding menu it sets the keyboard
        # focus to the widget
        if currentIndex == 1:
            self.studyProfileSelectionMenu.listWidget.setFocus()
        elif currentIndex == 2:
            self.shutterSpeedSelectionMenu.SS1250Button.setFocus()

    def executeStudyProfile(self):
        studyProfile = self.studyProfileSelectionMenu.studyProfileContents[
            self.studyProfileSelectionMenu.currentStudyProfileIndex]
        self.previewScreen.setStatusLabel(True)
        self.previewScreen.cameraControl.setExposure(
            self.previewScreen.cameraHandles,
            float(studyProfile["shutterSpeed"]))
        self.previewScreen.cameraControl.setWhiteBalance(
            self.previewScreen.cameraHandles,
            int(studyProfile["whiteBalance"]))
        dq = databaseQuery.DatabaseQuery()
        entry_id = dq.insertMediaEntry(
            studyProfile["shotType"], MainMenu.getCurrentTime(),
            studyProfile["illuminationType"], float(studyProfile["gain"]),
            int(studyProfile["saturation"]),
            MainMenu.validate_shutterSpeed(studyProfile["shutterSpeed"]),
            int(studyProfile["whiteBalance"]))
        media_entry = dq.getMediaEntrybyId(entry_id)
        fsg = FolderStructureGenerator.FolderStructureGenerator()
        path = os.path.join(fsg.root_path, str(media_entry))
        fsg.create_folder_structure(entry_id)
        if studyProfile["shotType"] == "SINGLE":
            media_metadata = dq.insertMediaMetadata(entry_id, path, "jpg",
                                                    MainMenu.getCurrentTime(),
                                                    95.5, 100, 8, 0.5)
            media_metadata = dq.getMediaMetadatabyId(entry_id)
            self.cameraPictureControl.get_snapshot(
                self.previewScreen.cameraHandles[0],
                media_metadata.left_Camera_Media)
            self.cameraPictureControl.get_snapshot(
                self.previewScreen.cameraHandles[1],
                media_metadata.right_Camera_Media)
            print("test captured")
        elif studyProfile["shotType"] == "BURST":
            for _ in range(int(studyProfile["shotCount"])):
                media_metadata = dq.insertMediaMetadata(
                    entry_id, path, "jpg", MainMenu.getCurrentTime(), 95.5,
                    100, 8, 0.5)
                media_metadata = dq.getMediaMetadatabyId(media_entry)
                self.cameraPictureControl.get_snapshot(
                    self.previewScreen.cameraHandles[0],
                    media_metadata.left_Camera_Media)
                self.cameraPictureControl.get_snapshot(
                    self.previewScreen.cameraHandles[1],
                    media_metadata.right_Camera_Media)
        elif studyProfile["shotType"] == "TIMELAPSE":
            pass
        elif studyProfile["shotType"] == "TELESCOPIC":
            pass
        elif studyProfile["shotType"] == "VIDEO":
            pass
        self.previewScreen.setStatusLabel(False)
        fsg.exportMetadata(entry_id)

    @staticmethod
    def getCurrentTime() -> str:
        """Return current time in 'yyyy-MM-ddTHH:mm:ss.zzz' format."""
        date = datetime.now()
        return date.strftime('%Y-%m-%-dT%H:%M:%S.%f')

    @staticmethod
    def validate_shutterSpeed(field):
        shutterSpeed = field.data
        if re.match(r"^\d+\/\d+$", shutterSpeed):
            numerator = int(shutterSpeed.split("/")[0])
            denominator = int(shutterSpeed.split("/")[1])
            return numerator / denominator
        else:
            return float(field)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    form = QtWidgets.QWidget()
    ui = MainMenu(form)
    form.show()
    sys.exit(app.exec())
