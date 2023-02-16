from PyQt6 import QtTest
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6 import QtGui
from PyQt6.QtGui import QFont, QAction, QIcon
from carnatic import raaga, thaaLa, cplayer, settings, lessons, cparser, raaga_search, cdeeplearn, cmidi
from carnatic.ui import krithi_player
import os
#from fpdf import FPDF
_APP_TITLE = "PyCarnatic - Carnatic Music Guru"
_APP_VERSION='V1.2.1'
_IMAGES_PATH = settings._IMAGES_PATH #_APP_PATH + "/images/"
_NOTES_PATH = settings._NOTES_PATH #_APP_PATH + "/Notes/"
_GEETHAM_PATH = settings._GEETHAM_PATH #_APP_PATH + "/Lessons/Geetham/"
_VARNAM_PATH = settings._VARNAM_PATH #_APP_PATH + "/Lessons/Varnam/"
_SWARAJAATHI_PATH = settings._SWARAJAATHI_PATH #_APP_PATH + "/Lessons/Swarajaathi/"
_VOICE_PRACTICE_PATH = settings._VOICE_PRACTICE_PATH #_APP_PATH + "/Lessons/Voice/"
_RAAGA_PRACTICE_PATH = settings._RAAGA_PRACTICE_PATH #_APP_PATH + "/Lessons/Raaga/"
_TEMP_PATH = settings._TEMP_PATH #_APP_PATH + "/tmp/"
_TEMP_FILE = settings._TEMP_FILE #_TEMP_PATH + "delme.cmn"
_THAALAM_LESSONS_PATH = settings._THAALAM_LESSONS_PATH #_APP_PATH + "/Lessons/Percussion/"
class TutorUI(QMainWindow):
    """
        PyCarnatic UI Class
        @param language: 'en' for English (default) or 'ta' for Tamil
        @param raaga_list: 
            0 => Show Melakartha raagas only
            1 => Show Sampoorna raagas (note count = 8) only
            2 => Show raagas with 8 or more note count only
            3 => Show all raagas from the raaga input file (/config/raaga_list.inp)        
    """
    _EXIT_CODE_REBOOT = -123456
    _APP_LANG = 'en'
    def __init__(self,language:str='en',\
                 raaga_list_index:settings.RAAGA_LIST_SELECTION=settings.RAAGA_LIST_SELECTION.SIX_OR_MORE_NOTE_RAAGAS_ONLY, \
                 player_type:settings.PLAYER_TYPE=settings.PLAYER_TYPE.SF2_LOADER):
        super(TutorUI,self).__init__()
        TutorUI._APP_LANG = language
        settings.set_language(language)
        settings.set_raaga_list_selection(raaga_list_index)
        self._player_type = player_type
        settings.PLAYER_TYPE = player_type
        print('player type',self._player_type)
        self._resources = settings._get_resource_dictionary(language)
        self._APP_TITLE = self._resources['titApplication']
        self.setWindowTitle(self._APP_TITLE)
        window_height = 500
        window_width = 600
        self.setMinimumSize(window_width, window_height)
        self._include_percussion_layer = True
        self.MPlayer = cmidi.MPlayer(settings._SOUND_FONT_FILE)
        self._create_actions()
        self._create_menubar()
        self._create_toolbars()
        self._connectActions()
    def closeEvent(self, event):
        print('closing the application')
        self._exit_application()
    def _create_actions(self):
        # Creating action using the first constructor
        self._newAction = QAction(QIcon(_IMAGES_PATH+"NewNoteFile-icon.png"),self._resources["mnuNew"],self)
        self._newAction.setToolTip(self._resources["tipNewFile"])
        self._openAction = QAction(QIcon(_IMAGES_PATH+"NoteFile-icon.png"),self._resources["mnuOpen"], self)
        self._openAction.setToolTip(self._resources["tipOpenFile"])
        self._closeAction = QAction(self._resources["mnuClose"], self)
        self._saveAction = QAction(self._resources["mnuSave"], self)
        self._saveAsPDFAction = QAction(self._resources["mnuSaveAsPDF"], self)
        self._saveAsAudioAction = QAction(QIcon(_IMAGES_PATH+"save.jpg"),self._resources["mnuSaveAsAudio"], self)
        self._saveAsLilipondFileAction = QAction(self._resources["mnuSaveAsLilipondFile"], self)
        self._printAction = QAction(self._resources["mnuPrint"], self)
        self._exitAction = QAction(self._resources["mnuExit"], self)
        #self._copyAction = QAction(self._resources["mnuCopy"], self)
        #self._pasteAction = QAction(self._resources["mnuPaste"], self)
        self._raagasearchAction = QAction(QIcon(_IMAGES_PATH+"raaga_search_icon.png"),self._resources["mnuSearch"],self)
        self._raagasearchAction.setToolTip(self._resources["tipSearch"])
        self._musicPlayerAction = QAction(QIcon(_IMAGES_PATH+"music_player.png"),self._resources['mnuKrithiPlayer'],self)
        self._musicPlayerAction.setToolTip(self._resources["mnuKrithiPlayer"])
        self._playAroganamAvaroganamAction = QAction(self._resources["mnuPlayAroganamAvaroganam"], self)

        ' toolbar button actions'
        self._playButtonAction = QAction(QIcon(_IMAGES_PATH+"Button-Play-icon.png"),"",self)
        self._playButtonAction.setToolTip(self._resources["tipPlayer"])
        self._pauseButtonAction = QAction(QIcon(_IMAGES_PATH+"Button-Pause-icon.png"),"",self)
        self._pauseButtonAction.setToolTip(self._resources["tipPause"])
        #self._pauseButtonAction.setEnabled(False)
        self._stopButtonAction = QAction(QIcon(_IMAGES_PATH+"Button-Stop-icon.png"),"",self)
        self._stopButtonAction.setToolTip(self._resources["tipStop"])
        self._pauseButtonAction.setEnabled(False)
        self._stopButtonAction.setEnabled(False)
        self._veenaButtonAction = QAction(QIcon(_IMAGES_PATH+"instVeena_icon.jpg"),"",self)
        self._veenaButtonAction.setToolTip(self._resources["tipVeena"])
        self._violinButtonAction = QAction(QIcon(_IMAGES_PATH+"instViolin-icon.png"),"",self)
        self._violinButtonAction.setToolTip(self._resources["tipViolin"])
        self._fluteButtonAction = QAction(QIcon(_IMAGES_PATH+"inst-Flute-icon.png"),"",self)
        self._fluteButtonAction.setToolTip(self._resources["tipFlute"])
        self._mridangamButtonAction = QAction(QIcon(_IMAGES_PATH+"instMridangam.jpg"),"",self)
        self._mridangamButtonAction.setToolTip(self._resources["tipMridangam"])
        self._raaga_combo = QComboBox()
        raaga_list = raaga.get_raaga_list()
        self._raaga_combo.addItems(raaga_list)
        raagam = "MAyamAlava Gowla"
        self._raaga_combo.setCurrentText(raagam)
        raaga.set_raagam(raagam)
        self._percussion_instrument_combo = QComboBox()
        self._percussion_instrument_combo.addItems(settings._PERCUSSION_INSTRUMENTS)
        self._percussion_instrument_combo.setCurrentText(settings.CURRENT_PERCUSSION_INSTRUMENT)
        
        self._thaaLa_combo = QComboBox()
        thaaLa_list = thaaLa.get_thaaLam_names()
        self._thaaLa_combo.addItems(thaaLa_list)
        self._thaaLa_combo.setCurrentText(thaaLa_list[settings.THAALA_INDEX-1])

        self._jaathi_combo = QComboBox()
        jaathi_list = thaaLa.get_jaathi_names()
        self._jaathi_combo.addItems(jaathi_list)
        self._jaathi_combo.setCurrentText(jaathi_list[settings.JAATHI_INDEX-1])
        
        self._nadai_combo = QComboBox()
        nadai_list = thaaLa.get_nadai_names()
        self._nadai_combo.addItems(nadai_list)
        self._nadai_combo.setCurrentText(nadai_list[settings.NADAI_INDEX-1])
        ' second tool bar items'
        self._duration_combo = QSpinBox()
        self._duration_combo.setRange(1,200)
        self._duration_combo.setValue(60)
        self._shruthi_combo = QComboBox()
        """ TODO To implement Kattai change """
        shruthi_list = settings.KATTAI_LIST
        self._shruthi_combo.addItems(shruthi_list)
        self._shruthi_combo.setCurrentText("4.5")
        self._instrument_combo = QComboBox()
        instrument_list = cplayer.get_instrument_list(include_percussion_instruments=False)[:-1]
        self._instrument_combo.addItems(instrument_list)
        playing_instrument = instrument_list[0]
        self._instrument_combo.setCurrentText(playing_instrument)
        settings.INSTRUMENT_INDEX = settings._get_list_index(playing_instrument, settings._INSTRUMENT_LIST)
        settings.CURRENT_INSTRUMENT = playing_instrument
        self._raga_info_label = QLabel("Raaga information")
        raaga_index = settings.RAAGA_INDEX
        aaroganam = raaga.get_aaroganam(raaga_index)
        avaroganam = raaga.get_avaroganam(raaga_index)
        raaga_info = ' '.join(aaroganam) + "\n" + ' '.join(avaroganam)
        print('raaga_info',raaga_info)
        self._raga_info_label.setText(raaga_info)
        self._thaaLa_info_label = QLabel("ThaaLa information")
        thaaLaSymbols = thaaLa.get_thaaLa_positions(settings.THAALA_INDEX, settings.JAATHI_INDEX,as_string=True)
        print('thaaLa Symbols',thaaLaSymbols)
        self._thaaLa_info_label.setText(thaaLaSymbols)
        self._song_info_text = QTextEdit()
        self._song_info_text.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._song_info_text.setPlainText("#Enter commands and notes here")
        self.setCentralWidget(self._song_info_text)
        
    def _create_toolbars(self):
        toolbar = self.addToolBar("")
        toolbar.addAction(self._newAction)
        toolbar.addAction(self._openAction)
        toolbar.addAction(self._playButtonAction)
        toolbar.addAction(self._pauseButtonAction)
        toolbar.addAction(self._stopButtonAction)
        toolbar.addAction(self._veenaButtonAction)
        toolbar.addAction(self._violinButtonAction)
        toolbar.addAction(self._fluteButtonAction)
        toolbar.addAction(self._mridangamButtonAction)
        toolbar.addAction(self._raagasearchAction)
        toolbar.addAction(self._musicPlayerAction)
        self.addToolBarBreak()
        toolbar1 = self.addToolBar("")
        toolbar1.addWidget(QLabel(self._resources["lblDuration"]))
        toolbar1.addWidget(self._duration_combo)
        toolbar1.addWidget(QLabel(self._resources["lblShruthi"]))
        toolbar1.addWidget(self._shruthi_combo)
        toolbar1.addWidget(QLabel(self._resources["lblInstrument"]))
        toolbar1.addWidget(self._instrument_combo)
        toolbar1.addWidget(self._raaga_combo)
        self.addToolBarBreak()
        toolbar2 = self.addToolBar("")
        toolbar2.addWidget(self._percussion_instrument_combo)
        toolbar2.addWidget(self._thaaLa_combo)
        toolbar2.addWidget(self._jaathi_combo)
        toolbar2.addWidget(self._nadai_combo)
        toolbar2.addWidget(self._thaaLa_info_label)
        toolbar2.addWidget(self._raga_info_label)
        
    def _create_menubar(self):
        menuBar = self.menuBar()
