"""
    Module for 
            - setting thaaLam/jaathi/nadai
            - getting solkattu patterns for mridangam accompaniement - per music notation
"""
import configparser
import random
import itertools
import settings
import cparser
import cplayer

def _get_thaaLa_index(thaaLam):
    return settings.THAALA_NAMES.index(thaaLam)
def _get_jaathi_index(jaathi):
    return settings.JAATHI_NAMES.index(jaathi)
def _get_nadai_index(nadai):
    return settings.NADAI_NAMES.index(nadai)
def get_thaaLam_names():
    return settings.THAALA_NAMES
def get_jaathi_names():
    return settings.JAATHI_NAMES
def set_thaaLam(thaaLam):
    if thaaLam not in settings.THAALA_NAMES:
        raise ValueError(thaaLam, "Not in allowed ThaaLam Names:",settings.THAALA_NAMES)
    thaaLa_index = _get_thaaLa_index(thaaLam)
    settings.THAALA_INDEX = thaaLa_index
def set_jaathi(jaathi):
    if jaathi not in settings.JAATHI_NAMES:
        raise ValueError(jaathi,"Not in allowed Jaathi Names:",settings.JAATHI_NAMES)
    jaathi_index = _get_jaathi_index(jaathi)
    settings.JAATHI_INDEX = jaathi_index
def set_nadai(nadai):
    if nadai not in settings.NADAI_NAMES:
        raise ValueError(nadai,"Not in allowed Nadai Names:",settings.NADAI_NAMES)
    nadai_index = _get_nadai_index(nadai)
    settings.NADAI_INDEX = nadai_index
def total_akshara_count(thaaLa_index=None, jaathi_index=None, nadai_index=None): 
    if thaaLa_index==None:
        thaaLa_index=settings.THAALA_INDEX
    if jaathi_index==None:
        jaathi_index = settings.JAATHI_INDEX
    if nadai_index==None:
        nadai_index = settings.NADAI_INDEX
    tac = (settings.thaaLa_laghu_no[thaaLa_index] * settings.jaathi_no[jaathi_index] + settings.thaaLa_drutam_no[thaaLa_index] * 2 \
           + settings.thaaLa_anudrutam_no[thaaLa_index]) * settings.jaathi_no[nadai_index]
    return tac

total_akshara_count_default = total_akshara_count(settings.THAALA_INDEX,settings.JAATHI_INDEX,settings.NADAI_INDEX)

def partition_nr_into_given_set_of_nrs(nr, S):
    nrs = sorted(S, reverse=True)
    def inner(n, i):
        if n == 0:
            yield []
        for k in range(i, len(nrs)):
            if nrs[k] <= n:
                for rest in inner(n - nrs[k], k):
                    yield [nrs[k]] + rest
    return list(inner(nr, 0))
    
def _combination(list1, list2,reverse=True):
    lst1 =  [(x +" " + y) for x in list1 for y in list2]
    if reverse:
        lst2 = [ (y +" " + x) for x in list1 for y in list2]
        combined_list = lst1 + lst2
    else:
        combined_list = lst1
    return combined_list
def get_thaaLa_patterns_for_beat_string(thaaLa_beat_string,generate_random=True):
    lst = []
    for c in thaaLa_beat_string:
        ci = int(c)
        #print('ci=',ci)
        tpc = settings.THAALA_PATTERN_COUNTS[ci-1]
        #print('tpc=',tpc)
        rn = random.randint(0,tpc-1)
        #print('ci,rn',ci,rn)
        tp = settings.THAALA_PATTERNS[ci-1][rn].split()
        #print("thaal beat",c,'pattern',tp)
        lst.append(tp)
    return lst
def get_thaaLa_patterns_for_thaaLa_jaathi_nadai(thaaLa_index=None, jaathi_index=None, nadai_index=None):
    if thaaLa_index==None:
        thaaLa_index=settings.THAALA_INDEX
    if jaathi_index==None:
        jaathi_index = settings.JAATHI_INDEX
    if nadai_index==None:
        nadai_index = settings.NADAI_INDEX
    tac = total_akshara_count(thaaLa_index, jaathi_index, nadai_index)
    #print('tac',tac)
    ret1 = partition_nr_into_given_set_of_nrs(tac, settings.BEAT_LENGTH_SELECTION)
    #print('ret1',ret1)
    ret2 = str("".join(map(str, ret1[0])))
    thaaLa_patterns = get_thaaLa_patterns_for_beat_string(ret2,True)
    return thaaLa_patterns
