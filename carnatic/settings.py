import os
import configparser
import csv
from enum import IntEnum
"""
    PyCarnatic supports two types of players using either SCAMP or SF2_LOADER
    Change the PLAYER_TYPE to one of the following
    PLAYER_TYPE = "SCAMP"
    PLAYER_TYPE = "SF2_LOADER
    NOTE: SF2_LOADER can pause/resume music. SCAMP cannot pause/resume player
"""
### Enums
PLAYER_TYPE = IntEnum("PLAYER_TYPE","SCAMP SF2_LOADER")
_PLAYER_TYPE = PLAYER_TYPE.SF2_LOADER
RAAGA_LIST_SELECTION = IntEnum("RAAGA_LIST_SELECTION","KRITHI_RAAGAS_ONLY MELAKARTHA_RAAGAS_ONLY SAMPOORNA_RAAGAS_ONLY SIX_OR_MORE_NOTE_RAAGAS_ONLY ALL_RAAGAS")
RAAGA_LIST_SELECTION_INDEX = RAAGA_LIST_SELECTION.SIX_OR_MORE_NOTE_RAAGAS_ONLY

"""
    Module for global settings for carnatic music guru (carnatic)
"""
_APP_PATH = os.path.dirname(__file__)
_APP_LANG = "en"
_APP_LANGUAGES = []
_APP_LANG_STR1 = "msg_strings_"
_APP_LANG_STR2 = ".txt"
""" global path names """
_SAVE_FILES_PATH = "./"
_LIB_PATH = _APP_PATH + "/Lib/"
_TEMP_PATH = _APP_PATH + "/tmp/"
_CONFIG_PATH = _APP_PATH + "/Config/"
_LANGUAGE_PATH = _APP_PATH + "/lang/"
_IMAGES_PATH = _APP_PATH + "/images/"
_NOTES_PATH = _APP_PATH + "/Notes/"
_LESSONS_PATH = _APP_PATH + "/Lessons/"
_GEETHAM_PATH = _LESSONS_PATH + "Geetham/"
_VARNAM_PATH = _LESSONS_PATH + "Varnam/"
_SWARAJAATHI_PATH = _LESSONS_PATH + "Swarajaathi/"
_VOICE_PRACTICE_PATH = _LESSONS_PATH + "Voice/"
_RAAGA_PRACTICE_PATH = _LESSONS_PATH + "Raaga/"
_THAALAM_LESSONS_PATH = _LESSONS_PATH + "Percussion/"
_MODEL_WEIGHTS_PATH = _APP_PATH + "/model_weights/"
""" global file names """
_TEMP_FILE = _TEMP_PATH + "delme.cmn"
GLOBAL_CONSTANTS_FILE = _CONFIG_PATH + "jraaga.inp"
RAAGA_LIST_FILE = _CONFIG_PATH + "raaga_list.inp"
KRITHI_LIST_FILE = _CONFIG_PATH + "krithi_list.inp"
THAALA_PATTERN_FILE = _CONFIG_PATH + "thaaLaPattern2.inp"
""" notation Patterns """
_NOTES_PATTERN_1 = "(([SsPp]|[RrGgMmDdNn][1-4]?)([\\.\\'\\^]?)([</!~>]?[1-5]?))"
_NOTES_PATTERN = "([SsRrGgMmPpDdNn,;\(\)/!][1-4]?[\\.\\'\\^]?[<~>]?[1-5]?)"
_COMMENT_PATTERN = r"^\s*\{(?P<comment>.*)"
_COMMAND_PATTERN = r"^\s*[#](?P<cmd_key>[\$CDIJMNPST])(?P<cmd_value>\d*)" # V1.2.2 Removed K and added C
_SILENT_PATTERN = r"(\$)"
_DIRECTION_PATTERN = r"^\s*(?P<dir_key>[UD])(?P<dir_value>.*)"
""" RAAGA SPECIFIC VARIABES """
SCALE_OF_NOTES = IntEnum("SCALE_OF_NOTES","WESTERN_SCALE CARNATIC_SCALE_12_NOTES CARNATIC_SCALE_16_NOTES CARNATIC_SCALE_22_NOTES")
SCALE_OF_NOTES_INDEX = SCALE_OF_NOTES.CARNATIC_SCALE_16_NOTES
CARNATIC_NOTES_LIST_12 = ["S","R1","R2","G2","G3","M1","M2","P","D1","D2","N2","N3","S^","S'"]
WEST_MIDI_NOTES_LIST_12= ["C","C#","D" ,"D#","E" ,"F" ,"F#","G","G#","A" ,"A#","B", "C", "C"]
CARNATIC_NOTES_LIST_16 = ["S",   "R1",  "R2",  "R3",  "G1",  "G2",  "G3",  "M1",  "M2",  "P",   "D1",  "D2",  "D3",  "N1",  "N2",  "N3", "S^","S'"]
WEST_MIDI_NOTES_LIST_16= ["C",   "C#",  "D" ,  "D#",  "D" ,  "D#",  "E" ,  "F" ,  "F#",  "G" ,  "G#",  "A" ,  "A#",  "A",   "A#",  "B",  "C","C"]
KATTAI_LIST            = ["1.0", "1.5", "2.0", "2.5", "3.0", "4.0", "4.5", "5.0", "5.5", "6.0", "6.5"]
CARNATIC_NOTES_LIST_22 = ["S","R1","R2","R3","R4","G1","G2","G3","G4","M1","M2","M3","M4","P","D1","D2","D3","D4","N1","N2","N3","N4","S^","S'"]
WEST_MIDI_NOTES_LIST_22= ["C","C#","C#","D","D","D#","D#","E","E","F","F","F#","F#","G","G#","G#","A","A","A#","A#","B","B","C","C"]
BASE_OCTAVE = 4
#INSTRUMENT_BASE_NOTES = ["G#3","G#3","G#3","G#3","G#3","G#3","G#3","G#3","G#3","C3","C#3","C3","C#3"]
INSTRUMENT_BASE_NOTES = ["D#4","D#4","D#4","D#4","D#4","D#4","D#4","D#4","D#4","C4","C#4","C4","C#4"]
RAAGA_NAMES = []
RAAGA_DICT = {}
RAAGA_INDEX = 52 ## MayaMaalava GowLai
MELAKARTHA_INDEX = 15
MELAKARTHA_DICT = []
KRITHI_NAMES = []
KRITHI_DICT = {}
KRITHI_INDEX = 0
""" THAALA SPECIFIC VARIABLES """
THAALA_PATTERNS = []
THAALA_PATTERN_COUNTS = []
THAALA_NAMES = IntEnum("THAALA_NAMES","EKA ROOPAKA JAMPA THRIPUTAI MATHYA ATA DHURVA")
JAATHI_NAMES = IntEnum("JAATHI_NAMES","THISRA CHATHUSRA KHANDA MISRA SANKEERNA")
#NADAI_NAMES = JAATHI_NAMES
NADAI_NAMES = IntEnum("NADAI_NAMES","FIRST_SPEED SECOND_SPEED THISRA CHATHUSRA_THIRD_SPEED KHANDA MISRA SANKEERNA")
THAALA_INDEX = THAALA_NAMES.THRIPUTAI
JAATHI_INDEX = JAATHI_NAMES.CHATHUSRA
NADAI_INDEX = NADAI_NAMES.CHATHUSRA_THIRD_SPEED
jaathi_no = [1,3,4,5,7,9]
nadai_no = [0,1,2,3,4,5,7,9]
thaaLa_laghu_no = [0,1,1,1,1,2,2,3]
thaaLa_drutam_no = [0,0,1,1,2,1,2,1]
thaaLa_anudrutam_no = [0,0,0,1,0,0,0,0]
RHYTHM_NOTE_ARR = ["R", "C","C#","D","D#","E","F","F#","G","G#","A","A#","B","C","C#","D","E","F","E","F#","F","G","G","D#","C#",]
SOLKATTU_ARR =      ["$", "tha", "dhi", "thom", "num", "ki", "ta", "ka", "na", "chap", "dhin", "ta*thom","num*thom", "chap*thom", "dhin*thom", "dhin*tha", "jo", "gu", "gi", "ri", "mi","nu","na", "nam","thi"]
SOLKATTU_NOTE_ARR = ["R", "C3",  "C#3", "D3",   "D#3", "E3", "F3", "F#3","G3", "G#3",  "A3",   "A#3",    "B3",       "C4",        "C#4",       "D4",       "C3", "C#3","D3", "D#3","E3","F3","F#3","G3", "G#3"]
BEAT_LENGTH_SELECTION = [3,4,5,7,9]
THAALA_LOC = [ 
 [ {1:"||\n"},{1:"||\n"},{1:"||\n"},{1:"||\n"},{1:"||\n"},{1:"||\n"}],
 [ {1:"||\n"},{3:"||\n"},{4:"||\n"},{5:"||\n"},{7:"||\n"},{9:"||\n"}],
 [ {1:"||\n"},{2:"|",5:"||\n"}, {2:"|",6:"||\n"}, {2:"|",7:"||\n"}, {2:"|",9:"||\n"}, {2:"|",11:"||\n"} ],
 [ {1:"||\n"}, {3:"|",4:"|",6:"||\n"}, {4:"|",5:"|",7:"||\n"}, {5:"|",6:"|",8:"||\n"}, {7:"|",8:"|",10:"||\n"}, {9:"|",10:"|",12:"||\n"} ],
 [ {1:"||\n"}, {3:"|",5:"|",7:"||\n"}, {4:"|",6:"|",8:"||\n"}, {5:"|",7:"|",9:"||\n"}, {7:"|",9:"|",11:"||\n"}, {9:"|",11:"|",13:"||\n"} ],
 [ {1:"||\n"}, {3:"|",5:"|",8:"||\n"}, {4:"|",6:"|",10:"||\n"}, {5:"|",7:"|",12:"||\n"}, {7:"|",9:"|",16:"||\n"}, {9:"|",11:"|",20:"||\n"} ],
 [ {1:"||\n"}, {3:"|",6:"|",8:"|",10:"||\n"}, {4:"|",8:"|",10:"|",12:"||\n"}, {5:"|",10:"|",12:"|",14:"||\n"}, {7:"|",14:"|",16:"|",18:"||\n"}, {9:"|",18:"|",20:"|",22:"||\n"} ],
 [ {1:"||\n"}, {3:"|",5:"|",8:"|",11:"||\n"}, {4:"|",6:"|",10:"|",14:"||\n"}, {5:"|",7:"|",12:"|",17:"||\n"}, {7:"|",9:"|",16:"|",23:"||\n"}, {9:"|",11:"|",20:"|",29:"||\n"} ]
]
#_RHYTHM_NOTE_LIST = ["R", "C2",  "C#2", "D2",   "D#2", "E2", "F2", "F#2","G2", "G#2",  "A2",   "A#2",    "B2",       "C3",        "C#3",       "D3",       "E2", "F2","E2","F#2","F2","G2","G2","D#2","C#2"]
_RHYTHM_NOTE_LIST = ["R", "C3",  "C#3", "D3",   "D#3", "E3", "F3", "F#3","G3", "G#3",  "A3",   "A#3",    "B3",       "C4",        "C#4",       "D4",       "C#3","D3", "D#3","E3","F3","F#3","G3", "G#3", "A3"]
_SOLKATTU_LIST =    [",", "tha", "dhi", "thom", "num", "ki", "ta", "ka", "na", "chap", "dhin", "ta*thom","num*thom", "chap*thom", "dhin*thom", "dhin*tha", "jo", "gu", "gi", "ri", "mi","nu","na", "nam","thi"]
PERCUSSION_BASE_OCTAVE = BASE_OCTAVE
""" SONG COMMAND SETTINGS (Also included are:  MELAKARTHA_INDEX, THAALA_INDEX and JAATHI_INDEX) """
TEMPO = 60 # Changed in V1.2.3
PLAY_SPEED = 1
PLAY_SPEED_MAX = 4
PLAYER_MODE = 1 # 1 for Carnatic Notes and 2 for Solkattu
_FULL_NOTE_DURATION = 1.0 # 0.25 quarter, 0.5 half, 1.0 full
_KAMPITAM_NOTE_STEP = 0.2
_MICROTONE_PITCH_INCREMENT = 0.1
_PITCH_BEND_MAX = 8192
" Note that SCAMP uses 0.0 to 1.0 for volume range whereas SF2_LOADER uses 0 to 127 integer"
_VOLUME = 1.0 # 0.0 to 1.0 (of _VOLUME_MAX)
_VOLUME_MAX = 127
" Flatten a list of lists "
flatten_list = lambda list: [item for sublist in list for item in sublist]

