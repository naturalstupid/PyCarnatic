import re
#from settings import *
import settings

#settings.RAAGA_DICT = get_raaga_dictionary()
def _get_raaga_attribute(field,ri=None):
    if ri==None:
        ri=settings.RAAGA_INDEX
    result = ''
    if field in settings.RAAGA_DICT[0].keys():
        return settings.RAAGA_DICT[ri][field]
    return ''    
def _search_raaga_for_values(search_key, search_str,is_exact=False):
    matching_keys = []
    for k,v in settings.RAAGA_DICT.items():
        if is_exact:
            if search_str.lower() == settings.RAAGA_DICT[k][search_key].lower():
                name = settings.RAAGA_DICT[k]['Name']
                matching_keys.append([k,name])
        else:
            if search_str.lower() in settings.RAAGA_DICT[k][search_key].lower():
                name = settings.RAAGA_DICT[k]['Name']
                matching_keys.append([k,name])
    return matching_keys    
def get_aroganam(ri=None):
    if ri==None:
        ri=settings.RAAGA_INDEX
    return _get_raaga_attribute("Aroganam",ri).split()
def get_avaroganam(ri=None):
    if ri==None:
        ri=settings.RAAGA_INDEX

    return _get_raaga_attribute("Avaroganam",ri).split()
def is_sampoorna(ri=None):
    if ri==None:
        ri=settings.RAAGA_INDEX
    return _get_raaga_attribute("Arohanam Note Count",ri) == 8 and _get_raaga_attribute("Avarohanam Note Count",ri) == 8
def is_janya(ri=settings.RAAGA_INDEX):
    return "Janya" in _get_raaga_attribute("Melakartha_or_Janya",ri)
def is_melakartha(ri=None):
    if ri==None:
        ri=settings.RAAGA_INDEX
    return ri in settings.MELAKARTHA_LIST
def get_janya_raagas(ri=None):
    if ri==None:
        ri=settings.RAAGA_INDEX
    janya_str = "Janya of MK-"+str(_get_raaga_attribute('mELakartha',ri))
    janya_list = _search_raaga_for_values("Melakartha_or_Janya",janya_str)
    return janya_list
def search_for_raaga_by_name(search_str,is_exact=False):
    search_key = "Name"
    return _search_raaga_for_values(search_key, search_str, is_exact)
def search_for_raaga_by_attributes(attribute_value_dictionary,is_exact=False):
    results = []
    found = True
    for attr, attr_value in attribute_value_dictionary.items():
        results = _search_raaga_for_values(attr,attr_value,is_exact)
        found  = found and  len(results) > 0
    return results
def get_raaga_name(ri=None):
    if ri==None:
        ri=settings.RAAGA_INDEX
    return _get_raaga_attribute("Name",ri)
def get_raasi(ri=None):
    if ri==None:
        ri=settings.RAAGA_INDEX
    return _get_raaga_attribute("Raasi",ri)
def get_parent_raaga_id(ri=None):
    if ri==None:
        ri=settings.RAAGA_INDEX
    parent_raaga_id = -1 
    melakartha_number = get_melakartha(ri)
    filter_options = {'mELakartha' : str(melakartha_number), 'Melakartha_or_Janya':"mELakartha-"+str(melakartha_number)}
    parent_raaga_id = search_for_raaga_by_attributes(filter_options)[0]
    return parent_raaga_id
def get_default_raaga():
    return settings.RAAGA_INDEX
def set_default_raaga(ri):
    raaga_dict_length = len(settings.RAAGA_DICT)
    if ri >= raaga_dict_length:
        raise ValueError("Raaga ID should be in the range 0.."+str(raaga_dict_length))
    settings.RAAGA_INDEX = ri
    melakartha_number = get_melakartha(ri)
    settings.MELAKARTHA_INDEX = melakartha_number
def get_melakartha(ri=None):
    if ri==None:
        ri=settings.RAAGA_INDEX
    return settings.MELAKARTHA_LIST.index(ri)+1
def set_melakartha(melakartha_number):
    """ Setting melakartha will change the raaga to melakartha raaga """
    if melakartha_number <= 0 or melakartha_number > 72:
        raise ValueError("Melakartha number should be in the range 1..72")
    settings.MELAKARTHA_INDEX = melakartha_number
    settings.RAAGA_INDEX = settings.MELAKARTHA_LIST[melakartha_number-1]
def get_krithis(ri=None):
    if ri==None:
        ri=settings.RAAGA_INDEX
    return _get_raaga_attribute("Krithi_IDs",ri).split(";")

if __name__ == '__main__':
    exit()
    """
    print(get_parent_raaga_id(290))
    exit()
    """
    #"""
    set_melakartha(10)
    print('raaga index',settings.RAAGA_INDEX)
    print(is_melakartha(115))
    set_default_raaga(71)
    print(get_melakartha())
    print(get_parent_raaga_id())
    exit()
    #"""
    #"""
    #filter_options = {'mELakartha' : '15', 'Melakartha_or_Janya':"mELakartha-15"}
    filter_options = {'Krithi_IDs' : '1000'}
    print(_search_raaga_for_values('Krithi_IDs','1000'))
    print(search_for_raaga_by_attributes(filter_options))
    exit()
    #"""
    #"""
    #print(_get_raaga_attribute("Krithi_IDs"))
    print(get_krithis())
    exit()
    #"""
    #"""
    print(search_for_raaga_by_name("hamsa"))
    #"""