def __get_thaaLa_patterns():
    thaaLa_config = configparser.ConfigParser()
    thaala_settings = thaaLa_config.read(settings.THAALA_PATTERN_FILE)
    sections = thaaLa_config.sections()
    settings.THAALA_PATTERNS.clear()
    settings.THAALA_PATTERN_COUNTS.clear()
    for section in sections:
        section_items =  dict(thaaLa_config.items(section))
        #print(section_items)
        for key in section_items:
            key_id = int(key)-1
            patterns = list(part for part in section_items[key].replace("|","").split(";") if (part.strip() != "|" and part.strip() !="") )
            settings.THAALA_PATTERNS.append(patterns)
    """ Now construct for 5-beats to 9 beats """
    """ 5 beats = 1 + 4 and 4 + 1 """
    settings.THAALA_PATTERNS.append(_combination(settings.THAALA_PATTERNS[0],settings.THAALA_PATTERNS[3]))
    """ 6 beats = 1 + 5 and 5 + 1 and 3 + 3"""
    lst1 = _combination(settings.THAALA_PATTERNS[1],settings.THAALA_PATTERNS[3])
    lst2 = _combination(settings.THAALA_PATTERNS[1],settings.THAALA_PATTERNS[3],False)
    settings.THAALA_PATTERNS.append(lst1+lst2)
    
    """ 7 beats = 2 + 5 and 5 + 2 and 3 + 4 and 4+3 """
    lst1 = _combination(settings.THAALA_PATTERNS[1],settings.THAALA_PATTERNS[4])
    lst2 = _combination(settings.THAALA_PATTERNS[2],settings.THAALA_PATTERNS[3])
    settings.THAALA_PATTERNS.append(lst1+lst2)
    
    """ 8 beats = 3 + 5 and 5 + 3 and 4 + 4  2+6/6+2 """
    lst1 = _combination(settings.THAALA_PATTERNS[2],settings.THAALA_PATTERNS[4])
    lst2 = _combination(settings.THAALA_PATTERNS[1],settings.THAALA_PATTERNS[5])
    lst3 = _combination(settings.THAALA_PATTERNS[3],settings.THAALA_PATTERNS[3],False)
    settings.THAALA_PATTERNS.append(lst1+lst2+lst3)
    
    """ 9 beats = 4 + 5 and 5 + 4 and 3 + 6 and 6+3 and 2+7/7+2"""
    lst1 = _combination(settings.THAALA_PATTERNS[3],settings.THAALA_PATTERNS[4])
    lst2 = _combination(settings.THAALA_PATTERNS[5],settings.THAALA_PATTERNS[2])
    lst3 = _combination(settings.THAALA_PATTERNS[1],settings.THAALA_PATTERNS[6])
    settings.THAALA_PATTERNS.append(lst1+lst2+lst3)
    
    for pattern in settings.THAALA_PATTERNS:
        settings.THAALA_PATTERN_COUNTS.append(len(pattern))
    return settings.THAALA_PATTERNS
def get_thaaLa_positions(thaaLa_index=None, jaathi_index=None):
    if thaaLa_index==None:
        thaaLa_index=settings.THAALA_INDEX
    if jaathi_index==None:
        jaathi_index = settings.JAATHI_INDEX
    #print('inside thaaLa',thaaLa_index,jaathi_index)
    return settings.THAALA_LOC[thaaLa_index][jaathi_index]
def get_thaaLa_patterns_for_avarthanam(avarthanam_count,thaaLa_index=None, jaathi_index=None, nadai_index=None):
    result = []
    for a in range(avarthanam_count):
        res = []
        res = get_thaaLa_patterns_for_thaaLa_jaathi_nadai(thaaLa_index, jaathi_index, nadai_index)
        result = result + res
    return result
if __name__ == '__main__':
    """
    for t in range(1,8):
        for j in range(1,6):
            print(settings.THAALA_NAMES[t], settings.JAATHI_NAMES[j], settings.THAALA_LOC[t][j])
    exit()
    """
    #"""
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
    #"""