def _get_list_index(name, list):
    return list.index(name)
def _get_list_name(index, list):
    return list[index]    
def _custom_formatwarning(msg, *args, **kwargs):
    # ignore everything except the message
    return str(msg) + '\n'
def get_application_path():
    """ 
        Get Application Path (oath to site package)
        @return: application path
    """
    return _APP_PATH
def set_raaga_list_selection(raaga_list_index):
    _rli = RAAGA_LIST_SELECTION(raaga_list_index)
    assert (_rli.value >= 1 and _rli.value <= len(RAAGA_LIST_SELECTION)) 
    global RAAGA_LIST_SELECTION_INDEX, RAAGA_DICT,RAAGA_NAMES, MELAKARTHA_DICT,KRITHI_DICT
    RAAGA_LIST_SELECTION_INDEX = _rli
    print('raaga_list_index set to ',RAAGA_LIST_SELECTION_INDEX)
    get_raaga_dictionary()
    get_melakartha_dictionary()
    _get_krithi_dictionary()
def get_raaga_dictionary():
    """
        Reads config/raaga_kist.inp and store raaga dictionary in RAAGA_DICT variable
    """
    global RAAGA_DICT, RAAGA_NAMES,RAAGA_LIST_SELECTION_INDEX
    csv_data = open(RAAGA_LIST_FILE,'r')
    RAAGA_DICT.clear()
    with csv_data:
        reader = csv.reader(csv_data)
        headers = next(reader)
        headers[0]='id'
        RAAGA_NAMES.clear()
        raaga_id = -1
        for row in reader:
            not_krithi_raaga = row[9].strip() ==''
            not_melakartha_raaga = 'mELakartha-' not in row[-2]
            not_sampoorna_raaga = (int(row[5]) != 8) and (int(row[6]) != 8)
            not_raaga_with_6_or_more_notes = (int(row[5]) < 6) or (int(row[6]) < 6) and (int(row[5]) != int(row[6]))
            if RAAGA_LIST_SELECTION_INDEX == RAAGA_LIST_SELECTION.KRITHI_RAAGAS_ONLY and not_krithi_raaga:
                continue
            elif RAAGA_LIST_SELECTION_INDEX == RAAGA_LIST_SELECTION.MELAKARTHA_RAAGAS_ONLY and not_melakartha_raaga:
                continue
            elif RAAGA_LIST_SELECTION_INDEX == RAAGA_LIST_SELECTION.SAMPOORNA_RAAGAS_ONLY and not_sampoorna_raaga:
                continue
            elif RAAGA_LIST_SELECTION_INDEX == RAAGA_LIST_SELECTION.SIX_OR_MORE_NOTE_RAAGAS_ONLY and not_raaga_with_6_or_more_notes:
                continue
            raaga_id += 1
            RAAGA_NAMES.append(row[2])
            #RAAGA_DICT[int(row[0])] = {key: value for key, value in zip(headers, row)}
            RAAGA_DICT[raaga_id] = {key.strip(): value.strip() for key, value in zip(headers, row)}
            RAAGA_DICT[raaga_id]['id'] = raaga_id
    return RAAGA_DICT
