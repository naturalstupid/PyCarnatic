"""
    Module for 
            - generating carnatic song notations through programming
            - add tempo, instrument, comment, notes
            - open / save notation file
            - play notation
            - TODO: save as pdf, staff notation file using Lilypond, save as wav/mp3
"""
import re
import settings, raaga, thaaLa,cparser,cplayer

class Song(object):
    def __init__(self):
        self._lines = []
        self._instruments = []
    def open(self,song_file_name):
        pass
    def get_lines(self):
        return self._lines
    def set_tempo(self,tempo):
        settings.Tempo = tempo
        self._lines.append("#D"+str(tempo))
    def set_notation_type(self,scale_of_notes):
        if scale_of_notes >= 0 and scale_of_notes <= 3:
            settings._SCALE_OF_NOTES = scale_of_notes
    def set_instrument_base_note(instrument_base_note):
        instruent_octave = settings.INSTRUMENT_BASE_NOTES[settings.INSTRUMENT_INDEX][-1]
        settings.INSTRUMENT_BASE_NOTES[settings.INSTRUMENT_INDEX] = instrument_base_note + instruent_octave
    def add_comment(self,comment):
        self._lines.append("{"+comment)
    def add_instrument(self, instrument):
        available_instruments = settings._CARNATIC_INSTRUMENTS + settings._DEFAULT_INSTRUMENTS
        if instrument in available_instruments:
            instrument_index = available_instruments.index(instrument)
            self._lines.append("#I"+str(instrument_index))
            self._instruments.append(instrument)
    def set_melakartha(self,melakartha_number):
        raaga.set_melakartha(melakartha_number)
        self._lines.append("#M"+str(melakartha_number))
    def set_raagam(self, raagam):
        raaga.set_raagam(raagam)
    def set_thaaLam(self, thaaLam, jaathi,nadai=None):
        thaaLa.set_thaaLam(thaaLam)
        thaaLa.set_jaathi(jaathi)
        if nadai != None:
            thaaLa.set_nadai(nadai)
        self._lines.append("#T"+str(settings.THAALA_INDEX))
        self._lines.append("#J"+str(settings.JAATHI_INDEX))
    def add_notes(self, notes):
        rx = re.compile(settings._NOTES_PATTERN + ".*")
        if not rx.search(notes):
            raise ValueError(notes,"does not meet pattern",settings._NOTES_PATTERN)
        self._lines.append(notes)
    def set_speed(self,speed):
        if speed < 1 or speed > 5:
            raise ValueError("Allowed speed range: 1..5")
        self._lines.append("#S"+str(speed))
        settings.PLAY_SPEED = speed
    def save(self,output_file_name):
        print("Saving the song as",output_file_name)
        file_object = open(output_file_name,"w")
        for line in self._lines:
            file_object.write(line+"\n")
        file_object.close()
    def play(self,fit_notes_to_speed_and_thaaLa=True):
        temp_file = "../tmp/notations.txt"
        self.save(temp_file)
        cplayer.play_notations_from_file(temp_file)
    def _overline(self,text):
        unicode_overline = u'\u0305'
        #result = ''.join([c  if re.match("\s+",c) else c+unicode_overline+"\t" for c in text])
        result = re.sub(r"([SsRrGgMmPpDdNn,;\(\)/!])([1-4]?[\\.\\'^]?[<~>]?[1-5]?)",r"\1"+unicode_overline+r"\2",text)
        return result
if __name__ == '__main__':
    s = Song()
    ss = "S     R1     G2    M1 P D2 N3 S^"
    print(s._overline(ss))
    exit()
    s.set_melakartha(15)
    s.set_tempo(60)
    s.set_thaaLam("Thriputai ThaaLa", "Chathusra Jaathi")
    s.add_instrument("Veena2")
    s.set_speed(1)
    s.set_notation_type(1)
    s.add_comment("This is a comment")
    s.add_notes("S R G M P D N S'")
    s.play()
    s.save("delme.txt")