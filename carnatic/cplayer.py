import regex
from scamp import *
#import fluidsynth
import cparser, raaga, thaaLa
_FULL_NOTE_DURATION = 1.0
_VOLUME = 1
raaga.set_melakartha(72)
thaaLa.set_thaaLa(3)
thaaLa.set_jaathi(5)

def play_notes(carnatic_note_list, instrument="Violin"):
    s = Session()
    #s = Session(default_soundfont_preset="Lib/SIWF8.sf2")
    inst = s.new_part(instrument)
    for item in carnatic_note_list:
        car_notes = regex.findall(cparser._NOTES_PATTERN, item)
        #print('item notes',car_notes,len(car_notes))
        if car_notes:
            d = _FULL_NOTE_DURATION /  len(car_notes)
            for cn in car_notes:
                if cn:
                    #pitch = cparser._get_midi_notes(cn)
                    pitch = cparser._get_midi_note(cn)
                    #print(cn,"=>",pitch,"durn",d)
                    inst.play_note(pitch, _VOLUME, d)
def play_lesson(lesson_file,instrument="Violin"):
    file_carnatic_note_list = cparser.parse_file(lesson_file, fit_notes_to_speed_and_thaaLa=True)
    play_notes(file_carnatic_note_list,instrument=instrument)

if __name__ == '__main__':
    """
    s = Session(default_soundfont="Lib/SIWF8.sf2")
    pitch_list = [[72.5,74.6],[76.7,80.8],[82.9,84]]
    inst = s.new_part("Violin")
    for pitch in pitch_list:
        inst.play_note(pitch, [0.1,1.0], [0.5,1.0])
    for pitch in pitch_list:
        inst.play_note(pitch, 1, 0.5)
    for pitch in pitch_list:
        inst.play_note(pitch, 1, 0.25)
    for pitch in pitch_list:
        inst.play_note(pitch, 1, 0.125)
    exit()
    """
    #"""
    lesson_file = "test_lesson.inp"
    play_lesson(lesson_file,instrument="Sitar")
    #"""
    """
    car_list = ["S", "R1", "G2", "M1", "P", "D2", "N3", "S^"]
    play_notes(car_list)
    """