def get_melakartha_dictionary():
    """
        Create Melakartha List into MELAKARTHA_DICT variable
    """
    global MELAKARTHA_DICT
    if RAAGA_DICT:
        MELAKARTHA_DICT.clear()
        for raaga_id in range(len(RAAGA_DICT)):
            if 'mELakartha-' in RAAGA_DICT[raaga_id]['Melakartha_or_Janya']:
                raaga_name = RAAGA_DICT[raaga_id]['Name']
                MELAKARTHA_DICT.append([raaga_id,raaga_name])
        return MELAKARTHA_DICT
def _get_krithi_dictionary():
    global KRITHI_DICT
    csv_data = open(KRITHI_LIST_FILE,'r')
    KRITHI_DICT.clear()
    with csv_data:
        reader = csv.reader(csv_data)
        headers = next(reader)
        headers[0]='id'
        KRITHI_NAMES.clear()
        for row in reader:
            raaga_name = row[2]
            mp3_link = row[7]
            if raaga_name.upper() in (name.upper() for name in RAAGA_NAMES):
                KRITHI_NAMES.append(row[1])
                KRITHI_DICT[int(row[0])] = {key.strip(): value.strip() for key, value in zip(headers, row)}
    return KRITHI_DICT
def _combination(list1, list2,reverse=True):
    lst1 =  [(x +" " + y) for x in list1 for y in list2]
    if reverse:
        lst2 = [ (y +" " + x) for x in list1 for y in list2]
        combined_list = lst1 + lst2
    else:
        combined_list = lst1
    return combined_list
