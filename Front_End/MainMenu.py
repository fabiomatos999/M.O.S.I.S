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
import sensor
import time as timer


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
        global mainMenuForm
        mainMenuForm = self.form
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
        self.shutterSpeedSelectionMenu = \
            PreviewScreen.Ui_ShutterSpeedConfigMenu()
        self.shutterSpeedSelectionMenuForm = BaseMenuWidget()
        self.shutterSpeedSelectionMenu.setupUi(
            self.shutterSpeedSelectionMenuForm)
        self.stackedLayout.addWidget(self.shutterSpeedSelectionMenuForm)
        self.saturationConfigurationMenu = \
            PreviewScreen.Ui_SaturationConfigurationMenu()
        self.saturationConfigurationMenuForm = BaseMenuWidget()
        self.saturationConfigurationMenu.setupUi(
            self.saturationConfigurationMenuForm)
        self.stackedLayout.addWidget(self.saturationConfigurationMenuForm)
        self.gainConfigurationMenu = \
            PreviewScreen.Ui_GainConfigurationMenu()
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
        self.lightingIndex = 0

    def cycleLighting(self):
        """Cycle through lighting when function is called."""
        GPIO.output(2, GPIO.LOW)
        GPIO.output(3, GPIO.LOW)
        GPIO.output(4, GPIO.LOW)
        self.lightingIndex += 1
        self.lightingIndex %= 4
        if self.lightingIndex == 1:
            GPIO.output(2, GPIO.HIGH)
        elif self.lightingIndex == 2:
            GPIO.output(3, GPIO.HIGH)
        elif self.lightingIndex == 3:
            GPIO.output(4, GPIO.HIGH)

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
        if GPIO.input(27) == GPIO.LOW:
            now = time.time()
            while GPIO.input(27) == GPIO.LOW:
                if time.time() - now > 5:
                    subprocess.call(["sudo", "shutdown", "-h", "now"])
            return
        if pin == 17:
            key_event = QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_W,
                                  Qt.KeyboardModifier(0), "W")
            time.sleep(0.5)
            while GPIO.input(27) == GPIO.LOW:
                QtWidgets.QApplication.sendEvent(self.form, key_event)
                time.sleep(0.01)
        elif pin == 27:
            key_event = QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_A,
                                  Qt.KeyboardModifier(0), "A")
        elif pin == 5:
            key_event = QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_D,
                                  Qt.KeyboardModifier(0), "D")
        elif pin == 6:
            key_event = QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_S,
                                  Qt.KeyboardModifier(0), "S")
            while GPIO.input(6) == GPIO.LOW:
                QtWidgets.QApplication.sendEvent(self.form, key_event)
                time.sleep(0.01)
        elif pin == 26:
            key_event = QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_F1,
                                  Qt.KeyboardModifier(0), "F1")
        elif pin == 23:
            key_event = QKeyEvent(QEvent.Type.KeyPress, Qt.Key.Key_Return,
                                  Qt.KeyboardModifier(0), "Return")
        elif pin == 24:
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
        self.shutterSpeedSelectionMenu.label.setText(
            "ShutterSpeed: " + studyProfile["shutterSpeed"])

    def keyPressEvent(self, event):
        """Override of key press event handler in QWidget class.

        Pressing F1 and F2 cycles through the menus.
        """
        currentIndex = self.stackedLayout.currentIndex()
        if event.key() == Qt.Key.Key_W and currentIndex == 0:
            self.previewScreen.cameraControl.setFocus(
                self.previewScreen.cameraHandles,
                self.previewScreen.cameraControl.customFocus[0] + 20, "")
            print(self.previewScreen.cameraControl.customFocus[0])
        elif event.key() == Qt.Key.Key_W and currentIndex == 1:
            if (self.studyProfileSelectionMenu.isValidIndex(
                    self.studyProfileSelectionMenu.currentStudyProfileIndex -
                    1)):
                self.studyProfileSelectionMenu.listWidget.setCurrentItem(
                    self.studyProfileSelectionMenu.listWidget.item(
                        self.studyProfileSelectionMenu.currentStudyProfileIndex
                        - 1))
            return
        elif event.key() == Qt.Key.Key_D and currentIndex == 0:
            self.cycleLighting()
        elif event.key() == Qt.Key.Key_S and currentIndex == 1:
            if (self.studyProfileSelectionMenu.isValidIndex(
                    self.studyProfileSelectionMenu.currentStudyProfileIndex +
                    1)):
                self.studyProfileSelectionMenu.listWidget.setCurrentItem(
                    self.studyProfileSelectionMenu.listWidget.item(
                        self.studyProfileSelectionMenu.currentStudyProfileIndex
                        + 1))
            return
        elif event.key() == Qt.Key.Key_S and currentIndex == 0:
            self.previewScreen.cameraControl.setFocus(
                self.previewScreen.cameraHandles,
                self.previewScreen.cameraControl.customFocus[0] - 20, "")
            print(self.previewScreen.cameraControl.customFocus[0])

        if event.key() == Qt.Key.Key_W and currentIndex == 2:
            if (self.shutterSpeedSelectionMenu.isValidIndex(
                    self.shutterSpeedSelectionMenu.currentShutterSpeedIndex -
                    1)):
                self.shutterSpeedSelectionMenu.listWidget.setCurrentItem(
                    self.shutterSpeedSelectionMenu.listWidget.item(
                        self.shutterSpeedSelectionMenu.currentShutterSpeedIndex
                        - 1))
                return
        elif event.key() == Qt.Key.Key_S and currentIndex == 2:
            if (self.shutterSpeedSelectionMenu.isValidIndex(
                    self.shutterSpeedSelectionMenu.currentShutterSpeedIndex +
                    1)):
                self.shutterSpeedSelectionMenu.listWidget.setCurrentItem(
                    self.shutterSpeedSelectionMenu.listWidget.item(
                        self.shutterSpeedSelectionMenu.currentShutterSpeedIndex
                        + 1))
                return
        if event.key() == Qt.Key.Key_W and currentIndex == 3:
            if (self.saturationConfigurationMenu.horizontalSlider.value()
                    < 200):
                self.saturationConfigurationMenu.horizontalSlider.setValue(
                    self.saturationConfigurationMenu.horizontalSlider.value() +
                    1)

        elif event.key() == Qt.Key.Key_S and currentIndex == 3:
            if (self.saturationConfigurationMenu.horizontalSlider.value() > 0):
                self.saturationConfigurationMenu.horizontalSlider.setValue(
                    self.saturationConfigurationMenu.horizontalSlider.value() -
                    1)

        if event.key() == Qt.Key.Key_W and currentIndex == 4:
            if (self.gainConfigurationMenu.horizontalSlider.value() < 240):
                self.gainConfigurationMenu.horizontalSlider.setValue(
                    self.gainConfigurationMenu.horizontalSlider.value() + 1)

        elif event.key() == Qt.Key.Key_S and currentIndex == 4:
            if (self.gainConfigurationMenu.horizontalSlider.value() > 0):
                self.gainConfigurationMenu.horizontalSlider.setValue(
                    self.gainConfigurationMenu.horizontalSlider.value() - 1)

        if event.key() == Qt.Key.Key_W and currentIndex == 5:
            if (self.whiteBalanceCalibrationMenu.WBSlider.value() < 6500):
                self.whiteBalanceCalibrationMenu.WBSlider.setValue(
                    self.whiteBalanceCalibrationMenu.WBSlider.value() + 10)

        elif event.key() == Qt.Key.Key_S and currentIndex == 5:
            if (self.whiteBalanceCalibrationMenu.WBSlider.value() > 3200):
                self.whiteBalanceCalibrationMenu.WBSlider.setValue(
                    self.whiteBalanceCalibrationMenu.WBSlider.value() - 10)

        elif event.key() == Qt.Key.Key_W and currentIndex == 6:
            self.dissolvedOxygenCalibrationMenu.CalibrateZeroCal.clicked.emit()

        elif event.key() == Qt.Key.Key_A and currentIndex == 6:
            self.dissolvedOxygenCalibrationMenu.CalibrateAtmoCal.clicked.emit()

        elif event.key() == Qt.Key.Key_D and currentIndex == 6:
            self.dissolvedOxygenCalibrationMenu.Clear.clicked.emit()

        elif event.key() == Qt.Key.Key_W and currentIndex == 7:
            self.phSensorCalibrationMenu.LowPointCal.clicked.emit()

        elif event.key() == Qt.Key.Key_A and currentIndex == 7:
            self.phSensorCalibrationMenu.MidPointCal.clicked.emit()

        elif event.key() == Qt.Key.Key_D and currentIndex == 7:
            self.phSensorCalibrationMenu.HighPointCal.clicked.emit()

        elif event.key() == Qt.Key.Key_F1:
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

        elif event.key() == Qt.Key.Key_Q and currentIndex != 0:
            self.cameraPictureControl.stopStudy = True
            time.sleep(4)
            self.cameraPictureControl.stopStudy = False
        elif event.key() == Qt.Key.Key_Q:
            if self.focusPoint1 is None:
                self.focusPoint1 = \
                    self.previewScreen.cameraControl.customFocus[0]
                self.previewScreen.status_label.setText("FP1 Set")
            elif self.focusPoint2 is None and self.previewScreen.cameraControl.customFocus[
                    0] != self.focusPoint1:
                self.focusPoint2 = \
                    self.previewScreen.cameraControl.customFocus[0]
                self.previewScreen.status_label.setText("FP2 Set")

        # When the menu cycles to the corresponding menu it sets the keyboard
        # focus to the widget
        # self.unfocus_widgets()
        if currentIndex == 1:
            self.studyProfileSelectionMenuForm.setEnabled(True)
            self.studyProfileSelectionMenu.listWidget.setFocus()

        elif currentIndex == 2:
            self.shutterSpeedSelectionMenuForm.setEnabled(True)
            self.shutterSpeedSelectionMenu.listWidget.setFocus()

        elif currentIndex == 3:
            self.saturationConfigurationMenuForm.setEnabled(True)
            self.saturationConfigurationMenu.horizontalSlider.setFocus()

        elif currentIndex == 4:
            self.gainConfigurationMenuForm.setEnabled(True)
            self.gainConfigurationMenu.horizontalSlider.setFocus()

        elif currentIndex == 5:
            self.whiteBalanceCalibrationMenuForm.setEnabled(True)
            self.whiteBalanceCalibrationMenu.WBSlider.setFocus()

        elif currentIndex == 6:
            self.dissolvedOxygenCalibrationMenuForm.setEnabled(True)
            self.dissolvedOxygenCalibrationMenu.doZeroCal.setFocus()

        elif currentIndex == 7:
            self.phSensorCalibrationMenuForm.setEnabled(True)
            self.phSensorCalibrationMenu.LowPointCal.setFocus()

        mainMenuForm.showFullScreen()

    def unfocus_widgets(self):
        """Clear focus of all widgets."""
        """
        self.studyProfileSelectionMenu.listWidget.setDisabled()
        self.shutterSpeedSelectionMenu.listWidget.setDisabled
        self.saturationConfigurationMenu.horizontalSlider.setDisabled()
        self.gainConfigurationMenu.horizontalSlider.setDisabled()
        self.whiteBalanceCalibrationMenu.WBSlider.setDisabled()
        self.dissolvedOxygenCalibrationMenu.doAtmoCal.setDisabled()
        self.dissolvedOxygenCalibrationMenu.doZeroCal.setDisabled()
        self.dissolvedOxygenCalibrationMenu.doZeroCal_2.setDisabled()
        self.phSensorCalibrationMenu.HighPointCal.setDisabled()
        self.phSensorCalibrationMenu.MidPointCal.setDisabled()
        self.phSensorCalibrationMenu.LowPointCal.setDisabled()
        """
        self.studyProfileSelectionMenuForm.setDisabled(True)
        self.shutterSpeedSelectionMenuForm.setDisabled(True)
        self.saturationConfigurationMenuForm.setDisabled(True)
        self.gainConfigurationMenuForm.setDisabled(True)
        self.dissolvedOxygenCalibrationMenuForm.setDisabled(True)
        self.phSensorCalibrationMenuForm.setDisabled(True)

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
        self.previewScreen.active = False
        self.previewScreen.capturing = True
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
        entry_id = dq.insertMediaEntry(studyProfile["shotType"],
                                       MainMenu.getCurrentTime(),
                                       studyProfile["illuminationType"],
                                       self.getCurrentGain(),
                                       self.getCurrentSaturation(),
                                       self.getCurrentShutterSpeed(),
                                       self.getCurrentWhiteBalance())
        media_entry = dq.getMediaEntrybyId(entry_id)
        fsg = FolderStructureGenerator.FolderStructureGenerator()
        path = os.path.join(fsg.root_path, str(media_entry))
        fsg.create_folder_structure(entry_id)

        if studyProfile["shotType"] == "SINGLE":
            media_metadata = dq.insertMediaMetadata(
                entry_id, path, "jpg", MainMenu.getCurrentTime(),
                self.previewScreen.tempReading, self.previewScreen.baroReading,
                self.previewScreen.phReading, self.previewScreen.DOreading)
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
                    entry_id, path, "jpg", MainMenu.getCurrentTime(),
                    self.previewScreen.tempReading,
                    self.previewScreen.baroReading,
                    self.previewScreen.phReading, self.previewScreen.DOreading)
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
            counter = 0
            stepInterval = (time * 60) / photoCount
            stepTime = timer.time() + stepInterval

            while counter < photoCount:
                if timer.time() > stepTime or counter == 0:
                    media_metadata = dq.insertMediaMetadata(
                        entry_id, path, "jpg", MainMenu.getCurrentTime(),
                        self.previewScreen.tempReading,
                        self.previewScreen.baroReading,
                        self.previewScreen.phReading,
                        self.previewScreen.DOreading)
                    media_metadata = dq.getMediaMetadatabyId(media_metadata)
                    GPIO.output(2, GPIO.LOW)
                    GPIO.output(3, GPIO.LOW)
                    GPIO.output(4, GPIO.LOW)
                    if illuminationType == "WHITE":
                        GPIO.output(2, GPIO.HIGH)
                    elif illuminationType == "RED":
                        GPIO.output(3, GPIO.HIGH)
                    elif illuminationType == "ULTRAVIOLET":
                        GPIO.output(4, GPIO.HIGH)
                    self.cameraPictureControl.get_snapshot(
                        self.previewScreen.cameraHandles[0],
                        media_metadata.left_Camera_Media)
                    self.cameraPictureControl.get_snapshot(
                        self.previewScreen.cameraHandles[1],
                        media_metadata.right_Camera_Media)
                    GPIO.output(2, GPIO.LOW)
                    GPIO.output(3, GPIO.LOW)
                    GPIO.output(4, GPIO.LOW)
                    stepTime = timer.time() + stepInterval
                    counter += 1

        elif studyProfile["shotType"] == "TELESCOPIC":
            steps = int(studyProfile["zoomOutCount"])
            if self.focusPoint1 is not None and self.focusPoint2 is not None:

                temp = self.focusPoint1
                self.focusPoint1 = self.focusPoint2
                self.focusPoint2 = temp
                minFocus = self.focusPoint1
                maxFocus = self.focusPoint2
                self.focuPoint2 = maxFocus
                if minFocus > maxFocus:
                    temp = minFocus
                    minFocus = maxFocus
                    maxFocus = temp
                for shot in range(steps):
                    focus = minFocus + ((maxFocus - minFocus) / steps) * shot
                    self.previewScreen.cameraControl.setExposure(
                        self.previewScreen.cameraHandles, focus, "")
                    media_metadata = dq.insertMediaMetadata(
                        entry_id, path, "jpg", MainMenu.getCurrentTime(),
                        self.previewScreen.tempReading,
                        self.previewScreen.baroReading,
                        self.previewScreen.phReading,
                        self.previewScreen.DOreading)
                    media_metadata = dq.getMediaMetadatabyId(media_metadata)
                    self.cameraPictureControl.get_snapshot(
                        self.previewScreen.cameraHandles[0],
                        media_metadata.left_Camera_Media)
                    self.cameraPictureControl.get_snapshot(
                        self.previewScreen.cameraHandles[1],
                        media_metadata.right_Camera_Media)

            self.focusPoint1 = None
            self.focusPoint2 = None
        elif studyProfile["shotType"] == "VIDEO":
            videoLength = int(float(studyProfile["videoLength"]))

            now = timer.time()
            while timer.time() < now + videoLength:
                metadata = dq.insertMediaMetadata(
                    entry_id, path, "jpg", MainMenu.getCurrentTime(),
                    self.previewScreen.tempReading,
                    self.previewScreen.baroReading,
                    self.previewScreen.phReading, self.previewScreen.DOreading)
                metadata = dq.getMediaMetadatabyId(metadata)
                self.cameraPictureControl.get_snapshot(
                    self.previewScreen.cameraHandles[0],
                    metadata.left_Camera_Media)
                self.cameraPictureControl.get_snapshot(
                    self.previewScreen.cameraHandles[1],
                    metadata.right_Camera_Media)

        self.previewScreen.setStatusLabel(False)
        self.previewScreen.active = True
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
        string = self.shutterSpeedSelectionMenu.label.text()
        string = string.replace(" ", "")
        strings = string.split(":")
        fraction = strings[1]
        shutterspeed = fraction.replace("/", "_")
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

    def closeEvent(self):
        """Run when Main Menu closes. Clean up resources."""
        self.previewScreen.cameraControl.cleanUpCameras(
            self.previewScreen.cameraHandles)
        GPIO.cleanup()

    def __del__(self):
        """Run when Main Menu closes. Clean up resources."""
        self.previewScreen.cameraControl.cleanUpCameras(
            self.previewScreen.cameraHandles)
        GPIO.cleanup()


if __name__ == "__main__":
    sensorHub = sensor.sensorHub()
    sensorStatus = sensorHub.SysCheck()
    if sensorStatus.isWorking():
        app = QtWidgets.QApplication(sys.argv)
        form = QtWidgets.QWidget()
        ui = MainMenu(form)
        form.showFullScreen()
        sys.exit(app.exec())
    else:
        tempSensorStatus = sensorStatus.isTempWorking()
        phSensorStatus = sensorStatus.isPhWorking()
        pressureSensorStatus = sensorStatus.isBaroWorking()
        dissolvedOxygenStatus = sensorStatus.isDOWorking()
        print(f"Temperature Sensor Working: {str(tempSensorStatus)}")
        print(f"pH Sensor Working: {str(phSensorStatus)}")
        print(f"Pressure Sensor Working: {str(pressureSensorStatus)}")
        print(f"Dissolved Oxygen Sensor Working: {str(dissolvedOxygenStatus)}")
        sys.exit(1)
