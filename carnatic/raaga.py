"""
    Module for 
            - setting raaga / melakartha
            - searching for raaga, getting attributes of raaga (e.g. is janya, is sampoorna, get parent etc
"""
import re

from carnatic import settings, cparser
_RAAGA_DICT = settings.RAAGA_DICT
#settings.RAAGA_DICT = get_raaga_dictionary()
def _get_raaga_attribute(field,raagam_index=None):
    if raagam_index==None:
        raagam_index=settings.RAAGA_INDEX
    result = []
    if field in _RAAGA_DICT[0].keys():
        result = _RAAGA_DICT[raagam_index][field]
        return result
    return ''    
def _search_raaga_for_values(search_key, search_str,is_exact=False):
    if isinstance(search_str, int):
        search_str = str(search_str)
    matching_keys = []
    for k,v in _RAAGA_DICT.items():
        if is_exact:
            if search_str.lower() == _RAAGA_DICT[k][search_key].lower():
                name = _RAAGA_DICT[k]['Name']
                matching_keys.append([k,name])
        else:
            if search_str.lower() in _RAAGA_DICT[k][search_key].lower():
                name = _RAAGA_DICT[k]['Name']
                matching_keys.append([k,name])
    return matching_keys
def get_previous_note(carnatic_note,note_step=1,raagam_index=None):
    """
        Get the previous carnatic note for the specified raaga
        @param carnatic_note: The carnatic note for which previous note is needed
        @param note_step: 1 means immediate previous note of the raaga's aroganam Value 1 to length of aroganam minus one
        @param raagam_index: Index of raaga. See docs/help or get_raaaga_list for id and raaga_name
        @return: previous carnatic note
    """
    note,oct_str,pitch_str = cparser._split_carnatic_note_to_parts(carnatic_note)
    note = re.sub("\d+","",note)
    result = None
    if raagam_index==None:
        raagam_index=settings.RAAGA_INDEX
    aroganam = get_aaroganam(raagam_index)
    aro_len = len(aroganam)
    aroganam_copy = [re.sub("\d","",a.upper()) for a in aroganam[:]]
    note_index = aroganam_copy.index(note.upper())
    #print('get_previous_note','note index in aroganam',note.upper(),carnatic_note, note_index)
    if note_index > note_step-1:
        result = aroganam[note_index-note_step]+oct_str
        #print('prev note 1',result)
    else:
        if carnatic_note.upper() != "S^" and carnatic_note.upper() != "S'":
            result = aroganam[aro_len-note_step-1]+"."
            #print('prev note 2',result)
        else:
            result = aroganam[aro_len-note_step-1]
            #print('prev note 3',result)
    return result
def get_next_note(carnatic_note,note_step=1,raagam_index=None):
    """
        Get the next carnatic note for the specified raaga
        @param carnatic_note: The carnatic note for which previous note is needed
        @param note_step: 1 means immediate next note of the raaga's aroganam Value 0 to length of aroganam
        @param raagam_index: Index of raaga. See docs/help or get_raaaga_list for id and raaga_name
        @return: next carnatic note
    """
    note,oct_str,pitch_str = cparser._split_carnatic_note_to_parts(carnatic_note)
    note = re.sub("\d+","",note)
    result = None
    if raagam_index==None:
        raagam_index=settings.RAAGA_INDEX
    aroganam = get_aaroganam(raagam_index)
    aroganam_copy = [re.sub("\d","",a.upper()) for a in aroganam[:]]
    note_index = aroganam_copy.index(note.upper())
    #print('get_next_note','note index in aroganam',note.upper(),carnatic_note, note_index,'oct_str',oct_str)
    if note_index < len(aroganam)-note_step:
        if note.upper() == "N" and oct_str == ".":
            result = aroganam[note_step-1]
            #print('next note 1',result)
        else:
            result = aroganam[note_index+note_step]+oct_str
            #print('next note 1',result)
    return result
def get_aaroganam(raagam_index=None):
    """
        Get the aroganam for the specified raaga
        @param raagam_index: Index of raaga. See docs/help or get_raaaga_list for id and raaga_name
        @return: aroganam of the raaga as a list of note
    """
    if raagam_index==None:
        raagam_index=settings.RAAGA_INDEX
    aroganam = _get_raaga_attribute("Aroganam",raagam_index)
    return aroganam.split()
def get_avaroganam(raagam_index=None):
    """
        Get the avaroganam for the specified raaga
        @param raagam_index: Index of raaga. See docs/help or get_raaaga_list for id and raaga_name
        @return: avaroganam of the raaga as a list of note
    """
    if raagam_index==None:
        raagam_index=settings.RAAGA_INDEX

    return _get_raaga_attribute("Avaroganam",raagam_index).split()