def get_thaaLa_patterns():
    """
        Read fundamental (2.3.4.5) Thaala patterns from config/thaaLaPattern.inp
    """
    thaaLa_config = configparser.ConfigParser()
    thaala_settings = thaaLa_config.read(THAALA_PATTERN_FILE)
    sections = thaaLa_config.sections()
    THAALA_PATTERNS.clear()
    THAALA_PATTERN_COUNTS.clear()
    for section in sections:
        section_items =  dict(thaaLa_config.items(section))
        for key in section_items:
            key_id = int(key)-1
            patterns = list(part for part in section_items[key].replace("|","").split(";") if (part.strip() != "|" and part.strip() !="") )
            THAALA_PATTERNS.append(patterns)
    """ Now construct for 5-beats to 9 beats """
    """ 5 beats = 1 + 4 and 4 + 1 """
    THAALA_PATTERNS.append(_combination(THAALA_PATTERNS[0],THAALA_PATTERNS[3]))
    """ 6 beats = 1 + 5 and 5 + 1 and 3 + 3"""
    lst1 = _combination(THAALA_PATTERNS[1],THAALA_PATTERNS[3])
    lst2 = _combination(THAALA_PATTERNS[1],THAALA_PATTERNS[3],False)
    THAALA_PATTERNS.append(lst1+lst2)
    
    """ 7 beats = 2 + 5 and 5 + 2 and 3 + 4 and 4+3 """
    lst1 = _combination(THAALA_PATTERNS[1],THAALA_PATTERNS[4])
    lst2 = _combination(THAALA_PATTERNS[2],THAALA_PATTERNS[3])
    THAALA_PATTERNS.append(lst1+lst2)
    
    """ 8 beats = 3 + 5 and 5 + 3 and 4 + 4  2+6/6+2 """
    lst1 = _combination(THAALA_PATTERNS[2],THAALA_PATTERNS[4])
    lst2 = _combination(THAALA_PATTERNS[1],THAALA_PATTERNS[5])
    lst3 = _combination(THAALA_PATTERNS[3],THAALA_PATTERNS[3],False)
    THAALA_PATTERNS.append(lst1+lst2+lst3)
    
    """ 9 beats = 4 + 5 and 5 + 4 and 3 + 6 and 6+3 and 2+7/7+2"""
    lst1 = _combination(THAALA_PATTERNS[3],THAALA_PATTERNS[4])
    lst2 = _combination(THAALA_PATTERNS[5],THAALA_PATTERNS[2])
    lst3 = _combination(THAALA_PATTERNS[1],THAALA_PATTERNS[6])
    THAALA_PATTERNS.append(lst1+lst2+lst3)
    
    for pattern in THAALA_PATTERNS:
        THAALA_PATTERN_COUNTS.append(len(pattern))
    return THAALA_PATTERNS
