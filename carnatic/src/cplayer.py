import regex
import sys
from scamp import *
#playback_settings.soundfont_search_paths.append("Lib/")
#playback_settings.make_persistent()
import settings, cparser, raaga, thaaLa

available_instruments = {}
def get_player():
    global available_instruments
    available_instruments.clear()
    player = Session()# load default_soundfont
    for inst in settings._CARNATIC_INSTRUMENTS:
        available_instruments[inst] = player.new_part(inst,soundfont=settings._SOUND_FONT_FILE) 
    for inst in settings._DEFAULT_INSTRUMENTS:
        available_instruments[inst] = player.new_part(inst,soundfont="default") 
    for inst in settings._PERCUSSION_INSTRUMENTS:
        available_instruments[inst] = player.new_part(inst,soundfont=settings._SOUND_FONT_FILE) 
    return player
def play_notes(scamp_note_list):
    player = get_player()
    player.tempo = settings.TEMPO
    for item in scamp_note_list:
        note = item[0]
        instrument, pitch,durn = item[1]
        inst = available_instruments[instrument]
        print(note,inst,instrument,pitch,durn)
        inst.play_note(pitch, settings._VOLUME, durn)    

def play_lesson(lesson_file,instrument="Flute"):
    file_carnatic_note_list = cparser.parse_file(lesson_file, fit_notes_to_speed_and_thaaLa=True)
    play_notes(file_carnatic_note_list,instrument=instrument)

if __name__ == '__main__':
    """
    inst = get_instrument("Violin")
    inst.play_note(71,1,1)
    exit()
    """
    """
    lesson_file = "test_lesson.inp"
    play_lesson(lesson_file,"Sarod")
    exit()
    """
    #"""
    lesson_file = "../test_lesson.inp"
    lesson_file = "../Notes/vAtApi_Adhi_1.cmn"
    lesson_file = "../Notes/PancharathnaKrithi-jagadhaandhakaaraka.cmn"
    lesson_file="../test_notes.inp"
    scamp_note_list= cparser.parse_file(lesson_file)
    #scamp_note_list = cparser._get_note_frequency_duration(c_note_arr)
    play_notes(scamp_note_list)
    #"""
    