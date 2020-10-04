"""
    Module for 
            - setting thaaLam/jaathi/nadai
            - getting solkattu patterns for mridangam accompaniement - per music notation
"""
import configparser
import random
import itertools

from carnatic import settings
from carnatic import cparser
from carnatic import cplayer

def _get_thaaLa_index(thaaLam):
    return settings.THAALA_NAMES.index(thaaLam.upper())
def _get_jaathi_index(jaathi):
    return settings.JAATHI_NAMES.index(jaathi.upper())
def _get_nadai_index(nadai):
    return settings.NADAI_NAMES.index(nadai.upper())
def get_thaaLam_names():
    """
    @return: list of thaaLam names
    """
    return settings.THAALA_NAMES
def get_jaathi_names():
    """
    @return: list of Jaathi names
    """
    return settings.JAATHI_NAMES
def get_nadai_names():
    """
    @return: list of Nadai names
    """
    return settings.NADAI_NAMES
def set_thaaLam_speed(thaaLam_speed=1):
    """
        Set the thaaLam speed of the song.
        ****** CAUTION ******
        Speed is in addition to Nadai 
        Values 1 to 3
        Example: Speed =2, Chathusra Nadai => 8 beats per note or 
        Speed = 3 No nadai is same as Chathusra Nadai  =< Both will have 4 notes per note
        SO KNOW WHAT YOU ARE DOING BY SETTING NADAI AND SPEED
        *********************
        @param thaaLam_speed: thaaLam speed (also called kalai)
     """
    if thaaLam_speed < 1 or thaaLam_speed > 3:
         raise ValueError("ThaaLam Speed should be in the range 1 to 3")
    settings.THAALAM_SPEED = thaaLam_speed
def set_thaaLam(thaaLam,jaathi,nadai=None):
    """
        Set the thaaLam and Jaathi to specified names
        @param thaaLam: one of "EKA","ROOPAKA", "JAMPA", "THRIPUTAI","MATHYA", "ATA", "DHURVA" (case insensitive)
        @param jaathi: one of "THISRA", "CHATHUSRA", "KHANDA", "MISRA", "SANKEERNA" (case insensitive)
        @param nadai: one of "THISRA", "CHATHUSRA", "KHANDA", "MISRA", "SANKEERNA" (case insensitive)
    """
    if nadai == None:
        nadai = ""
    if thaaLam.upper() not in (name.upper() for name in settings.THAALA_NAMES):
        raise ValueError(thaaLam, "Not in allowed ThaaLam Names:",settings.THAALA_NAMES)
    thaaLa_index = _get_thaaLa_index(thaaLam)
    if jaathi.upper() not in (name.upper() for name in settings.JAATHI_NAMES):
        raise ValueError(jaathi,"Not in allowed Jaathi Names:",settings.JAATHI_NAMES)
    jaathi_index = _get_jaathi_index(jaathi)
    if nadai.upper() not in (name.upper() for name in settings.NADAI_NAMES):
        raise ValueError(nadai,"Not in allowed Nadai Names:",settings.NADAI_NAMES)
    nadai_index = _get_nadai_index(nadai)
    set_thaaLam_index(thaaLa_index,jaathi_index,nadai_index)
def set_thaaLam_index(thaaLa_index, jaathi_index,nadai_index=None):
    """
        Set the thaaLam and Jaathi using their indices
        @param thaaLa_index: 1 to 7
        @param jaathi_index: 1 to 5
        @param nadai_index: 0 to 5 (0 means No Nadai)
    """
    if nadai_index == None:
        nadai_index = settings.NADAI_INDEX
    if thaaLa_index <= 0 or thaaLa_index > len(settings.THAALA_NAMES):
        raise ValueError("ThaaLa index should be in the range 1..7")
    if jaathi_index <= 0 or jaathi_index > len(settings.JAATHI_NAMES):
        raise ValueError("Jaathi index should be in the range 1..5")
    if nadai_index < 0 or nadai_index > len(settings.NADAI_NAMES):
        raise ValueError("Nadai index should be in the range 1..5")
    settings.THAALA_INDEX = thaaLa_index
    settings.JAATHI_INDEX = jaathi_index
    settings.NADAI_INDEX = nadai_index
def total_beat_count(thaaLa_index=None, jaathi_index=None): 
    """
        Get total beats per thaaLa. Beat count is without nadai. Akshara count is including nadai
        @param thaaLa_index: 1 to 7
        @param jaathi_index: 1 to 5
    """
    if thaaLa_index==None:
        thaaLa_index=settings.THAALA_INDEX
    if jaathi_index==None:
        jaathi_index = settings.JAATHI_INDEX
    tab = (settings.thaaLa_laghu_no[thaaLa_index] * settings.jaathi_no[jaathi_index] + settings.thaaLa_drutam_no[thaaLa_index] * 2 \
           + settings.thaaLa_anudrutam_no[thaaLa_index]) * 1
    return tab

