import settings
import configparser
import random
import itertools

def set_thaaLa(thaaLa_index):
    if thaaLa_index > 0 and thaaLa_index < 8:
        settings.THAALA_INDEX = thaaLa_index
    else:
        raise ValueError("Thaala Index should be in the range 1..7")
def set_jaathi(jaathi_index):
    if jaathi_index > 0 and jaathi_index < 6:
        settings.JAATHI_INDEX = jaathi_index
    else:
        raise ValueError("Jaathi Index should be in the range 1..5")
def set_nadai(nadai_index):
    if nadai_index > 0 and nadai_index < 6:
        settings.NADAI_INDEX = nadai_index
    else:
        raise ValueError("Nadai Index should be in the range 1..5")
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
        rn = random.randint(0,settings.THAALA_PATTERN_COUNTS[ci-1])
        lst.append(settings.THAALA_PATTERNS[ci-1][rn])
    return ' '.join(lst)
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
def get_thaaLa_patterns():
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

if __name__ == '__main__':
    for t in range(1,8):
        for j in range(1,6):
            print(settings.THAALA_NAMES[t], settings.JAATHI_NAMES[j], settings.THAALA_LOC[t][j])
    exit()
    settings.THAALA_PATTERNS = get_thaaLa_patterns()
    print(settings.THAALA_PATTERN_COUNTS)
    thaaLa_index = 2
    jaathi_index = 2
    nadai_index = 2
    print(get_thaaLa_patterns_for_thaaLa_jaathi_nadai(thaaLa_index, jaathi_index, nadai_index))
        
                                  