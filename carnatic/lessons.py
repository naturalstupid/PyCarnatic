"""
    Module for 
            - generating notations for music lessons for specified raaga and thaaLa
            - Lesson Names supported are: "SARALI_VARISAI", "JANTAI_VARISAI", "DHAATTU_VARISAI", "MELSTHAAYI_VARISAI", "KEEZHSTHAAYI_VARISAI"]
            - Alankaaram can be generated as in carnatic books for 35 thaaLa for tbhe specified raaga
            - Alankaaram can also be generated for specified raaga and thaaLa combination (this is different from that in books)
"""
import os, re
from carnatic import settings, raaga, thaaLa, cparser, cmarkov, cmarkovn, cdeeplearn
#from lessons import LESSON_TYPES
_LINE_BREAK_AT = thaaLa.total_akshara_count(settings.THAALA_INDEX, settings.JAATHI_INDEX, settings.NADAI_INDEX)
_DEFAULT_KALPANA_SWARA_LENGTH = _LINE_BREAK_AT * 10 # 10 Avarthanas
_TAC_LESSON_DICT = {3:12, 4:16, 5:18, 6:12, 7:14, 8:16, 9:18, 10:18, 12:12, 14:14, 16:16, 18:18, 20:18, }
""" LESSON SPECIFIC VARIABLES """
_SARALI_FILE_PREFIX = settings._APP_PATH + "/config/SaraLi/saraLivarisai_n"
_JANTAI_FILE_PREFIX = settings._APP_PATH + "/config/Jantai/jantaivarisai_n"
_DHAATTU_FILE_PREFIX = settings._APP_PATH + "/config/Dhaattu/dhaattuvarisai_n"
_MELSTHAAYI_FILE_PREFIX = settings._APP_PATH + "/config/mElsthaayi/mElsthaayivarisai_n"
_KEEZHSTHAYI_FILE_PREFIX = settings._APP_PATH + "/config/KeezhSthaayi/keezhsthaayivarisai_n"
_ALANKARAM_FILE_PREFIX = settings._APP_PATH + "/config/Alankaaram/alankaaram_"
LESSON_TYPES = {"SARALI_VARISAI":_SARALI_FILE_PREFIX, 
                "JANTAI_VARISAI":_JANTAI_FILE_PREFIX, 
                "DHAATTU_VARISAI":_DHAATTU_FILE_PREFIX, 
                "MELSTHAAYI_VARISAI":_MELSTHAAYI_FILE_PREFIX, 
                "KEEZHSTHAAYI_VARISAI":_KEEZHSTHAYI_FILE_PREFIX
               }#,"ALANKAARA_VARISAI_FROM_BOOK","ALANKAARA_VARISAI_FROM_ALGORITHM"}

def __sarali_varisai(arrange_notes_to_speed_and_thaaLa=True, raaga_index=settings.RAAGA_INDEX, 
                     thaaLa_index:settings.THAALA_NAMES=None, 
                     jaathi_index:settings.JAATHI_NAMES=None):
    if thaaLa_index == None:
        thaaLa_index = thaaLa.get_thaaLa_index()
    if jaathi_index == None:
        jaathi_index = thaaLa.get_jaathi_index()
    #thaaLa_index = int(thaaLa_index)
    #jaathi_index = int(jaathi_index)
    tac = thaaLa.total_akshara_count(thaaLa_index, jaathi_index, 1) # V1.0.3 Changed from 0 to 1
    f_tmp = _TAC_LESSON_DICT[tac]
    aroganam_length = len(settings.RAAGA_DICT[raaga_index]["Aroganam"].split())
    lesson_file = _SARALI_FILE_PREFIX + str(aroganam_length)+"_a"+str(f_tmp)+".inp"
    print('lesson_file',lesson_file)
    if os.path.isfile(lesson_file):
        _, result,_ = cparser.parse_notation_file(lesson_file, arrange_notes_to_speed_and_thaaLa)
    else:
        raise ValueError("Feature not implemented for supplied arguments (raaga_index,thaaLa_index,jaathi_index)",raaga_index,thaaLa_index,jaathi_index)
    return result
    
def __jantai_varisai(arrange_notes_to_speed_and_thaaLa=True, raaga_index=settings.RAAGA_INDEX, 
                     thaaLa_index:settings.THAALA_NAMES=None, 
                     jaathi_index:settings.JAATHI_NAMES=None):
    if thaaLa_index == None:
        thaaLa_index = thaaLa.get_thaaLa_index()
    if jaathi_index == None:
        jaathi_index = thaaLa.get_jaathi_index()
    #thaaLa_index = int(thaaLa_index)
    #jaathi_index = int(jaathi_index)
    tac = thaaLa.total_akshara_count(thaaLa_index, jaathi_index, 1)
    f_tmp = _TAC_LESSON_DICT[tac]
    aroganam_length = len(settings.RAAGA_DICT[raaga_index]["Aroganam"].split())
    lesson_file = _JANTAI_FILE_PREFIX + str(aroganam_length)+"_a"+str(f_tmp)+".inp"
    print('lesson_file',lesson_file)
    if os.path.isfile(lesson_file):
        _, result,_ = cparser.parse_notation_file(lesson_file, arrange_notes_to_speed_and_thaaLa)
    else:
        raise ValueError("Feature not implemented for supplied arguments (raaga_index,thaaLa_index,jaathi_index)",raaga_index,thaaLa_index,jaathi_index)
    return result
    