def _get_solkattu_regex_pattern():
    sk_pat = "("
    for sk in SOLKATTU_ARR[1:]:
        sk_pat += sk + "|"
    sk_pat += "\(|\)"
    sk_pat = sk_pat+")?"
    sk_pat = sk_pat.replace("*", "\*")
    return sk_pat
def _get_resource_dictionary(lang):
    if lang in _APP_LANGUAGES:
        _APP_LANG = lang
    msg_file = _LANGUAGE_PATH+_APP_LANG_STR1+_APP_LANG+_APP_LANG_STR2
    import os.path
    from os import path
    import codecs
    if not path.exists(msg_file):
        print('Error: List Types File:'+msg_file+' does not exist. Script aborted.')
        exit()        
    resources = {}
    with codecs.open(msg_file, encoding='utf-8', mode='r') as fp:
        line_list = fp.read().splitlines()
    fp.close()
    for line in line_list: #  fp:
        line_new = line.replace("\r\n","").replace("\r","").rstrip().lstrip()
        if line_new == "":
            continue
        if line_new[0] == '#':
            continue
        #print(line_new)
        splitLine = line_new.split('=',1)
        key = splitLine[0].strip()
        value = splitLine[1].strip()
        resources[key]=value
    return resources       

def _get_available_languages():
    lang_list = []
    for file in os.listdir(_LANGUAGE_PATH):
        if _APP_LANG_STR1 in file and _APP_LANG_STR2 in file:
            lang = file.replace(_APP_LANG_STR1,"")
            lang = lang.replace(_APP_LANG_STR2,"")
            if len(lang)==2:
                lang_list.append(lang)
            else:
                print("The language part in msg_strings file should be only two char long. e.g. 'en'",lang)
    return lang_list
