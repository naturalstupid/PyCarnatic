"""
    Module for 
            - generating carnatic song notations through programming
            - add tempo, instrument, comment, notes
            - open / save notation file
            - play notation
            - TODO: save as pdf, staff notation file using Lilypond, save as wav/mp3
"""
import re
import os.path
from carnatic import settings, raaga, thaaLa, cparser, cplayer

_temp_file = settings._APP_PATH+"/tmp/notations.txt"
class Song(object):
    """
        Carnatic Song Class:
            Functions: read a notation file, set tempo, thaalam, raagam, speed. Add comments, notes, instrument
                       Save notations, play notations
    """    
    def __init__(self):
        self._lines = []
        self._instruments = []
        self._file_name = _temp_file
    def read(self,song_file_name):
        """
            Read notations from a file
            @param song_file_name    - notation file
        """
        if os.path.isfile(song_file_name):
            self._file_name = song_file_name
            """ TODO: To read the file and get all the lines """
        else:
            raise ValueError("File:"+song_file_name+" does not exist")
    def get_lines(self):
        """
            @return:    all the lines of the notation file
        """
        return self._lines
    def set_tempo(self,tempo):
        """
            @param    Tempo. Set the tempo of the song. Value 1 - 200 beats per minute. Default = 60
        """
        settings.Tempo = tempo
        self._lines.append("#D"+str(tempo))
    def set_notation_type(self,scale_of_notes):
        """
            Set the svale of notes to Western, Carnatic scale of 12, 16 or 22 notes
            @param scale_of_notes  0 = Western, 1 = 12 notes (Defau;t), 2= 16 notes and 3 = 22 notes
        """
        if scale_of_notes >= 0 and scale_of_notes <= 3:
            settings._SCALE_OF_NOTES = scale_of_notes
    def set_instrument_base_note(instrument_base_note):
        """
            Sets the base note of the default instrumemt
            @param instrument_base_note - Piano Key - Example A#4
        """
        instruent_octave = settings.INSTRUMENT_BASE_NOTES[settings.INSTRUMENT_INDEX][-1]
        settings.INSTRUMENT_BASE_NOTES[settings.INSTRUMENT_INDEX] = instrument_base_note + instruent_octave
    def add_comment(self,comment):
        """
            Add comment at the current line
            @param comment - text to be added as a comment. Need not prefix "{"
        """
        self._lines.append("{"+comment)
    def add_instrument(self, instrument):
        """
            Add instrument to the current line
            @param instrument    Supported instruments are "Veena","Veena2","Flute","Sarod", "Violin","Sitar","Shenai","Piano","Guitar"
                    Always use cplayer.get_instrument_list() to get the supported list
        """
        available_instruments = settings._CARNATIC_INSTRUMENTS + settings._DEFAULT_INSTRUMENTS
        if instrument in available_instruments:
            instrument_index = available_instruments.index(instrument)
            self._lines.append("#I"+str(instrument_index))
            self._instruments.append(instrument)
    def set_percussion_instrument(self, percussion_instrument):
        """
            Set percussion instrument to the song
            @param percussion_instrument    Supported instruments are "Mridangam","EastWestMix"
        """
        if percussion_instrument in settings._PERCUSSION_INSTRUMENTS:
            settings.CURRENT_PERCUSSION_INSTRUMENT = percussion_instrument
    def set_melakartha(self,melakartha_number):
        """
            @param melakartha_number: Calls raaga.set_melakartha() to set song to melkartha
            Note: setting melakaratha will also change raaga to melakartha raaga
        """
        raaga.set_melakartha(melakartha_number)
        self._lines.append("#M"+str(melakartha_number))
    def set_raagam(self, raagam):
        """
            @param raagam: Calls raaga.set_raagam() to set song to the raagam
            Note: setting raagam will also change melakartha to melakartha of the raaga 
        """
        raaga.set_raagam(raagam)
    def set_thaaLam(self, thaaLam, jaathi,nadai=None):
        """
            Calls thaaLa.set_thaaLam() to set song to the thaaLam and jaathi
            @param thaaLam: thaaLam name
            @param jaathi: jaathi name
            @param nadai: nadai name. Default - no nadai
            Also see set_thaaLam_index() to set using the indices of thaaLam and jaathi
        """
        thaaLa.set_thaaLam(thaaLam, jaathi,nadai)
        self._lines.append("#T"+str(settings.THAALA_INDEX))
        self._lines.append("#J"+str(settings.JAATHI_INDEX))
    def set_thaaLam_index(self, thaaLam_index, jaathi_index,nadai_index=None):
        """
            Calls thaaLa.set_thaaLam_index() to set song to the thaaLam and jaathi
            @param thaaLam_index: index of the thaaLam (1 to 7)
            @param jaathi_index: jaathi index ( 1 to 5 )
            @param nadai_index: 0 to 5 (0 means No Nadai)
            Also see set_thaaLam() to set using the names of thaaLam and jaathi
        """
        thaaLa.set_thaaLam_index(thaaLam_index, jaathi_index,nadai_index)
        self._lines.append("#T"+str(settings.THAALA_INDEX))
        self._lines.append("#J"+str(settings.JAATHI_INDEX))
    def add_notes(self, notes):
        """
            Adds carnatic notes to the song. 
            @param notes: following the pattern. Acceptable Note Pattern: [SsPp|RrGgMmDdNn][1-4][.'^][~/!] *
        """
        rx = re.compile(settings._NOTES_PATTERN + ".*")
        if not rx.search(notes):
            raise ValueError(notes,"does not meet pattern",settings._NOTES_PATTERN)
        self._lines.append(notes)
    def set_speed(self,speed):
        """
            @param speed: Speed of the song Values 1 to 5 (typicallt only 1 to 3)
        """ 
        if speed < 1 or speed > 5:
            raise ValueError("Allowed speed range: 1..5")
        self._lines.append("#S"+str(speed))
        settings.PLAY_SPEED = speed
    def set_thaaLam_speed(thaaLam_speed=1):
        """
            Set the thaaLam speed of the song.
            ****** CAUTION ******
            Speed is in addition to Nadai 
            Values 1 to 3
            Example: Speed =2, Chathusra Nadai => 8 beats per note or 
            Speed = 3 No nadai is same as Chathusra Nadai  =< Both will have 4 notes per note
            SO KNOW WHAT YOU ARE DOING BY SETTING NADAI AND SPEED
            *********************
            @param thaaLam_speed: thaaLam speed (also called kalai)
         """
        thaaLam.set_thaaLam_speed(thaaLam_speed)
    def save(self,output_file_name):
        """
            @param output_file_name:    Saves the song elements as as text file.
        """
        self._file_name = output_file_name
        print("Saving the song as",output_file_name)
        file_object = open(output_file_name,"w")
        for line in self._lines:
            file_object.write(line+"\n")
        file_object.close()
    def play(self,instrument="Flute",include_percussion_layer=False):
        """
            Plays the notation file with specified instrument and with/wuthout percussio
            @param instrument: Specify name of supported instrument
            @param include_percussion_layer:True - play notations with percussion to set thaaLa/Jaathi 
        """
        if self._file_name == _temp_file:
            self.save(self._file_name)
        cplayer.play_notations_from_file(self._file_name,instrument=instrument,include_percussion_layer=include_percussion_layer)
    def _overline(self,text):
        SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
        unicode_overline = u'\u0305'
        #result = ''.join([c  if re.match("\s+",c) else c+unicode_overline+"\t" for c in text])
        result = re.sub(r"([SsRrGgMmPpDdNn,;\(\)/!])([1-4]?[\\.\\'^]?[<~>]?[1-5]?)",r"\1"+unicode_overline+r"\2",text)
        result = result.translate(SUB)
        return result
if __name__ == '__main__':
    """
    s = Song()
    ss = "SR1     G2M1 PD2 N3S^"
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
    """