def __dhaattu_varisai(arrange_notes_to_speed_and_thaaLa=True, raaga_index=settings.RAAGA_INDEX, 
                     thaaLa_index:settings.THAALA_NAMES=None, 
                     jaathi_index:settings.JAATHI_NAMES=None):
    if thaaLa_index == None:
        thaaLa_index = thaaLa.get_thaaLa_index()
    if jaathi_index == None:
        jaathi_index = thaaLa.get_jaathi_index()
    #thaaLa_index = int(thaaLa_index)
    #jaathi_index = int(jaathi_index)
    tac = thaaLa.total_akshara_count(thaaLa_index, jaathi_index, 1)
    f_tmp = _TAC_LESSON_DICT[tac]
    aroganam_length = len(settings.RAAGA_DICT[raaga_index]["Aroganam"].split())
    lesson_file = _DHAATTU_FILE_PREFIX + str(aroganam_length)+"_a"+str(f_tmp)+".inp"
    print('lesson_file',lesson_file)
    if os.path.isfile(lesson_file):
        _, result,_ = cparser.parse_notation_file(lesson_file, arrange_notes_to_speed_and_thaaLa)
    else:
        raise ValueError("Feature not implemented for supplied arguments (raaga_index,thaaLa_index,jaathi_index)",raaga_index,thaaLa_index,jaathi_index)
    return result
    
def __melsthaayi_varisai(arrange_notes_to_speed_and_thaaLa=True, raaga_index=settings.RAAGA_INDEX, 
                     thaaLa_index:settings.THAALA_NAMES=None, 
                     jaathi_index:settings.JAATHI_NAMES=None):
    if thaaLa_index == None:
        thaaLa_index = thaaLa.get_thaaLa_index()
    if jaathi_index == None:
        jaathi_index = thaaLa.get_jaathi_index()
    #thaaLa_index = int(thaaLa_index)
    #jaathi_index = int(jaathi_index)
    tac = thaaLa.total_akshara_count(thaaLa_index, jaathi_index,1) #V1.0.3 0 changed to 1
    f_tmp = _TAC_LESSON_DICT[tac]
    aroganam_length = len(settings.RAAGA_DICT[raaga_index]["Aroganam"].split())
    lesson_file = _MELSTHAAYI_FILE_PREFIX + str(aroganam_length)+"_a"+str(f_tmp)+".inp"
    print('lesson_file',lesson_file)
    if os.path.isfile(lesson_file):
        _, result,_ = cparser.parse_notation_file(lesson_file, arrange_notes_to_speed_and_thaaLa)
    else:
        raise ValueError("Feature not implemented for supplied arguments (raaga_index,thaaLa_index,jaathi_index)",raaga_index,thaaLa_index,jaathi_index)
    return result
    
def __keezhsthaayi_varisai(arrange_notes_to_speed_and_thaaLa=True, raaga_index=settings.RAAGA_INDEX, 
                     thaaLa_index:settings.THAALA_NAMES=None, 
                     jaathi_index:settings.JAATHI_NAMES=None):
    if thaaLa_index == None:
        thaaLa_index = thaaLa.get_thaaLa_index()
    if jaathi_index == None:
        jaathi_index = thaaLa.get_jaathi_index()
    #thaaLa_index = int(thaaLa_index)
    #jaathi_index = int(jaathi_index)
    tac = thaaLa.total_akshara_count(thaaLa_index, jaathi_index, 1)
    f_tmp = _TAC_LESSON_DICT[tac]
    aroganam_length = len(settings.RAAGA_DICT[raaga_index]["Aroganam"].split())
    lesson_file = _KEEZHSTHAYI_FILE_PREFIX + str(aroganam_length)+"_a"+str(f_tmp)+".inp"
    print('lesson_file',lesson_file)
    if os.path.isfile(lesson_file):
        _, result,_ = cparser.parse_notation_file(lesson_file, arrange_notes_to_speed_and_thaaLa)
    else:
        raise ValueError("Feature not implemented for supplied arguments (raaga_index,thaaLa_index,jaathi_index)",raaga_index,thaaLa_index,jaathi_index)
    return result
    
def alankaara_varisai_from_book(arrange_notes_to_speed_and_thaaLa=True, raaga_name=None, save_to_file=None):
    """
        Generate alankaara varisai (from carnatic music lessons book) for the specified raaga
            @param    arrange_notes_to_speed_and_thaaLa    True the notations generated will be fit to speed and thaaLa
            @param    raaga_name    If not specified default raaga from settings will be used
            @param    save_to_file - File name (if specified) to save the results to.
            :return:   alankaara varisai for the selected raaga
    """
    """
        While generating lessons from config files - to avoid using current NADAI info
        reset it to single speed and revert to original nadai after generation
    """
    current_nadai = settings.NADAI_INDEX
    settings.NADAI_INDEX = 1
    if raaga_name==None:
        raaga_index=settings.RAAGA_INDEX
    else:
        raaga.set_raagam(raaga_name)
        raaga_index = settings.RAAGA_INDEX
    aroganam_length = len(settings.RAAGA_DICT[raaga_index]["Aroganam"].split())
    lesson_file = _ALANKARAM_FILE_PREFIX + str(aroganam_length) + ".inp"
    print('lesson_file',lesson_file)
    if os.path.isfile(lesson_file):
        _, result,_ = cparser.parse_notation_file(lesson_file, arrange_notes_to_speed_and_thaaLa)
        if save_to_file:
            file_object = open(save_to_file,"w")
            file_object.write(result)
            file_object.close()
    else:
        raise ValueError("Feature not implemented for supplied arguments (raaga_index)",raaga_index)
        settings.NADAI_INDEX = current_nadai
    settings.NADAI_INDEX = current_nadai
    return result