# Creating menus using a QMenu object
        fileMenu = QMenu(self._resources["mnuFile"], self)
        fileMenu.addAction(self._newAction)
        fileMenu.addAction(self._openAction)
        fileMenu.addAction(self._closeAction)
        fileMenu.addAction(self._saveAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self._saveAsPDFAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self._saveAsAudioAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self._saveAsLilipondFileAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self._printAction)
        fileMenu.addAction(self._exitAction)
        
        menuBar.addMenu(fileMenu)
        #editMenu = menuBar.addMenu(self._resources["mnuEdit"])
        #editMenu.addAction(self._copyAction)
        #editMenu.addAction(self._pasteAction)
        raagamMenu = menuBar.addMenu(self._resources["mnuRaagam"])
        raagamMenu.addAction(self._raagasearchAction)
        generateMenu = raagamMenu.addMenu(self._resources["mnuGenerate"])
        self._generateSaraLiAction = generateMenu.addAction(self._resources["mnuGenerateSaraliVarisai"])
        self._generateJantaiAction = generateMenu.addAction(self._resources["mnuGenerateJantaiVarisai"])
        self._generateDhaattuAction = generateDhaattuAction = generateMenu.addAction(self._resources["mnuGenerateDhaattuVarisai"])
        self._generateMelSthaayiAction =  generateMenu.addAction(self._resources["mnuGenerateMelSthaayiVarisai"])
        self._generateKeezhSthaayiAction = generateMenu.addAction(self._resources["mnuGenerateKeezhSthaayiVarisai"])
        self._generateAlankaaraFromBookAction = generateMenu.addAction(self._resources["mnuGenerateAlankaaraVarisaiFromBook"])
        self._generateAlankaaraFromAlgorithmAction = generateMenu.addAction(self._resources["mnuGenerateAlankaaraVarisaiFromAlgorithm"])
        self._generateKalpanaswaramFromCorpusAction = generateMenu.addAction(self._resources["mnuGenerateKalpanaSwaramFromCorpus"])
        self._generateKalpanaswaramFromLessonsAction = generateMenu.addAction(self._resources["mnuGenerateKalpanaSwaramFromLessons"])
        playMenu = menuBar.addMenu(self._resources["mnuPlay"])
        self._playAroganamAvaroganamAction = playMenu.addAction(self._resources["mnuPlayAroganamAvaroganam"])
        self._playSaraliAction = playMenu.addAction(self._resources["mnuPlaySaraliVarisai"])
        self._playJantaiAction = playMenu.addAction(self._resources["mnuPlayJantaiVarisai"])
        self._playDhaattuAction = playMenu.addAction(self._resources["mnuPlayDhaattuVarisai"])
        self._playMelSthaayiAction = playMenu.addAction(self._resources["mnuPlayMelSthaayiVarisai"])
        self._playKeezhSthaayiAction = playMenu.addAction(self._resources["mnuPlayKeezhSthaayiVarisai"])
        playMenu.addSeparator()
        self._playAlankaaraFromBookAction = playMenu.addAction(self._resources["mnuPlayAlankaaraVarisaiFromBook"])
        self._playAlankaaraFromAlgorithmAction = playMenu.addAction(self._resources["mnuPlayAlankaaraVarisaiFromAlgorithm"])
        playMenu.addSeparator()
        self._playGeethamAction = playMenu.addAction(self._resources["mnuGeetham"])
        self._playVarnamAction = playMenu.addAction(self._resources["mnuVarnam"])
        self._playSwarajaathiAction = playMenu.addAction(self._resources["mnuSwarajaathi"])
        self._playVoicePracticeAction = playMenu.addAction(self._resources["mnuVoicePractice"])
        self._playRaagaPracticeAction = playMenu.addAction(self._resources["mnuRaagamPractice"])
        thaaLamMenu = menuBar.addMenu(self._resources["mnuThaaLam"])
        self._playSelectedThaaLamAction = thaaLamMenu.addAction(self._resources["mnuPlaySelectedThaaLam"])
        self._playSolkattuAction = thaaLamMenu.addAction(self._resources["mnuPlaySolkattu"])
        self._playThaaLamLessonsAction = thaaLamMenu.addAction(self._resources["mnuPlayLessons"])
        self._playMetronomeAction = thaaLamMenu.addAction(self._resources["mnuPlayMetronome"])
        toolsMenu = menuBar.addMenu(self._resources["mnuTools"])
        self._toolsOptionsAction = toolsMenu.addAction(self._resources["mnuOptions"])
        self._toolsRaagamQuizAction = toolsMenu.addAction(self._resources["mnuRaagamQuiz"])
        self._toolsVolumeAction = toolsMenu.addAction(self._resources["mnuVolume"])
        #self._toolsCheckShruthiAction = toolsMenu.addAction(self._resources["mnuCheckShruthi"])
        changeLanguageMenu = toolsMenu.addMenu(self._resources["mnuChangeLanguage"])
        lang_dict_str = self._resources['dictLang']
        self._lang_dict = {}
        self._lang_dict = dict((x.strip(), y.strip())
             for x, y in (element.split(':') 
             for element in lang_dict_str.split(',')))
        for lang in settings._APP_LANGUAGES:
            if lang.lower() != TutorUI._APP_LANG:
                changeLanguageMenu.addAction(self._lang_dict[lang],self._tools_change_language_clicked)        
        toolsMenu.addAction(self._musicPlayerAction)
        ' help menu'
        helpMenu = menuBar.addMenu(self._resources["mnuHelp"])
        self._helpFeaturesAction = helpMenu.addAction(self._resources["mnuFeatures"])
        self._helpUpdateAction = helpMenu.addAction(self._resources["mnuCheckForUpdate"])
        self._helpAboutAction = helpMenu.addAction(self._resources["mnuAbout"])
    def _connectActions(self):
        ' file menu signals'
        self._newAction.triggered.connect(lambda: self._new_file(file_path=settings._SAVE_FILES_PATH))
        self._openAction.triggered.connect(lambda: self._open_file(file_path=_NOTES_PATH))
        self._closeAction.triggered.connect(lambda: self._close_file(file_path=settings._SAVE_FILES_PATH))
        self._saveAction.triggered.connect(lambda: self._save_file(file_path=settings._SAVE_FILES_PATH))
        self._saveAsPDFAction.triggered.connect(self._save_as_pdf)
        self._saveAsAudioAction.triggered.connect(self._save_as_audio)
        self._saveAsLilipondFileAction.triggered.connect(self._save_as_lilipond_file)
        self._exitAction.triggered.connect(self._exit_application)
        ' Edit menu signals'
        #self._copyAction.triggered.connect(self._copy_clipboard)
        #self._pasteAction.triggered.connect(self._paste_clipboard)
        ' Raagam menu signals '
        self._raagasearchAction.triggered.connect(self._search_for_raaga)
        self._generateSaraLiAction.triggered.connect(self._generate_sarali_varisai)
        self._generateJantaiAction.triggered.connect(self._generate_jantai_varisai)
        self._generateDhaattuAction.triggered.connect(self._generate_dhaattu_varisai)
        self._generateMelSthaayiAction.triggered.connect(self._generate_melsthaayi_varisai)
        self._generateKeezhSthaayiAction.triggered.connect(self._generate_keezhsthaayi_varisai)
        self._generateAlankaaraFromBookAction.triggered.connect(self._generate_alankaara_varisai_book)
        self._generateAlankaaraFromAlgorithmAction.triggered.connect(self._generate_alankaara_varisai_algorithm)
        self._generateKalpanaswaramFromCorpusAction.triggered.connect(self._generate_kalpana_swaram_from_corpus)
        self._generateKalpanaswaramFromLessonsAction.triggered.connect(self._generate_kalpana_swaram_from_lessons)
        ' Play menu signals'
        self._playAroganamAvaroganamAction.triggered.connect(self._play_aaroganam_avaroganam)
        self._playSaraliAction.triggered.connect(self._play_sarali_varisai)
        self._playJantaiAction.triggered.connect(self._play_jantai_varisai)
        self._playDhaattuAction.triggered.connect(self._play_dhaattu_varisai)
        self._playMelSthaayiAction.triggered.connect(self._play_melsthaayi_varisai)
        self._playKeezhSthaayiAction.triggered.connect(self._play_keezhsthaayi_varisai)
        self._playAlankaaraFromBookAction.triggered.connect(self._play_alankaara_varisai_book)
        self._playAlankaaraFromAlgorithmAction.triggered.connect(self._play_alankaara_varisai_algorithm)
        self._playGeethamAction.triggered.connect(self._play_geetham)
        self._playVarnamAction.triggered.connect(self._play_varnam)
        self._playSwarajaathiAction.triggered.connect(self._play_swarajaathi)
        self._playVoicePracticeAction.triggered.connect(self._play_voice_practice)
        self._playRaagaPracticeAction.triggered.connect(self._play_raagam_practice)
        ' thaaLam signals '
        self._playSelectedThaaLamAction.triggered.connect(lambda: self._playSelectedThaaLam(avarthanam_count=2))
        self._playSolkattuAction.triggered.connect(self._playSolkattu)
        self._playThaaLamLessonsAction.triggered.connect(self._playThaaLamLessons)
        self._playMetronomeAction.triggered.connect(self._playMetronome)
        ' tools menu signals'
        self._toolsOptionsAction.triggered.connect(self._tools_options_clicked)
        #self._toolsCheckShruthiAction.triggered.connect(self._tools_check_shruthi_clicked)
        self._musicPlayerAction.triggered.connect(self._tools_krithi_player_clicked)
        self._toolsRaagamQuizAction.triggered.connect(self._tools_raagam_quiz_clicked)
        self._toolsVolumeAction.triggered.connect(self._tools_volume_clicked)
        ' help menu signals'
        self._helpAboutAction.triggered.connect(self._help_about_clicked)
        self._helpFeaturesAction.triggered.connect(self._help_features_clicked)
        self._helpUpdateAction.triggered.connect(self._help_update_clicked)
        ' toolbar button signals'
        self._playButtonAction.triggered.connect(self._play_notes_on_screen)
        self._pauseButtonAction.triggered.connect(self._pause_or_resume_playing)
        self._stopButtonAction.triggered.connect(self._stop_playing)
        self._fluteButtonAction.triggered.connect(self._flute_selected)
        self._veenaButtonAction.triggered.connect(self._veena_selected)
        self._violinButtonAction.triggered.connect(self._violin_selected)
        self._mridangamButtonAction.triggered.connect(self._set_percussion_layer_on_off)
        self._raaga_combo.currentIndexChanged.connect(self._raaga_selection_changed)
        self._percussion_instrument_combo.currentIndexChanged.connect(self._percussion_instrument_selected_changed)
        self._thaaLa_combo.currentIndexChanged.connect(self._thaaLa_selection_changed)
        self._jaathi_combo.currentIndexChanged.connect(self._thaaLa_selection_changed)
        self._nadai_combo.currentIndexChanged.connect(self._thaaLa_selection_changed)
        self._shruthi_combo.currentIndexChanged.connect(self._shruthi_selection_changed)
        self._duration_combo.valueChanged.connect(self._duration_selection_changed)
        self._instrument_combo.currentIndexChanged.connect(self._instrument_selection_changed)
    def _percussion_instrument_selected_changed(self):
        percussion_instrument = self._percussion_instrument_combo.currentText()
        settings.CURRENT_PERCUSSION_INSTRUMENT = percussion_instrument
        settings.CURRENT_PERCUSSION_INDEX = settings._get_list_index(percussion_instrument, settings._PERCUSSION_INSTRUMENTS)
    def _search_for_raaga(self):
        raaga_search.show()
        QApplication.processEvents()
        raaga_name = raaga.get_raaga_name(settings.RAAGA_INDEX)
        self._raaga_combo.setCurrentText(raaga_name)
        print("Set the raaga to "+raaga_name)
    def _flute_selected(self):
        self._instrument_combo.setCurrentText(settings._CARNATIC_INSTRUMENTS[2])
    def _veena_selected(self):
        self._instrument_combo.setCurrentText(settings._CARNATIC_INSTRUMENTS[0])
    def _violin_selected(self):
        self._instrument_combo.setCurrentText(settings._DEFAULT_INSTRUMENTS[0])
    def _set_percussion_layer_on_off(self):
        self._include_percussion_layer = not self._include_percussion_layer
        if self._include_percussion_layer:
            self._mridangamButtonAction.setToolTip(self._resources["tipMridangam1"])
        else:
            self._mridangamButtonAction.setToolTip(self._resources["tipMridangam2"])
    def _shruthi_selection_changed(self):
        return
    def _duration_selection_changed(self):
        tempo = self._duration_combo.value()
        settings.TEMPO = tempo
    def _instrument_selection_changed(self):
        playing_instrument = self._instrument_combo.currentText()
        settings.CURRENT_INSTRUMENT = playing_instrument
        settings.INSTRUMENT_INDEX = settings._get_list_index(playing_instrument, settings._INSTRUMENT_LIST)
    def _raaga_selection_changed(self):
        raagam = self._raaga_combo.currentText()
        raaga.set_raagam(raagam)
        aaroganam = raaga.get_aaroganam()
        avaroganam = raaga.get_avaroganam()
        raaga_info = ' '.join(aaroganam) + "\n" + ' '.join(avaroganam)
        self._raga_info_label.setText(raaga_info)
    def _thaaLa_selection_changed(self):
        thaaLam = self._thaaLa_combo.currentText()
        thaaLam = settings.THAALA_NAMES[thaaLam.upper()]
        jaathi = self._jaathi_combo.currentText()
        jaathi = settings.JAATHI_NAMES[jaathi.upper()]
        nadai = self._nadai_combo.currentText()
        nadai = settings.NADAI_NAMES[nadai.upper()]
        thaaLa.set_thaaLam(thaaLam,jaathi,nadai)
        ret = thaaLa.get_thaaLa_positions(as_string=False)
        tmp = ''
        for k,v in ret.items():
            tmp += ' ' + str(k*settings.nadai_no[nadai]) +' ' + str(v)
        thaaLa_info = tmp.strip().strip('\n')
        self._thaaLa_info_label.setText(thaaLa_info)
    def _show_feature_not_implemented(self):
        msg_box = QMessageBox()
        msg_box.setText(self._resources["titFeatureTobeImplemented"])
        msg_box.setWindowTitle(self._resources["titFeatureNotAvailable"])
        msg_box.exec()
    def _delete_file(self,temp_file=_TEMP_FILE):
        if os.path.exists(temp_file):
          os.remove(temp_file)                
    def _new_file(self,file_path=_NOTES_PATH):
        path = QFileDialog.getSaveFileName(self, self._resources["titOpenNotesFile"], file_path, self._resources["titNotesFile"])
        if path:
            self.notes_file = path[0]
            self.setWindowTitle(self._APP_TITLE+"-"+os.path.basename(self.notes_file))
        return self.notes_file
    def _open_file(self,file_path=_NOTES_PATH):
        path = QFileDialog.getOpenFileName(self, self._resources["titOpenNotesFile"], file_path, self._resources["titNotesFile"])
        self.notes_file = path[0]
        if self.notes_file:
            with open(self.notes_file, 'r') as f:
                self._song_info_text.setPlainText(f.read())
            self.setWindowTitle(self._APP_TITLE+"-"+os.path.basename(self.notes_file))
            return True
        return False
    def _close_file(self,file_path=_NOTES_PATH):
        self._save_file(file_path)
        self.notes_file = ""
        self._song_info_text.setPlainText("#Enter commands and notes here")
        self.setWindowTitle(self._APP_TITLE+"-"+os.path.basename(self.notes_file))
    def _save_file(self,file_path=_NOTES_PATH):
        #if self.notes_file.strip() == "":
        save_file = file_path + os.path.basename(self.notes_file)
        path = QFileDialog.getSaveFileName(self, self._resources["titOpenNotesFile"], save_file, self._resources["titNotesFile"])
        if self.notes_file.strip() == "":
            return
        save_file = os.path.abspath(save_file)
        print("Saving to ",save_file)
        contents = self._song_info_text.toPlainText()
        if save_file:
            with open(save_file, 'w') as f:
                f.write(contents)
            f.close()
    def _save_as_pdf(self):
        """
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial",size=12)
        contents = self._song_info_text.toPlainText()
        for text in contents:
            pdf.cell(200,10,txt=text,ln=1)
        pdf_file = self.notes_file.replace(".cmn",".pdf")
        pdf.output(pdf_file)
        """
        self._show_feature_not_implemented()
    def _save_as_audio(self):
        self._save_notes_on_screen_to_temporary_file()
        scamp_note_list,_,solkattu_list = cparser.parse_notation_file(_TEMP_FILE)
        self._update_ui_per_settings()
        temp_midi_file = 'tmp/output.mid' 
        cmidi.write_to_midifile_from_scamp_notes(scamp_note_list,temp_midi_file,include_percussion_layer=self._include_percussion_layer,solkattu_list=solkattu_list)
        path,_ = QFileDialog.getSaveFileName(self, "Save as MP3",settings._TEMP_PATH)
        if path.strip() == "":
            return
        mp3_file = os.path.abspath(path)
        self.MPlayer.save_as_mp3(temp_midi_file,mp3_file)
    def _save_as_lilipond_file(self):
        self._show_feature_not_implemented()
    def _exit_application(self):
        print('exiting the application')
        if self.MPlayer.is_playing:
            print('stopping player before exiting')
            self.MPlayer.stop()
        QApplication.quit()
    def _copy_clipboard(self):
        self._show_feature_not_implemented()
    def _paste_clipboard(self):
        self._show_feature_not_implemented()
    def _generate_lessons(self, lesson_type):
        raagam = self._raaga_combo.currentText()
        thaaLam = settings.THAALA_NAMES[self._thaaLa_combo.currentText().upper()]
        jaathi = settings.JAATHI_NAMES[self._jaathi_combo.currentText()]
        result = lessons.generate_lessons(lesson_type=lesson_type, arrange_notes_to_speed_and_thaaLa=True, raaga_name=raagam, 
                                 thaaLa_index=thaaLam, jaathi_index=jaathi)
        self._song_info_text.setPlainText(result)
    def _generate_sarali_varisai(self):
        self._generate_lessons("SARALI_VARISAI")
    def _generate_jantai_varisai(self):
        self._generate_lessons("JANTAI_VARISAI")
    def _generate_dhaattu_varisai(self):
        self._generate_lessons("DHAATTU_VARISAI")
    def _generate_melsthaayi_varisai(self):
        self._generate_lessons("MELSTHAAYI_VARISAI")
    def _generate_keezhsthaayi_varisai(self):
        self._generate_lessons("KEEZHSTHAAYI_VARISAI")
    def _generate_alankaara_varisai_book(self):
        raagam = self._raaga_combo.currentText()
        result = lessons.alankaara_varisai_from_book(arrange_notes_to_speed_and_thaaLa=True, raaga_name=raagam)
        self._song_info_text.setPlainText(result)
    def _generate_alankaara_varisai_algorithm(self):
        raagam = self._raaga_combo.currentText()
        thaaLa_index = settings.THAALA_NAMES[self._thaaLa_combo.currentText()]
        jaathi_index = settings.JAATHI_NAMES[self._jaathi_combo.currentText()]
        result = lessons.alankaara_varisai_from_algorithm(arrange_notes_to_speed_and_thaaLa=True, raaga_name=raagam, 
                                 thaaLa_index=thaaLa_index, jaathi_index=jaathi_index)
        self._song_info_text.setPlainText(result)
    def _get_kalpana_swara_options(self):
        dlg = QDialog()
        dlg.setWindowModality(Qt.WindowModality.ApplicationModal)
        dlg.setWindowTitle(self._resources['titKalpanaSwaramSettings'])
        v_layout = QVBoxLayout()
        " get default raaga"
        raaga_info = ""
        aroganam = raaga.get_aaroganam()
        avaroganam = raaga.get_avaroganam()
        raaga_info += raaga.get_raaga_name() + " " + ' '.join(aroganam) + " " + ' '.join(avaroganam)
        raaga_info_label = QLabel(raaga_info)
        v_layout.addWidget(raaga_info_label)
        " get thaaLa info"
        thaaLa_info = ""
        t_id,j_id,_ = thaaLa.get_current_thaaLam()
        thaaLa_info += thaaLa.get_thaaLam_names()[t_id]+" "+thaaLa.get_jaathi_names()[j_id]+" "+thaaLa.get_thaaLa_positions(t_id, j_id, as_string=True)
        thaaLa_info_label = QLabel(thaaLa_info)
        v_layout.addWidget(thaaLa_info_label)
        h_layout = QHBoxLayout()
        _lbl = QLabel(self._resources["lblMethod"])
        h_layout.addWidget(_lbl)
        _cmb = QComboBox()
        _cmb.addItems(["Markov","DeepLearn"])
        h_layout.addWidget(_cmb)
        _lbl1 = QLabel(self._resources["lblAvarthanamCount"])
        h_layout.addWidget(_lbl1)
        _spn1 = QSpinBox()
        _spn1.setRange(1,10)
        _spn1.setValue(4)
        h_layout.addWidget(_spn1)
        v_layout.addLayout(h_layout)
        h_layout = QHBoxLayout()
        _lbl2 = QLabel(self._resources["lblStartingNote"])
        h_layout.addWidget(_lbl2)
        _cmb1 = QComboBox()
        _cmb1.addItems(aroganam)
        h_layout.addWidget(_cmb1)
        _lbl3 = QLabel(self._resources["lblEndingNote"])
        h_layout.addWidget(_lbl3)
        _cmb2 = QComboBox()
        _cmb2.addItems(avaroganam)
        h_layout.addWidget(_cmb2)
        v_layout.addLayout(h_layout)
        def _ks_generate_clicked():
            self._ks_method = _cmb.currentText()
            self._ks_starting_note = _cmb1.currentText()
            self._ks_ending_note = _cmb2.currentText()
            self._ks_avarthanam_count = _spn1.value()
            print(self._ks_method,self._ks_starting_note,self._ks_ending_note,self._ks_avarthanam_count)
            self._ks_cancel_generation = False
            dlg.close()
        def _ks_cancel_clicked():
            self._ks_cancel_generation = True
            dlg.close()
        h_layout = QHBoxLayout()
        _btn1 = QPushButton(self._resources["btnGenerate"])
        _btn1.clicked.connect(_ks_generate_clicked)
        h_layout.addWidget(_btn1)
        _btn2 = QPushButton(self._resources["btnCancel"])
        _btn2.clicked.connect(_ks_cancel_clicked)
        h_layout.addWidget(_btn2)
        v_layout.addLayout(h_layout)
        dlg.setLayout(v_layout)
        dlg.exec()
    def _generate_kalpana_swaram_from_corpus(self):
        self._show_feature_not_implemented()
    def _check_to_proceed_with_ks_training(self,model_file):
        if not os.path.exists(model_file):
            msg_box = QMessageBox()
            msg = self._resources['msgModelFileMissing1']
            msg_box.setText(msg)
            msg_i = self._resources['msgModelFileMissing2']
            msg_box.setInformativeText(msg_i)
            btnYes = msg_box.addButton(self._resources['btnYes'],QMessageBox.ButtonRole.AcceptRole)
            btnAbort = msg_box.addButton(self._resources['btnAbort'],QMessageBox.ButtonRole.RejectRole)
            msg_box.exec()
            return (msg_box.clickedButton()==btnYes)
    def _generate_kalpana_swaram_from_lessons(self):
        self._get_kalpana_swara_options()
        if self._ks_cancel_generation:
            return
        _method = self._ks_method.lower()
        _avarthanam_count = self._ks_avarthanam_count
        _starting_note = self._ks_starting_note
        _ending_note = self._ks_ending_note
        raagam = raaga.get_raaga_name(settings.RAAGA_INDEX)
        thaaLa_index,jaathi_index,nadai_index = thaaLa.get_current_thaaLam()
        perform_training = False
        jraaga_notation=True
        if _method.lower() == "deeplearn":
            raagam_model_file = settings._MODEL_WEIGHTS_PATH+raagam+"_lessons.h5"
            if not self._check_to_proceed_with_ks_training(raagam_model_file):
                return
            cdeeplearn.set_parameters(batch_size=20, number_of_epochs=100, model_weights_folder=settings._MODEL_WEIGHTS_PATH)
        result = lessons.generate_kalpana_swarams(method=_method, raaga_name=raagam, starting_note=_starting_note,ending_note=_ending_note,
                                                    thaaLa_index=thaaLa_index, jaathi_index=jaathi_index,nadai_index=nadai_index,
                                                    avarthanam_count=_avarthanam_count,arrange_notes_to_thaaLa=True,
                                                    jraaga_notation=jraaga_notation, save_to_file="../score_output.txt",
                                                    perform_training=perform_training,width=1)
        self._song_info_text.setPlainText(result)
    def _play_sarali_varisai(self):
        self._generate_sarali_varisai()
        self._play_notes_on_screen()
    def _play_aaroganam_avaroganam(self):
        raagam_index = raaga.get_default_raaga_id()
        aaroganam = ' '.join(raaga.get_aaroganam(raagam_index))
        avaroganam = ' '.join(raaga.get_avaroganam(raagam_index))
        str = aaroganam + "\n$$\n" + avaroganam
        self._song_info_text.setPlainText(str)
        self._play_notes_on_screen()
    def _play_jantai_varisai(self):
        self._generate_jantai_varisai()
        self._play_notes_on_screen()
    def _play_dhaattu_varisai(self):
        self._generate_dhaattu_varisai()
        self._play_notes_on_screen()
    def _play_melsthaayi_varisai(self):
        self._generate_melsthaayi_varisai()
        self._play_notes_on_screen()
    def _play_keezhsthaayi_varisai(self):
        self._generate_keezhsthaayi_varisai()
        self._play_notes_on_screen()
    def _play_alankaara_varisai_book(self):
        self._generate_alankaara_varisai_book()
        self._play_notes_on_screen()
    def _play_alankaara_varisai_algorithm(self):
        self._generate_alankaara_varisai_algorithm()
        self._play_notes_on_screen()
    def _play_geetham(self):
        if self._open_file(_GEETHAM_PATH):
            self._play_notes_on_screen()
    def _play_varnam(self):
        if self._open_file(_VARNAM_PATH):
            self._play_notes_on_screen()
    def _play_swarajaathi(self):
        if self._open_file(_SWARAJAATHI_PATH):
            self._play_notes_on_screen()
    def _play_voice_practice(self):
        if self._open_file(_VOICE_PRACTICE_PATH):
            self._play_notes_on_screen()
    def _play_raagam_practice(self):
        if self._open_file(_RAAGA_PRACTICE_PATH):
            self._play_notes_on_screen()
    def _save_notes_on_screen_to_temporary_file(self):
        contents = self._song_info_text.toPlainText()
        QApplication.processEvents()
        self._delete_file(_TEMP_FILE)
        f = open(_TEMP_FILE,"w")
        f.write(contents)
        f.close()
        if os.path.isfile(_TEMP_FILE):
            print("Notes on screen saved to",_TEMP_FILE)
        else:
            print("Notes on screen could not be saved to",_TEMP_FILE)
        return _TEMP_FILE        
    def _stop_playing(self):
        if self.MPlayer and self.MPlayer.is_playing:
            self.MPlayer.stop()
            self._pauseButtonAction.setEnabled(False)
            self._stopButtonAction.setEnabled(False)
            self.MPlayer.is_playing = False
    def _pause_or_resume_playing(self):
        if self.MPlayer and self.MPlayer.is_playing:
            self.MPlayer.pause()
            self._pauseButtonAction.setToolTip('Click to resume the player')
            self.MPlayer.is_playing = False
        elif self.MPlayer and not self.MPlayer.is_playing:
            self.MPlayer.resume()
            self._pauseButtonAction.setToolTip('Click to pause the player')
            self.MPlayer.is_playing = True
    def _update_ui_per_settings(self):
        raaga_id = settings.RAAGA_INDEX
        raagam = settings.RAAGA_DICT[raaga_id]['Name']
        thaaLam = settings.THAALA_NAMES(settings.THAALA_INDEX).name
        jaathi = settings.JAATHI_NAMES(settings.JAATHI_INDEX).name
        nadai = settings.NADAI_NAMES(settings.NADAI_INDEX).name
        print(raaga_id,raagam,thaaLam,jaathi,nadai,'tempo',settings.TEMPO,'Speed=',settings.PLAY_SPEED)
        self._raaga_combo.setCurrentText(raagam)
        self._thaaLa_combo.setCurrentText(thaaLam)
        self._jaathi_combo.setCurrentText(jaathi)
        self._duration_combo.setValue(settings.TEMPO)
        self._nadai_combo.setCurrentText(nadai)
    def _play_notes_on_screen(self):
        """ Save screen notations to _TEMP_FILE """
        self._save_notes_on_screen_to_temporary_file()
        print('changing UI settings per screen notations')
        instrument = self._instrument_combo.currentText()
        self._pauseButtonAction.setEnabled(True)
        self._stopButtonAction.setEnabled(True)
        QApplication.processEvents()
        print('player type',self._player_type)
        if self._player_type == settings.PLAYER_TYPE.SCAMP:
            print('calling scamp player')
            self._pauseButtonAction.setEnabled(False)
            self._stopButtonAction.setEnabled(False)
            file_carnatic_note_list,_,file_solkattu_array = cparser.parse_notation_file(_TEMP_FILE)
            self._update_ui_per_settings()
            QApplication.processEvents()
            if (instrument != None):
                cplayer.set_instrument(instrument)
            cplayer.play_notes(file_carnatic_note_list,self._include_percussion_layer,file_solkattu_array)
        else: # SF2_LOADER Option
            print('calling sf2_loader player')
            self._pauseButtonAction.setEnabled(True)
            self._stopButtonAction.setEnabled(True)
            self.MPlayer.is_playing = True
            scamp_note_list,_,solkattu_list = cparser.parse_notation_file(_TEMP_FILE)
            self._update_ui_per_settings()
            cmidi._write_to_midi_and_play(scamp_note_list,include_percussion_layer=self._include_percussion_layer,solkattu_list=solkattu_list)
        QApplication.processEvents()
        self._delete_file(_TEMP_FILE)
    def _playSelectedThaaLam(self,avarthanam_count=2):
        thaaLa_index = settings.THAALA_NAMES[self._thaaLa_combo.currentText()]
        jaathi_index = settings.JAATHI_NAMES[self._jaathi_combo.currentText()]
        nadai_index = settings.NADAI_NAMES[self._nadai_combo.currentText()]
        solkattu_list = thaaLa.get_thaaLa_patterns_for_avarthanam(avarthanam_count,thaaLa_index=thaaLa_index,jaathi_index=jaathi_index,nadai_index=nadai_index,generate_random=True)
        scamp_note_list = cparser.parse_solkattu(solkattu_list)
        self._song_info_text.setPlainText(' '.join(solkattu_list))
        # since SCAMP notes are already percussion, include_percussion_layer should be False
        if self._player_type == settings.PLAYER_TYPE.SCAMP:
            self._pauseButtonAction.setEnabled(False)
            self._stopButtonAction.setEnabled(False)
            cplayer.play_notes(scamp_note_list, include_percussion_layer=False)
        else: # SF2_LOADER Option
            self._pauseButtonAction.setEnabled(True)
            self._stopButtonAction.setEnabled(True)
            self.MPlayer.is_playing = True
            cmidi.play_solkattu(scamp_note_list)
        QApplication.processEvents()
    def _playSolkattu(self):
        self._save_notes_on_screen_to_temporary_file()
        if self._player_type == settings.PLAYER_TYPE.SCAMP:  # SCAMP Option
            self._pauseButtonAction.setEnabled(False)
            self._stopButtonAction.setEnabled(False)
            cplayer.play_solkattu_from_file(_TEMP_FILE)
        else: # SF2_LOADER Option
            self._pauseButtonAction.setEnabled(True)
            self._stopButtonAction.setEnabled(True)
            self.MPlayer.is_playing = True
            cmidi.play_solkattu_from_file(_TEMP_FILE)
        QApplication.processEvents()
        self._delete_file(_TEMP_FILE)
    def _playThaaLamLessons(self):
        """
            TODO: Since THAALAM_SPEED removed from v1.0.2, Lesson speeds need to be re-implemented
        """
        if self._open_file(_THAALAM_LESSONS_PATH):
            self._playSolkattu()
            return
    def _playMetronome(self):
        thaaLa_index = thaaLa.get_thaaLa_index()
        jaathi_index = thaaLa.get_jaathi_index()
        nadai_index = thaaLa.get_nadai_index()
        sk_list = thaaLa.get_thaaLa_patterns_for_avarthanam(avarthanam_count=1,thaaLa_index=thaaLa_index,jaathi_index=jaathi_index,nadai_index=nadai_index,generate_random=True)
        solkattu_list = []
        for i in range(9): # 10 avarthanams
            solkattu_list += sk_list
        scamp_note_list = cparser.parse_solkattu(solkattu_list)
        self._song_info_text.setPlainText(' '.join(solkattu_list))
        QApplication.processEvents()
        if self._player_type == settings.PLAYER_TYPE.SCAMP:  # SCAMP Option
            self._pauseButtonAction.setEnabled(False)
            self._stopButtonAction.setEnabled(False)
            # since SCAMP notes are already percussion, include_percussion_layer should be False
            cplayer.play_notes(scamp_note_list, include_percussion_layer=False)
        else: # SF2_LOADER Option
            self._save_notes_on_screen_to_temporary_file()
            self._pauseButtonAction.setEnabled(True)
            self._stopButtonAction.setEnabled(True)
            self.MPlayer.is_playing = True
            cmidi.play_solkattu_from_file(_TEMP_FILE)
    def _tools_options_clicked(self):
        self._show_feature_not_implemented()
    def _tools_check_shruthi_clicked(self):
        self._show_feature_not_implemented()
    def _tools_change_language_clicked(self):
        lang_selected_str = self.sender().text()
        lang_selected = list(self._lang_dict.keys())[list(self._lang_dict.values()).index(lang_selected_str)]
        import sys
        settings.set_language(lang_selected)
        TutorUI._APP_LANG = lang_selected
        QApplication.exit(TutorUI._EXIT_CODE_REBOOT)
    def _tools_krithi_player_clicked(self):
        krithi_player.show()
        QApplication.processEvents()        
    def _tools_raagam_quiz_clicked(self):
        from carnatic.ui import quiz
        quiz.show()
    def _tools_volume_clicked(self):
        from carnatic.ui import adjust_volume
        adjust_volume.show()
    def _help_about_clicked(self):
        msg_box = QMessageBox()
        about_msg = self._resources['lblApp']+":\t\t"+self._resources['titApplication']+'\n'
        about_msg += self._resources['lblVersion']+":\t\t"+_APP_VERSION+'\n'
        about_msg += self._resources['lblCreator']+":\t\t"+self._resources['app_author']+'\n'
        about_msg += self._resources['lblWebsite']+":\t"+self._resources['app_url']+'\n'
        msg_box.setText(about_msg)
        msg_box.setWindowTitle(self._resources["titApplication"])
        msg_box.exec()
    def _help_content_clicked(self):
        self._show_feature_not_implemented()
    def _help_features_clicked(self):
        self._show_feature_not_implemented()
    def _help_update_clicked(self):
        self._show_feature_not_implemented()
