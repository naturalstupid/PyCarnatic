from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6 import QtGui
from PyQt6.QtGui import QFont, QAction, QIcon
from carnatic import raaga, thaaLa, cplayer, settings, lessons, cparser, raaga_search, cdeeplearn, cmidi
from carnatic.ui.qtplayer import QtPlayer
import os

_krithi_dict = settings.KRITHI_DICT

class Player(QDialog):
    def __init__(self):
        super().__init__()
        self._resources = settings._get_resource_dictionary(settings._APP_LANG)
        self.setWindowTitle(self._resources['titMusicPlayer'])
        window_height = 550
        window_width = 500
        self.song_list = {} # song_name : song_path
        self._song_count = 0
        self._is_paused = True
        self._is_playing = False
        self._play_list_is_local = False
        self.qt_player = QtPlayer()
        self.setMinimumSize(window_width, window_height)
        self._main_ui()
        self._enable_disable_buttons()
    def _main_ui(self):
        self._v_layout = QVBoxLayout()
        self._song_info_table = QTableWidget(7,2)
        self._song_info_table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self._song_info_table.horizontalHeader().hide()
        self._song_info_table.verticalHeader().hide()
        self._song_info_table.setEnabled(False)
        self._song_summary_label = QLabel(self._resources["lblSongSummary"])
        self._song_summary_label.setEnabled(False)
        self._create_actions_1()
        self._create_actions_2()
        self._create_actions_3()
        self._create_actions_4()
        self._create_actions_5()
        self._create_button_row()
        self.setLayout(self._v_layout)
    def _create_actions_1(self):
        h_layout = QHBoxLayout()
        self._raaga_option = QRadioButton(self._resources['lblShowForRaaga'])
        self._raaga_option.setChecked(True)
        self._raaga_option.clicked.connect(self._get_song_list_per_criteria)
        h_layout.addWidget(self._raaga_option,alignment=Qt.AlignmentFlag.AlignLeft)
        self._raaga_search_button = QPushButton(QIcon(settings._IMAGES_PATH+"raaga_search_icon.png"),'')
        self._raaga_search_button.clicked.connect(self._search_for_raaga)
        self._raaga_search_button.setAutoDefault(False)
        h_layout.addWidget(self._raaga_search_button,alignment=Qt.AlignmentFlag.AlignRight)
        self._raaga_combo = QComboBox()
        self._krithi_raaga_list = raaga.get_raagas_that_have_krithis() #raaga.get_raaga_list()
        self._raaga_combo.addItems(self._krithi_raaga_list.keys())
        raagam = "MAyamAlava Gowla"
        self._raaga_combo.setCurrentText(raagam)
        raaga.set_raagam(raagam)
        self._raaga_combo.currentIndexChanged.connect(self._get_song_list_per_criteria)
        h_layout.addWidget(self._raaga_combo,alignment=Qt.AlignmentFlag.AlignLeft)
        self._v_layout.addLayout(h_layout)
        
        _criteria_option = QRadioButton(self._resources['lblShowForCriteria'])
        self._raaga_option.setChecked(not self._raaga_option.isChecked())
        _criteria_option.clicked.connect(self._get_song_list_per_criteria)
        self._v_layout.addWidget(_criteria_option,alignment=Qt.AlignmentFlag.AlignLeft)

        #self._v_layout.addLayout(h_layout)
    def _create_actions_2(self):
        h_layout = QHBoxLayout()
        _song_name_label = QLabel(self._resources['lblSongTitlePartial'])
        h_layout.addWidget(_song_name_label)
        self._partial_song_text = QLineEdit('')
        self._partial_song_text.editingFinished.connect(self._get_song_list_per_criteria)
        h_layout.addWidget(self._partial_song_text)
        _composer_label = QLabel(self._resources['lblComposer'])
        h_layout.addWidget(_composer_label)
        self._composer_combo = QComboBox()
        self._composer_combo.addItems(['']+_get_unique_field_values('Composer'))
        self._composer_combo.currentIndexChanged.connect(self._get_song_list_per_criteria)
        h_layout.addWidget(self._composer_combo)
        self._v_layout.addLayout(h_layout)
    def _create_actions_3(self):
        h_layout = QHBoxLayout()
        _language_label = QLabel(self._resources['lblLanguage'])
        h_layout.addWidget(_language_label)
        self._language_combo = QComboBox()
        self._language_combo.addItems(['']+_get_unique_field_values('Language'))
        self._language_combo.currentIndexChanged.connect(self._get_song_list_per_criteria)
        h_layout.addWidget(self._language_combo)
        self._v_layout.addLayout(h_layout)
        _songtype_label = QLabel(self._resources['lblType'])
        h_layout.addWidget(_songtype_label)
        self._songtype_combo = QComboBox()
        self._songtype_combo.addItems(['']+_get_unique_field_values('Type'))
        self._songtype_combo.currentIndexChanged.connect(self._get_song_list_per_criteria)
        h_layout.addWidget(self._songtype_combo)
        self._v_layout.addLayout(h_layout)
    def _create_actions_4(self):
        self._raagas_song_list = QListWidget()
        #self._raagas_song_list.setEnabled(False)
        self._raagas_song_list.currentTextChanged.connect(self._show_song_info)
        self._raagas_song_list.itemClicked.connect(self._show_song_info)
        self._get_song_list_per_criteria()
        self._v_layout.addWidget(self._raagas_song_list)
    def _create_actions_5(self):
        self._v_layout.addWidget(self._song_info_table)
        self._v_layout.addWidget(self._song_summary_label)
    def _create_button_row(self):
        _h_layout = QHBoxLayout()
        self._shuffle_on_off_button = QPushButton(QIcon(settings._IMAGES_PATH+'shuffle_on.png'),'') # QPushButton(QIcon(settings._IMAGES_PATH+'shuffle_off.png'))
        self._shuffle_on_off_button.setToolTip(self._resources['titShuffleSongs'])
        self._shuffle_on_off_button.clicked.connect(self._shuffle)
        self._shuffle_on_off_button.setAutoDefault(False)
        _h_layout.addWidget(self._shuffle_on_off_button)
        self._load_button = QPushButton(QIcon(settings._IMAGES_PATH+'load.jpg'),'')
        self._load_button.setToolTip(self._resources['titLoadSongs'])
        self._load_button.clicked.connect(self._load)
        self._load_button.setAutoDefault(False)
        _h_layout.addWidget(self._load_button)
        self._previous_button = QPushButton(QIcon(settings._IMAGES_PATH+'backward.jpg'),'')
        self._previous_button.setToolTip(self._resources['titPreviousSong'])
        self._previous_button.clicked.connect(self._previous)
        self._previous_button.setAutoDefault(False)
        _h_layout.addWidget(self._previous_button)
        self._play_button = QPushButton(QIcon(settings._IMAGES_PATH+'play.jpg'),'')
        self._play_button.setToolTip(self._resources['titPlaySong'])
        self._play_button.clicked.connect(self._play)
        self._play_button.setAutoDefault(False)
        _h_layout.addWidget(self._play_button)
        self._pause_button = QPushButton(QIcon(settings._IMAGES_PATH+'pause.jpg'),'')
        self._pause_button.setToolTip(self._resources['titPauseResumeSong'])
        self._pause_button.clicked.connect(self._pause_resume)
        self._pause_button.setAutoDefault(False)
        _h_layout.addWidget(self._pause_button)
        self._stop_button = QPushButton(QIcon(settings._IMAGES_PATH+'stop.jpg'),'')
        self._stop_button.setToolTip(self._resources['titStopSong'])
        self._stop_button.clicked.connect(self._stop)
        self._stop_button.setAutoDefault(False)
        _h_layout.addWidget(self._stop_button)
        self._next_button = QPushButton(QIcon(settings._IMAGES_PATH+'forward.jpg'),'')
        self._next_button.setToolTip(self._resources['titNextSong'])
        self._next_button.clicked.connect(self._next)
        self._next_button.setAutoDefault(False)
        _h_layout.addWidget(self._next_button)
        self._save_button = QPushButton(QIcon(settings._IMAGES_PATH+'save.jpg'),'')
        self._save_button.setToolTip(self._resources['titSaveSong'])
        self._save_button.clicked.connect(self._save)
        self._save_button.setAutoDefault(False)
        _h_layout.addWidget(self._save_button)
        self._close_button = QPushButton(QIcon(settings._IMAGES_PATH+'close.jpg'),'')
        self._close_button.setToolTip(self._resources['titClosePlayer'])
        self._close_button.clicked.connect(self._close)
        self._close_button.setAutoDefault(False)
        _h_layout.addWidget(self._close_button)
        self._repeat_on_off_button = QPushButton(QIcon(settings._IMAGES_PATH+'repeat_on.png'),'') # QPushButton(QIcon(settings._IMAGES_PATH+'repeat_off.png'))
        self._repeat_on_off_button.setToolTip(self._resources['titRepeatSongList'])
        self._repeat_on_off_button.clicked.connect(self._repeat)
        self._repeat_on_off_button.setAutoDefault(False)
        _h_layout.addWidget(self._repeat_on_off_button)
        self._v_layout.addLayout(_h_layout)
    def _search_for_raaga(self):
        raaga_search.show(raaga_list=list(raaga.get_raagas_that_have_krithis().keys()))
        QApplication.processEvents()
        raaga_name = raaga.get_raaga_name(settings.RAAGA_INDEX)
        self._raaga_combo.setCurrentText(raaga_name)
        print("Set the raaga to "+raaga_name)
    def _show_feature_not_implemented(self):
        msg_box = QMessageBox()
        msg_box.setText(self._resources["titFeatureTobeImplemented"])
        msg_box.setWindowTitle(self._resources["titFeatureNotAvailable"])
        msg_box.exec()
    def _shuffle(self):
        self._show_feature_not_implemented()
    def _load(self):
        file_names, _ = QFileDialog.getOpenFileNames(None,self._resources["titSaveAudioFile"],settings._TEMP_PATH,
                                                    self._resources['titOpenAudioFileFilter'])
        self.song_list.clear()
        for fn in file_names:
            file = os.path.basename(fn)
            self.song_list[file]=fn
        self._play_list_is_local = True        
        self._raagas_song_list.clear()
        self._raagas_song_list.addItems(self.song_list.keys())
        self._raagas_song_list.setCurrentRow(0)
        self._song_count = self._raagas_song_list.count()
        self.qt_player.set_playing_list(self.song_list)
        self.qt_player.set_playing_index = 0
        self._raagas_song_list.setFocus()      
    def _play(self):
        self._stop()
        cur_row = self._raagas_song_list.currentRow()
        self.qt_player.set_playing_index(cur_row)
        self.qt_player.play()
        self._is_playing = True
        self._is_paused = False
        self._enable_disable_buttons()
    def _pause_resume(self):
        self.qt_player.pause_resume()
        self._enable_disable_buttons()
    def _stop(self):
        self.qt_player.stop()
        self._is_playing = False
        self._is_paused = True
        self._enable_disable_buttons()
    def _previous(self):
        if self._song_count > 0:
            self._stop()
            cur_row = self._raagas_song_list.currentRow()
            cur_row = (cur_row+self._song_count-1) % self._song_count
            self._raagas_song_list.setCurrentRow(cur_row)
            self.qt_player.previous()
            self._is_playing = True
            self._is_paused = False
            self._enable_disable_buttons()
    def _next(self):
        if self._song_count > 0:
            self._stop()
            cur_row = self._raagas_song_list.currentRow()
            cur_row = (cur_row+self._song_count+1) % self._song_count
            self._raagas_song_list.setCurrentRow(cur_row)
            self.qt_player.next()
            self._is_playing = True
            self._is_paused = False
            self._enable_disable_buttons()
    def _save(self):
        mp3_save_file,_ = QFileDialog.getSaveFileName(self, self._resources["titSaveAudioFile"], settings._TEMP_PATH, self._resources["titAudioFileFilter"])
        if mp3_save_file.strip() == '':
            return
        current_krithi_id = self._get_current_song_id()
        mp3_file = _krithi_dict[current_krithi_id]['MP3 Link']
        print('Saving',mp3_file,'as',mp3_save_file)
        import requests
        mp3 = requests.get(mp3_file)
        with open(mp3_save_file,"wb") as f:
            f.write(mp3.content)
        f.close()
    def _close(self):
        self.close()
    def _repeat(self):
        self._show_feature_not_implemented()        
    def _enable_disable_buttons(self):
        self._play_button.setEnabled(not self._is_playing)
        self._stop_button.setEnabled(self._is_playing or self._is_paused)
        self._pause_button.setEnabled(self._is_playing)
        # enable prev and next buttons only when playing
        self._previous_button.setEnabled(self._is_playing)
        self._next_button.setEnabled(self._is_playing)
    def _get_song_ids_for_selected_raagam(self):
        current_raagam = self._raaga_combo.currentText()
        selected_raagam_index = int(self._krithi_raaga_list[current_raagam])
        kids = raaga.get_krithis(selected_raagam_index,has_mp3_link=True)
        self.song_list.clear()
        for kid in kids:
            key = _krithi_dict[kid]['Title']
            value = _krithi_dict[kid]['id']
            self.song_list[key] = value
    def _enable_raaga_ui(self,enabled=True):
        self._raaga_combo.setEnabled(enabled)
        self._raaga_search_button.setEnabled(enabled)
    def _enable_criteria_ui(self,enabled=True):
        self._partial_song_text.setEnabled(enabled)
        self._language_combo.setEnabled(enabled)
        self._composer_combo.setEnabled(enabled)
        self._songtype_combo.setEnabled(enabled)
    def _get_song_list_per_criteria(self):
        self._play_list_is_local = False
        self._enable_criteria_ui(not self._raaga_option.isChecked())
        self._enable_raaga_ui(self._raaga_option.isChecked())
        self.song_list.clear()
        self._raagas_song_list.clear()
        if self._raaga_option.isChecked():
            self._get_song_ids_for_selected_raagam()
        else:
            criteria_pair = [('Composer',self._composer_combo.currentText()),
                             ('Language',self._language_combo.currentText()),
                             ('Type',self._songtype_combo.currentText()),
                             ('Title',self._partial_song_text.text().strip())
                            ]
            criteria = [(key,value) for key,value in criteria_pair if value != '' ]
            if len(criteria)>0:
                matching_song_ids = _search_krithis_for_field_value_pairs(criteria)
                for kid in matching_song_ids:
                    key = _krithi_dict[kid]['Title']
                    value = _krithi_dict[kid]['id']
                    mp3_link = _krithi_dict[kid]['MP3 Link'].strip()
                    if mp3_link != '':
                        self.song_list[key.strip()] = value
        self._raagas_song_list.addItems(self.song_list.keys())
        self._raagas_song_list.setCurrentRow(0)
        media_list = {k:_krithi_dict[int(v)]['MP3 Link'] for k,v in self.song_list.items()}
        self._song_count = self._raagas_song_list.count()
        self.qt_player.set_playing_list(media_list)
        self.qt_player.set_playing_index(0)
        self._raagas_song_list.setFocus()
    def _get_current_song_id(self):
        if len(self._raagas_song_list)==0:
            return
        current_item = self._raagas_song_list.currentItem()
        if current_item == None:
            self._raagas_song_list.setCurrentRow(0)
            current_item = self._raagas_song_list.currentItem()
        current_krithi = current_item.text()
        current_krithi_id = int(self.song_list[current_krithi])
        return current_krithi_id
    def _show_song_info(self):
        if self._is_playing:
            return
        krithi_info = [[self._resources[key],self._resources['msgNoInfoAboutSong']] 
                        for key in ['lblTitle','lblRaaga','lblThaaLa','lblComposer','lblLanguage','lblType','lblCredits']
                      ]
        if len(self._raagas_song_list)==0 or len(self.song_list)==0 or self._play_list_is_local:
            for row in range(self._song_info_table.rowCount()):
                for col in range(self._song_info_table.columnCount()):
                    self._song_info_table.setItem(row,col,QTableWidgetItem(krithi_info[row][col]))
            self._song_info_table.resizeColumnsToContents()
            self._song_info_table.resizeRowsToContents()
            self.song_list.clear()
            self._raagas_song_list.clear()
            self._song_summary_label.setText(self._resources['lblNoMatchingSongsFound'])
            return
        current_krithi_id = self._get_current_song_id()
        mp3_url = _krithi_dict[current_krithi_id]['MP3 Link']
        mp3_credits = '.'.join(mp3_url.split('/')[2].split('.')[1:])
        krithi_info = [[self._resources['lbl'+key],_krithi_dict[current_krithi_id][key]] 
                        for key in ['Title','Raaga','ThaaLa','Composer','Language','Type']
                      ]+[[self._resources['lblCredits'],mp3_credits]]
        for row in range(self._song_info_table.rowCount()):
            for col in range(self._song_info_table.columnCount()):
                self._song_info_table.setItem(row,col,QTableWidgetItem(krithi_info[row][col]))
        self._song_info_table.resizeColumnsToContents()
        self._song_info_table.resizeRowsToContents()
        self._song_count = self._raagas_song_list.count()
        self._song_summary_label.setText(str(self._song_count)+' '+self._resources['lblSongsFound'])
        self._raagas_song_list.setFocus()
