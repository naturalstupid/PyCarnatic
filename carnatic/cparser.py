import re
import regex
import settings
import raaga, thaaLa

_NOTES_PATTERN = "([SsRrGgMmPpDdNn,;][1-4]?[\\.\\'^]?[</!~>]?[1-5]?)"
_COMMENT_PATTERN = r"^\s*\{(?P<comment>.*)"
_COMMAND_PATTERN = r"^\s*#(?P<cmd_key>[DIJMNPST])(?P<cmd_value>\d+)"
_DIRECTION_PATTERN = r"^\s*(?P<dir_key>[UD])(?P<dir_value>.*)"
RE_DICT = {
    'comment': re.compile(_COMMENT_PATTERN),
    'command':re.compile(_COMMAND_PATTERN),
    'dirn':re.compile(_DIRECTION_PATTERN),
    "car_notes": re.compile(_NOTES_PATTERN + ".*")
    }
global total_note_count_in_file, carnatic_note_counter, carnatic_note_array, file_carnatic_note_array
total_note_count_in_file = 0
carnatic_note_counter = 0
carnatic_note_array = []
file_carnatic_note_array=[]
def _get_midi_note_from_note_number(note_number):
    octave = int (note_number / 12) - 1;
    notes = "C C#D D#E F F#G G#A A#B "
    note = notes[(note_number % 12) * 2: (note_number % 12) * 2 + 2]
    return note.strip()+str(octave).strip()
def _parse_commands(cmd_key, cmd_value):
    if cmd_value =="" or not cmd_value.isdigit():
        raise ValueError("Command argument for",cmd_key,"should be a number")
    cmd_key = cmd_key.upper()
    cmd_value = int(cmd_value.strip())
    if cmd_key == "D":
        settings.DURATION = cmd_value
    elif cmd_key == "I":
        settings.INSTRUMENT_INDEX = cmd_value
    elif cmd_key == "J":
        settings.JAATHI_INDEX = cmd_value
        #print(cmd_value," JAATHI INDEX SET TO ",settings.JAATHI_INDEX)
    elif cmd_key == "M":
        #settings.MELAKARTHA_INDEX = cmd_value
        raaga.set_melakartha(cmd_value)
    elif cmd_key == "N":
        settings.SCALE_OF_NOTES = cmd_value
    elif cmd_key == "P":
        settings.PLAYER_MODE = cmd_value
    elif cmd_key == "S":
        settings.PLAY_SPEED = cmd_value
    elif cmd_key == "T":
        settings.THAALA_INDEX = cmd_value
        #print(cmd_value," THAALA INDEX SET TO ",settings.THAALA_INDEX)
    else:
        raise ValueError("Invalid command value:"+cmd_key+cmd_value)
    
def _parse_line(line):
    for key, rx in RE_DICT.items():
        match = rx.search(line)
        if match:
            return key, match
    # if there are no matches
    return None, None

def _parse_UD_digits(text):
    raaga_index = settings.RAAGA_INDEX
    result = ""
    c_note_arr = []
    up = False
    ci = 0
    for c in text:
        if c == "U":
            up = True
        elif c == "D":
            up = False
        elif c.isdigit():
            ci = int(c)
            if up:
                note = raaga.get_aroganam(raaga_index)[ci-1]
                result += note
                c_note_arr.append(note)
            else:
                note = raaga.get_avaroganam(raaga_index)[ci-1]
                result += note
                c_note_arr.append(note)
        else:
            result += c
    return result,c_note_arr   

