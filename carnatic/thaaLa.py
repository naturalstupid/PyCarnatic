"""
    Module for 
            - setting thaaLam/jaathi/nadai
            - getting solkattu patterns for mridangam accompaniement - per music notation
"""
import configparser
import random
import itertools
from carnatic import settings

def get_thaaLa_index():
    return settings.THAALA_INDEX
def get_jaathi_index():
    return settings.JAATHI_INDEX
def get_nadai_index():
    return settings.NADAI_INDEX
def get_current_thaaLam():
    return settings.THAALA_INDEX,settings.JAATHI_INDEX,settings.NADAI_INDEX
def get_thaaLam_names():
    """
    @return: list of thaaLam names
    """
    return [t.name for t in settings.THAALA_NAMES]
def get_jaathi_names():
    """
    @return: list of Jaathi names
    """
    return [t.name for t in settings.JAATHI_NAMES]
def get_nadai_names():
    """
    @return: list of Nadai names
    """
    return [t.name for t in settings.NADAI_NAMES]
def set_thaaLam(thaaLa_index:settings.THAALA_NAMES=None,jaathi_index:settings.JAATHI_NAMES=None,nadai_index:settings.NADAI_NAMES=None):
    """
        Set the thaaLam and Jaathi to specified names
        @param thaaLam: one of "EKA","ROOPAKA", "JAMPA", "THRIPUTAI","MATHYA", "ATA", "DHURVA" (case insensitive)
        @param jaathi: one of "THISRA", "CHATHUSRA", "KHANDA", "MISRA", "SANKEERNA" (case insensitive)
        @param nadai: one of "FIRST-SPEED","SECOND-SPEED","THISRA", "CHATHUSRA/THIRRD-SPEED", "KHANDA", "MISRA", "SANKEERNA" (case insensitive)
    """
    if thaaLa_index == None:
        thaaLa_index = get_thaaLa_index()
    if jaathi_index == None:
        jaathi_index = get_jaathi_index()
    if nadai_index == None:
        nadai_index = get_nadai_index()
    settings.THAALA_INDEX = thaaLa_index
    settings.JAATHI_INDEX = jaathi_index
    settings.NADAI_INDEX = nadai_index
    #print('set_thaaLam',thaaLam,jaathi,nadai)
def set_thaaLam_index(thaaLa_index:settings.THAALA_NAMES=None,
                      jaathi_index:settings.JAATHI_NAMES=None,
                      nadai_index:settings.NADAI_NAMES=None):
    """
        Set the thaaLam and Jaathi using their indices
        @param thaaLa_index: 1 to 7
        @param jaathi_index: 1 to 5
        @param nadai_index: 0 to 5 (0 means No Nadai)
    """
    if thaaLa_index == None:
        thaaLa_index = get_thaaLa_index()
    if jaathi_index == None:
        jaathi_index = get_jaathi_index()
    if nadai_index == None:
        nadai_index = get_nadai_index()
    settings.THAALA_INDEX = thaaLa_index
    settings.JAATHI_INDEX = jaathi_index
    settings.NADAI_INDEX = nadai_index
def total_beat_count(thaaLa_index:settings.THAALA_NAMES=None, 
                        jaathi_index:settings.JAATHI_NAMES=None): 
    """
        Get total beats per thaaLa. Beat count is without nadai. Akshara count is including nadai
        @param thaaLa_index: 1 to 7
        @param jaathi_index: 1 to 5
    """
    if thaaLa_index == None:
        thaaLa_index = get_thaaLa_index()
    if jaathi_index == None:
        jaathi_index = get_jaathi_index()
    tab = (settings.thaaLa_laghu_no[thaaLa_index] * settings.jaathi_no[jaathi_index] + settings.thaaLa_drutam_no[thaaLa_index] * 2 \
           + settings.thaaLa_anudrutam_no[thaaLa_index]) * 1
    return tab