def set_language(lang):
    global _APP_LANG, _RESOURCES
    if lang in _APP_LANGUAGES:
        _APP_LANG = lang
        _RESOURCES = _get_resource_dictionary(lang)
        _set_instrument_list()
        #import inspect
        #print('Setting language to',lang,'called by',inspect.stack()[1].function)

_APP_LANGUAGES = _get_available_languages()            

print("Application Path",_APP_PATH,_APP_LANGUAGES,_APP_LANG)
_RESOURCES = _get_resource_dictionary(_APP_LANG)
_CARNATIC_INSTRUMENTS = _RESOURCES['_CARNATIC_INSTRUMENTS'].split(',') # ["Veena","Veena2","Flute","Sarod",]
_DEFAULT_INSTRUMENTS = _RESOURCES['_DEFAULT_INSTRUMENTS'].split(',') # ["Violin","Sitar","Shenai","Piano","Guitar"] #[0-Piano,24-Guitar,Violib-40,Sitar=104,Shenai-111[
_PERCUSSION_INSTRUMENTS = _RESOURCES['_PERCUSSION_INSTRUMENTS'].split(',') # ["Mridangam","Thavil"]
_INSTRUMENT_LIST = _CARNATIC_INSTRUMENTS + _DEFAULT_INSTRUMENTS
_ALL_INSTRUMENTS = _INSTRUMENT_LIST + _PERCUSSION_INSTRUMENTS 
def _set_instrument_list():
    global _CARNATIC_INSTRUMENTS,_DEFAULT_INSTRUMENTS, _PERCUSSION_INSTRUMENTS,_INSTRUMENT_LIST,_ALL_INSTRUMENTS
    global CURRENT_INSTRUMENT, INSTRUMENT_INDEX, CURRENT_PERCUSSION_INSTRUMENT,CURRENT_PERCUSSION_INDEX
    global _INSTRUMENT_VOLUME_LEVELS
    _CARNATIC_INSTRUMENTS = _RESOURCES['_CARNATIC_INSTRUMENTS'].split(',') # ["Veena","Veena2","Flute","Sarod",]
    _DEFAULT_INSTRUMENTS = _RESOURCES['_DEFAULT_INSTRUMENTS'].split(',') # ["Violin","Sitar","Shenai","Piano","Guitar"] #[0-Piano,24-Guitar,Violib-40,Sitar=104,Shenai-111[
    _PERCUSSION_INSTRUMENTS = _RESOURCES['_PERCUSSION_INSTRUMENTS'].split(',') # ["Mridangam","Thavil"]
    _INSTRUMENT_LIST = _CARNATIC_INSTRUMENTS + _DEFAULT_INSTRUMENTS
    _ALL_INSTRUMENTS = _INSTRUMENT_LIST + _PERCUSSION_INSTRUMENTS 
    if _PLAYER_TYPE == PLAYER_TYPE.SF2_LOADER:
        _INSTRUMENT_VOLUME_LEVELS = [ int(_VOLUME*_VOLUME_MAX) for inst in _ALL_INSTRUMENTS ]
    else:
        _INSTRUMENT_VOLUME_LEVELS = [ _VOLUME for inst in _ALL_INSTRUMENTS ]
    CURRENT_INSTRUMENT = _CARNATIC_INSTRUMENTS[0]
    INSTRUMENT_INDEX = _INSTRUMENT_LIST.index(CURRENT_INSTRUMENT)
    CURRENT_PERCUSSION_INDEX = int(config['percussion_instrument'])
    CURRENT_PERCUSSION_INSTRUMENT = _PERCUSSION_INSTRUMENTS[CURRENT_PERCUSSION_INDEX]
    #print(_ALL_INSTRUMENTS)
    global THAALA_NAMES,JAATHI_NAMES,NADAI_NAMES
    THAALA_NAMES = IntEnum("THAALA_NAMES",_RESOURCES['THAALA_NAMES'].split(','))
    JAATHI_NAMES = IntEnum("JAATHI_NAMES",_RESOURCES['JAATHI_NAMES'].split(','))
    NADAI_NAMES = IntEnum("NADAI_NAMES",_RESOURCES['NADAI_NAMES'].split(','))

