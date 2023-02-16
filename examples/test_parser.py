from carnatic import cparser, settings, thaaLa, cplayer
#""" Example - 1
note_array = ["S", ",", "$", "$", "G", ",", "M", ",", "P", ",", "D", ",", "N", ",", "S'", ",", \
              "S", "R", ";", "G", ",", "M", ",", ",", "D", ";", ",", "S'", ";", \
              "S", ",", "R", ",", "G", ",", "M", ",", "P", ",", "D", ",", "N", ",", "S'", ",", \
              "S", "R", ";", "G", ",", "M", ",", ",", "D", ";", ",", "S'", ";"]
settings.SCALE_OF_NOTES = settings._CARNATIC_SCALE_16_NOTES
note_array = "S R1. R2' G2 G3 M1 M2 P D1 D2 N2 N3 S^"
#settings.SCALE_OF_NOTES = settings._CARNATIC_SCALE_16_NOTES
#note_array = "S R1. R2' R3 G1 G2 G3 M1 M2 P D1 D2 D3 N1 N2 N3 S^"
#settings.SCALE_OF_NOTES = settings._CARNATIC_SCALE_16_NOTES
#note_array = "S R1. R2' R3 R4 G1 G2 G3 G4 M1 M2 M3 M4 P D1 D2 D3 D4 N1 N2 N3 N4 S^"
for carnatic_note in note_array.split():
    print(carnatic_note,cparser._get_midi_note(carnatic_note))
print(note_array,cparser._get_note_frequency_duration(note_array))
exit()    
settings.PLAY_SPEED = 3
print (cparser._arrange_notes_to_thaaLa(note_array,play_speed=settings.PLAY_SPEED))
#note_array = ["S.~", "R.~", "G.~", "M.~", "P.~", "D.~", "N.~", "S~", "R~", "G~", "M~",  "P~","D~", "N~", "S^~", "R^~", "G^~", "M^~", "P^~", "D^~", "N^~"]
c_note_arr = cparser._get_note_frequency_duration(note_array)
total_duration_of_notes=cparser.total_duration(c_note_arr)
print(total_duration_of_notes)
tab = thaaLa.total_beat_count()
import math
avarthanam_count = math.ceil(total_duration_of_notes/tab) 
thaaLa_patterns = thaaLa.get_thaaLa_patterns_for_avarthanam(avarthanam_count)
print(thaaLa_patterns)
solkattu = cparser.parse_solkattu(thaaLa_patterns)
thaaLa_duration = cparser.total_duration(solkattu)
print(thaaLa_duration)
cplayer.play_notes(c_note_arr, include_percussion_layer=True)
#"""
""" - Example - 2
lesson_file = settings._APP_PATH + "/Notes/PancharathnaKrithi-jagadhaandhakaaraka.cmn"
c_note_arr,result = cparser.parse_file(lesson_file,arrange_notes_to_speed_and_thaaLa = True)
total_note_count_in_file = len(c_note_arr)
total_duration_of_notes=cparser.total_duration(c_note_arr)
print('c_note_arr',c_note_arr,'\n',total_duration_of_notes,'total note count',total_note_count_in_file)
print(result)
"""