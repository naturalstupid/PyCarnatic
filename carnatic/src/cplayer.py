"""
    Module for 
            - collecting carnatic instruments from soundfont and default midi instruments
            - playing notations from file or argument
        play_notes function will play notations returned by cparser.parse_file
        play_file function will gather notations from a file abd play
"""
import regex
import sys
from scamp import *
#playback_settings.soundfont_search_paths.append("Lib/")
#playback_settings.make_persistent()
import settings, cparser, raaga, thaaLa
player=None
available_instruments = {}

def _get_instrument_list():
    return settings._CARNATIC_INSTRUMENTS + settings._DEFAULT_INSTRUMENTS + settings._PERCUSSION_INSTRUMENTS
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
    return player
def get_instrument(instrument_name):
    global available_instruments,player
    player = _get_player()
    if available_instruments:
        if instrument_name in settings._CARNATIC_INSTRUMENTS + settings._DEFAULT_INSTRUMENTS:
            return available_instruments[instrument_name]
    return None
        
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
        :param: scamp_note_list            SCAMP notes list [ "Carntic Note", ["Instrument", "Volume", "Duration"], ...]
                                            notes list can be obtained from cparser.parser_file function
        :param: include_percussion_layer    True: Includes Percussion according to the set ThaaLam and Jaathi
                                            ThaaLam and Jaathi can be set using thaaLa.set_thaaLam(thaaLam_Name, Jaathi_Name) 
    """
    global player
    if player==None:
        player = _get_player()
    player.tempo = settings.TEMPO
    if include_percussion_layer:
        duration = cparser.total_duration(scamp_note_list)
        avarthanam_count = int(duration/thaaLa.total_akshara_count())
        print('avarthanam_count',avarthanam_count)
        if not settings.THAALA_PATTERNS:
            settings.THAALA_PATTERNS = thaaLa.__get_thaaLa_patterns()
        tp = thaaLa.get_thaaLa_patterns_for_avarthanam(avarthanam_count,nadai_index = 2)
        sk = cparser.parse_solkattu(tp)
        #player.fork(play_notes,args=[scamp_note_list])
        player.fork(__play_notes, args=[sk])
    __play_notes(scamp_note_list)
    if include_percussion_layer:
        player.wait_for_children_to_finish()

def play_notations_from_file(notation_file,instrument="Flute",include_percussion_layer=False):
    """
        To play notes from the notation file
        :param: notation_file    File containing commands, notations - see help
        :param: instrument:             Play using the instrument specified. 
                                    Will be overwritten by instruments if specified in the notation_file 
        :param: include_percussion_layer    True: Includes Percussion according to the set ThaaLam and Jaathi
                                            ThaaLam and Jaathi can be set using thaaLa.set_thaaLam(thaaLam_Name, Jaathi_Name) 
    """
    file_carnatic_note_list,_ = cparser.parse_file(notation_file, fit_notes_to_speed_and_thaaLa=True)
    play_notes(file_carnatic_note_list,include_percussion_layer)

if __name__ == '__main__':
    from scamp import Envelope
    def _float_range(start, stop, step):
      while start < stop:
        yield float(start)
        start += step #decimal.Decimal(step)

if __name__ == '__main__':
    #"""
    lesson_file = "../Notes/PancharathnaKrithi-jagadhaandhakaaraka.cmn"
    lesson_file = "../test_notes.inp"
    scamp_note_list,_= cparser.parse_file(lesson_file)
    print(scamp_note_list)
    play_notes(scamp_note_list,False)
    #"""
    