def parse_file(file_name,fit_notes_to_speed_and_thaaLa = False):
    global total_note_count_in_file, carnatic_note_counter, carnatic_note_array, file_carnatic_note_array
    """
    if raaga_index==None:
        raaga_index=settings.RAAGA_INDEX
    if thaaLa_index==None:
        thaaLa_index=settings.THAALA_INDEX
    if jaathi_index==None:
        jaathi_index = settings.JAATHI_INDEX
    """
    #print('parse_file','settings.THAALA_INDEX',settings.THAALA_INDEX,'settings.JAATHI_INDEX',settings.JAATHI_INDEX)
    #print('parse_file','thaaLa_index, jaathi_index',thaaLa_index, jaathi_index)
    result = ''
    carnatic_note_counter = 0
    total_note_count_in_file = 0
    carnatic_note_array.clear()
    with open(file_name,"r") as file_object:
        line = file_object.readline()
        while line:
            key, match = _parse_line(line)
            if key == "comment":
                comment = match.group('comment')
                if "Raagam:" in line or "Ragam:" in line:
                    i = line.index(":")+1
                    raagam=line[i:].strip()
                    raaga_id = raaga.search_for_raaga_by_name(raagam)[0][0]
                    raaga.set_default_raaga(raaga_id)
                    print('Raagam set to :',raagam,raaga_id)
                result += line
            elif key == "command":
                if carnatic_note_counter >0:
                    total_note_count_in_file += len(carnatic_note_array)
                    result += '\t'.join(parse_notes_to_thaala())#thaaLa_index, jaathi_index))
                    file_carnatic_note_array += carnatic_note_array[:]
                    carnatic_note_array.clear()
                    carnatic_note_counter = 0
                cmd_key = match.group("cmd_key")
                cmd_value = match.group("cmd_value")
                _parse_commands(cmd_key, cmd_value)
                """ Update thaala, jaathi based on command values """
                if cmd_key == "T":
                    thaaLa_index=settings.THAALA_INDEX
                if cmd_key == "J":
                    jaathi_index = settings.JAATHI_INDEX
                result += line
            elif key=="dirn":
                dir_key = match.group("dir_key")
                dir_value = match.group("dir_value")
                carnatic_notes,c_note_arr = _parse_UD_digits(dir_key+dir_value)#,raaga_index)
                carnatic_note_array = carnatic_note_array+c_note_arr
                carnatic_note_counter += len(c_note_arr)
                #if fit_notes_to_speed_and_thaaLa:
                #    carnatic_notes = '\t'.join(_parse_notes(carnatic_notes,fit_notes_to_speed_and_thaaLa,thaaLa_index, jaathi_index))
                result = result.strip()
                #result += carnatic_notes
            elif key == "car_notes":
                c_note_arr = _parse_notes(line,fit_notes_to_speed_and_thaaLa)#,thaaLa_index, jaathi_index))
                carnatic_note_array = carnatic_note_array+c_note_arr
                carnatic_note_counter += len(c_note_arr)
                result = result.strip()
            line = file_object.readline()
            if result != "" and (key=="dirn" or key=="car_notes"):
                result += "\n"
        if carnatic_note_counter >0:
            total_note_count_in_file += len(carnatic_note_array)
            result += '\t'.join(parse_notes_to_thaala())#thaaLa_index, jaathi_index))
            file_carnatic_note_array += carnatic_note_array[:]
            carnatic_note_array.clear()
            carnatic_note_counter = 0
    file_object.close()
    return file_carnatic_note_array
def _parse_notes(line,fit_notes_to_speed_and_thaaLa=False):#,thaaLa_index=None, jaathi_index=None):
    thaaLa_index=settings.THAALA_INDEX
    jaathi_index = settings.JAATHI_INDEX
    #print('_parse_notes','settings.THAALA_INDEX',settings.THAALA_INDEX,'settings.JAATHI_INDEX',settings.JAATHI_INDEX)
    #print('_parse_notes','thaaLa_index, jaathi_index',thaaLa_index, jaathi_index)
    notes_string = regex.findall(_NOTES_PATTERN, line)
    return notes_string

def _get_western_note(carnatic_note):
    cNote = carnatic_note.replace("'","^")
    cNote = cNote.replace(".","")
    if cNote[0] == "S" or cNote[0] == "P" or bool(re.match("[RGMDN][1-4]",cNote)):
        wNote = settings.WEST_MIDI_NOTES_LIST_16[settings.CARNATIC_NOTES_LIST_16.index(cNote)]
    else:
        wNote = settings.WEST_MIDI_NOTES_LIST_16[_w_index_mk(cNote,settings.MELAKARTHA_INDEX)]
    if '.' in carnatic_note:
        octave = settings.BASE_OCTAVE - 1
    elif "'" in carnatic_note or "^" in carnatic_note:
        octave = settings.BASE_OCTAVE + 1
    else:
        octave = settings.BASE_OCTAVE
    midi_note = wNote.strip()+str(octave).strip()
    #print(carnatic_note,'=>',midi_note)
    return midi_note  
