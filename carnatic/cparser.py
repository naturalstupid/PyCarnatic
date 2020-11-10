"""
    Module for 
            - parsing notations file and generating SCAMP list of pitches, durations and instruments
"""
import numpy as np
from scamp import Envelope
import math
import re
import regex
from carnatic import settings, raaga, thaaLa, cplayer

_NOTES_PATTERN_1 = settings._NOTES_PATTERN_1 # "(([SsPp]|[RrGgMmDdNn][1-4]?)([\\.\\'^]?)([</!~>]?[1-5]?))"
_NOTES_PATTERN = settings._NOTES_PATTERN # "([SsRrGgMmPpDdNn,;\(\)/!][1-4]?[\\.\\'^]?[<~>]?[1-5]?)"
_COMMENT_PATTERN = settings._COMMENT_PATTERN # r"^\s*\{(?P<comment>.*)"
_COMMAND_PATTERN = settings._COMMAND_PATTERN # r"^\s*#(?P<cmd_key>[DIJMNPST])(?P<cmd_value>\d+)"
_SILENT_PATTERN = settings._SILENT_PATTERN
_DIRECTION_PATTERN = settings._DIRECTION_PATTERN # r"^\s*(?P<dir_key>[UD])(?P<dir_value>.*)"
_RE_DICT = {
    'comment': re.compile(_COMMENT_PATTERN),
    'command':re.compile(_COMMAND_PATTERN),
    #'silent':re.compile(_SILENT_PATTERN),
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
        settings.THAALAM_SPEED = cmd_value
    elif cmd_key == "T":
        settings.THAALA_INDEX = cmd_value
    elif cmd_key == "[":
        if cmd_value.isdigit():
            settings.THAALAM_SPEED = cmd_value
        else:
            settings.THAALAM_SPEED = 0 ## Mean do not play percussion
        print("thaaLam Speed set to", settings.THAALAM_SPEED)
    elif cmd_key == "]":
        if settings.THAALAM_SPEED == 0:
            settings.THAALAM_SPEED = 1
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
        elif c=="," or c == ";":
            c_note_arr.append(c)
            result += c
        elif c=="." or c == "'" or c =="^" and c_note_arr[-1][-1] != c:
            c_note_arr[-1] += c
            result += c
        else:
            result += c
    return result,c_note_arr   
def _get_notes_from_file(notations_file):
    c_note_arr =[]
    with open(notations_file,"r") as file_object:
        line = file_object.readline()
        while line:
            key, match = _parse_line(line)
            if key == "car_notes":
                notes = regex.findall(_NOTES_PATTERN, line)
                c_note_arr += notes
            line = file_object.readline()
    file_object.close()
    return c_note_arr
def parse_file(file_name,arrange_notes_to_speed_and_thaaLa = True):
    """
        To parse a notation file and generate SCAAMP list
        @param    file_name: Notations file - see help for notation syntax
        @param    arrange_notes_to_speed_and_thaaLa    True the notations generated will be fit to speed and thaaLa
        @return:  file_carnatic_note_array     SCAMP notes list [ "Carnatic Note", ["Instrument", Volume_float, Duration_float], ...]
        @return:  result lines of notations
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
                #"""
                #rint('inside comment carnatic note counter',carnatic_note_counter,comment)
                if carnatic_note_counter >0:
                    if arrange_notes_to_speed_and_thaaLa:
                        arranged_notes = _arrange_notes_to_thaaLa(carnatic_note_array)
                        result += arranged_notes
                        result = result.strip()
                    carnatic_note_array = _get_note_frequency_duration(carnatic_note_array)
                    file_carnatic_note_array += carnatic_note_array[:]
                    carnatic_note_array.clear()
                    carnatic_note_counter = 0
                #"""
                if "Raagam:" in line or "Ragam:" in line:
                    i = line.index(":")+1
                    raagam=line[i:].strip()
                    raaga_id = raaga.search_for_raaga_by_name(raagam)[0][0]
                    raaga.set_default_raaga_id(raaga_id)
                    print('Raagam set to :',raagam,raaga_id)
                result += "\n" + line
            elif key == "command":
                if carnatic_note_counter >0:
                    if arrange_notes_to_speed_and_thaaLa:
                        arranged_notes = _arrange_notes_to_thaaLa(carnatic_note_array)
                        result += arranged_notes
                        result = result.strip()
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
                result +=  line 
            elif key=="dirn":
                dir_key = match.group("dir_key")
                dir_value = match.group("dir_value")
                if arrange_notes_to_speed_and_thaaLa:
                    dir_value = dir_value.replace("|","")
                carnatic_notes,c_note_arr = _parse_UD_digits(dir_key+dir_value)#,raaga_index)
                carnatic_note_array = carnatic_note_array+c_note_arr
                carnatic_note_counter += len(c_note_arr)
                if not arrange_notes_to_speed_and_thaaLa:
                    result+= carnatic_notes
                result = result.strip()
                #result += carnatic_notes
            elif key == "car_notes":
                c_note_arr = regex.findall(_NOTES_PATTERN, line)
                carnatic_note_array = carnatic_note_array+c_note_arr
                carnatic_note_counter += len(c_note_arr)
            """
            elif key == "silent":
                silent_note_arr = regex.findall(_SILENT_PATTERN, line)
                carnatic_note_array = carnatic_note_array+silent_note_arr
                carnatic_note_counter += len(silent_note_arr)
                #print("Processing silent note",silent_note_arr)
            """
            line = file_object.readline()
        if carnatic_note_counter >0:
            if arrange_notes_to_speed_and_thaaLa:
                arranged_notes = _arrange_notes_to_thaaLa(carnatic_note_array)
                result += arranged_notes
                result = result.strip()
            carnatic_note_array = _get_note_frequency_duration(carnatic_note_array)
            file_carnatic_note_array += carnatic_note_array[:]
            carnatic_note_array.clear()
            carnatic_note_counter = 0
    file_object.close()
    result = result.replace("||", "||\n")
    return file_carnatic_note_array,result
def _arrange_notes_to_thaaLa(note_array, play_speed=settings.PLAY_SPEED):
    note_count = 0
    thaaLa_count = 0
    s = 0
    speed = 2 ** (play_speed-1)
    thaaLa_loc = thaaLa.get_thaaLa_positions()
    thaaLa_length = int(list(thaaLa_loc)[len(thaaLa_loc)-1])*speed
    #print('thaaLa_loc',thaaLa_loc,len(thaaLa_loc),thaaLa_length)
    thaaLa_loc_inc = 0
    result = '\n'
    for n,note in enumerate(note_array):
        key = int(list(thaaLa_loc)[thaaLa_loc_inc])*speed
        value = list(thaaLa_loc.values())[thaaLa_loc_inc]
        thaaLa_count += 1
        result += note
        if note == ";":
            #print("; thaaLa_count incremented")
            thaaLa_count += 1
        if thaaLa_count == thaaLa_length:
            #print('thaal end reached')
            result += " " + value + " "
            thaaLa_count = 0
            thaaLa_loc_inc = 0
        elif thaaLa_count == key:
            #print('thaala pos reached')
            result += " " + value + " "
            thaaLa_loc_inc += 1
        if thaaLa_count % speed ==0:
            #print('speed reached',thaaLa_count,speed)
            result += " "
        #print(n,note,thaaLa_count,key,value,thaaLa_loc_inc,result)
        #result = re.sub(r'\n\s*\n', '\n\n', result)
    return result
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
def _get_midi_note_number(midi_note):
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
    note_number = (base_note_number + fractional_note)
    return note_number
def _split_carnatic_note_to_parts(carnatic_note):
    p = re.compile(_NOTES_PATTERN_1)
    m = p.match(carnatic_note)
    m1 = m.groups()
    #print('pattern groups',m1)
    note = m1[1]
    oct_str = m1[2]
    pitch_str = ''
    if m1[3] != '':
        pitch_str = m1[3][0]
    return m1[1],m1[2],m1[3]
def _get_midi_note(carnatic_note):
    note,oct_str,pitch_str = _split_carnatic_note_to_parts(carnatic_note)
    instrument_base_note = settings.INSTRUMENT_BASE_NOTES[settings.INSTRUMENT_INDEX]
    octave = int(instrument_base_note[-1]) #settings.BASE_OCTAVE
    #print(instrument_base_note, octave)
    if oct_str.strip() == ".":
        octave += -1
    elif oct_str.strip() == "'" or oct_str.strip() == "^":
        octave += 1
    midi_note = _get_western_note(note)
    midi_note = re.sub("\d",str(octave),midi_note)
    midi_note_number = _get_midi_note_number(midi_note)
    #print(carnatic_note,'groups',note,oct_str,pitch_str,micro_pitch,midi_note_number)
    return midi_note_number
def _get_microtone_pitch(carnatic_note):
    pitch_no = 0.0
    micro_tone_pitch = 0.0
    if carnatic_note[-1].isdigit():
        pitch_no = int(carnatic_note[-1])*settings._MICROTONE_PITCH_INCREMENT
    note = carnatic_note[:]
    #note_s = re.sub("\d","",note)
    #note_s = re.sub("[><]","",note_s)
    note_freq = _get_midi_note(carnatic_note)
    if ">" in carnatic_note:
        next_note = raaga.get_next_note(note)
        #print('next_note',next_note,note_s)
        next_note_freq = _get_midi_note(next_note)
        micro_tone_pitch = pitch_no * (next_note_freq - note_freq)
        #print(note_freq,next_note_freq,micro_tone_pitch)
    elif "<" in carnatic_note:
        previous_note = raaga.get_previous_note(note)
        #print('prev_note',previous_note,note_s)
        previous_note_freq = _get_midi_note(previous_note)
        micro_tone_pitch = -1.0 * pitch_no * (note_freq-previous_note_freq)
        #print(previous_note_freq,note_freq,micro_tone_pitch)
    micro_tone_pitch = note_freq + micro_tone_pitch
    #print(carnatic_note,micro_tone_pitch)
    return micro_tone_pitch
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
            #"""
            if "~" in note:
                kampitam_note_increment = 1
                if note[-1].isdigit():
                    kampitam_note_increment = int(note[-1])
                note = note.split("~")[0]
                freq = _kampitam(note, kampitam_note_increment)
                if freq == None:
                    freq = _get_microtone_pitch(note)
            else:
                freq = _get_microtone_pitch(note) # _get_midi_note(note)
            #"""
            #freq = _get_midi_note(note)
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
            if result:
                #print("Last note",result[-1],'duration',durn)
                durn = duration / ( ( 2 ** (speed-1) ) *1.0 )
                result[-1][1][-1] += 2 * durn # Add duration to last nore
        elif note.strip() == "/" or note.strip() == "!":
            #print("glide note set to True")
            glide_next_note =True
        """
        elif note.strip() == "$":
            inst = "silent"
            freq = 60.0
            durn = duration / ( ( 2 ** (speed-1) ) *1.0 )
            res_arr = [note,[inst,freq,durn]]
            result.append(res_arr)
        """
    return result
def _kampitam(note, kampitam_note_increment=1,pitch_step=settings._KAMPITAM_NOTE_STEP):
    invalid_end_note = "S." in note.upper()
    invalid_end_note = invalid_end_note or ("N" in note.upper() and ("'" in note or "^" in note))
    #print(note,invalid_end_note)
    if invalid_end_note:
        return None
    pitch = _get_midi_note(note)
    previous_note = raaga.get_previous_note(note,kampitam_note_increment)
    next_note = raaga.get_next_note(note,kampitam_note_increment)
    pitch_low = _get_midi_note(previous_note)
    pitch_high = _get_midi_note(next_note)
    #print('kampitam',previous_note,pitch_low,note,pitch,next_note,pitch_high)
    return _shake(pitch_low,pitch_high)
def _shake(pitch_low,pitch_high,pitch_step=settings._KAMPITAM_NOTE_STEP):
    result = []
    while pitch_high > pitch_low:
        pitch = list(np.arange(pitch_low,pitch_high,pitch_step))
        result += pitch
        #print('up',result)
        pitch = list(np.arange(pitch_high,pitch_low,-pitch_step))
        result += pitch
        #print('down',result)
        pitch_high -= 1.0
    #print('result',result)
    env = Envelope.from_levels(result)
    return env
def total_duration(final_note_list):
    """
        To compute total duration from the SCAMP note list supplied
        @param final_note_list: SCAMP notes list [ "Carntic Note", ["Instrument", "Volume", "Duration"], ...]
        @return: total duration
    """
    sum = 0.0
    for note in final_note_list:
        [_,[_,_,durn]] = note
        sum += durn
    return sum
def parse_solkattu(solkattu_list):
    """
        To parse solkattu phrases of percussion instrument and  generate SCAAMP list
        @param    solkattu_list
        @param    arrange_notes_to_speed_and_thaaLa    True the notations generated will be fit to speed and thaaLa
        @return:  result     SCAMP notes list [ "Carnatic Note", ["Instrument", Volume_float, Duration_float], ...]
    """
    result = []
    speed = settings.THAALAM_SPEED
    """ TODO: To handle NADAI_INDEX and KALAI of THAALAM - and adjust duration """
    """ Duration for one avarthanam of notes and rhythm should be SAME """
    #if (settings.NADAI_INDEX > 0 ):
    #    speed = 1
    duration = settings._FULL_NOTE_DURATION # / ( ( 2 ** (speed-1) ) *1.0 )
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
            durn = duration / ( ( 2 ** (speed-1) ) *1.0) / settings.jaathi_no[settings.NADAI_INDEX]
            inst = settings.CURRENT_PERCUSSION_INSTRUMENT
            if sol.strip() == ",":
                inst = "silent"
            elif sol.strip() == ";":
                inst = "silent"
                durn = durn * 2.0
            res_arr = [sol,[inst,freq,durn]]
            result.append(res_arr)
    return result
                
if __name__ == '__main__':
    """
    
    lesson_file = "../Notes/PancharathnaKrithi-jagadhaandhakaaraka.cmn"
    #lesson_file = "../Notes/vAtApi_Adhi_1.cmn"
    lesson_file = "../test_notes.inp"
    c_note_arr,result = parse_file(lesson_file,arrange_notes_to_speed_and_thaaLa = True)
    total_note_count_in_file = len(c_note_arr)
    total_duration_of_notes=total_duration(c_note_arr)
    print('c_note_arr',c_note_arr,'\n',total_duration_of_notes,'total note count',total_note_count_in_file)
    print(result)
    #print('f_di_i',f_d_i)
    #print(settings.DURATION, settings.THAALA_INDEX, settings.JAATHI_INDEX)
    exit()
    """