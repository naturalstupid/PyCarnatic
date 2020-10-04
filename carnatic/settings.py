import os
import configparser
import csv
"""
    Module for global settings for carnatic music guru (carnatic)
"""
""" global file names """
_APP_PATH = os.path.dirname(__file__)
GLOBAL_CONSTANTS_FILE = _APP_PATH + "/config/jraaga.inp"
RAAGA_LIST_FILE = _APP_PATH + "/config/raaga_list.inp"
KRITHI_LIST_FILE = _APP_PATH + "/config/krithi_list.inp"
THAALA_PATTERN_FILE = _APP_PATH + "/config/thaaLaPattern.inp"
_SOUND_FONT_FILE = _APP_PATH + "/Lib/SIWF8.sf2"
""" notation Patterns """
_NOTES_PATTERN_1 = "(([SsPp]|[RrGgMmDdNn][1-4]?)([\\.\\'\\^]?)([</!~>]?[1-5]?))"
_NOTES_PATTERN = "([SsRrGgMmPpDdNn,;\(\)/!][1-4]?[\\.\\'\\^]?[<~>]?[1-5]?)"
_COMMENT_PATTERN = r"^\s*\{(?P<comment>.*)"
_COMMAND_PATTERN = r"^\s*[#|\[\]](?P<cmd_key>[\$DIJMNPST\[\]])(?P<cmd_value>\d+)"
_SILENT_PATTERN = r"(\$)"
_DIRECTION_PATTERN = r"^\s*(?P<dir_key>[UD])(?P<dir_value>.*)"
""" RAAGA SPECIFIC VARIABES """
_WESTERN_SCALE = 0
_CARNATIC_SCALE_12_NOTES = 1
_CARNATIC_SCALE_16_NOTES = 2
_CARNATIC_SCALE_22_NOTES = 3
_SCALE_OF_NOTES = _CARNATIC_SCALE_16_NOTES
CARNATIC_NOTES_LIST_12 = ["S","R1","R2","G2","G3","M1","M2","P","D1","D2","N2","N3","S^","S'"]
WEST_MIDI_NOTES_LIST_12= ["C","C#","D" ,"D#","E" ,"F" ,"F#","G","G#","A" ,"A#","B", "C", "C"]
CARNATIC_NOTES_LIST_16 = ["S",   "R1",  "R2",  "R3",  "G1",  "G2",  "G3",  "M1",  "M2",  "P",   "D1",  "D2",  "D3",  "N1",  "N2",  "N3", "S^","S'"]
WEST_MIDI_NOTES_LIST_16= ["C",   "C#",  "D" ,  "D#",  "D" ,  "D#",  "E" ,  "F" ,  "F#",  "G" ,  "G#",  "A" ,  "A#",  "A",   "A#",  "B",  "C","C"]
KATTAI_LIST            = ["0.5", "1.0", "1.5", "2.0", "1.5", "2.0", "2.5", "3.0", "4.0", "4.5", "5.0", "5.5", "6.0", "5.5", "6.0", "6.5","0.5"]
CARNATIC_NOTES_LIST_22 = ["S","R1","R2","R3","R4","G1","G2","G3","G4","M1","M2","M3","M4","P","D1","D2","D3","D4","N1","N2","N3","N4","S^","S'"]
C12_FREQ_RATIO = [1.0, 16.0/15.0, 9.0/8.0, 6.0/5.0, 5.0/4.0, 4.0/3.0, 45.0/32.0,3.0/2.0, 8.0/5.0, 27.0/16.0, 9.0/5.0, 15.0/8.0, 2.0]
C16_FREQ_RATIO = [1.0, 32.0/31.0, 16.0/15.0, 10.0/9.0, 32.0/27.0, 6.0/5.0, 5.0/4.0, 4.0/3.0, 27.0/20.0, 3.0/2.0, 128.0/81.0, 8.0/5.0, 5.0/3.0, 16.0/9.0, 9.0/5.0, 15.0/8.0, 2.0]
C22_FREQ_RATIO = [1.0, 32.0/31.0, 16.0/15.0, 10.0/9.0, 9.0/8.0, 32.0/27.0, 6.0/5.0, 5.0/4.0, 81.0/64.0, 4.0/3.0, 27.0/20.0, 45.0/32.0, 64.0/45.0, 3.0/2.0, 128.0/81.0, 8.0/5.0, 5.0/3.0, 27.0/16.0, 16.0/9.0, 9.0/5.0, 15.0/8.0, 31.0/16.0, 2.0]
C22_FREQ_RATIO_1 = [1.0, 256.0/243.0, 16.0/15.0, 10.0/9.0, 9.0/8.0, 32.0/27.0, 6.0/5.0, 5.0/4.0, 81.0/64.0, 4.0/3.0, 27.0/20.0, 35.0/32.0, 729.0/512.0, 3.0/2.0, 128.0/81.0, 8.0/5.0, 5.0/3.0, 27.0/16.0, 16.0/9.0, 9.0/5.0, 15.0/8.0, 243.0/129.0, 2.0 ]
BASE_OCTAVE = 3
INSTRUMENT_BASE_NOTES = ["F#3","G3","G#3","A3","A#3","B3","C3","C#3","D3","C2","C2","C2","C2"]
RAAGA_NAMES = []
RAAGA_DICT = {}
RAAGA_INDEX = 52 ## MayaMaalava GowLai
MELAKARTHA_INDEX = 15
MELAKARTHA_DICT = []
KRITHI_NAMES = []
KRITHI_DICT = {}
KRITHI_INDEX = 0
""" THAALA SPECIFIC VARIABLES """
THAALA_INDEX = 4
JAATHI_INDEX = 2
NADAI_INDEX = 0
THAALA_PATTERNS = []
THAALA_PATTERN_COUNTS = []
THAALA_NAMES = ["","EKA","ROOPAKA", "JAMPA", "THRIPUTAI","MATHYA", "ATA", "DHURVA"]
JAATHI_NAMES = ["","THISRA", "CHATHUSRA", "KHANDA", "MISRA", "SANKEERNA"]
NADAI_NAMES = JAATHI_NAMES
jaathi_no = [1,3,4,5,7,9]
thaaLa_laghu_no = [0,1,1,1,1,2,2,3]
thaaLa_drutam_no = [0,0,1,1,2,1,2,1]
thaaLa_anudrutam_no = [0,0,0,1,0,0,0,0]
RHYTHM_NOTE_ARR = ["R", "C","C#","D","D#","E","F","F#","G","G#","A","A#","B","C","C#","D","E","F","E","F#","F","G","G","D#","C#",]
SOLKATTU_ARR =      ["$", "tha", "dhi", "thom", "num", "ki", "ta", "ka", "na", "chap", "dhin", "ta*thom","num*thom", "chap*thom", "dhin*thom", "dhin*tha", "jo", "gu","gi","ri", "mi","nu","na","nam","thi"]
SOLKATTU_NOTE_ARR = ["R", "C3",  "C#3", "D3",   "D#3", "E3", "F3", "F#3","G3", "G#3",  "A3",   "A#3",    "B3",       "C4",        "C#4",       "D4",       "E3", "F3","E3","F#3","F3","G3","G3","D#3","C#3",]
BEAT_LENGTH_SELECTION = [4,5,7,9]
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
_RHYTHM_NOTE_LIST = ["R", "C2",  "C#2", "D2",   "D#2", "E2", "F2", "F#2","G2", "G#2",  "A2",   "A#2",    "B2",       "C3",        "C#3",       "D3",       "E2", "F2","E2","F#2","F2","G2","G2","D#2","C#2"]
_SOLKATTU_LIST =    ["$", "tha", "dhi", "thom", "num", "ki", "ta", "ka", "na", "chap", "dhin", "ta*thom","num*thom", "chap*thom", "dhin*thom", "dhin*tha", "jo", "gu","gi","ri", "mi","nu","na","nam","thi"]
PERCUSSION_BASE_OCTAVE = BASE_OCTAVE
""" SONG COMMAND SETTINGS (Also included are:  MELAKARTHA_INDEX, THAALA_INDEX and JAATHI_INDEX) """
TEMPO = 72
PLAY_SPEED = 1
THAALAM_SPEED = 1
PLAYER_MODE = 1 # 1 for Carnatic Notes and 2 for Solkattu
_FULL_NOTE_DURATION = 1.0
_KAMPITAM_NOTE_STEP = 0.2
_MICROTONE_PITCH_INCREMENT = 0.1
_VOLUME = 1
_CARNATIC_INSTRUMENTS = ["Veena","Veena2","Flute","Sarod",]
_DEFAULT_INSTRUMENTS = ["Violin","Sitar","Shenai","Piano","Guitar"]
_PERCUSSION_INSTRUMENTS = ["Mridangam","EastWestMix"]
CURRENT_INSTRUMENT = "Veena" #_CARNATIC_INSTRUMENTS[0]
INSTRUMENT_INDEX = 0
CURRENT_PERCUSSION_INSTRUMENT = "Mridangam"