def _w_index(carnatic_note):
    if settings.SCALE_OF_NOTES == settings.CARNATIC_SCALE_12_NOTES and carnatic_note in settings.CARNATIC_NOTES_LIST_12:
        return settings.CARNATIC_NOTES_LIST_12.index(carnatic_note)
    elif settings.SCALE_OF_NOTES == settings.CARNATIC_SCALE_16_NOTES and carnatic_note in settings.CARNATIC_NOTES_LIST_16:
        return settings.CARNATIC_NOTES_LIST_16.index(carnatic_note)
    if settings.SCALE_OF_NOTES == settings.CARNATIC_SCALE_22_NOTES and carnatic_note in settings.CARNATIC_NOTES_LIST_22:
        return settings.CARNATIC_NOTES_LIST_22.index(carnatic_note)
    else:
        return -1    
def _w_index_mk(carnatic_note, melakartha_number):
    result = -1
    mk = int(melakartha_number)
    cn = re.sub("\d","",carnatic_note).strip()
    mainS = [[0,1],[1,2],[1,3],[2,2],[2,3],[3,3]]
    if(mk > 36):
        mk1 = mk - 36
    else:
        mk1 = mk
    mk2 = int(mk1 / 6)
    mk3 = int(mk1 - mk2*6)
    if(mk3 == 0):
        mk3 = 6
        mk2 = mk2 - 1
    ri = str(mainS[mk2][0])
    gi = str(mainS[mk2][1])
    di = str(mainS[mk3-1][0])
    ni = str(mainS[mk3-1][1])
    if cn[0].lower() == "s" or cn.lower() == "p":
        result = settings.CARNATIC_NOTES_LIST_16.index(cn)
    elif cn.lower() == "r":
        result = settings.CARNATIC_NOTES_LIST_16.index(cn+ri)
    elif cn.lower() == "g":
        result = settings.CARNATIC_NOTES_LIST_16.index(cn+gi)
    elif cn.lower() == "d":
        result = settings.CARNATIC_NOTES_LIST_16.index(cn+di)
    elif cn.lower() == "n":
        result = settings.CARNATIC_NOTES_LIST_16.index(cn+ni)
    elif cn.lower() == "m":
        if mk > 36:
            result = settings.CARNATIC_NOTES_LIST_16.index("M2")
        else:
            result = settings.CARNATIC_NOTES_LIST_16.index("M2")
    #result = WEST_MIDI_NOTES[result]
    return result
def _get_midi_note_number(midi_note):
    octave = int(midi_note[-1])
    note = midi_note[0:-1]
    #note_number = (octave+1)*12 + settings.WEST_MIDI_NOTES_LIST_12.index(note)
    note_number = (octave+1)*12 + (settings.C16_FREQ_RATIO[settings.WEST_MIDI_NOTES_LIST_16.index(note)] - 1.0)*12
    return note_number
def _get_midi_note(carnatic_note):
    car_index = settings.CARNATIC_NOTES_LIST_16.index(carnatic_note)
    octave = settings.BASE_OCTAVE
    if "." in carnatic_note:
        octave += -1
    elif "'" in carnatic_note or "^" in carnatic_note:
        octave += 1
    midi_note = _get_western_note(carnatic_note)
    midi_note = re.sub("\d",str(octave),midi_note)
    midi_note_number = _get_midi_note_number(midi_note)
    #print(carnatic_note,"=>",midi_note,"=>",midi_note_number)
    return midi_note_number
