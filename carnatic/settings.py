import configparser
import csv

""" file names """
GLOBAL_CONSTANTS_FILE = "config/jraaga.inp"
RAAGA_LIST_FILE = "config/raaga_list.inp"
KRITHI_LIST_FILE = "config/krithi_list.inp"
THAALA_PATTERN_FILE = "config/thaaLaPattern.inp"
""" RAAGA SPECIFIC VARIABES """
WESTERN_SCALE = 0
CARNATIC_SCALE_12_NOTES = 1
CARNATIC_SCALE_16_NOTES = 2
CARNATIC_SCALE_22_NOTES = 3
SCALE_OF_NOTES = CARNATIC_SCALE_16_NOTES
CARNATIC_NOTES_LIST_12 = ["S","R1","R2","G2","G3","M1","M2","P","D1","D2","N2","N3","S^","S'"]
WEST_MIDI_NOTES_LIST_12= ["C","C#","D" ,"D#","E" ,"F" ,"F#","G","G#","A" ,"A#","B", "C", "C"]
CARNATIC_NOTES_LIST_16 = ["S","R1","R2","R3","G1","G2","G3","M1","M2","P","D1","D2","D3","N1","N2","N3","S^"]
WEST_MIDI_NOTES_LIST_16= ["C","C#","D" ,"D#","D" ,"D#","E" ,"F" ,"F#","G" ,"G#","A" ,"A#","A","A#", "B", "C"]
CARNATIC_NOTES_LIST_22 = ["S","R1","R2","R3","R4","G1","G2","G3","G4","M1","M2","M3","M4","P","D1","D2","D3","D4","N1","N2","N3","N4","S^"]
C12_FREQ_RATIO = [1.0, 16.0/15.0, 9.0/8.0, 6.0/5.0, 5.0/4.0, 4.0/3.0, 45.0/32.0,3.0/2.0, 8.0/5.0, 27.0/16.0, 9.0/5.0, 15.0/8.0, 2.0]
C16_FREQ_RATIO = [1.0, 32.0/31.0, 16.0/15.0, 10.0/9.0, 32.0/27.0, 6.0/5.0, 5.0/4.0, 4.0/3.0, 27.0/20.0, 3.0/2.0, 128.0/81.0, 8.0/5.0, 5.0/3.0, 16.0/9.0, 9.0/5.0, 15.0/8.0, 2.0]
C22_FREQ_RATIO = [1.0, 32.0/31.0, 16.0/15.0, 10.0/9.0, 9.0/8.0, 32.0/27.0, 6.0/5.0, 5.0/4.0, 81.0/64.0, 4.0/3.0, 27.0/20.0, 45.0/32.0, 64.0/45.0, 3.0/2.0, 128.0/81.0, 8.0/5.0, 5.0/3.0, 27.0/16.0, 16.0/9.0, 9.0/5.0, 15.0/8.0, 31.0/16.0, 2.0]
C22_FREQ_RATIO_1 = [1.0, 256.0/243.0, 16.0/15.0, 10.0/9.0, 9.0/8.0, 32.0/27.0, 6.0/5.0, 5.0/4.0, 81.0/64.0, 4.0/3.0, 27.0/20.0, 35.0/32.0, 729.0/512.0, 3.0/2.0, 128.0/81.0, 8.0/5.0, 5.0/3.0, 27.0/16.0, 16.0/9.0, 9.0/5.0, 15.0/8.0, 243.0/129.0, 2.0 ]
BASE_OCTAVE = 5