def alankaara_varisai_from_algorithm(arrange_notes_to_speed_and_thaaLa=True, raaga_name=None, 
                     thaaLa_index:settings.THAALA_NAMES=None, 
                     jaathi_index:settings.JAATHI_NAMES=None, 
                                     save_to_file=None):
    """
        Generate alankaara varisai (from computer generated algorithm) for the specified raaga
            @param    arrange_notes_to_speed_and_thaaLa    True the notations generated will be fit to speed and thaaLa
            @param    raaga_name    If not specified default raaga from settings will be used
            @param    thaaLa_name   If not specified default thaaLa from settings will be used
            @param    jaathi_name   If not specified default jaathi from settings will be used
                       Use raaga.get_raaga_list() to get the list of raaga names
                       Use thaaLa.get_thaaLam_names() to get the list of thaaLa names
                       Use thaaLa.get_jaathi_names() to get the list of jaathi names
            @param    save_to_file - File name (if specified) to save the results to.
            :return:   alankaara varisai for the selected raaga
    """
    """
        While generating lessons from config files - to avoid using current NADAI info
        reset it to single speed and revert to original nadai after generation
    """
    current_nadai = settings.NADAI_INDEX
    settings.NADAI_INDEX = 1
    if thaaLa_index == None:
        thaaLa_index = thaaLa.get_thaaLa_index()
    if jaathi_index == None:
        jaathi_index = thaaLa.get_jaathi_index()
    if raaga_name==None:
        raaga_index=settings.RAAGA_INDEX
    else:
        raaga.set_raagam(raaga_name)
        raaga_index = settings.RAAGA_INDEX
    thaaLa_index = int(thaaLa_index)
    jaathi_index = int(jaathi_index)
    aroganam_length = len(settings.RAAGA_DICT[raaga_index]["Aroganam"].split())
    f_tmp = str(aroganam_length)+"_"+str(thaaLa_index)+"_"+str(jaathi_index)
    lesson_file = _ALANKARAM_FILE_PREFIX + f_tmp + ".inp"
    print('lesson_file',lesson_file)
    if os.path.isfile(lesson_file):
        _, result,_ = cparser.parse_notation_file(lesson_file, arrange_notes_to_speed_and_thaaLa)
        if save_to_file:
            file_object = open(save_to_file,"w")
            file_object.write(result)
            file_object.close()
    else:
        raise ValueError("Feature not implemented for supplied arguments (raaga_index,thaaLa_index,jaathi_index)",raaga_index,thaaLa_index,jaathi_index)
        settings.NADAI_INDEX = current_nadai
    settings.NADAI_INDEX = current_nadai
    return result

def generate_lessons(lesson_type,arrange_notes_to_speed_and_thaaLa=True, raaga_name=None, 
                     thaaLa_index:settings.THAALA_NAMES=None, 
                     jaathi_index:settings.JAATHI_NAMES=None, 
                     save_to_file=None):
    """
            - generating notations for music lessons for specified raaga and thaaLa
            - Lesson Names supported are: "SARALI_VARISAI", "JANTAI_VARISAI", "DHAATTU_VARISAI", "MELSTHAAYI_VARISAI", "KEEZHSTHAAYI_VARISAI"]
            @param    lesson_type    case not sensitive
            @param    arrange_notes_to_speed_and_thaaLa    True the notations generated will be fit to speed and thaaLa
            @param    raaga_name    If not specified default raaga from settings will be used
            @param    thaaLa_name   If not specified default thaaLa from settings will be used
            @param    jaathi_name   If not specified default jaathi from settings will be used
                       Use raaga.get_raaga_list() to get the list of raaga names
                       Use thaaLa.get_thaaLam_names() to get the list of thaaLa names
                       Use thaaLa.get_jaathi_names() to get the list of jaathi names
            @param    save_to_file - File name (if specified) to save the results to.
            :return:    notations for the selected lesson
    """
    """
        While generating lessons from config files - to avoid using current NADAI info
        reset it to single speed and revert to original nadai after generation
    """
    current_nadai = settings.NADAI_INDEX
    settings.NADAI_INDEX = 1
    if raaga_name==None:
        raaga_index=settings.RAAGA_INDEX
    else:
        raaga.set_raagam(raaga_name)
        raaga_index = settings.RAAGA_INDEX
    if thaaLa_index == None:
        thaaLa_index = thaaLa.get_thaaLa_index()
    if jaathi_index == None:
        jaathi_index = thaaLa.get_jaathi_index()
    thaaLa.set_thaaLam(thaaLa_index, jaathi_index)
    #thaaLa_index=int(settings.THAALA_INDEX)
    #jaathi_index = int(settings.JAATHI_INDEX)
    if lesson_type.upper() in LESSON_TYPES.keys():
        print("Nadai set to",settings.NADAI_INDEX)
        results = eval("__"+lesson_type.lower())(arrange_notes_to_speed_and_thaaLa, raaga_index, thaaLa_index, jaathi_index)
        if save_to_file:
            file_object = open(save_to_file,"w")
            file_object.write(results)
            file_object.close()
    else:
        settings.NADAI_INDEX = current_nadai
        raise ValueError("lesson_type should be one of:",LESSON_TYPES.keys(), " not case sensitive")
    settings.NADAI_INDEX = current_nadai
    return results