def _get_krithi_field_names():
    fields = [k for k,_ in _krithi_dict[0].items()]
    return fields
def _get_krithi_attribute(field,krithi_id=None):
    if krithi_id==None:
        krithi_id=settings.RAAGA_INDEX
    result = []
    if field in _krithi_dict[0].keys():
        result = _krithi_dict[krithi_id][field]
        return result
    return ''    
def _search_krithi_for_values(search_field, search_str,is_exact=False):
    if isinstance(search_str, int):
        search_str = str(search_str)
    matching_keys = []
    for k,_ in _krithi_dict.items():
        if is_exact:
            if search_str.lower() == _krithi_dict[k][search_field].lower():
                matching_keys.append(k)
        else:
            if search_str.lower() in _krithi_dict[k][search_field].lower():
                matching_keys.append(k)
    return matching_keys
def _search_krithis_for_field_value_pairs(field_value_pairs):
    matching_krithi_ids = []
    for field,value in field_value_pairs:
        mk_ids = _search_krithi_for_values(field, value)
        if len(mk_ids)==0:
            return mk_ids
        int_ids = mk_ids
        if len(matching_krithi_ids)>0:
            int_ids = list(set(matching_krithi_ids) & set(mk_ids))
            if len(int_ids) == 0:
                return int_ids
        matching_krithi_ids = int_ids
    return matching_krithi_ids
def _get_unique_field_values(field):
    values = list(set([_krithi_dict[k][field] for k,_ in _krithi_dict.items()]))
    return sorted(values)
def show(raaga_list=None):
    import sys
    def except_hook(cls, exception, traceback):
        sys.__excepthook__(cls, exception, traceback)
    sys.excepthook = except_hook

    dialog = Player()
    dialog.exec()
if __name__ == "__main__":
    import sys
    def except_hook(cls, exception, traceback):
        sys.__excepthook__(cls, exception, traceback)
    sys.excepthook = except_hook
    settings.set_language('ta')
    app = QApplication(sys.argv)
    window = Player()
    window.show()
    sys.exit(app.exec())        