def total_akshara_count(thaaLa_index:settings.THAALA_NAMES=None, 
                        jaathi_index:settings.JAATHI_NAMES=None,
                        nadai_index:settings.NADAI_NAMES=None): 
    """
        Get total akshara count
        @param thaaLa_index: 1 to 7
        @param jaathi_index: 1 to 5
        @param nadai_index: 0 to 5 (0 means No Nadai)
    """
    if thaaLa_index == None:
        thaaLa_index = get_thaaLa_index()
    if jaathi_index == None:
        jaathi_index = get_jaathi_index()
    if nadai_index == None:
        nadai_index = get_nadai_index()
    tac = total_beat_count(thaaLa_index, jaathi_index) * settings.nadai_no[nadai_index] #V1.0.2
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
    ret = list(inner(nr, 0))
    return ret
    
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
def get_thaaLa_patterns_for_thaaLa_jaathi_nadai(thaaLa_index:settings.THAALA_NAMES=None,
                      jaathi_index:settings.JAATHI_NAMES=None,
                      nadai_index:settings.NADAI_NAMES=None,
                      generate_random=True,maintain_nadai=False):
    """
        Get solkattu pattern for given thaaLa / Jaathi / Nadai combination 
        @param thaaLa_index: 1 to 7
        @param jaathi_index: 1 to 5
        @param nadai_index: 0 to 6
        @param generate_random: True means for each call pattern generated will be random for each of digits of the beqat string
            0 = 1st Speed, 1 = second speed, 2 = thisra, 3=chathusra/3rd speed, 4=Khanda, 5=Misra 6=Sankeerna 
    """
    """
        TODO: Nadai_Index should account for ThaaLam Speed. There should be no separate variable for thaaLam speed
    """
    if thaaLa_index == None:
        thaaLa_index = get_thaaLa_index()
    if jaathi_index == None:
        jaathi_index = get_jaathi_index()
    if nadai_index == None:
        nadai_index = get_nadai_index()
    tac = total_akshara_count(thaaLa_index, jaathi_index, nadai_index)
    if maintain_nadai:
        n1 = settings.nadai_no[nadai_index]
        n2 = int(tac / n1)
        ret1 = _partition_nr_into_given_set_of_nrs(tac, [n1]*n2)
    else:
        ret1 = _partition_nr_into_given_set_of_nrs(tac, settings.BEAT_LENGTH_SELECTION) #_get_beat_length_based_on_nadai(nadai_index,tac)) #
    #print(ret1) 
    ret2 = str("".join(map(str, ret1[0])))
    #print(ret2)
    thaaLa_patterns = get_thaaLa_patterns_for_beat_string(ret2,generate_random=generate_random)
    return thaaLa_patterns
def _get_beat_length_based_on_nadai(nadai_index:settings.NADAI_INDEX,total_akshara_count):
    if settings.jaathi_no[nadai_index] in settings.BEAT_LENGTH_SELECTION:
        ret = [(ni+1) for ni in range(total_akshara_count) if (ni+1) %settings.nadai_no[nadai_index] ==0 ]
    else:
        ret = settings.BEAT_LENGTH_SELECTION
    return ret
def get_thaaLa_positions(thaaLa_index:settings.THAALA_NAMES=None,
                      jaathi_index:settings.JAATHI_NAMES=None,
                      as_string=False):
    """
        Get thaaLam positions for specified thaaLam and Jaathi
        @param thaaLa_index: 1 to 7
        @param jaathi_index: 1 to 5
    """
    if thaaLa_index == None:
        thaaLa_index = get_thaaLa_index()
    if jaathi_index == None:
        jaathi_index = get_jaathi_index()
    ret = settings.THAALA_LOC[thaaLa_index][jaathi_index]
    if as_string:
        tmp = ''
        for k,v in ret.items():
            tmp += ' ' + str(k) +' ' + str(v)
        ret = tmp.strip().strip('\n')
    #print('get_thaaLa_positions',ret,'as_string',as_string)
    return ret
def get_thaaLa_patterns_for_avarthanam(avarthanam_count,
                      thaaLa_index:settings.THAALA_NAMES=None,
                      jaathi_index:settings.JAATHI_NAMES=None,
                      nadai_index:settings.NADAI_NAMES=None,generate_random=True,maintain_nadai=settings._MAINTAIN_NADAI):
    """
        Get thaaLam positions for specified number of avarthanams and specified thaaLam and Jaathi
        @param avarthanam_count: Number of avarthanams
        @param thaaLa_index: 1 to 7
        @param jaathi_index: 1 to 5
        @param nadai_index: 0 to 5 (0 means No Nadai)
        @param generate_random: True means for each call pattern generated will be random for each of digits of the beqat string
    """
    if thaaLa_index == None:
        thaaLa_index = get_thaaLa_index()
    if jaathi_index == None:
        jaathi_index = get_jaathi_index()
    if nadai_index == None:
        nadai_index = get_nadai_index()
    result = []
    for a in range(avarthanam_count):
        res = []
        res = get_thaaLa_patterns_for_thaaLa_jaathi_nadai(thaaLa_index, jaathi_index, nadai_index,
                                                          generate_random=generate_random,maintain_nadai=maintain_nadai)
        result = result + res
    result = settings.flatten_list(result)
    return result
if __name__ == '__main__':
    from carnatic import cparser, cplayer
    import time
    start_time = time.time()
    #"""
    settings.TEMPO = 72
    thaaLa_index = 4
    settings.THAALA_INDEX = thaaLa_index
    jaathi_index = 2
    settings.JAATHI_INDEX = jaathi_index
    nadai_index = 3
    settings.NADAI_INDEX = nadai_index
    print('thaala',settings.THAALA_NAMES(thaaLa_index).name)
    print('jaathi',settings.JAATHI_NAMES(jaathi_index).name)
    print('nadai',settings.NADAI_NAMES(nadai_index).name)
    print('thaala positions',get_thaaLa_positions(thaaLa_index, jaathi_index,as_string=True))
    tac = total_akshara_count(thaaLa_index, jaathi_index, nadai_index)
    print('total_akshara_count',tac)
    avarthanam_count = 2
    thaaLa_patterns = get_thaaLa_patterns_for_avarthanam(avarthanam_count,maintain_nadai=True)
    print(thaaLa_patterns)
    solkattu = cparser.parse_solkattu(thaaLa_patterns)
    thaaLa_duration = cparser.total_duration(solkattu)
    cplayer.__play_notes(solkattu)
    print(time.time()-start_time)
    