def show_ui(language=settings._APP_LANG,raaga_list_index=4,player_type:settings.PLAYER_TYPE=settings.PLAYER_TYPE.SF2_LOADER):
    """
        @param language: 'en' for English (default) or 'ta' for Tamil
        @param raaga_list: 
            0 => Show Melakartha raagas only
            1 => Show Sampoorna raagas (note count = 8) only
            2 => Show raagas with 8 or more note count only
            3 => Show all raagas from the raaga input file (/config/raaga_list.inp)
        @return: shows the PyQt UI for PyCarnatic
    """        
    import sys
    def except_hook(exc_type, exc_value, exc_tb):
        import traceback
        tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
        print("Tutor Exception error message:\n", tb)
    TutorUI._APP_LANG = language
    sys.excepthook = except_hook
    currentExitCode = TutorUI._EXIT_CODE_REBOOT
    while currentExitCode==TutorUI._EXIT_CODE_REBOOT:
        app = QApplication(sys.argv)
        window = TutorUI(language=TutorUI._APP_LANG,raaga_list_index=raaga_list_index,player_type=player_type)
        window.show()
        currentExitCode = app.exec()
        app=None
if __name__ == "__main__":
    show_ui(language='ta',
            raaga_list_index=settings.RAAGA_LIST_SELECTION.SIX_OR_MORE_NOTE_RAAGAS_ONLY,
            player_type=settings.PLAYER_TYPE.SF2_LOADER)
    