def total_akshara_count(thaaLa_index=None, jaathi_index=None, nadai_index=None): 
    """
        Get total akshara count
        @param thaaLa_index: 1 to 7
        @param jaathi_index: 1 to 5
        @param nadai_index: 0 to 5 (0 means No Nadai)
    """
    if nadai_index==None:
        nadai_index = settings.NADAI_INDEX
    tac = total_beat_count(thaaLa_index, jaathi_index) * settings.jaathi_no[nadai_index]
    return tac

total_akshara_count_default = total_akshara_count(settings.THAALA_INDEX,settings.JAATHI_INDEX,settings.NADAI_INDEX)

def _partition_nr_into_given_set_of_nrs(nr, S):
    nrs = sorted(S, reverse=True)
    def inner(n, i):
        if n == 0:
            yield []
        for k in range(i, len(nrs)):
            if nrs[k] <= n:
                for rest in inner(n - nrs[k], k):
                    yield [nrs[k]] + rest
    return list(inner(nr, 0))
    
def get_thaaLa_patterns_for_beat_string(thaaLa_beat_string,generate_random=True):
    """
        Get solkattu pattern for a given beat string. 
        A beat string is a 4 digit string. Example: "9754"
        @param thaaLa_beat_string: Example: "9754"
        @param generate_random: True means for each call pattern generated will be random for each of digits of the beqat string
    """
    lst = []
    for c in thaaLa_beat_string:
        ci = int(c)
        tpc = settings.THAALA_PATTERN_COUNTS[ci-1]
        rn = 0
        if generate_random:
            rn = random.randint(0,tpc-1)
        tp = settings.THAALA_PATTERNS[ci-1][rn].split()
        lst.append(tp)
    return lst
def get_thaaLa_patterns_for_thaaLa_jaathi_nadai(thaaLa_index=None, jaathi_index=None, nadai_index=None,generate_random=True):
    """
        Get solkattu pattern for given thaaLa / Jaathi / Nadai combination 
        @param thaaLa_index: 1 to 7
        @param jaathi_index: 1 to 5
        @param nadai_index: 0 to 5 (0 means No Nadai)
        @param generate_random: True means for each call pattern generated will be random for each of digits of the beqat string
    """
    if thaaLa_index==None:
        thaaLa_index=settings.THAALA_INDEX
    if jaathi_index==None:
        jaathi_index = settings.JAATHI_INDEX
    if nadai_index==None:
        nadai_index = settings.NADAI_INDEX
    tac = total_akshara_count(thaaLa_index, jaathi_index, nadai_index)*settings.THAALAM_SPEED
    #print('tac',tac)
    ret1 = _partition_nr_into_given_set_of_nrs(tac, settings.BEAT_LENGTH_SELECTION)
    #print('ret1',ret1)
    ret2 = str("".join(map(str, ret1[0])))
    thaaLa_patterns = get_thaaLa_patterns_for_beat_string(ret2,generate_random=generate_random)
    return thaaLa_patterns
def get_thaaLa_positions(thaaLa_index=None, jaathi_index=None):
    """
        Get thaaLam positions for specified thaaLam and Jaathi
        @param thaaLa_index: 1 to 7
        @param jaathi_index: 1 to 5
    """
    if thaaLa_index==None:
        thaaLa_index=settings.THAALA_INDEX
    if jaathi_index==None:
        jaathi_index = settings.JAATHI_INDEX
    #print('inside thaaLa',thaaLa_index,jaathi_index)
    return settings.THAALA_LOC[thaaLa_index][jaathi_index]
def get_thaaLa_patterns_for_avarthanam(avarthanam_count,thaaLa_index=None, jaathi_index=None, nadai_index=None,generate_random=True):
    """
        Get thaaLam positions for specified number of avarthanams and specified thaaLam and Jaathi
        @param avarthanam_count: Number of avarthanams
        @param thaaLa_index: 1 to 7
        @param jaathi_index: 1 to 5
        @param nadai_index: 0 to 5 (0 means No Nadai)
        @param generate_random: True means for each call pattern generated will be random for each of digits of the beqat string
    """
    result = []
    for a in range(avarthanam_count):
        res = []
        res = get_thaaLa_patterns_for_thaaLa_jaathi_nadai(thaaLa_index, jaathi_index, nadai_index,generate_random=generate_random)
        result = result + res
    return result
if __name__ == '__main__':
    """
    for t in range(1,8):
        for j in range(1,6):
            print(settings.THAALA_NAMES[t], settings.JAATHI_NAMES[j], settings.THAALA_LOC[t][j])
    exit()
    """
    """
    settings.THAALA_PATTERNS = __get_thaaLa_patterns()
    #print(settings.THAALA_PATTERN_COUNTS)
    thaaLa_index = 2
    jaathi_index = 2
    nadai_index = 2
    #tp = get_thaaLa_patterns_for_thaaLa_jaathi_nadai(thaaLa_index, jaathi_index, nadai_index)
    tp = get_thaaLa_patterns_for_avarthanam(2,thaaLa_index, jaathi_index, nadai_index)
    print(tp)
    sk = cparser.parse_solkattu(tp)
    print(sk)
    td = cparser.total_duration(sk)
    print('total duration',td)
    #cplayer.play_notes(sk)
    """