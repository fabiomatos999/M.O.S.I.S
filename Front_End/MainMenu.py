"""Main Menu for the M.O.S.I.S UI.

Contains preview screen, study select menu,
gain, shutter speed, saturation, white balance control menus,
pH sensor calibration menu and dissolved oxygen sensor calibration menu.
"""
from PyQt6 import QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6 import QtCore
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import QEvent
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
import HallEffectSensor
import RPi.GPIO as GPIO
import subprocess
import time


class BaseMenuWidget(QtWidgets.QWidget):
    """Wrapper class for screens to enable highlighting elements.

    Allows the button to be highlighted when changing into it
    """

    def showEvent(self, event):
        """Set focus on next child element within a screen."""
        first_button = self.findChild(QtWidgets.QPushButton)
        if first_button:
            first_button.setFocus()


class MainMenu(object):
    """Hold all screens and spawn application."""

    def __init__(self, form):
        """Initialize cameras, connect to GPIO, load study profile.

        :param form QWidget parent object.
        The form will show the user interface.
        """
        form.resize(800, 480)
        self.form = form
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
        self.saturationConfigurationMenu = \
            SaturationConfigurationMenu.Ui_SaturationConfigurationMenu()
        self.saturationConfigurationMenuForm = BaseMenuWidget()
        self.saturationConfigurationMenu.setupUi(
            self.saturationConfigurationMenuForm)
        self.stackedLayout.addWidget(self.saturationConfigurationMenuForm)
        self.gainConfigurationMenu = \
            GainConfigurationMenu.Ui_GainConfigurationMenu()
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
        self.studyProfileSelectionMenu.listWidget.currentItemChanged.connect(
            self.studyProfileSettings)
        self.cameraPictureControl = CameraPictureControl.CameraPictureControl()
        self.hallEffectSensors = []
        GPIO.setmode(GPIO.BCM)
        self.hallEffectSensors.append(
            HallEffectSensor.HallEffectSensor(17, self.decodeGPIOtoKeyPress))
        self.hallEffectSensors.append(
            HallEffectSensor.HallEffectSensor(27, self.decodeGPIOtoKeyPress))
        self.hallEffectSensors.append(
            HallEffectSensor.HallEffectSensor(5, self.decodeGPIOtoKeyPress))
        self.hallEffectSensors.append(
            HallEffectSensor.HallEffectSensor(6, self.decodeGPIOtoKeyPress))
        self.hallEffectSensors.append(
            HallEffectSensor.HallEffectSensor(26, self.decodeGPIOtoKeyPress))
        self.hallEffectSensors.append(
            HallEffectSensor.HallEffectSensor(23, self.decodeGPIOtoKeyPress))
        self.hallEffectSensors.append(
            HallEffectSensor.HallEffectSensor(24, self.decodeGPIOtoKeyPress))
        self.hallEffectSensors.append(
            HallEffectSensor.HallEffectSensor(25, self.decodeGPIOtoKeyPress))
        self.focusPoint1 = None
        self.focusPoint2 = None
        self.whiteLED = GPIO.setup(2, GPIO.OUT)
        self.redLED = GPIO.setup(3, GPIO.OUT)
        self.uvLED = GPIO.setup(4, GPIO.OUT)

    def decodeGPIOtoKeyPress(self, pin: int):
        """Decode Raspberry Pi GPIO interrupt into a QKeyEvent.

        Serve as the callback function for the GPIO pins.
        The physical layout of the Hall effect sensors and
        the GPIO pins are as follows:

        17  --> |-------------| <--  26
        27  --> |             | <--  23
        5   --> |   Display   | <--  24
        6   --> |_____________| <--  25

        Note: Will ignore GPIO interrupts that are not bound to the Hall effect
        sensors.
        """
        key_event = None
        if GPIO.input(17) and GPIO.input(6):
            now = time.time()
            while GPIO.input(17) and GPIO.input(6):
                if time.time() - now > 3:
                    subprocess.call(["sudo", "shutdown", "now"])
            return
        if pin == 17:
            key_event = QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_Up,
                                  Qt.KeyboardModifier(0), "Up")
        elif pin == 27:
            key_event = QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_Left,
                                  Qt.KeyboardModifier(0), "Left")
        elif pin == 5:
            self.form.keyPressEvent.emit(Qt.Key.Key_Right)
            key_event = QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_Right,
                                  Qt.KeyboardModifier(0), "Right")
        elif pin == 6:
            key_event = QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_Down,
                                  Qt.KeyboardModifier(0), "Down")
        elif pin == 26:
            key_event = QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_F1,
                                  Qt.KeyboardModifier(0), "F1")
        elif pin == 23:
            key_event = QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_Enter,
                                  Qt.KeyboardModifier(0), "Enter")
        elif pin == 24:
            self.form.keyPressEvent.emit(Qt.Key.Key_Q)
            key_event = QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_Q,
                                  Qt.KeyboardModifier(0), "Q")
        elif pin == 25:
            key_event = QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_F2,
                                  Qt.KeyboardModifier(0), "F2")
        else:
            return
        QtWidgets.QApplication.sendEvent(self.form, key_event)

    def changePreviewWindow(self):
        """Disable camera preview when preview screen is not visible."""
        if self.stackedLayout.currentIndex() == 0:
            self.previewScreen.active = True
        else:
            self.previewScreen.active = False
        self.stackedLayout.setCurrentIndex(self.stackedLayout.currentIndex())

    def studyProfileSettings(self):
        """Change labels on other screens when a study profile overrides them.

        When a StudyProfile is chosen changes the default settings to the
        one on the StudyProfile
        """
        studyProfile = self.studyProfileSelectionMenu.studyProfileContents[
            self.studyProfileSelectionMenu.currentStudyProfileIndex]
        gain = float(studyProfile["gain"])
        gain = int(gain * 10)
        self.whiteBalanceCalibrationMenu.CurrentWB.setText(
            "White Balance: " + studyProfile["whiteBalance"])
        self.whiteBalanceCalibrationMenu.WBSlider.setValue(
            int(studyProfile["whiteBalance"]))
        self.gainConfigurationMenu.CurrentGainLabel.setText(
            "Gain: " + studyProfile["gain"])
        self.gainConfigurationMenu.horizontalSlider.setValue(gain)
        self.saturationConfigurationMenu.CurrentSaturationLabel.setText(
            "Saturation: " + studyProfile["saturation"])
        self.saturationConfigurationMenu.horizontalSlider.setValue(
            int(studyProfile["saturation"]))
        self.shutterSpeedSelectionMenu.CurrentShutterSpeedLabel.setText(
            "ShutterSpeed: " + studyProfile["shutterSpeed"])

    def keyPressEvent(self, event):
        """Override of key press event handler in QWidget class.

        Pressing F1 and F2 cycles through the menus.
        """
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
        elif event.key() == Qt.Key.Key_Q:
            if self.focusPoint1 is None:
                pass
            elif self.focusPoint2 is None:
                pass

        # When the menu cycles to the corresponding menu it sets the keyboard
        # focus to the widget
        if currentIndex == 1:
            self.studyProfileSelectionMenu.listWidget.setFocus()
        elif currentIndex == 2:
            self.shutterSpeedSelectionMenu.SS1250Button.setFocus()

    def executeStudyProfile(self):
        """Execute currently selected study profile.

        Will change the shutter speed and white balance of the cameras.
        Executes single, burst, time lapse, telescopic or video depending
        on the shot type defined in the study profile, created by the host
        software.
        """
        studyProfile = self.studyProfileSelectionMenu.studyProfileContents[
            self.studyProfileSelectionMenu.currentStudyProfileIndex]
        self.previewScreen.setStatusLabel(True)
        self.previewScreen.cameraControl.setExposure(
            self.previewScreen.cameraHandles,
            MainMenu.decodeShutterSpeed(studyProfile["shutterSpeed"]))
        self.previewScreen.cameraControl.setWhiteBalance(
            self.previewScreen.cameraHandles,
            int(studyProfile["whiteBalance"]))
        illuminationType = studyProfile["illuminationType"]
        GPIO.output(2, GPIO.LOW)
        GPIO.output(3, GPIO.LOW)
        GPIO.output(4, GPIO.LOW)
        if illuminationType == "WHITE":
            GPIO.output(2, GPIO.HIGH)
        elif illuminationType == "RED":
            GPIO.output(3, GPIO.HIGH)
        elif illuminationType == "ULTRAVIOLET":
            GPIO.output(4, GPIO.HIGH)
        dq = databaseQuery.DatabaseQuery()
        entry_id = dq.insertMediaEntry(
            studyProfile["shotType"], MainMenu.getCurrentTime(),
            studyProfile["illuminationType"], float(studyProfile["gain"]),
            int(studyProfile["saturation"]),
            MainMenu.decodeShutterSpeed(studyProfile["shutterSpeed"]),
            int(studyProfile["whiteBalance"]))
        media_entry = dq.getMediaEntrybyId(entry_id)
        fsg = FolderStructureGenerator.FolderStructureGenerator()
        path = os.path.join(fsg.root_path, str(media_entry))
        fsg.create_folder_structure(entry_id)

        if studyProfile["shotType"] == "SINGLE":
            media_metadata = dq.insertMediaMetadata(entry_id, path, "jpg",
                                                    MainMenu.getCurrentTime(),
                                                    95.5, 100, 8, 0.5)
            media_metadata = dq.getMediaMetadatabyId(media_metadata)
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
                media_metadata = dq.getMediaMetadatabyId(media_metadata)
                self.cameraPictureControl.get_snapshot(
                    self.previewScreen.cameraHandles[0],
                    media_metadata.left_Camera_Media)
                self.cameraPictureControl.get_snapshot(
                    self.previewScreen.cameraHandles[1],
                    media_metadata.right_Camera_Media)
        elif studyProfile["shotType"] == "TIMELAPSE":
            time = float(studyProfile["time"])
            photoCount = int(studyProfile["photoCount"])
            self.cameraPictureControl.getIntervalSnapshot(
                self.previewScreen.cameraHandles, time, photoCount, entry_id,
                path)
        elif studyProfile["shotType"] == "TELESCOPIC":
            steps = int(studyProfile["zoomOutCount"])
            if self.focusPoint1 < self.focusPoint2:
                temp = self.focusPoint1
                self.focusPoint1 = self.focusPoint2
                self.focusPoint2 = temp
            for focus in range(self.focusPoint1, self.focusPoint2, steps):
                self.previewScreen.cameraControl.setExposure(
                    self.previewScreen.cameraHandles, focus, "")

                media_metadata = dq.insertMediaMetadata(
                    entry_id, path, "jpg", MainMenu.getCurrentTime(), 95.5,
                    100, 8, 0.5)
                media_metadata = dq.getMediaMetadatabyId(media_metadata)
                self.cameraPictureControl.get_snapshot(
                    self.previewScreen.cameraHandles[0],
                    media_metadata.left_Camera_Media)
                self.cameraPictureControl.get_snapshot(
                    self.previewScreen.cameraHandles[1],
                    media_metadata.right_Camera_Media)
        elif studyProfile["shotType"] == "VIDEO":
            videoLength = int(float(studyProfile["videoLength"]) * 60.0)
            self.cameraPictureControl.getVideo(
                self.previewScreen.cameraHandles, entry_id, path, videoLength)

        self.previewScreen.setStatusLabel(False)
        fsg.exportMetadata(entry_id)
        GPIO.output(2, GPIO.LOW)
        GPIO.output(3, GPIO.LOW)
        GPIO.output(4, GPIO.LOW)

    @staticmethod
    def getCurrentTime() -> str:
        """Return current time in 'yyyy-MM-ddTHH-mm-ss.zzz' format."""
        date = datetime.now()
        return date.strftime('%Y-%m-%-dT%H-%M-%S.%f')

    @staticmethod
    def decodeShutterSpeed(shutterSpeed: str) -> float:
        """Convert either fractional or floating point string into float.

        :param shutterSpeed The string representation of a fraction
        (i.e "1/60") or a string of a floating point number.

        Note: If the shutter speed string given to the function
        cannot be coerced into a float, it will return a NaN.
        """
        shutterSpeed = shutterSpeed
        if re.match(r"^\d+\/\d+$", shutterSpeed):
            numerator = int(shutterSpeed.split("/")[0])
            denominator = int(shutterSpeed.split("/")[1])
            return numerator / denominator
        else:
            return float(shutterSpeed)

    def getCurrentShutterSpeed(self) -> str:
        """Return current shutterspeed from the shutterspeed config menu."""
        string = self.shutterSpeedSelectionMenu.CurrentShutterSpeedLabel.text()
        string = string.replace(" ", "")
        strings = string.split(":")
        shutterspeed = strings[1]
        return shutterspeed

    def getCurrentGain(self) -> float:
        """Return current gain from the gain configuration menu."""
        string = self.gainConfigurationMenu.CurrentGainLabel.text()
        string = string.replace(" ", "")
        strings = string.split(":")
        gain = float(strings[1])
        return gain

    def getCurrentWhiteBalance(self) -> int:
        """Return current whitebalance from the whitebalance config menu."""
        string = self.whiteBalanceCalibrationMenu.CurrentWB.text()
        string = string.replace(" ", "")
        string = string.replace("K", "")
        strings = string.split(":")
        whitebalance = int(strings[1])
        return whitebalance

    def getCurrentSaturation(self) -> float:
        """Return current saturation from the saturation configuration menu."""
        string = self.saturationConfigurationMenu.CurrentSaturationLabel.text()
        string = string.replace(" ", "")
        strings = string.split(":")
        saturation = float(strings[1])
        return saturation


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    form = QtWidgets.QWidget()
    ui = MainMenu(form)
    form.showFullScreen()
    sys.exit(app.exec())
