import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt
from phSensorCalibrationMenu import Ui_Form
#from DissolvedOxygenCalibrationMenu import Ui_Form
#from WhiteBalanceCalibrationMenu import Ui_Form
from IsoConfigurationMenu import Ui_ISOConfigurationMenu
from ApertureSizeConfigurationMenu import Ui_ApertureSizeConfigurationMenu
from ShutterSpeedConfigurationMenu import Ui_ShutterSpeedConfigurationMenu
from GainConfigurationMenu import Ui_GainConfigurationMenu
from SaturationConfigurationMenu import Ui_SaturationConfigurationMenu
class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
       # self.ui = Ui_ISOConfigurationMenu()
     #   self.ui = Ui_ApertureSizeConfigurationMenu()
        #self.ui = Ui_ShutterSpeedConfigurationMenu()
        #self.ui = Ui_GainConfigurationMenu()
        #self.ui = Ui_SaturationConfigurationMenu()
        self.ui.setupUi(self)
        self.sliders = [self.ui.LowPointslide, self.ui.MidPointslide, self.ui.Highpointslide]
        self.current_slider_index = 0
        self.sliders[self.current_slider_index].setFocus()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_K:
            # Increment the current slider index and cycle through the list
            self.current_slider_index = (self.current_slider_index + 1) % len(self.sliders)
        else:
            self.current_slider_index = (self.current_slider_index - 1) % len(self.sliders)
            # Set focus to the next slider in the cycle
        self.sliders[self.current_slider_index].setFocus()
        self.sliders[self.current_slider_index].setStyleSheet( "QSlider::handle:horizontal {background-color:rgb(204, 255, 89);}")

        if self.sliders[self.current_slider_index] % len(self.sliders) == 0:
            self.sliders[1].setStyleSheet("QSlider::handle:horizontal {background-color:rgb(89, 239, 150);}")
            self.sliders[2].setStyleSheet("QSlider::handle:horizontal {background-color:rgb(89, 239, 150);}")

        if self.sliders[self.current_slider_index] % len(self.sliders) == 1:
            self.sliders[0].setStyleSheet("QSlider::handle:horizontal {background-color:rgb(89, 239, 150);}")
            self.sliders[2].setStyleSheet("QSlider::handle:horizontal {background-color:rgb(89, 239, 150);}")

        if self.sliders[self.current_slider_index] % len(self.sliders) == 2:
            self.sliders[1].setStyleSheet("QSlider::handle:horizontal {background-color:rgb(89, 239, 150);}")
            self.sliders[0].setStyleSheet("QSlider::handle:horizontal {background-color:rgb(89, 239, 150);}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec())
