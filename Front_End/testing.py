import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
# from phSensorCalibrationMenu import Ui_Form
# from DissolvedOxygenCalibrationMenu import Ui_Form
from WhiteBalanceCalibrationMenu import Ui_Form
from IsoConfigurationMenu import Ui_ISOConfigurationMenu
from ApertureSizeConfigurationMenu import Ui_ApertureSizeConfigurationMenu
class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
       # self.ui = Ui_Form()
        self.ui = Ui_ISOConfigurationMenu()
        self.ui = Ui_ApertureSizeConfigurationMenu()
        self.ui.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec())