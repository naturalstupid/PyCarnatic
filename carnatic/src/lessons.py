"""
    Module for 
            - generating notations for music lessons for specified raaga and thaaLa
            - Lesson Names supported are: "SARALI_VARISAI", "JANTAI_VARISAI", "DHAATTU_VARISAI", "MELSTHAAYI_VARISAI", "KEEZHSTHAAYI_VARISAI"]
            - Alankaaram can be generated as in carnatic books for 35 thaaLa for tbhe specified raaga
            - Alankaaram can also be generated for specified raaga and thaaLa combination (this is different from that in books)
"""
import os
import settings
import cparser
import thaaLa

_TAC_LESSON_DICT = {3:12, 4:16, 5:18, 6:12, 7:14, 8:16, 9:18, 10:18, 12:12, 14:14, 16:16, 18:18, 20:18, }
""" LESSON SPECIFIC VARIABLES """
_SARALI_FILE_PREFIX = "../config/SaraLi/saraLivarisai_n"
_JANTAI_FILE_PREFIX = "../config/Jantai/jantaivarisai_n"
_DHAATTU_FILE_PREFIX = "../config/Dhaattu/dhaattuvarisai_n"
_MELSTHAAYI_FILE_PREFIX = "../config/mElsthaayi/mElsthaayivarisai_n"
_KEEZHSTHAYI_FILE_PREFIX = "../config/KeezhSthaayi/keezhsthaayivarisai_n"
_ALANKARAM_FILE_PREFIX = "../config/Alankaaram/alankaaram_"
LESSON_TYPES = ["SARALI_VARISAI", "JANTAI_VARISAI", "DHAATTU_VARISAI", "MELSTHAAYI_VARISAI", "KEEZHSTHAAYI_VARISAI"]#,"ALANKAARA_VARISAI_FROM_BOOK","ALANKAARA_VARISAI_FROM_ALGORITHM"]

def __sarali_varisai(fit_notes_to_speed_and_thaaLa=False, raaga_index=None, thaaLa_index=None, jaathi_index=None):
    if raaga_index==None:
        raaga_index=settings.RAAGA_INDEX
    else:
        settings.RAAGA_INDEX = raaga_index
    if thaaLa_index==None:
        thaaLa_index=settings.THAALA_INDEX
    else:
        settings.THAALA_INDEX = thaaLa_index
    if jaathi_index==None:
        jaathi_index = settings.JAATHI_INDEX
    else:
        settings.JAATHI_INDEX = jaathi_index
    tac = thaaLa.total_akshara_count(thaaLa_index, jaathi_index, 0)
    f_tmp = _TAC_LESSON_DICT[tac]
    aroganam_length = len(settings.RAAGA_DICT[raaga_index]["Aroganam"].split())
    lesson_file = _SARALI_FILE_PREFIX + str(aroganam_length)+"_a"+str(f_tmp)+".inp"
    if os.path.exists(lesson_file):
        result = cparser.parse_file(lesson_file, fit_notes_to_speed_and_thaaLa)
    else:
        raise ValueError("Feature not implemented for supplied arguments (raaga_index,thaaLa_index,jaathi_index)",raaga_index,thaaLa_index,jaathi_index)
    return result
    
def __jantai_varisai(fit_notes_to_speed_and_thaaLa=False, raaga_index=None, thaaLa_index=None, jaathi_index=None):
    if raaga_index==None:
        raaga_index=settings.RAAGA_INDEX
    else:
        settings.RAAGA_INDEX = raaga_index
    if thaaLa_index==None:
        thaaLa_index=settings.THAALA_INDEX
    else:
        settings.THAALA_INDEX = thaaLa_index
    if jaathi_index==None:
        jaathi_index = settings.JAATHI_INDEX
    else:
        settings.JAATHI_INDEX = jaathi_index
    tac = thaaLa.total_akshara_count(thaaLa_index, jaathi_index, 0)
    f_tmp = _TAC_LESSON_DICT[tac]
    aroganam_length = len(settings.RAAGA_DICT[raaga_index]["Aroganam"].split())
    lesson_file = _JANTAI_FILE_PREFIX + str(aroganam_length)+"_a"+str(f_tmp)+".inp"
    if os.path.exists(lesson_file):
        result = cparser.parse_file(lesson_file, fit_notes_to_speed_and_thaaLa)
    else:
        raise ValueError("Feature not implemented for supplied arguments (raaga_index,thaaLa_index,jaathi_index)",raaga_index,thaaLa_index,jaathi_index)
    return result
    
def __dhaattu_varisai(fit_notes_to_speed_and_thaaLa=False, raaga_index=None, thaaLa_index=None, jaathi_index=None):
    if raaga_index==None:
        raaga_index=settings.RAAGA_INDEX
    else:
        settings.RAAGA_INDEX = raaga_index
    if thaaLa_index==None:
        thaaLa_index=settings.THAALA_INDEX
    else:
        settings.THAALA_INDEX = thaaLa_index
    if jaathi_index==None:
        jaathi_index = settings.JAATHI_INDEX
    else:
        settings.JAATHI_INDEX = jaathi_index
    tac = thaaLa.total_akshara_count(thaaLa_index, jaathi_index, 0)
    f_tmp = _TAC_LESSON_DICT[tac]
    aroganam_length = len(settings.RAAGA_DICT[raaga_index]["Aroganam"].split())
    lesson_file = _DHAATTU_FILE_PREFIX + str(aroganam_length)+"_a"+str(f_tmp)+".inp"
    if os.path.exists(lesson_file):
        result = cparser.parse_file(lesson_file, fit_notes_to_speed_and_thaaLa)
    else:
        raise ValueError("Feature not implemented for supplied arguments (raaga_index,thaaLa_index,jaathi_index)",raaga_index,thaaLa_index,jaathi_index)
    return result
    
def __melsthaayi_varisai(fit_notes_to_speed_and_thaaLa=False, raaga_index=None, thaaLa_index=None, jaathi_index=None):
    if raaga_index==None:
        raaga_index=settings.RAAGA_INDEX
    else:
        settings.RAAGA_INDEX = raaga_index
    if thaaLa_index==None:
        thaaLa_index=settings.THAALA_INDEX
    else:
        settings.THAALA_INDEX = thaaLa_index
    if jaathi_index==None:
        jaathi_index = settings.JAATHI_INDEX
    else:
        settings.JAATHI_INDEX = jaathi_index
    tac = thaaLa.total_akshara_count(thaaLa_index, jaathi_index, 0)
    f_tmp = _TAC_LESSON_DICT[tac]
    aroganam_length = len(settings.RAAGA_DICT[raaga_index]["Aroganam"].split())
    lesson_file = _MELSTHAAYI_FILE_PREFIX + str(aroganam_length)+"_a"+str(f_tmp)+".inp"
    if os.path.exists(lesson_file):
        result = cparser.parse_file(lesson_file, fit_notes_to_speed_and_thaaLa)
    else:
        raise ValueError("Feature not implemented for supplied arguments (raaga_index,thaaLa_index,jaathi_index)",raaga_index,thaaLa_index,jaathi_index)
    return result
    
def __keezhsthaayi_varisai(fit_notes_to_speed_and_thaaLa=False, raaga_index=None, thaaLa_index=None, jaathi_index=None):
    if raaga_index==None:
        raaga_index=settings.RAAGA_INDEX
    else:
        settings.RAAGA_INDEX = raaga_index
    if thaaLa_index==None:
        thaaLa_index=settings.THAALA_INDEX
    else:
        settings.THAALA_INDEX = thaaLa_index
    if jaathi_index==None:
        jaathi_index = settings.JAATHI_INDEX
    else:
        settings.JAATHI_INDEX = jaathi_index
    tac = thaaLa.total_akshara_count(thaaLa_index, jaathi_index, 0)
    f_tmp = _TAC_LESSON_DICT[tac]
    aroganam_length = len(settings.RAAGA_DICT[raaga_index]["Aroganam"].split())
    lesson_file = _KEEZHSTHAYI_FILE_PREFIX + str(aroganam_length)+"_a"+str(f_tmp)+".inp"
    if os.path.exists(lesson_file):
        result = cparser.parse_file(lesson_file, fit_notes_to_speed_and_thaaLa)
    else:
        raise ValueError("Feature not implemented for supplied arguments (raaga_index,thaaLa_index,jaathi_index)",raaga_index,thaaLa_index,jaathi_index)
    return result
    
def alankaara_varisai_from_book(fit_notes_to_speed_and_thaaLa=False, raaga_name=None):
    """
        Generate alankaara varisai (from carnatic music lessons book) for the specified raaga
            :param:    fit_notes_to_speed_and_thaaLa    True the notations generated will be fit to speed and thaaLa
            :param:    raaga_name    If not specified default raaga from settings will be used
            :return:   alankaara varisai for the selected raaga
    """
    if raaga_name==None:
        raaga_index=settings.RAAGA_INDEX
    else:
        raaga.set_raagam(raaga_name)
        settings.RAAGA_INDEX = raaga_index
    aroganam_length = len(settings.RAAGA_DICT[raaga_index]["Aroganam"].split())
    lesson_file = _ALANKARAM_FILE_PREFIX + str(aroganam_length) + ".inp"
    if os.path.exists(lesson_file):
        result = cparser.parse_file(lesson_file, fit_notes_to_speed_and_thaaLa)
    else:
        raise ValueError("Feature not implemented for supplied arguments (raaga_index)",raaga_index)
    return result
    
def alankaara_varisai_from_algorithm(fit_notes_to_speed_and_thaaLa=False, raaga_name=None, thaaLa_name=None, jaathi_name=None):
    """
        Generate alankaara varisai (from computer generated algorithm) for the specified raaga
            :param:    fit_notes_to_speed_and_thaaLa    True the notations generated will be fit to speed and thaaLa
            :param:    raaga_name    If not specified default raaga from settings will be used
            :param:    thaaLa_name   If not specified default thaaLa from settings will be used
            :param:    jaathi_name   If not specified default jaathi from settings will be used
                       Use raaga.get_raaga_list() to get the list of raaga names
                       Use thaaLa.get_thaaLam_names() to get the list of thaaLa names
                       Use thaaLa.get_jaathi_names() to get the list of jaathi names
            :return:   alankaara varisai for the selected raaga
    """
    if raaga_name==None:
        raaga_index=settings.RAAGA_INDEX
    else:
        raaga.set_raagam(raaga_name)
        settings.RAAGA_INDEX = raaga_index
    if thaaLa_name==None:
        thaaLa_index=settings.THAALA_INDEX
    else:
        thaaLa.set_thaaLam(thaaLa_name)
        settings.THAALA_INDEX = thaaLa_index
    if jaathi_name==None:
        jaathi_index = settings.JAATHI_INDEX
    else:
        thaaLa.set_jaathi(jaathi_name)
        settings.JAATHI_INDEX = jaathi_index
    aroganam_length = len(settings.RAAGA_DICT[raaga_index]["Aroganam"].split())
    f_tmp = str(aroganam_length)+"_"+str(thaaLa_index)+"_"+str(jaathi_index)
    lesson_file = _ALANKARAM_FILE_PREFIX + f_tmp + ".inp"
    if os.path.exists(lesson_file):
        result = cparser.parse_file(fit_notes_to_speed_and_thaaLa, lesson_file)
    else:
        raise ValueError("Feature not implemented for supplied arguments (raaga_index,thaaLa_index,jaathi_index)",raaga_index,thaaLa_index,jaathi_index)
    return result

def generate_lessons(lesson_type,fit_notes_to_speed_and_thaaLa=False, raaga_name=None, thaaLa_name=None, jaathi_name=None):
    """
            - generating notations for music lessons for specified raaga and thaaLa
            - Lesson Names supported are: "SARALI_VARISAI", "JANTAI_VARISAI", "DHAATTU_VARISAI", "MELSTHAAYI_VARISAI", "KEEZHSTHAAYI_VARISAI"]
            :param:    lesson_type    case not sensitive
            :param:    fit_notes_to_speed_and_thaaLa    True the notations generated will be fit to speed and thaaLa
            :param:    raaga_name    If not specified default raaga from settings will be used
            :param:    thaaLa_name   If not specified default thaaLa from settings will be used
            :param:    jaathi_name   If not specified default jaathi from settings will be used
                       Use raaga.get_raaga_list() to get the list of raaga names
                       Use thaaLa.get_thaaLam_names() to get the list of thaaLa names
                       Use thaaLa.get_jaathi_names() to get the list of jaathi names
            :return:    notations for the selected lesson
    """
    if raaga_name==None:
        raaga_index=settings.RAAGA_INDEX
    else:
        raaga.set_raagam(raaga_name)
        settings.RAAGA_INDEX = raaga_index
    if thaaLa_name==None:
        thaaLa_index=settings.THAALA_INDEX
    else:
        thaaLa.set_thaaLam(thaaLa_name)
        settings.THAALA_INDEX = thaaLa_index
    if jaathi_name==None:
        jaathi_index = settings.JAATHI_INDEX
    else:
        thaaLa.set_jaathi(jaathi_name)
        settings.JAATHI_INDEX = jaathi_index
    if lesson_type.upper() in LESSON_TYPES:
        #if "alankaara_varisai_from_book" in lesson_type.lower():
        #    results = eval(lesson_type.lower())(fit_notes_to_speed_and_thaaLa, raaga_index)
        #else:
            results = eval("__"+lesson_type.lower())(fit_notes_to_speed_and_thaaLa, raaga_index, thaaLa_index, jaathi_index)
    else:
        raise ValueError("lesson_type should be one of:",LESSON_TYPES, " not case sensitive")
    return results
if __name__ == '__main__':
    #result = alankaara_varisai_from_book(fit_notes_to_speed_and_thaaLa=True)
    result = generate_lessons("sarali_varisai",fit_notes_to_speed_and_thaaLa=True)#,thaaLa_index=2,jaathi_index=2)
    print(result)
    pass