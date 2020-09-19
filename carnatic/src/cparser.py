"""
    Module for 
            - parsing notations file and generating SCAMP list of pitches, durations and instruments
"""
import math
import re
import regex
import settings
import raaga, thaaLa
import cplayer


_NOTES_PATTERN_1 = settings._NOTES_PATTERN_1 # "(([SsPp]|[RrGgMmDdNn][1-4]?)([\\.\\'^]?)([</!~>]?[1-5]?))"
_NOTES_PATTERN = settings._NOTES_PATTERN # "([SsRrGgMmPpDdNn,;\(\)/!][1-4]?[\\.\\'^]?[<~>]?[1-5]?)"
_COMMENT_PATTERN = settings._COMMENT_PATTERN # r"^\s*\{(?P<comment>.*)"
_COMMAND_PATTERN = settings._COMMAND_PATTERN # r"^\s*#(?P<cmd_key>[DIJMNPST])(?P<cmd_value>\d+)"
_DIRECTION_PATTERN = settings._DIRECTION_PATTERN # r"^\s*(?P<dir_key>[UD])(?P<dir_value>.*)"
_RE_DICT = {
    'comment': re.compile(_COMMENT_PATTERN),
    'command':re.compile(_COMMAND_PATTERN),
    'dirn':re.compile(_DIRECTION_PATTERN),
    "car_notes": re.compile(_NOTES_PATTERN + ".*")
    }
global carnatic_note_counter, carnatic_note_array, file_carnatic_note_array, glide_next_note
carnatic_note_counter = 0
carnatic_note_array = []
file_carnatic_note_array=[]
glide_next_note = False

def _parse_commands(cmd_key, cmd_value):
    if cmd_value =="" or not cmd_value.isdigit():
        raise ValueError("Command argument for",cmd_key,"should be a number")
    cmd_key = cmd_key.upper()
    cmd_value = int(cmd_value.strip())
    if cmd_key == "D":
        settings.TEMPO = cmd_value
    elif cmd_key == "I":
        inst_list = list(settings._CARNATIC_INSTRUMENTS+settings._DEFAULT_INSTRUMENTS)
        if cmd_value >= len(inst_list):
            raise ValueError("Instrument index should be less than",len(inst_list))
        settings.CURRENT_INSTRUMENT = inst_list[cmd_value]
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
    for key, rx in _RE_DICT.items():
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
    """
        To parse a notation file and generate SCAAMP list
        :param:    file_name: Notations file - see help for notation syntax
        :param:    fit_notes_to_speed_and_thaaLa    True the notations generated will be fit to speed and thaaLa
        :return:   file_carnatic_note_array     SCAMP notes list [ "Carntic Note", ["Instrument", "Volume", "Duration"], ...]
        :return:   result lines of notations
    """
    global carnatic_note_counter, carnatic_note_array, file_carnatic_note_array
    global glide_next_note
    """ Reset Speed to 1 """
    settings.PLAY_SPEED = 1
    #print('parse_file','settings.THAALA_INDEX',settings.THAALA_INDEX,'settings.JAATHI_INDEX',settings.JAATHI_INDEX)
    #print('parse_file','thaaLa_index, jaathi_index',thaaLa_index, jaathi_index)
    result = ''
    carnatic_note_counter = 0
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
                    raaga.set_default_raaga_id(raaga_id)
                    print('Raagam set to :',raagam,raaga_id)
                result += line
            elif key == "command":
                if carnatic_note_counter >0:
                    carnatic_note_array = _get_note_frequency_duration(carnatic_note_array)
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
                c_note_arr = _parse_notes(line,fit_notes_to_speed_and_thaaLa=False)#,thaaLa_index, jaathi_index))
                carnatic_note_array = carnatic_note_array+c_note_arr
                carnatic_note_counter += len(c_note_arr)
                car_notes = '\t\t'.join(_parse_notes(line,fit_notes_to_speed_and_thaaLa))
                result += car_notes
            line = file_object.readline()
            if result != "" and (key=="dirn" or key=="car_notes"):
                result += "\n"
        if carnatic_note_counter >0:
            carnatic_note_array = _get_note_frequency_duration(carnatic_note_array)
            file_carnatic_note_array += carnatic_note_array[:]
            carnatic_note_array.clear()
            carnatic_note_counter = 0
    file_object.close()
    return file_carnatic_note_array,result
def _parse_notes(line,fit_notes_to_speed_and_thaaLa=False):#,thaaLa_index=settings.THAALA_INDEX, jaathi_index=settings.JAATHI_INDEX):
    #print('_parse_notes','settings.THAALA_INDEX',settings.THAALA_INDEX,'settings.JAATHI_INDEX',settings.JAATHI_INDEX)
    #print('_parse_notes','thaaLa_index, jaathi_index',thaaLa_index, jaathi_index)
    notes_string = regex.findall(_NOTES_PATTERN, line)
    #print('notes before',notes_string)
    if fit_notes_to_speed_and_thaaLa:
        result = _parse_notes_to_thaala(notes_string)#,thaaLa_index, jaathi_index)
        #print('notes',result)
        return result
    else:
        return notes_string

