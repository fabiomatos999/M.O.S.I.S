# Form implementation generated from reading ui file '.\IsoConfigurationMenu.ui'
#
# Created by: PyQt6 UI code generator 6.4.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QPushButton

class Ui_ISOConfigurationMenu(object):
    def setupUi(self, ISOConfigurationMenu):
        ISOConfigurationMenu.setObjectName("ISOConfigurationMenu")
        ISOConfigurationMenu.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
        ISOConfigurationMenu.setEnabled(True)
        ISOConfigurationMenu.resize(800, 480)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 149, 1))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 110, 128))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 110, 128))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(160, 160, 160))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 149, 1))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 110, 128))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 149, 1))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 170, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 110, 128))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 149, 1))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 110, 128))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.Link, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 149, 1))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Active, QtGui.QPalette.ColorRole.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 149, 1))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 110, 128))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 110, 128))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 149, 1))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 110, 128))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 149, 1))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 110, 128))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 149, 1))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.HighlightedText, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 110, 128))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.Link, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 149, 1))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Inactive, QtGui.QPalette.ColorRole.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 110, 128))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 110, 128))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 110, 128))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 110, 128))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 110, 128))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 110, 128))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 110, 128))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.Link, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 149, 1))
        brush.setStyle(QtCore.Qt.BrushStyle.SolidPattern)
        palette.setBrush(QtGui.QPalette.ColorGroup.Disabled, QtGui.QPalette.ColorRole.ToolTipText, brush)
        ISOConfigurationMenu.setPalette(palette)
        ISOConfigurationMenu.setAutoFillBackground(False)
        self.CurrentISOLabel = QtWidgets.QLabel(parent=ISOConfigurationMenu)
        self.CurrentISOLabel.setGeometry(QtCore.QRect(116, 0, 581, 100))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(60)
        self.CurrentISOLabel.setFont(font)
        self.CurrentISOLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.CurrentISOLabel.setObjectName("CurrentISOLabel")
        self.ISO100Button = QtWidgets.QPushButton(parent=ISOConfigurationMenu)
        self.ISO100Button.setGeometry(QtCore.QRect(10, 110, 212, 46))
        self.ISO100Button.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 149, 1);")
        self.ISO100Button.setCheckable(False)
        self.ISO100Button.setObjectName("ISO100Button")
        self.ISO200Button = QtWidgets.QPushButton(parent=ISOConfigurationMenu)
        self.ISO200Button.setGeometry(QtCore.QRect(10, 160, 212, 46))
        self.ISO200Button.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 149, 1);")
        self.ISO200Button.setObjectName("ISO200Button")
        self.ISO400Button = QtWidgets.QPushButton(parent=ISOConfigurationMenu)
        self.ISO400Button.setGeometry(QtCore.QRect(10, 210, 212, 46))
        self.ISO400Button.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 149, 1);")
        self.ISO400Button.setObjectName("ISO400Button")
        self.ISO800Button = QtWidgets.QPushButton(parent=ISOConfigurationMenu)
        self.ISO800Button.setGeometry(QtCore.QRect(10, 260, 212, 46))
        self.ISO800Button.setStyleSheet("color: rgb(255, 149, 1);\n"
"selection-color: rgb(255, 255, 255);\n"
"background-color: rgb(0, 0, 0);")
        self.ISO800Button.setAutoDefault(True)
        self.ISO800Button.setDefault(True)
        self.ISO800Button.setObjectName("ISO800Button")
        self.ISO1600Button = QtWidgets.QPushButton(parent=ISOConfigurationMenu)
        self.ISO1600Button.setGeometry(QtCore.QRect(10, 310, 212, 46))
        self.ISO1600Button.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 149, 1);")
        self.ISO1600Button.setObjectName("ISO1600Button")
        self.ISO3200Button = QtWidgets.QPushButton(parent=ISOConfigurationMenu)
        self.ISO3200Button.setGeometry(QtCore.QRect(10, 360, 212, 46))
        self.ISO3200Button.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 149, 1);")
        self.ISO3200Button.setObjectName("ISO3200Button")
        self.ISO6400Button = QtWidgets.QPushButton(parent=ISOConfigurationMenu)
        self.ISO6400Button.setGeometry(QtCore.QRect(10, 410, 212, 46))
        self.ISO6400Button.setStyleSheet("background-color: rgb(0, 0, 0);\n"
"color: rgb(255, 149, 1);")
        self.ISO6400Button.setObjectName("ISO6400Button")

        # Changes the label to match the button clicked
        self.ISO100Button.clicked.connect(lambda: self.CurrentISOLabel.setText("Current ISO: 100"))
        self.ISO200Button.clicked.connect(lambda: self.CurrentISOLabel.setText("Current ISO: 200"))
        self.ISO400Button.clicked.connect(lambda: self.CurrentISOLabel.setText("Current ISO: 400"))
        self.ISO800Button.clicked.connect(lambda: self.CurrentISOLabel.setText("Current ISO: 800"))
        self.ISO1600Button.clicked.connect(lambda: self.CurrentISOLabel.setText("Current ISO: 1600"))
        self.ISO3200Button.clicked.connect(lambda: self.CurrentISOLabel.setText("Current ISO: 3200"))
        self.ISO6400Button.clicked.connect(lambda: self.CurrentISOLabel.setText("Current ISO: 6400"))

        self.retranslateUi(ISOConfigurationMenu)
        QtCore.QMetaObject.connectSlotsByName(ISOConfigurationMenu)

    def retranslateUi(self, ISOConfigurationMenu):
        _translate = QtCore.QCoreApplication.translate
        ISOConfigurationMenu.setWindowTitle(_translate("ISOConfigurationMenu", "ISOConfigurationMenu"))
        self.CurrentISOLabel.setText(_translate("ISOConfigurationMenu", "Current ISO: 800"))
        self.ISO100Button.setText(_translate("ISOConfigurationMenu", "ISO 100"))
        self.ISO200Button.setText(_translate("ISOConfigurationMenu", "ISO 200"))
        self.ISO400Button.setText(_translate("ISOConfigurationMenu", "ISO 400"))
        self.ISO800Button.setText(_translate("ISOConfigurationMenu", "ISO 800"))
        self.ISO1600Button.setText(_translate("ISOConfigurationMenu", "ISO 1600"))
        self.ISO3200Button.setText(_translate("ISOConfigurationMenu", "ISO 3200"))
        self.ISO6400Button.setText(_translate("ISOConfigurationMenu", "ISO 6400"))