def _write_notes_to_file(kalpana_swarams,save_to_file,jraaga_notation=False,raaga_name=None,
                     thaaLa_index:settings.THAALA_NAMES=None, 
                     jaathi_index:settings.JAATHI_NAMES=None,
                     nadai_index:settings.NADAI_NAMES=None,
                     song_speed=None,arrange_notes_to_thaaLa=True, line_break_at=_LINE_BREAK_AT):
    #print('_write_notes_to_file',settings.THAALA_INDEX,settings.JAATHI_INDEX,settings.NADAI_INDEX)
    if thaaLa_index == None:
        thaaLa_index = thaaLa.get_thaaLa_index()
    if jaathi_index == None:
        jaathi_index = thaaLa.get_jaathi_index()
    if nadai_index == None:
        nadai_index = thaaLa.get_nadai_index()
    #thaaLa_index = int(thaaLa_index)
    #jaathi_index = int(jaathi_index)
    if not jraaga_notation:
        kalpana_swarams = [c.upper()+"^"  if c.isupper() else c.upper() for c in kalpana_swarams ]
    if arrange_notes_to_thaaLa:
        thaaLa.set_thaaLam_index(thaaLa_index, jaathi_index,settings.NADAI_INDEX) 
        kalpana_swarams = cparser._arrange_notes_to_thaaLa(kalpana_swarams,play_speed=song_speed)
    else:
        kalpana_swarams = '\n'.join(' '.join(kalpana_swarams[i:i+line_break_at]) for i in range(0, len(kalpana_swarams), (line_break_at)))
    ks = ''
    if jraaga_notation:
        ks += "{Ragam: "+raaga_name+ "\n"
        ks += "#D"+str(settings.TEMPO)+"\n"
        ks += "#S"+str(song_speed)+"\n"
        ks += "#T"+str(int(thaaLa_index))+"\n"
        ks += "#J"+str(int(jaathi_index))+"\n"
        ks += "#I"+str(settings.INSTRUMENT_INDEX)
    ks += ''.join(kalpana_swarams)
    if save_to_file:
        file_object = open(save_to_file,"w")
        file_object.write(ks)
        #file_object.write(kalpana_swarams)
        file_object.close()
    return ks
def _is_valid_note(note, start_or_end, raaga_index, jraaga_notation,width=1):
    aaroganam_orig = (raaga.get_aaroganam(raaga_index))
    aaroganam = aaroganam_orig
    avaroganam_orig = (raaga.get_avaroganam(raaga_index))
    avaroganam = avaroganam_orig
    if jraaga_notation==False:
        aaroganam = re.sub("\d+","",' '.join(aaroganam_orig))
        avaroganam = re.sub("\d+","",' '.join(avaroganam_orig))
        aaroganam = list(map(str.lower, aaroganam))
        avaroganam = list(map(str.lower, avaroganam))
        
    is_valid = note != None and set(note.split()).issubset(aaroganam+avaroganam) #V0.7.7 !=None added
    msg = "' does not meet criteria:\n 1. Notes should be in aaroganam ("+''.join(aaroganam)+") or avaroganam ("+''.join(avaroganam)+").\n \
    2. Number of notes should match the width argument value.\n"
    if note==None or len(note.split()) != width or not is_valid:
        if start_or_end == "start":
            print("Supplied starting note: '"+str(note)+msg+"Starting note changed to:",aaroganam_orig[0:width])
            note = ' '.join(aaroganam[0:width])
        else:
            """ TODO: Should ending note be forced to one note above/below of starting note """
            print("Supplied ending note: '"+str(note)+msg+"Ending note changed to:",aaroganam_orig[-width:])
            note = ' '.join(aaroganam[-width:])
    return note
            
