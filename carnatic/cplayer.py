"""
    Module for 
            - collecting carnatic instruments from soundfont and default midi instruments
            - playing notations from file or argument
        play_notes function will play notations returned by cparser.parse_notation_file
        play_file function will gather notations from a file abd play
"""
import math
import warnings
from scamp import Session, playback_settings
playback_settings.soundfont_search_paths.append("Lib/")
playback_settings.make_persistent()
from carnatic import settings, thaaLa, cparser
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
    instrument_list += ['silent']
    settings._INSTRUMENT_VOLUME_LEVELS.append(settings._VOLUME)
    return instrument_list
def _get_player():
    global available_instruments, player
    if player==None:
        available_instruments.clear()
        player = Session(tempo=settings.TEMPO)# load default_soundfont
        inst_index = 0
        for inst in settings._CARNATIC_INSTRUMENTS:
            available_instruments[inst_index] = player.new_part(preset=inst_index,soundfont=settings._SOUND_FONT_FILE)
            inst_index += 1 
        for inst in settings._DEFAULT_INSTRUMENTS:
            available_instruments[inst_index] = player.new_part(preset=inst_index,soundfont="default") 
            inst_index += 1 
        for inst in settings._PERCUSSION_INSTRUMENTS:
            available_instruments[inst_index] = player.new_part(preset=inst_index,soundfont=settings._SOUND_FONT_FILE) 
            inst_index += 1 
        available_instruments[inst_index] = player.new_silent_part("silent")
    return player
def _get_instrument(instrument_name):
    global available_instruments,player
    player = _get_player()
    if available_instruments:
        if instrument_name in get_instrument_list():
            return available_instruments[instrument_name]
    return None
def set_percussion_instrument(percussion_instrument_name):
    """
        Set default percussion instrument
        @param percussion_instrument_name: Name of the instrument from settings._PERCUSSION_INSTRUMENTS
    """
    instruments = settings._PERCUSSION_INSTRUMENTS
    if percussion_instrument_name in instruments:
        settings.CURRENT_PERCUSSION_INSTRUMENT = percussion_instrument_name
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
        #note = item[0]
        instrument, pitch,durn = item[1]
        #print(note,instrument,pitch,durn)
        inst = available_instruments[instrument]
        inst.play_note(pitch, settings._INSTRUMENT_VOLUME_LEVELS[instrument], durn)    
def play_carnatic_notes(carnatic_notes,instrument='Flute',include_percussion_layer=False):
    set_instrument(instrument)
    scamp_note_list = cparser._get_note_frequency_duration(carnatic_notes)
    play_notes(scamp_note_list)
def play_notes(scamp_note_list,include_percussion_layer=False,solkattu_list=None): #, save_audio_file=None):
    """
        To play notes
        @param scamp_note_list            SCAMP notes list [ "Carnatic Note", ["Instrument", Pitch_Float, Duration_float], ...]
                                            notes list can be obtained from cparser.parser_file function
        @param include_percussion_layer    True: Includes Percussion according to the set ThaaLam and Jaathi
                                            ThaaLam and Jaathi can be set using thaaLa.set_thaaLam(thaaLam_Name, Jaathi_Name) 
                                            or using thaaLam.set_thaaLam_index(thaaLam_index, jaathi_index)
    """
    global player
    if player==None:
        player = _get_player()
    player.tempo = settings.TEMPO
    if include_percussion_layer: #V1.0.2
        solkattu = solkattu_list
        player.fork(__play_notes,args=[scamp_note_list])
        player.fork(__play_notes, args=[solkattu])
    else:
        __play_notes(scamp_note_list)
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
    file_carnatic_note_list,_,file_solkattu_array = cparser.parse_notation_file(notation_file)
    play_notes(file_carnatic_note_list,include_percussion_layer,file_solkattu_array)

def play_solkattu_from_file(solkattu_file,percussion_instrument=None,lesson_mode=False):
    """
        To play solkattu from the notation file
        @param solkattu_file    File containing commands, notations - see help
        @param percussion_instrument:             Play using the percussion instrument specified. 
                                    Will be overwritten by instruments if specified in the notation_file
        @param lesson_mode = True default nadai is switched off to play thaaLa lessons from file 
    """
    old_nadai_index = settings.NADAI_INDEX
    if lesson_mode:
        settings.NADAI_INDEX = 0
    if (percussion_instrument != None):
        set_percussion_instrument(percussion_instrument)
    file_carnatic_note_list,_ = cparser.parse_solkattu_file(solkattu_file)
    play_notes(file_carnatic_note_list,include_percussion_layer=False)
    settings.NADAI_INDEX = old_nadai_index
if __name__ == '__main__':
    #"""
    settings._PLAYER_TYPE = settings.PLAYER_TYPE.SCAMP
    inst_index = 0
    settings.TEMPO = 72
    thaaLa_index = 4
    settings.THAALA_INDEX = thaaLa_index
    jaathi_index = 2
    settings.JAATHI_INDEX = jaathi_index
    nadai_index = 3
    settings.NADAI_INDEX = nadai_index
    print('thaala',settings.THAALA_NAMES(thaaLa_index).name)
    print('jaathi',settings.JAATHI_NAMES(jaathi_index).name)
    print('thaala',settings.NADAI_NAMES(nadai_index).name)
    print('thaala positions',thaaLa.get_thaaLa_positions(thaaLa_index, jaathi_index))
    tac = thaaLa.total_akshara_count(thaaLa_index, jaathi_index, nadai_index)
    print('total_akshara_count',tac)
    #lesson_file = "Notes/PancharathnaKrithi-jagadhaandhakaaraka.cmn"
    lesson_file = "../test_notes.inp"
    include_percussion_layer = True
    settings.INSTRUMENT_INDEX = inst_index
    instrument = settings._INSTRUMENT_LIST[inst_index]
    settings.CURRENT_INSTRUMENT = instrument
    print("PLAYER =>",settings._PLAYER_TYPE)
    if settings._PLAYER_TYPE == settings.PLAYER_TYPE.SCAMP:
        play_notations_from_file(lesson_file,instrument,include_percussion_layer=include_percussion_layer)
    else: # SF2_LOADER Option
        from carnatic import cmidi
        cmidi.play_notes_from_file(lesson_file,include_percussion_layer=include_percussion_layer)
    #"""
    