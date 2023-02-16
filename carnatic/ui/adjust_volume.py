from PyQt6 import QtTest
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6 import QtGui
from PyQt6.QtGui import QFont, QAction, QIcon
from carnatic import settings
class VolumeControl(QDialog):
    def __init__(self,*args):
        super().__init__()
        self._resources = settings._RESOURCES
        self._instruments = settings._ALL_INSTRUMENTS
        self._instrument_index = settings.INSTRUMENT_INDEX
        self._instrument_volume_levels = settings._INSTRUMENT_VOLUME_LEVELS        
        self.create_ui()
    def create_ui(self):
        self.setWindowTitle(self._resources['mnuVolume'])
        self.setFixedSize(250, 275)
        h_layout = QHBoxLayout()
        self._instrument_list = QListWidget()
        self._instrument_list.addItems(self._instruments)
        self._instrument_list.setMinimumHeight(220)
        #self._instrument_list.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._instrument_list.setCurrentRow(self._instrument_index)
        self._instrument_list.itemClicked.connect(self._update_slider_position_for_instrument)
        h_layout.addWidget(self._instrument_list)
        self._volume_slider = QSlider(Qt.Orientation.Vertical)
        self._volume_slider.setFixedHeight(200)
        self._volume_slider.setRange(0,settings._VOLUME_MAX)
        self._volume_slider.setValue(63)
        self._volume_slider.setSingleStep(16)
        self._volume_slider.setTickInterval(16)
        self._volume_slider.setTickPosition(QSlider.TickPosition.TicksBothSides)
        self._volume_slider.sliderReleased.connect(self._update_selected_instrument_volume)
        h_layout.addWidget(self._volume_slider)
        h_layout.addLayout(self._set_slider_tick_labels())
        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout)
        h_layout = QHBoxLayout()
        accept_button = QPushButton(self._resources['btnAccept'])
        accept_button.clicked.connect(self._accept_button_clicked)
        cancel_button = QPushButton(self._resources['btnCancel'])
        cancel_button.clicked.connect(self._cancel_button_clicked)
        h_layout.addWidget(accept_button)
        h_layout.addWidget(cancel_button)
        v_layout.addLayout(h_layout)
        self.setLayout(v_layout)
    def _set_slider_tick_labels(self):
        tick_interval = self._volume_slider.tickInterval()
        tick_max = self._volume_slider.maximum()
        tick_min = self._volume_slider.minimum()
        tick_count = int ( (tick_max-tick_min)/tick_interval )
        label_layout = QGridLayout()
        for t in range(tick_count+2):
            tick_value = t*tick_interval
            label = QLabel(str(tick_max - tick_value))
            label_layout.addWidget(label,t,1,1,1)
        return label_layout
    def _update_selected_instrument_volume(self):
        self._instrument_volume_levels[self._instrument_list.currentRow()] = self._volume_slider.value()
    def _update_slider_position_for_instrument(self):
        self._volume_slider.setValue(self._instrument_volume_levels[self._instrument_list.currentRow()])
    def _cancel_button_clicked(self):
        self.close()
    def _accept_button_clicked(self):
        if settings._PLAYER_TYPE == settings.PLAYER_TYPE.SCAMP:
            settings._INSTRUMENT_VOLUME_LEVELS = [x/settings._VOLUME_MAX for x in self._instrument_volume_levels]
        else:
            settings._INSTRUMENT_VOLUME_LEVELS = self._instrument_volume_levels
        print(settings._INSTRUMENT_VOLUME_LEVELS)
        self.close()
def show():
    import sys
    def except_hook(cls, exception, traceback):
        sys.__excepthook__(cls, exception, traceback)
    sys.excepthook = except_hook

    dialog = VolumeControl()
    dialog.exec()
if __name__ == "__main__":
    import sys
    def except_hook(cls, exception, traceback):
        sys.__excepthook__(cls, exception, traceback)
    sys.excepthook = except_hook
    settings.set_language('ta')
    app = QApplication(sys.argv)
    window = VolumeControl()
    window.show()
    sys.exit(app.exec())        
         