def _get_midi_notes(carntic_note_list):
    # remove thaala symbols
    new_list = [x for x in carntic_note_list  if x not in ["|","||\n"]]
    midi_notes = []
    _NOTES_PATTERN_1 = "(([SsPp]|[RrGgMmDdNn][1-4]?)([\\.\\'^]?)([</!~>]?[1-5]?))?"
    base_midi_note_number = _get_midi_note_number("C"+str(settings.BASE_OCTAVE))
    #print('inside _get_mid_notes',carntic_note_list, new_list)
    for note in new_list:
        p = re.compile(_NOTES_PATTERN_1)
        m = p.match(note)
        m1 = m.groups()
        #print(note,'groups',m1)
        if m1:
            base_note = m1[1]
            car_index = settings.CARNATIC_NOTES_LIST_16.index(base_note)
            octave_str = m1[2]
            octave = settings.BASE_OCTAVE
            if octave_str == ".":
                octave +=  - 1
            elif octave_str == "'" or octave_str == "^":
                octave +=  1
            midi_note = _get_western_note(base_note)
            midi_note = re.sub("\d",str(octave),midi_note)
            midi_note_number = _get_midi_note_number(midi_note)
            midi_notes.append(midi_note_number)
            #print('note',note,'midi note',midi_note,'midi note number', midi_note_number)
    return midi_notes 
def _group_notes_by_speed(notes_list, speed):
    results = []
    for i in range(0, len(notes_list), speed):
        results.append(''.join(notes_list[i:i+speed]))
    return results
def parse_notes_to_thaala():#thaaLa_index=None, jaathi_index=None):
    global total_note_count_in_file, carnatic_note_counter, carnatic_note_array, file_carnatic_note_array
    thaaLa_index=settings.THAALA_INDEX
    jaathi_index = settings.JAATHI_INDEX
    #print('parse_notes_to_thaala','settings.THAALA_INDEX',settings.THAALA_INDEX,'settings.JAATHI_INDEX',settings.JAATHI_INDEX)
    #print('parse_notes_to_thaala','thaaLa_index',thaaLa_index,'jaathi_index',jaathi_index)
    #result = carnatic_note_array[:]
    speed = 2 ** (settings.PLAY_SPEED-1)
    if speed > 1:
        carnatic_note_array = _group_notes_by_speed(carnatic_note_array, speed)
    note_len = len(carnatic_note_array)
    thaaLa_pos = thaaLa.get_thaaLa_positions(thaaLa_index, jaathi_index)
    #print('thaaLa_pos',thaaLa_index,jaathi_index,thaaLa_pos)
    key_len = len(thaaLa_pos)
    thaaLa_len = list(thaaLa_pos.keys())[-1]
    #print('parse_notes_to_thaala','thaaLa_index, jaathi_index',thaaLa_index, jaathi_index,thaaLa_pos)
    #print(thaaLa_pos,key_len, thaaLa_len)
    k = 1
    n = carnatic_note_counter+1 #1
    i = 0
    for ip,c in enumerate(carnatic_note_array):
        #print('ip',ip,'c',c)
        key = int(list(thaaLa_pos)[k-1])
        value = list(thaaLa_pos.values())[k-1]
        #print(n, k, key)
        if (n == key):
            carnatic_note_array.insert(ip+i,value )
            #print(value,'inserted after',ip+i,result[:ip+i+1])
            k += 1
            i += 1
            if (k > key_len):
                carnatic_note_array[ip+i-1]+="\n"
                #print('k reset at ip=',ip)
                k = 1
        n += 1
        if (n > thaaLa_len):
            #print('n reset at ip=',ip)
            n = 1
        if ip >= note_len:
            break
    #col_width = max(len(word) for row in note_string for word in row)  + 2  # padding
    #note_string = [word.ljust(col_width) for row in note_string for word in row]
    #print('result',result)
    return carnatic_note_array