def _generate_kalpana_swarams(method="markov", corpus_files=None, raaga_name=None, 
                    thaaLa_index:settings.THAALA_NAMES=None, 
                    jaathi_index:settings.JAATHI_NAMES=None, 
                    nadai_index:settings.NADAI_NAMES=None, 
                    song_speed=3, save_to_file=None,
                    starting_note=None,ending_note=None,length=_DEFAULT_KALPANA_SWARA_LENGTH,line_break_at=_LINE_BREAK_AT,
                    arrange_notes_to_thaaLa=True,jraaga_notation=True,
                    lesson_types_for_kalpana_swaram = ["JANTAI_VARISAI", "DHAATTU_VARISAI", "MELSTHAAYI_VARISAI", 
                                      "KEEZHSTHAAYI_VARISAI","ALANKAARA_VARISAI_FROM_BOOK"],
                                          perform_training=False, width=1
                                          ):
    """
            - generating kalpana swaram either from the corpus notation files
                Or from music lessons for specified raaga and thaaLa.
            @param method: method="deeplearn" will use deep learning to learn the notation - slower method
                           method="markov" will use markov chain random walk - default
            @param corpus_files: List of notation file names to be used for learning 
                If you specify corpus files you need not specify thaaLa and song speed arguments
                Instead of corpus files you can generate from music lessons in which case you should specify
                raaga, thaaLam, jaathi and song speed arguments 
            @param    raaga_name    If not specified default raaga from settings will be used
            @param    thaaLa_name   If not specified default thaaLa from settings will be used
            @param    jaathi_name   If not specified default jaathi from settings will be used
                       Use raaga.get_raaga_list() to get the list of raaga names
                       Use thaaLa.get_thaaLam_names() to get the list of thaaLa names
                       Use thaaLa.get_jaathi_names() to get the list of jaathi names
            @param    song_speed    Song Speed 1 .. 3 - default = 3
            @param    save_to_file - File name (if specified) to save the results to.
            @param    starting_note    Starting note - default = "S". 
                      If you specify raaga_name the default will be first note of arogana
            @param    ending_note    ending note - default = None
                      If you specify raaga_name the default will be last note of arogana
                      If specified ending notes are not in corpus they are randomly chosen from corpus
            @param    length    number of notes to be generated - default = _DEFAULT_KALPANA_SWARA_LENGTH=Total Akashara Count
                      Preferably be multiple of thaLa count (avarthana)
            @param    line_break_at    insert line break at - default at thaaLa end
                      this is needed only for generating using corpus text files and
                      this argument makes sense on if arrange_notes_to_thaaLa is set to False 
            @param    arrange_notes_to_thaaLa True/False - Default = True
            @param    jraaga_notation  True/False - default True
            @param    lesson_types_for_kalpana_swaram list of lesson types that should be used to generate kalpana swarams
                      Default: ["JANTAI_VARISAI", "DHAATTU_VARISAI", "MELSTHAAYI_VARISAI", 
                                "KEEZHSTHAAYI_VARISAI","ALANKAARA_VARISAI_FROM_BOOK"]
            @param perform_training: True/False. Force perfoming training even if model weights are found. 
                    Default = False. Applicable only for method="deeplearn"
            @param width: Number of adjacent notes to be used for prediction. Only applicable for markov model
            :return:    kalpana swaram for the specified raaga/thaaLa
    """
    if thaaLa_index == None:
        thaaLa_index = thaaLa.get_thaaLa_index()
    if jaathi_index == None:
        jaathi_index = thaaLa.get_jaathi_index()
    if nadai_index == None:
        nadai_index = thaaLa.get_nadai_index()
    #thaaLa_index = int(thaaLa_index)
    #jaathi_index = int(jaathi_index)
    #print('lessons _generate_kalpana_swarams tempo',settings.TEMPO)
    if (method.lower() != "markov" and method.lower() != "deeplearn") :
        method = "markov"
    if method != "deeplearn" and width > 4:
        width = 4
    if raaga_name==None:
        raaga_index=settings.RAAGA_INDEX
    else:
        raaga.set_raagam(raaga_name)
        raaga_index = settings.RAAGA_INDEX
    thaaLa.set_thaaLam(thaaLa_index, jaathi_index)
    tac = thaaLa.total_akshara_count(thaaLa_index, jaathi_index, 1)
    if arrange_notes_to_thaaLa:
        line_break_at = tac*(2**(song_speed-1))
    #print('thaaLa_index, jaathi_index',thaaLa_index, jaathi_index)
    aaroganam = (raaga.get_aaroganam(raaga_index))
    avaroganam = (raaga.get_avaroganam(raaga_index))
    if jraaga_notation==False:
        aaroganam = list(map(str.lower, aaroganam))
        avaroganam = list(map(str.lower, avaroganam))
        #print(aaroganam,avaroganam)
    """
    is_note_in_aaroganam_avaroganam = lambda note: set(note.split()).issubset(aaroganam+avaroganam)
    msg = "' does not meet criteria:\n 1. Notes should be in aaroganam ("+''.join(aaroganam)+") or avaroganam ("+''.join(avaroganam)+").\n \
    2. Number of notes should match the width argument value.\n"
    if starting_note==None or len(starting_note.split()) != width or not is_note_in_aaroganam_avaroganam(starting_note):
        print("Supplied starting note: '"+str(starting_note)+msg+"Starting note changed to:",aaroganam[0:width])
        starting_note = ' '.join(aaroganam[0:width])
    if ending_note==None or len(ending_note.split()) != width or not is_note_in_aaroganam_avaroganam(ending_note):
        print("Supplied ending note: '"+str(ending_note)+msg+"Ending note changed to:",aaroganam[-width:])
        ending_note = ' '.join(aaroganam[-width:])
    """
    starting_note = _is_valid_note(starting_note,"start",raaga_index, jraaga_notation,width)
    ending_note = _is_valid_note(ending_note,"end",raaga_index, jraaga_notation,width)
    print('starting_note',starting_note,'ending_note',ending_note)
    kalpana_swarams = []
    if corpus_files:
        if method.lower()=="deeplearn":
            kalpana_swarams = cdeeplearn.generate_notes_from_corpus(corpus_files=corpus_files,
                                        starting_note=starting_note,ending_note=ending_note,length=length, 
                                        save_to_file=save_to_file,perform_training=perform_training)
        else:
            if width==None or width==1:
                kalpana_swarams = cmarkov.generate_notes_from_corpus(corpus_files=corpus_files,starting_note=starting_note,
                                    ending_note=ending_note,length=length, save_to_file=save_to_file)
            else:
                print("Calling markovn corpus")
                kalpana_swarams = cmarkovn.generate_notes_from_corpus(corpus_files=corpus_files,starting_note=starting_note,
                                    ending_note=ending_note,length=length, save_to_file=save_to_file,width=width)
            kalpana_swarams = ' '.join(kalpana_swarams).split()
        if kalpana_swarams or save_to_file:
            #print('lessons _generate_kalpana_swarams tempo',settings.TEMPO)
            kalpana_swarams = _write_notes_to_file(kalpana_swarams,save_to_file,jraaga_notation=jraaga_notation,
                                     raaga_name=raaga_name,thaaLa_index=thaaLa_index,jaathi_index=jaathi_index,nadai_index=nadai_index,
                                     arrange_notes_to_thaaLa=arrange_notes_to_thaaLa, song_speed=song_speed,
                                     line_break_at=line_break_at)
        return kalpana_swarams
    
    f_tmp = _TAC_LESSON_DICT[tac]
    aroganam_length = len(settings.RAAGA_DICT[raaga_index]["Aroganam"].split())
    notation_files = []
    """ Check if lesson files are found """
    for lesson_type in lesson_types_for_kalpana_swaram[:-1]:
        lesson_file = LESSON_TYPES[lesson_type] + str(aroganam_length)+"_a"+str(f_tmp)+".inp"
        if not (os.path.isfile(lesson_file)):
            #raise ValueError("Kalpana Swaram cannot be generated since lesson file",lesson_file,'is not available')
            print("Kalpana Swaram cannot be generated since lesson file",lesson_file,'is not available')
        else:
            """ Generate lesson and save to tmp folder """
            temp_file = settings._APP_PATH + "/tmp/"+raaga_name+"_"+lesson_type+".txt"
            _ = generate_lessons(lesson_type, True, raaga_name, thaaLa_index, jaathi_index, temp_file)
            notation_files.append(temp_file)
    lesson_file = _ALANKARAM_FILE_PREFIX + str(aroganam_length) + ".inp" 
    if not (os.path.isfile(lesson_file)):
        #raise ValueError("Kalpana Swaram cannot be generated since lesson file",lesson_file,'is not available')
        print("Kalpana Swaram cannot be generated since lesson file",lesson_file,'is not available')
    else:
        """ Generate lesson and save to tmp folder """
        temp_file = settings._APP_PATH + "/tmp/"+raaga_name+"_Alankaaram.txt"
        _ = alankaara_varisai_from_book(True, raaga_name, temp_file)
        notation_files.append(temp_file)
    if notation_files:
        if method.lower()=="deeplearn":
            cdeeplearn.set_parameters(json_file=raaga_name+"_lessons.json", model_weights_file=raaga_name+"_lessons.h5")
            kalpana_swarams = cdeeplearn.generate_notes_from_corpus(corpus_files=notation_files,starting_note=starting_note,
                                        ending_note=ending_note,length=length, save_to_file=save_to_file,
                                        perform_training=perform_training)
        else:
            if width==None or width==1:
                kalpana_swarams = cmarkov.generate_notes_from_corpus(corpus_files=notation_files,starting_note=starting_note,
                                        ending_note=ending_note,length=_DEFAULT_KALPANA_SWARA_LENGTH)
            else:
                kalpana_swarams = cmarkovn.generate_notes_from_corpus(corpus_files=notation_files,starting_note=starting_note,
                                        ending_note=ending_note,length=_DEFAULT_KALPANA_SWARA_LENGTH,width=width)
            #print('raagam',raaga_name,'kalpana_swarams\n',kalpana_swarams)
            kalpana_swarams = ' '.join(kalpana_swarams).split()
    for temp_file in notation_files:
        os.remove(temp_file)
    if kalpana_swarams or save_to_file:
        #print('lessons _generate_kalpana_swarams tempo',settings.TEMPO)
        kalpana_swarams = _write_notes_to_file(kalpana_swarams,save_to_file,jraaga_notation=jraaga_notation,
                                 raaga_name=raaga_name,thaaLa_index=thaaLa_index,jaathi_index=jaathi_index,nadai_index=nadai_index,song_speed=song_speed)

    return kalpana_swarams