RAAGA_NAMES = []
RAAGA_DICT = {}
RAAGA_INDEX = 115
MELAKARTHA_INDEX = 15
MELAKARTHA_LIST = []
KRITHI_NAMES = []
KRITHI_DICT = {}
KRITHI_INDEX = 0
""" THAALA SPECIFIC VARIABLES """
THAALA_INDEX = 4
JAATHI_INDEX = 2
NADAI_INDEX = 0
THAALA_PATTERNS = []
THAALA_PATTERN_COUNTS = []
THAALA_NAMES = ["","Eka ThaaLa","Roopaka ThaaLa", "Jampa ThaaLa", "Thriputai ThaaLa","Mathya ThaaLa", "ATa ThaaLa", "Dhurva ThaaLa"]
JAATHI_NAMES = ["","Thisra Jaathi", "Chathusra Jaathi", "Khanda Jaathi", "Misra Jaathi", "Sankeerna Jaathi"]
NADAI_NAMES = ["Nadai Off","ThisraNadai", "Chathusra Nadai", "Khanda Nadai", "Misra Nadai", "Sankeerna Nadai"]
jaathi_no = [1,3,4,5,7,9]
thaaLa_laghu_no = [0,1,1,1,1,2,2,3]
thaaLa_drutam_no = [0,0,1,1,2,1,2,1]
thaaLa_anudrutam_no = [0,0,0,1,0,0,0,0]
RHYTHM_NOTE_ARR = ["R", "C","C#","D","D#","E","F","F#","G","G#","A","A#","B","C","C#","D","E","F","E","F#","F","G","G","D#","C#",]
SOLKATTU_ARR = ["$", "tha", "dhi", "thom", "num", "ki", "ta", "ka", "na", "chap", "dhin", "ta*thom","num*thom", "chap*thom", "dhin*thom", "dhin*tha", "jo", "gu","gi","ri","mi","nu","na","nam","thi"]
SOLKATTU_NOTE_ARR = ["R", "C4","C#4","D4","D#4","E4","F4","F#4","G4","G#4","A4","A#4","B4","C5","C#5","D5","E4","F4","E4","F#4","F4","G4","G4","D#4","C#4",]
BEAT_LENGTH_SELECTION = [4,5,7,9]
THAALA_LOC = [ 
 [ {1:"||"},{1:"||"},{1:"||"},{1:"||"},{1:"||"},{1:"||"}],
 [ {1:"||"},{3:"||"},{4:"||"},{5:"||"},{7:"||"},{9:"||"}],
 [ {1:"||"},{2:"|",5:"||"}, {2:"|",6:"||"}, {2:"|",7:"||"}, {2:"|",9:"||"}, {2:"|",11:"||"} ],
 [ {1:"||"}, {3:"|",4:"|",6:"||"}, {4:"|",5:"|",7:"||"}, {5:"|",6:"|",8:"||"}, {7:"|",8:"|",10:"||"}, {9:"|",10:"|",12:"||"} ],
 [ {1:"||"}, {3:"|",5:"|",7:"||"}, {4:"|",6:"|",8:"||"}, {5:"|",7:"|",9:"||"}, {7:"|",9:"|",11:"||"}, {9:"|",11:"|",13:"||"} ],
 [ {1:"||"}, {3:"|",5:"|",8:"||"}, {4:"|",6:"|",10:"||"}, {5:"|",7:"|",12:"||"}, {7:"|",9:"|",16:"||"}, {9:"|",11:"|",20:"||"} ],
 [ {1:"||"}, {3:"|",6:"|",8:"|",10:"||"}, {4:"|",8:"|",10:"|",12:"||"}, {5:"|",10:"|",12:"|",14:"||"}, {7:"|",14:"|",16:"|",18:"||"}, {9:"|",18:"|",20:"|",22:"||"} ],
 [ {1:"||"}, {3:"|",5:"|",8:"|",11:"||"}, {4:"|",6:"|",10:"|",14:"||"}, {5:"|",7:"|",12:"|",17:"||"}, {7:"|",9:"|",16:"|",23:"||"}, {9:"|",11:"|",20:"|",29:"||"} ]
]
""" SONG COMMAND SETTINGS (Also included are:  MELAKARTHA_INDEX, THAALA_INDEX and JAATHI_INDEX) """
DURATION = 72
PLAY_SPEED = 1
INSTRUMENT_INDEX = 0
PLAYER_MODE = 1 # 1 for Carnatic Notes and 2 for Solkattu


def set_default_raaga_index(ri):
    RAAGA_INDEX = ri
def get_default_raaga_index():
    return RAAGA_INDEX
def get_global_settings():
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
    csv_data = open(RAAGA_LIST_FILE,'r')
    RAAGA_DICT.clear()
    with csv_data:
        reader = csv.reader(csv_data)
        headers = next(reader)
        RAAGA_NAMES.clear()
        for row in reader:
            RAAGA_NAMES.append(row[2])
            RAAGA_DICT[int(row[0])] = {key: value for key, value in zip(headers, row)}
    return RAAGA_DICT
def get_melakartha_dictionary():
    if RAAGA_DICT:
        MELAKARTHA_LIST.clear()
        for raaga_id in range(len(RAAGA_DICT)):
            if 'mELakartha-' in RAAGA_DICT[raaga_id]['Melakartha_or_Janya']:
                mk_no = int(RAAGA_DICT[raaga_id]['mELakartha'])
                MELAKARTHA_LIST.append(raaga_id)
        return MELAKARTHA_LIST
def get_krithi_dictionary():
    csv_data = open(KRITHI_LIST_FILE,'r')
    KRITHI_DICT.clear()
    with csv_data:
        reader = csv.reader(csv_data)
        headers = next(reader)
        KRITHI_NAMES.clear()
        for row in reader:
            KRITHI_NAMES.append(row[2])
            KRITHI_DICT[int(row[0])] = {key: value for key, value in zip(headers, row)}
    return KRITHI_DICT

get_global_settings()
RAAGA_DICT = get_raaga_dictionary()
KRITHI_DICT = get_krithi_dictionary()
MELAKARTHA_DICT = get_melakartha_dictionary()
#print(MELAKARTHA_DICT)