if __name__ == '__main__':
    """
    settings.THAALA_INDEX = 4
    settings.JAATHI_INDEX = 2
    settings.PLAY_SPEED = 3
    print(settings.THAALA_INDEX, settings.JAATHI_INDEX, thaaLa.get_thaaLa_positions(settings.THAALA_INDEX, settings.JAATHI_INDEX))
    s =  ["S","R","G","M","P","D","N","S^","S","R","G","M","P","D","N","S^","S","R","G","M","P","D","N","S^","S","R","G","M","P","D","N","S^"]
    sp = parse_notes_to_thaala(s)
    print(s,"\n",sp)
    exit()
    tl = sp.index("||")+1
    sp1 = [sp[i:i + tl] for i in range(0, len(sp), tl)]
    sp2 = "\n".join(["\t\t".join(row) for row in sp1])
    print(sp1,"\n",sp2)
    exit()
    """
    """
    #settings.THAALA_INDEX = 2
    #settings.JAATHI_INDEX = 3
    #print('main','settings.THAALA_INDEX',settings.THAALA_INDEX,'settings.JAATHI_INDEX',settings.JAATHI_INDEX)
    print(parse_file("test_notes.inp",fit_notes_to_speed_and_thaaLa = True))#, thaaLa_index=settings.THAALA_INDEX, jaathi_index=settings.JAATHI_INDEX))
    #print(settings.DURATION, settings.THAALA_INDEX, settings.JAATHI_INDEX)
    exit()
    #"""
    """
    carnatic_note = ["G3"]
    print(carnatic_note, _w_index(carnatic_note),_w_index_mk(carnatic_note, settings.MELAKARTHA_INDEX),_get_midi_notes(carnatic_note))
    exit()
    """
    #"""
    #strng = ["S.", 'R3.', 'G3.', 'M2.',"|", 'P.', 'D3.',"|", 'N3.', "S","||\n","S", 'R3', 'G3', 'M2',"|", 'P', 'D3',"|", 'N3', "S'","||\n"]
    strng = ['S', 'R3', 'G3', 'M2', '|', 'P', 'D3', 'N3', 'S^', '|', 'S^', 'N3', '|', 'D3', 'P', '||\n', 'M2', 'G3', 'R3', 'S', '|', 'S', 'R3', 'G3', 'M2', '|', 'P', 'D3', '|', 'N3', 'S^', '||\n', 'S^', 'N3', 'D3', 'P', '|', 'M2', 'G3', 'R3', 'S', '|', 'S', 'R3', '|', 'G3', 'M2', '||\n', 'P', 'D3', 'N3', 'S^', '|', 'S^', 'N3', 'D3', 'P', '|', 'M2', 'G3', '|', 'R3', 'S', '||\n', 'S', 'R3', 'G3', 'M2', '|', 'P', 'D3', 'N3', 'S^', '|', 'S^', 'N3', '|', 'D3', 'P', '||\n', 'M2', 'G3', 'R3', 'S', '|', 'S', 'R3', 'G3', 'M2', '|', 'P', 'D3', '|', 'N3', 'S^', '||\n', 'S^', 'N3', 'D3', 'P', '|', 'M2', 'G3', 'R3', 'S', '|', 'S', 'R3', '|', 'G3', 'M2', '||\n', 'P', 'D3', 'N3', 'S^', '|', 'S^', 'N3', 'D3', 'P', '|', 'M2', 'G3', '|', 'R3', 'S', '||\n', 'SR3', 'G3M2', 'PD3', 'N3S^', '|', 'S^N3', 'D3P', 'M2G3', 'R3S', '|', 'SR3', 'G3M2', '|', 'PD3', 'N3S^', '||\n', 'S^N3', 'D3P', 'M2G3', 'R3S', '|', 'SR3', 'G3M2', 'PD3', 'N3S^', '|', 'S^N3', 'D3P', '|', 'M2G3', 'R3S', '||\n', 'SR3', 'G3M2', 'PD3', 'N3S^', '|', 'S^N3', 'D3P', 'M2G3', 'R3S', '|', 'SR3', 'G3M2', '|', 'PD3', 'N3S^', '||\n', 'S^N3', 'D3P', 'M2G3', 'R3S', '|', 'SR3', 'G3M2', 'PD3', 'N3S^', '|', 'S^N3', 'D3P', '|', 'M2G3', 'R3S', '||\n', 'SR3G3M2', 'PD3N3S^', 'S^N3D3P', 'M2G3R3S', '|', 'S^N3D3P', 'M2G3R3S', 'S^N3D3P', 'M2G3R3S', '|', 'SR3G3M2', 'PD3N3S^', '|', 'S^N3D3P', 'M2G3R3S', '||\n', 'S^N3D3P', 'M2G3R3S', 'S^N3D3P', 'M2G3R3S', '|', 'SR3G3M2', 'PD3N3S^', 'S^N3D3P', 'M2G3R3S', '|', 'S^N3D3P', 'M2G3R3S', '|', 'S^N3D3P', 'M2G3R3S', '||\n']
    #strng = ["S^"]
    midi_notes = _get_midi_notes(strng)
    print(strng, "\n",midi_notes)
    exit()
    