def _get_western_note(carnatic_note):
    cNote = carnatic_note.replace("'","^")
    cNote = cNote.replace(".","").upper()
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
def _w_index_mk(carnatic_note, melakartha_number):
    result = -1
    mk = int(melakartha_number)
    cn = re.sub("\d","",carnatic_note).strip().upper()
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
            result = settings.CARNATIC_NOTES_LIST_16.index("M1")
    #result = WEST_MIDI_NOTES[result]
    return result
def _get_midi_note_number(midi_note, micro_tone_factor = 0.0):
    is_carnatic_note=(settings.CURRENT_INSTRUMENT in settings._DEFAULT_INSTRUMENTS)
    octave = int(midi_note[-1])
    note = midi_note[0:-1]
    instrument_base_note = settings.INSTRUMENT_BASE_NOTES[settings.INSTRUMENT_INDEX][:-1]
    kattai_index = settings.WEST_MIDI_NOTES_LIST_12.index(instrument_base_note)
    #base_note_number = kattai_index + (octave+1)*12
    """ TODO: TO MATCH JFUGUE octave+1 changed to octave """
    base_note_number = kattai_index + (octave+1)*12
    if is_carnatic_note:
        fractional_note = 12.0 * math.log2(settings.C12_FREQ_RATIO[settings.WEST_MIDI_NOTES_LIST_12.index(note)])
    else:
        fractional_note = settings.WEST_MIDI_NOTES_LIST_12.index(note)
    note_number = (base_note_number + fractional_note) * (1+micro_tone_factor)
    """
    if is_carnatic_note:
        note_number = kattai_index + (octave+1)*12 + (settings.C16_FREQ_RATIO[settings.WEST_MIDI_NOTES_LIST_16.index(note)] - 1.0)*12*(1+micro_tone_factor)
    else:
        note_number = kattai_index + (octave+1)*12 + settings.WEST_MIDI_NOTES_LIST_12.index(note)*(1+micro_tone_factor)
    """
    return note_number
def _get_midi_note(carnatic_note):
    p = re.compile(_NOTES_PATTERN_1)
    m = p.match(carnatic_note)
    m1 = m.groups()
    #print('pattern groups',m1)
    note = m1[1]
    oct_str = m1[2]
    pitch_str = ''
    if m1[3] != '':
        pitch_str = m1[3][0]
    instrument_base_note = settings.INSTRUMENT_BASE_NOTES[settings.INSTRUMENT_INDEX]
    octave = int(instrument_base_note[-1]) #settings.BASE_OCTAVE
    #print(instrument_base_note, octave)
    if oct_str.strip() == ".":
        octave += -1
    elif oct_str.strip() == "'" or oct_str.strip() == "^":
        octave += 1
    micro_pitch = 0.0
    glide=False
    if pitch_str == ">":
        micro_pitch += int(carnatic_note[-1])*0.1
    elif pitch_str == "<":
        micro_pitch -= int(carnatic_note[-1])*0.1
    midi_note = _get_western_note(note)
    midi_note = re.sub("\d",str(octave),midi_note)
    midi_note_number = _get_midi_note_number(midi_note,micro_tone_factor=micro_pitch)
    #print(carnatic_note,'groups',note,oct_str,pitch_str,micro_pitch,midi_note_number)
    return midi_note_number
def _group_notes_by_speed(notes_list, speed):
    results = []
    for i in range(0, len(notes_list), speed):
        results.append(''.join(notes_list[i:i+speed]))
    return results
def _parse_notes_to_thaala(note_string):#, thaaLa_index=settings.THAALA_INDEX, jaathi_index=settings.JAATHI_INDEX):
    #print('parse_notes_to_thaala','settings.THAALA_INDEX',settings.THAALA_INDEX,'settings.JAATHI_INDEX',settings.JAATHI_INDEX)
    #print('parse_notes_to_thaala','thaaLa_index',thaaLa_index,'jaathi_index',jaathi_index)
    result = note_string[:]
    speed = 2 ** (settings.PLAY_SPEED-1)
    if speed > 1:
        result = _group_notes_by_speed(result, speed)
    note_len = len(result)
    thaaLa_pos = thaaLa.get_thaaLa_positions()#thaaLa_index, jaathi_index)
    key_len = len(thaaLa_pos)
    thaaLa_len = list(thaaLa_pos.keys())[-1]
    #print('parse_notes_to_thaala','thaaLa_index, jaathi_index',thaaLa_index, jaathi_index,thaaLa_pos)
    #print(thaaLa_pos,key_len, thaaLa_len)
    k = 1
    n = 1
    i = 0
    for ip,c in enumerate(result):
        #print('ip',ip,'c',c)
        key = int(list(thaaLa_pos)[k-1])
        value = list(thaaLa_pos.values())[k-1]
        #print(n, k, key)
        if (n == key):
            result.insert(ip+1+i,value )
            #print(value,'inserted after',ip+1+i,result[:ip+1+i+1])
            k += 1
            i += 1
            if (k > key_len):
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
    return result
