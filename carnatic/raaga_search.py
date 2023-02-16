from PyQt6 import QtTest
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6 import QtGui
from PyQt6.QtGui import QFont, QAction, QIcon
_DIALOG_TITLE = "Search for raaga"
from carnatic import raaga,settings

class RaagaSearchDialog(QDialog):
    def __init__(self, raaga_list=None):
        super().__init__()
        resources = settings._get_resource_dictionary(settings._APP_LANG)
        self._raaga_list = raaga_list
        if raaga_list==None:
            self._raaga_list = settings.RAAGA_NAMES
        #print(self._raaga_list)
        self.setWindowTitle(resources['titRaagaSearchDialog'])
        # Create widgets    
        layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        lblRaagaName = QLabel(resources["lblEnterPartOfRaagaName"])
        self._raagaToSearch = QLineEdit()
        self._raagaToSearch.textChanged.connect(self._update_raaga_list)
        self._raagaToSearch.returnPressed.connect(self._set_selected_raaga_as_default)
        h_layout.addWidget(lblRaagaName)
        h_layout.addWidget(self._raagaToSearch)
        layout.addLayout(h_layout)
        self._resultList = QListWidget()
        layout.addWidget(self._resultList)
        button_layout = QHBoxLayout()
        self._search_button = QPushButton(resources["btnSearch"])
        self._search_button.clicked.connect(self._update_raaga_list)
        self._accept_button = QPushButton(resources["btnAccept"])
        self._accept_button.clicked.connect(self._set_selected_raaga_as_default)
        self._cancel_button = QPushButton(resources["btnCancel"])
        self._cancel_button.clicked.connect(self._close_dialog)
        button_layout.addWidget(self._search_button)
        button_layout.addWidget(self._accept_button)
        button_layout.addWidget(self._cancel_button)
        layout.addLayout(button_layout)
        self.setLayout(layout)
    def _update_raaga_list(self):
        partial_raaga = self._raagaToSearch.text()
        matching_raagas = [raaga for raaga in self._raaga_list if partial_raaga.upper() in raaga.upper()]
        self._resultList.clear()
        self._resultList.addItems(matching_raagas)
        QApplication.processEvents()
        if self._resultList.count() > 0:
            self._resultList.setCurrentRow(0)
    def _set_selected_raaga_as_default(self):
        if self._resultList.count() > 0:
            raagam = self._resultList.currentItem().text()
            print('selected search raagam',raagam)
            self._selected_raaga = raagam
            raaga.set_raagam(raagam)
            self.close()
    def _close_dialog(self):
        self.close()
def show(raaga_list=None):
    import sys
    def except_hook(cls, exception, traceback):
        sys.__excepthook__(cls, exception, traceback)
    sys.excepthook = except_hook

    #print("Showing raaga search dialog ")
    #app = QApplication(sys.argv)
    dialog = RaagaSearchDialog(raaga_list=raaga_list)
    dialog.exec()
    #print("Showing raaga search dialog done")
    #sys.exit(app.exec())        
if __name__ == "__main__":
    pass