def is_sampoorna(raagam_index=None):
    """
        Returns whether the raaga is sampoorna (All 8 notes present in arogana/avarogana of the rraaga)
        @param raagam_index: Index of raaga. See docs/help or get_raaaga_list for id and raaga_name
        @return: True / False
    """
    if raagam_index==None:
        raagam_index=settings.RAAGA_INDEX
    return _get_raaga_attribute("Arohanam Note Count",raagam_index) == 8 and _get_raaga_attribute("Avarohanam Note Count",raagam_index) == 8
def is_janya(raagam_index=settings.RAAGA_INDEX):
    """
        Returns whether the raaga is Janya
        @param raagam_index: Index of raaga. See docs/help or get_raaaga_list for id and raaga_name
        @return: True / False
    """
    return "Janya" in _get_raaga_attribute("Melakartha_or_Janya",raagam_index)
def is_meLakartha(raagam_index=None):
    """
        Returns whether the raaga is meLakartha
        @param raagam_index: Index of raaga. See docs/help or get_raaaga_list for id and raaga_name
        @return: True / False
    """
    if raagam_index==None:
        raagam_index=settings.RAAGA_INDEX
    return raagam_index in settings.MELAKARTHA_DICT
def get_janya_raagas(raagam_index=None):
    """
        Returns list of janya raagas of the specified raagam
        @param raagam_index: Index of raaga. See docs/help or get_raaaga_list for id and raaga_name
        @return: list of id and names of janya raagas of specified raaga
    """
    if raagam_index==None:
        raagam_index=settings.RAAGA_INDEX
    janya_str = "Janya of MK-"+str(_get_raaga_attribute('mELakartha',raagam_index))
    janya_list = _search_raaga_for_values("Melakartha_or_Janya",janya_str)
    return janya_list
def search_for_raaga_by_name(search_str,is_exact=False):
    """
        Search for a raaga by full or partial name
        @param search_str: Full or partial name of the raagam. Example "hamsa" or "mohanam" (cae insensitive)
        @param is_exact: True if full name is specified. False otherwise
        @return: list of [raaga_id, raaga_name] that match specified search string in raaga names 
    """
    search_key = "Name"
    return _search_raaga_for_values(search_key, search_str, is_exact)
def search_for_raaga_by_attributes(attribute_value_dictionary,is_exact=False):
    """
        Search for raaga using its attributes - see raaga_list for attributes
        Example you can search for melakartha raaga as follows
            search_for_raaga_by_attributes({'Melakartha_or_Janya':"mELakartha-"},False)
        @param attribute_value_dictionary: dictionary of attributes and values
        @param is_exact: True if full name is specified. False otherwise
        @return: list of [raaga_id, raaga_name] that match specified attribute dictionary
    """
    results = []
    found = True
    for attr, attr_value in attribute_value_dictionary.items():
        results = _search_raaga_for_values(attr,attr_value,is_exact)
        found  = found and  len(results) > 0
    return results
def get_raaga_name(raagam_index=None):
    """
        Get raaga name of the specified raagam index
        @param raagam_index:ID of the raaga
        @return: raagam name 
    """
    if raagam_index==None:
        raagam_index=settings.RAAGA_INDEX
    return _get_raaga_attribute("Name",raagam_index)
def get_raasi(raagam_index=None):
    """
        Get raasi of the specified raagam index
        @param raagam_index:ID of the raaga
        @return: raasi
    """
    if raagam_index==None:
        raagam_index=settings.RAAGA_INDEX
    return _get_raaga_attribute("Raasi",raagam_index)
def get_parent_raaga(raagam_index=None):
    """
        Get ID and name of parent raaga
        @param raagam_index:ID of the raaga
        @return: [parent_raaga_id, parent_raga_name] 
    """
    if raagam_index==None:
        raagam_index=settings.RAAGA_INDEX
    melakartha_number = get_melakartha(raagam_index)
    filter_options = {'mELakartha' : str(melakartha_number), 'Melakartha_or_Janya':"mELakartha-"+str(melakartha_number)}
    parent_raaga_id, parent_raga_name = search_for_raaga_by_attributes(filter_options)[0]
    return parent_raaga_id, parent_raga_name
def get_raaga_list():
    """
        Get list of raaga names
        V0.7.6 @param removed from comment
        @return: [raaga_names] 
    """
    return settings.RAAGA_NAMES
def set_raagam(raagam):
    """
        set default raagam by name
        @param raagam: Full name of the raagam to be set as default
    """
    if not raagam.upper() in (name.upper() for name in settings.RAAGA_NAMES):
        raise ValueError(raagam,'not in supported raagas. Use get_raaga_list() for the list.')
    raaga_id = search_for_raaga_by_name(raagam,is_exact=True)[0][0]
    #print('ragam search raaga id',raaga_id)
    set_default_raaga_id(raaga_id)
    return raaga_id
