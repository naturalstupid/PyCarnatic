"""
import sounddevice as sd
from scipy.io.wavfile import write as save_as_wave

fs = 44100  # Sample rate
seconds = 3  # Duration of recording
sd.default.device = [1,4]
print(sd.query_devices())
exit()
"""
from carnatic import settings, song, cparser
#""" Example building a song from scratch ...
s = song.Song()
s.add_line("#N1 \n S R1. R2' G2 G3 M1 M2 P D1 D2 N2 N3 S^")
#s.add_line("#N1 \n S R. G M P D N S^")
s.add_line("#N2 \n S R1. R2' R3 G1 G2 G3 M1 M2 P D1 D2 D3 N1 N2 N3 S^")
#s.add_line("#N2 \n S R. G M P D N S^")
s.add_line("#N3 \n S R1. R2' R3 R4 G1 G2 G3 G4 M1 M2 M3 M4 P D1 D2 D3 D4 N1 N2 N3 N4 S^")
#s.add_line("#N3 \n S R. G M P D N S^")
s.play(include_percussion_layer=False)
exit()
#"""
"""
ss = ' '.join(["S.~", "R.~", "G.~", "M.~", "P.~", "D.~", "N.~", "S~", "R~", "G~", "M~",  "P~","D~", "N~", "S^~", "R^~", "G^~", "M^~", "P^~", "D^~", "N^~"])
s.set_melakartha(15)
s.set_tempo(60)
s.set_thaaLam_index(4,2)
s.add_instrument("Flute")
s.set_speed(1)
s.set_notation_type(1)
s.add_comment("This is a comment")
s.add_notes(ss)
s.play()
#s.save("delme.txt")
"""
"""
# Examole reading a song from a notation file and play 
song_file = settings._APP_PATH + "/Notes/PancharathnaKrithi-jagadhaandhakaaraka.cmn"
s = song.Song()
s.read(song_file)
s.play(instrument="Flute",include_percussion_layer=True)
"""