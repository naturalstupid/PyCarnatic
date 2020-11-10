"""
    Module for 
            - collecting carnatic instruments from soundfont and default midi instruments
            - playing notations from file or argument
        play_notes function will play notations returned by cparser.parse_file
        play_file function will gather notations from a file abd play
"""
import regex
import math
import sys
import warnings
from scamp import *
playback_settings.soundfont_search_paths.append("Lib/")
playback_settings.make_persistent()
from carnatic import settings, raaga, thaaLa, cparser

player=None
available_instruments = {}

def get_instrument_list(include_percussion_instruments=False):
    """
        Get list of available instruments
        @param include_percussion_instruments: True / False whether to include list of percussion instruments available
        @return: List of available instruments
    """
    instrument_list = settings._CARNATIC_INSTRUMENTS + settings._DEFAULT_INSTRUMENTS
    if include_percussion_instruments:
        instrument_list += settings._PERCUSSION_INSTRUMENTS
    return instrument_list
def _get_player():
    global available_instruments, player
    if player==None:
        print('setting player and instruments')
        available_instruments.clear()
        player = Session()# load default_soundfont
        for inst in settings._CARNATIC_INSTRUMENTS:
            available_instruments[inst] = player.new_part(inst,soundfont=settings._SOUND_FONT_FILE) 
        for inst in settings._DEFAULT_INSTRUMENTS:
            available_instruments[inst] = player.new_part(inst,soundfont="default") 
        for inst in settings._PERCUSSION_INSTRUMENTS:
            available_instruments[inst] = player.new_part(inst,soundfont=settings._SOUND_FONT_FILE) 
        #available_instruments["silent"] = player.new_silent_part("silent")
    return player
def _get_instrument(instrument_name):
    global available_instruments,player
    player = _get_player()
    if available_instruments:
        if instrument_name in get_instrument_list():
            return available_instruments[instrument_name]
    return None
def set_instrument(instrument_name):
    """
        Set default instrument
        @param instrument_name: Name of the instrument
    """
    instruments = get_instrument_list()
    if instrument_name in instruments:
        inst_index = instruments.index(instrument_name)
        settings.INSTRUMENT_INDEX = inst_index
        settings.CURRENT_INSTRUMENT = instrument_name
def __play_notes(scamp_note_list):
    global available_instruments, player
    if player==None:
        player = _get_player()
    player.tempo = settings.TEMPO
    for item in scamp_note_list:
        note = item[0]
        instrument, pitch,durn = item[1]
        inst = available_instruments[instrument]
        #print(note,inst,instrument,pitch,durn)
        inst.play_note(pitch, settings._VOLUME, durn)    

def play_notes(scamp_note_list,include_percussion_layer=False):
    """
        To play notes
        @param scamp_note_list            SCAMP notes list [ "Carnatic Note", ["Instrument", Volume_float, Duration_float], ...]
                                            notes list can be obtained from cparser.parser_file function
        @param include_percussion_layer    True: Includes Percussion according to the set ThaaLam and Jaathi
                                            ThaaLam and Jaathi can be set using thaaLa.set_thaaLam(thaaLam_Name, Jaathi_Name) 
                                            or using thaaLam.set_thaaLam_index(thaaLam_index, jaathi_index)
    """
    global player
    if player==None:
        player = _get_player()
    player.tempo = settings.TEMPO
    if include_percussion_layer and settings.THAALAM_SPEED > 0:
        duration = cparser.total_duration(scamp_note_list)
        #thaaLa_speed = ((2**(settings.THAALAM_SPEED-1)) - 1) 
        tab = thaaLa.total_beat_count()
        avarthanam_count = math.ceil(duration/tab)#*settings.jaathi_no[settings.NADAI_INDEX]) # multiply nadai_count since it is already accounted in duration
        print('duration',duration,'tab',tab,'avarthanam_count',avarthanam_count)
        if not settings.THAALA_PATTERNS:
            settings.THAALA_PATTERNS = thaaLa.__get_thaaLa_patterns()
        thaaLa_patterns = thaaLa.get_thaaLa_patterns_for_avarthanam(avarthanam_count)
        solkattu = cparser.parse_solkattu(thaaLa_patterns)
        thaaLa_duration = cparser.total_duration(solkattu)
        print("thaaLa duration",thaaLa_duration)
        #print('scamp_note_list',scamp_note_list)
        #print('thaala_patterns',thaaLa_patterns,"\n",'thaaLa_duration',thaaLa_duration,'\nsolkattu',solkattu)
        if duration != thaaLa_duration:
            warnings.formatwarning = settings._custom_formatwarning
            warnings.warn('WARNING: ThaaLa Duration does not match with song duration. Rhythm or Song may stop earlier')
        player.fork(play_notes,args=[scamp_note_list])
        player.fork(__play_notes, args=[solkattu])
    __play_notes(scamp_note_list)
    if include_percussion_layer:
        player.wait_for_children_to_finish()

def play_notations_from_file(notation_file,instrument=None,include_percussion_layer=False):
    """
        To play notes from the notation file
        @param notation_file    File containing commands, notations - see help
        @param instrument:             Play using the instrument specified. 
                                    Will be overwritten by instruments if specified in the notation_file 
        @param include_percussion_layer    True: Includes Percussion according to the set ThaaLam and Jaathi
                                            ThaaLam and Jaathi can be set using thaaLa.set_thaaLam(thaaLam_Name, Jaathi_Name) 
    """
    if (instrument != None):
        set_instrument(instrument)
    file_carnatic_note_list,_ = cparser.parse_file(notation_file)
    play_notes(file_carnatic_note_list,include_percussion_layer)

if __name__ == '__main__':
    """
    lesson_file = "../Notes/PancharathnaKrithi-jagadhaandhakaaraka.cmn"
    #lesson_file = "../test_notes.inp"
    scamp_note_list,_= cparser.parse_file(lesson_file)
    print(scamp_note_list)
    play_notes(scamp_note_list,False)
    """
    