def get_default_raaga_id():
    """
        Get the id of the default of raaga
        @return: raaga_id 
    """
    return settings.RAAGA_INDEX
def set_default_raaga_id(raagam_index):
    """
        Set the id of the default of raaga
        @param raaga_id 
    """
    print("INFO:Setting raaga will change the melakartha to that of the raaga")
    raaga_dict_length = len(_RAAGA_DICT)
    if raagam_index >= raaga_dict_length:
        raise ValueError("Raaga ID should be in the range 0.."+str(raaga_dict_length))
    settings.RAAGA_INDEX = raagam_index
    melakartha_number = get_melakartha(raagam_index)
    settings.MELAKARTHA_INDEX = melakartha_number
    print('raagam index',raagam_index,'melakartha number',melakartha_number)
def get_melakartha(raagam_index=None):
    """
        get the meLakartha number of the specified raaga
        @param raagam_index:
        @return: meLakartha number of the specified raagam 
    """
    if raagam_index==None:
        raagam_index=settings.RAAGA_INDEX
    return _get_raaga_attribute('mELakartha',raagam_index)
def set_melakartha(melakartha_number,change_raaga_index=False):
    """
        Set the default meLakartha
        @param meLakartha_number: 
    """
    if settings.MELAKARTHA_INDEX == melakartha_number:
        return
    if melakartha_number < 1 or melakartha_number > 72:
        raise ValueError("Melakartha number should be in the range 1..72")
    settings.MELAKARTHA_INDEX = melakartha_number
    if change_raaga_index:
        settings.RAAGA_INDEX = settings.MELAKARTHA_DICT[melakartha_number-1][0]
        print("INFO:Setting melakartha will change the raaga to melakartha raaga:",settings.RAAGA_NAMES[settings.RAAGA_INDEX])
    else:
        print("INFO:RAAGA_INDEX WAS NOT CHANGED",'change_raaga_index=',change_raaga_index)

def get_melakartha_raagas():
    """
        Get list of melakartha raagas
        @return: [raaga_ids, raaga_names]
    """
    return settings.MELAKARTHA_DICT
def write_json_file_for_raaga(model_weights_folder=None, json_file=None,remove_digits_from_notes=True):
    if model_weights_folder==None:
        model_weights_folder = "../carnatic/model_weights/"
    if json_file==None:
        json_file = get_raaga_name()+"_corpus.json"
    aroganam = get_aaroganam()[0:-2]
    avaroganam = get_avaroganam()[1:]
    if remove_digits_from_notes:
        aroganam = re.sub("\\d",""," ".join(aroganam)).split()
        avaroganam = re.sub("\\d",""," ".join(avaroganam)).split()
    raaga_notes = aroganam + avaroganam
    upper_notes = [note+"^" for note in raaga_notes]
    lower_notes = [note+"." for note in raaga_notes]
    space_notes = [",", ";"]
    full_set_of_notes = sorted(list(set(raaga_notes+upper_notes+lower_notes+space_notes)))
    """ Write the unique notes list to JSON FILE """
    char_to_index = {ch: i for (i, ch) in enumerate(full_set_of_notes)}
    #print("Number of unique characters in our whole tunes database = {}".format(len(char_to_index)),"\n",char_to_index) #87
    import os, json
    with open(os.path.join(model_weights_folder, json_file), mode = "w") as f:
        json.dump(char_to_index, f)
                     
def get_krithis(raagam_index=None,has_mp3_link=True):
    if raagam_index==None:
        raagam_index=settings.RAAGA_INDEX
    krithi_ids = [int(k) for k in _get_raaga_attribute("Krithi_IDs",raagam_index).split(";")]
    k_dict = settings.KRITHI_DICT
    if has_mp3_link:
        krithi_ids = [int(k) for k in krithi_ids for _,_ in k_dict.items() if k_dict[int(k)]['MP3 Link'] != '']
    return krithi_ids
def get_raagas_that_have_krithis():
    krithi_raaga_names = {}
    raaga_names = settings.RAAGA_NAMES
    #print('raaga names',raaga_names)
    k_dict = settings.KRITHI_DICT
    for k,_ in k_dict.items():
        k_raaga = k_dict[k]['Raaga']
        if k_raaga in raaga_names:
            raagam_index = raaga_names.index(k_raaga)
            #print('k_raaga',k_raaga,'found')
            krithi_raaga_names[k_raaga] = raagam_index
    return krithi_raaga_names
if __name__ == '__main__':
    pass
    