def _get_available_lesson_types_for_the_raaga(raaga_index):
    lesson_types = []
    thaaLa_index=settings.THAALA_INDEX
    jaathi_index = settings.JAATHI_INDEX
    tac = thaaLa.total_akshara_count(thaaLa_index, jaathi_index, 1)
    f_tmp = _TAC_LESSON_DICT[tac]
    raaga_name = raaga.get_raaga_name(raaga_index)
    aroganam_length = len(settings.RAAGA_DICT[raaga_index]["Aroganam"].split())
    """ Check if lesson files are found """
    for lesson_type in LESSON_TYPES.keys():
        lesson_file = LESSON_TYPES[lesson_type] + str(aroganam_length)+"_a"+str(f_tmp)+".inp"
        if not (os.path.isfile(lesson_file)):
            print("Lesson file",lesson_file,'is not available for raaga:',raaga_name)
        else:
            lesson_types.append(lesson_type)
    return lesson_types
def generate_kalpana_swarams(method="markov", corpus_files=None, raaga_name=None, 
                thaaLa_index:settings.THAALA_NAMES=None, 
                jaathi_index:settings.JAATHI_NAMES=None, 
                nadai_index:settings.NADAI_NAMES=None, 
                song_speed=3, save_to_file=None, \
                starting_note=None,ending_note=None,avarthanam_count=None,line_break_at=None,
                arrange_notes_to_thaaLa=True,jraaga_notation=True,
                lesson_types_for_kalpana_swaram = list(LESSON_TYPES.keys()) + ["ALANKAARA_VARISAI_FROM_BOOK"],
                perform_training=False, width=1):
    """
            - generating kalpana swaram either from the corpus notation files
                Or from music lessons for specified raaga and thaaLa.
            @param method: method="deeplearn" will use deep learning to learn the notation - slower method
                           method="markov" will use markov chain random walk - default
            @param corpus_files: List of notation file names to be used for learning 
                If you specify corpus files you need not specify thaaLa and song speed arguments
                Instead of corpus files you can generate from music lessons in which case you should specify
                raaga, thaaLam, jaathi and song speed arguments 
            @param    raaga_name    If not specified default raaga from settings will be used
            @param    thaaLa_name   If not specified default thaaLa from settings will be used
            @param    jaathi_name   If not specified default jaathi from settings will be used
                       Use raaga.get_raaga_list() to get the list of raaga names
                       Use thaaLa.get_thaaLam_names() to get the list of thaaLa names
                       Use thaaLa.get_jaathi_names() to get the list of jaathi names
            @param    song_speed    Song Speed 1 .. 3 - default = 3
            @param    save_to_file - File name (if specified) to save the results to.
            @param    starting_note    Starting note - default = "S". 
                      If you specify raaga_name the default will be first note of arogana
            @param    ending_note    ending note - default = None
                      If you specify raaga_name the default will be last note of arogana
                      If specified ending notes are not in corpus they are randomly chosen from corpus
            @param    avarthanam_count    number of avarthanam to be generated - default = 10
                      Preferably be multiple of thaLa count (avarthana)
            @param    line_break_at    insert line break at - default at thaaLa end
                      this is needed only for generating using corpus text files and
                      this argument makes sense on if arrange_notes_to_thaaLa is set to False 
            @param    arrange_notes_to_thaaLa True/False - Default = True
            @param    jraaga_notation  True/False - default True
            @param    lesson_types_for_kalpana_swaram list of lesson types that should be used to generate kalpana swarams
                      Default: ["JANTAI_VARISAI", "DHAATTU_VARISAI", "MELSTHAAYI_VARISAI", 
                                "KEEZHSTHAAYI_VARISAI","ALANKAARA_VARISAI_FROM_BOOK"]
            @param perform_training: True/False. Force perfoming training even if model weights are found. 
                    Default = False. Applicable only for method="deeplearn"
            @param width: Number of adjacent notes to be used for prediction. Only applicable for markov model
            :return:    kalpana swaram for the specified raaga/thaaLa
    """
    if thaaLa_index == None:
        thaaLa_index = thaaLa.get_thaaLa_index()
    if jaathi_index == None:
        jaathi_index = thaaLa.get_jaathi_index()
    if nadai_index == None:
        nadai_index = thaaLa.get_nadai_index()
    if (method.lower() != "markov" and method.lower() != "deeplearn") :
        method = "markov"
    if method.lower() != "deeplearn" and width > 4:
        width = 4
    if raaga_name==None:
        raaga_index=settings.RAAGA_INDEX
    else:
        raaga.set_raagam(raaga_name)
        raaga_index = settings.RAAGA_INDEX
    #print(settings.THAALA_INDEX,settings.JAATHI_INDEX,settings.NADAI_INDEX)
    thaaLa.set_thaaLam(thaaLa_index, jaathi_index,nadai_index)
    #print(settings.THAALA_INDEX,settings.JAATHI_INDEX,settings.NADAI_INDEX)
    tac = thaaLa.total_akshara_count(thaaLa_index,jaathi_index,nadai_index)
    length = tac * 10
    if avarthanam_count != None:
        length = tac * avarthanam_count
    elif length%tac !=0:
        print('length',length,'is not a multiple of akshara count',tac)
    if line_break_at == None:
        line_break_at = tac
    elif line_break_at%tac !=0:
        print('line_break_at',line_break_at,'is not a multiple of akshara count',tac)
    #tac = thaaLa.total_akshara_count(thaaLa_index, jaathi_index, 1)
    #if arrange_notes_to_thaaLa:
    #    line_break_at = tac*(2**(song_speed-1))
    #print('thaaLa_index, jaathi_index',thaaLa_index, jaathi_index)
    aaroganam = (raaga.get_aaroganam(raaga_index))
    avaroganam = (raaga.get_avaroganam(raaga_index))
    if jraaga_notation==False:
        aaroganam = list(map(str.lower, aaroganam))
        avaroganam = list(map(str.lower, avaroganam))
        #print(aaroganam,avaroganam)
    """
    is_note_in_aaroganam_avaroganam = lambda note: set(note.split()).issubset(aaroganam+avaroganam)
    msg = "' does not meet criteria:\n 1. Notes should be in aaroganam ("+''.join(aaroganam)+") or avaroganam ("+''.join(avaroganam)+").\n \
    2. Number of notes should match the width argument value.\n"
    if starting_note==None or len(starting_note.split()) != width or not is_note_in_aaroganam_avaroganam(starting_note):
        print("Supplied starting note: '"+str(starting_note)+msg+"Starting note changed to:",aaroganam[0:width])
        starting_note = ' '.join(aaroganam[0:width])
    if ending_note==None or len(ending_note.split()) != width or not is_note_in_aaroganam_avaroganam(ending_note):
        print("Supplied ending note: '"+str(ending_note)+msg+"Ending note changed to:",aaroganam[-width:])
        ending_note = ' '.join(aaroganam[-width:])
    """
    #print('Lessons KS tempo',settings.TEMPO)
    starting_note = _is_valid_note(starting_note,"start",raaga_index, jraaga_notation,width)
    ending_note = _is_valid_note(ending_note,"end",raaga_index, jraaga_notation,width)
    print('starting_note',starting_note,'ending_note',ending_note)
    kalpana_swarams = []
    if corpus_files:
        if method.lower()=="deeplearn":
            kalpana_swarams = cdeeplearn.generate_notes_from_corpus(corpus_files=corpus_files,
                                        starting_note=starting_note,ending_note=ending_note,length=length, 
                                        save_to_file=save_to_file,perform_training=perform_training)
        else:
            if width==None or width==1:
                kalpana_swarams = cmarkov.generate_notes_from_corpus(corpus_files=corpus_files,starting_note=starting_note,
                                    ending_note=ending_note,length=length, save_to_file=save_to_file)
            else:
                print("Calling markovn corpus")
                kalpana_swarams = cmarkovn.generate_notes_from_corpus(corpus_files=corpus_files,starting_note=starting_note,
                                    ending_note=ending_note,length=length, save_to_file=save_to_file,width=width)
            kalpana_swarams = ' '.join(kalpana_swarams).split()
        if kalpana_swarams or save_to_file:
            kalpana_swarams = _write_notes_to_file(kalpana_swarams,save_to_file,jraaga_notation=jraaga_notation,
                                     raaga_name=raaga_name,thaaLa_index=thaaLa_index,jaathi_index=jaathi_index,nadai_index=nadai_index,
                                     arrange_notes_to_thaaLa=arrange_notes_to_thaaLa, song_speed=song_speed,
                                     line_break_at=line_break_at)
        print('Corpus generate_kalpana_swarams song speed',song_speed)
        return kalpana_swarams
    available_lesson_types = _get_available_lesson_types_for_the_raaga(raaga_index)
    print('available lesson types',available_lesson_types,'for raaga',raaga_name)
    notation_files = []
    for lesson_type in available_lesson_types:
        """ Generate lesson and save to tmp folder """
        temp_file = settings._TEMP_PATH+raaga_name+"_"+lesson_type+".txt"
        notation_files.append(temp_file)
        _ = generate_lessons(lesson_type, True, raaga_name, thaaLa_index, jaathi_index, temp_file)
    aroganam_length = len(settings.RAAGA_DICT[raaga_index]["Aroganam"].split())
    lesson_file = _ALANKARAM_FILE_PREFIX + str(aroganam_length) + ".inp" 
    #print('1. generate_kalpana_swarams tempo',settings.TEMPO)
    if not (os.path.isfile(lesson_file)):
        print("Kalpana Swaram cannot be generated since lesson file",lesson_file,'is not available')
    else:
        """ Generate lesson and save to tmp folder """
        temp_file = settings._APP_PATH + "/tmp/"+raaga_name+"_Alankaaram.txt"
        #print('1.1 generate_kalpana_swarams tempo',settings.TEMPO)
        """ TODO: This call will change the tempo based on config lesson file #D value """
        old_tempo = settings.TEMPO
        _ = alankaara_varisai_from_book(True, raaga_name, temp_file)
        """ RESET TEMPO """
        settings.TEMPO = old_tempo
        #print('1.2 generate_kalpana_swarams tempo',settings.TEMPO)
        notation_files.append(temp_file)
    if notation_files:
        if method.lower()=="deeplearn":
            cdeeplearn.set_parameters(json_file=raaga_name+"_lessons.json", model_weights_file=raaga_name+"_lessons.h5")
            kalpana_swarams = cdeeplearn.generate_notes_from_corpus(corpus_files=notation_files,starting_note=starting_note,
                                        ending_note=ending_note,length=length, save_to_file=save_to_file,
                                        perform_training=perform_training)
        else:
            if width==None or width==1:
                kalpana_swarams = cmarkov.generate_notes_from_corpus(corpus_files=notation_files,starting_note=starting_note,
                                        ending_note=ending_note,length=length)
            else:
                kalpana_swarams = cmarkovn.generate_notes_from_corpus(corpus_files=notation_files,starting_note=starting_note,
                                        ending_note=ending_note,length=length,width=width)
            #print('raagam kalpana_swarams\n',kalpana_swarams)
            kalpana_swarams = ' '.join(kalpana_swarams).split()
    for temp_file in notation_files:
        os.remove(temp_file)
    if kalpana_swarams or save_to_file:
        kalpana_swarams = _write_notes_to_file(kalpana_swarams,save_to_file,jraaga_notation=jraaga_notation,
                                 raaga_name=raaga_name,thaaLa_index=thaaLa_index,jaathi_index=jaathi_index,nadai_index=nadai_index,song_speed=song_speed)

    print('Lessons generate_kalpana_swarams song speed',song_speed)
    return kalpana_swarams
if __name__ == '__main__':
    """
    #result = alankaara_varisai_from_book(arrange_notes_to_speed_and_thaaLa=True)
    result = generate_lessons("sarali_varisai",arrange_notes_to_speed_and_thaaLa=True)#,thaaLa_index=2,jaathi_index=2)
    print(result)
    pass
    """