def _custom_formatwarning(msg, *args, **kwargs):
    # ignore everything except the message
    return str(msg) + '\n'
def get_application_path():
    """ 
        Get Application Path (oath to site package)
        @return: application path
    """
    return _APP_PATH
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
def get_raaga_dictionary():
    """
        Reads config/raaga_kist.inp and store raaga dictionary in RAAGA_DICT variable
    """
    csv_data = open(RAAGA_LIST_FILE,'r')
    RAAGA_DICT.clear()
    with csv_data:
        reader = csv.reader(csv_data)
        headers = next(reader)
        headers[0]='id'
        RAAGA_NAMES.clear()
        for row in reader:
            RAAGA_NAMES.append(row[2])
            RAAGA_DICT[int(row[0])] = {key: value for key, value in zip(headers, row)}
    return RAAGA_DICT
def get_melakartha_dictionary():
    """
        Create Melakartha List into RAAGA_DICT variable
    """
    if RAAGA_DICT:
        MELAKARTHA_DICT.clear()
        for raaga_id in range(len(RAAGA_DICT)):
            if 'mELakartha-' in RAAGA_DICT[raaga_id]['Melakartha_or_Janya']:
                raaga_name = RAAGA_DICT[raaga_id]['Name']
                MELAKARTHA_DICT.append([raaga_id,raaga_name])
        return MELAKARTHA_DICT
def _get_krithi_dictionary():
    csv_data = open(KRITHI_LIST_FILE,'r')
    KRITHI_DICT.clear()
    with csv_data:
        reader = csv.reader(csv_data)
        headers = next(reader)
        headers[0]='id'
        KRITHI_NAMES.clear()
        for row in reader:
            raaga_name = row[2]
            if raaga_name.upper() in (name.upper() for name in RAAGA_NAMES):
                KRITHI_NAMES.append(row[1])
                KRITHI_DICT[int(row[0])] = {key: value for key, value in zip(headers, row)}
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
        #print(section_items)
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

print("Application Path",_APP_PATH)
get_global_settings()
RAAGA_DICT = get_raaga_dictionary()
#print(RAAGA_DICT.keys())
#print(RAAGA_DICT)
KRITHI_DICT = _get_krithi_dictionary()
MELAKARTHA_DICT = get_melakartha_dictionary()
THAALA_PATTERNS = get_thaaLa_patterns()
#print('KRITHI_DICT length',len(KRITHI_DICT))