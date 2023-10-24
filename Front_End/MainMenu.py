from PyQt6 import QtGui, QtWidgets
from QtWidgets import QtWidget, QSplitView
import PreviewScreen
import StudyProfileSelectionMenu


class MainMenu():

    def __init__(self):
        self.previewScreen = PreviewScreen.Ui_Form()
        self.previewScreen = self.previewScreen.groupBox
        self.studyProfileSelectionMenu = StudyProfileSelectionMenu.Ui_Form()
        self.studyProfileSelectionMenu = \
            self.studyProfileSelectionMenu.groupBox
        self.splitview = QSplitView()
        self.splitview.addWidget(self.previewScreen)
        self.splitview.addWidget(self.studyProfileSelectionMenu)