def _get_note_frequency_duration(note_array):
    #print('note_array',note_array)
    global glide_next_note
    result = []
    speed = settings.PLAY_SPEED
    duration = settings._FULL_NOTE_DURATION# / ( ( 2 ** (speed-1) ) *1.0 )
    #print("Duration",duration)
    for i,note in enumerate(note_array):
        res_arr = []
        if (re.match(_NOTES_PATTERN_1,note)):
            freq = _get_midi_note(note)
            durn = duration / ( ( 2 ** (speed-1) ) *1.0 ) 
            inst = settings.CURRENT_INSTRUMENT
            res_arr = [note,[inst,freq,durn]]
            result.append(res_arr)
            #print(note,'glide_next_note',glide_next_note)
            if glide_next_note:
                last_note_freq = result[-2][1][1]
                result[-2][1][1] = [last_note_freq,freq]
                #print("glide note set to False")
                glide_next_note = False
        elif note.strip() == "(":
            speed += 1
            #print('Speed increased to',speed)
        elif note.strip() == ")":
            speed -= 1
            #print('Speed decreased to',speed)
        elif note.strip() == ",":
            #print("Last note",result[-1],'duration',durn)
            durn = duration / ( ( 2 ** (speed-1) ) *1.0 )
            result[-1][1][-1] += durn # Add duration to last nore
        elif note.strip() == ";":
            #print("Last note",result[-1],'duration',durn)
            durn = duration / ( ( 2 ** (speed-1) ) *1.0 )
            result[-1][1][-1] += 2 * durn # Add duration to last nore
        elif note.strip() == "/" or note.strip() == "!":
            #print("glide note set to True")
            glide_next_note =True
        #print('note',note,res_arr)
    return result
def total_duration(final_note_list):
    sum = 0.0
    for note in final_note_list:
        [_,[_,_,durn]] = note
        sum += durn
    return sum
def parse_solkattu(solkattu_list):
    """
        To parse solkattu phrases of percussion instrument and  generate SCAAMP list
        :param:    solkattu_list
        :param:    fit_notes_to_speed_and_thaaLa    True the notations generated will be fit to speed and thaaLa
        :return:   result     SCAMP notes list [ "Carntic Note", ["Instrument", "Volume", "Duration"], ...]
    """
    result = []
    speed = settings.PLAY_SPEED
    duration = settings._FULL_NOTE_DURATION# / ( ( 2 ** (speed-1) ) *1.0 )
    for tp in solkattu_list:
        for sol in tp:
            if sol.strip() == '':
                continue
            elif sol.strip() == "(":
                speed += 1
                continue
            elif sol.strip() == ")":
                speed -= 1
                continue
            sol_index = settings._SOLKATTU_LIST.index(sol.lower())
            midi_note = settings._RHYTHM_NOTE_LIST[sol_index]
            freq = _get_midi_note_number(midi_note)
            #freq = _get_midi_note(note)
            durn = duration / ( ( 2 ** (speed-1) ) *1.0 ) 
            inst = settings.CURRENT_PERCUSSION_INSTRUMENT
            res_arr = [sol,[inst,freq,durn]]
            result.append(res_arr)
    return result
                
if __name__ == '__main__':
    """
    cn = ["S", "/" , "R", "/", "G", "M", "P", "D", "N", "S^"]
    mk = settings.MELAKARTHA_INDEX
    for c in cn:
        w_ind = _w_index_mk(c,mk)
        c_actual = settings.CARNATIC_NOTES_LIST_16[w_ind]
        f = _get_note_frequency_duration(c)
        print(c,w_ind,c_actual,f)
    exit()
    print(cn,_get_note_frequency_duration(cn))
    exit()
    """
    #"""
    lesson_file = "../Notes/PancharathnaKrithi-jagadhaandhakaaraka.cmn"
    #lesson_file = "../Notes/vAtApi_Adhi_1.cmn"
    c_note_arr,result = parse_file(lesson_file,fit_notes_to_speed_and_thaaLa = True)
    total_note_count_in_file = len(c_note_arr)
    total_duration_of_notes=total_duration(c_note_arr)
    print('c_note_arr',c_note_arr,'\n',total_duration_of_notes,'total note count',total_note_count_in_file)
    print(result)
    #print('f_di_i',f_d_i)
    #print(settings.DURATION, settings.THAALA_INDEX, settings.JAATHI_INDEX)
    exit()
    