def get_global_settings():
    """
        read global settings from config/jraaga.inp and set them before using carnatic modules
    """
    config = configparser.ConfigParser()
    config.read(GLOBAL_CONSTANTS_FILE)
    sections = config.sections()
    settings = {}
    for section in sections:
        section_items =  dict(config.items(section))
        #print(section_items)
        for key in section_items:
            #print(key, section_items[key])
            settings[key] = section_items[key]
    return settings

" Set global values from global config file"
config = get_global_settings()
_PLAYER_TYPE = int(config['player_type'])
SCALE_OF_NOTES_INDEX = int(config['scale_of_notes'])
_APP_LANG = config['language']
_SOUND_FONT_FILE = _LIB_PATH + config['sound_font_file'] # "SIWF10.sf2"
set_raaga_list_selection(int(config['raaga_selection'])) # SIX_OR_MORE_NOTE_RAAGAS_ONLY
_FULL_NOTE_DURATION = float(config['note_duration'])
CURRENT_PERCUSSION_INDEX = int(config['percussion_instrument']) 
CURRENT_PERCUSSION_INSTRUMENT = _PERCUSSION_INSTRUMENTS[CURRENT_PERCUSSION_INDEX]
#C12_FREQ_RATIO = [1.0, 16.0/15.0, 9.0/8.0, 6.0/5.0, 5.0/4.0, 4.0/3.0, 45.0/32.0,3.0/2.0, 8.0/5.0, 27.0/16.0, 9.0/5.0, 15.0/8.0, 2.0]
#C16_FREQ_RATIO = [1.0, 32.0/31.0, 16.0/15.0, 10.0/9.0, 32.0/27.0, 6.0/5.0, 5.0/4.0, 4.0/3.0, 27.0/20.0, 3.0/2.0, 128.0/81.0, 8.0/5.0, 5.0/3.0, 16.0/9.0, 9.0/5.0, 15.0/8.0, 2.0]
#C22_FREQ_RATIO = [1.0, 32.0/31.0, 16.0/15.0, 10.0/9.0, 9.0/8.0, 32.0/27.0, 6.0/5.0, 5.0/4.0, 81.0/64.0, 4.0/3.0, 27.0/20.0, 45.0/32.0, 64.0/45.0, 3.0/2.0, 128.0/81.0, 8.0/5.0, 5.0/3.0, 27.0/16.0, 16.0/9.0, 9.0/5.0, 15.0/8.0, 31.0/16.0, 2.0]
C22_FREQ_RATIO_1 = [1.0, 256.0/243.0, 16.0/15.0, 10.0/9.0, 9.0/8.0, 32.0/27.0, 6.0/5.0, 5.0/4.0, 81.0/64.0, 4.0/3.0, 27.0/20.0, 35.0/32.0, 729.0/512.0, 3.0/2.0, 128.0/81.0, 8.0/5.0, 5.0/3.0, 27.0/16.0, 16.0/9.0, 9.0/5.0, 15.0/8.0, 243.0/129.0, 2.0 ]
C12_FREQ_RATIO = [float(eval(f)) for f in config['carnatic_freq_12'].split(",")]
C16_FREQ_RATIO = [float(eval(f)) for f in config['carnatic_freq_16'].split(",")]
C22_FREQ_RATIO = [float(eval(f)) for f in config['carnatic_freq_22'].split(",")]
_MAINTAIN_NADAI = False
RAAGA_DICT = get_raaga_dictionary()
#print(RAAGA_DICT)
KRITHI_DICT = _get_krithi_dictionary()
MELAKARTHA_DICT = get_melakartha_dictionary()
THAALA_PATTERNS = get_thaaLa_patterns()
_SOLKATTU_PATTERN = _get_solkattu_regex_pattern()

set_language(_APP_LANG)
