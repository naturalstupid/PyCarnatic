# PyCarnatic / Carnatic Music Guru - V0.6.5
## This package was inspired from the Java Application: [JRaaga / Carnatic Music Guru](https://sourceforge.net/projects/carnaticmusicguru/)
<br>
<br>This provides a python package to <br>
	<li>Generate Music Lessons (SaraLi, Jantai, Dhaattu, Keezh/mEl sthaayi and Alankaaram) for about 400 raagas
	<li>Defines a notation system for carnatic music notes
		<li>- Will automatically use appropriate notes according to the melakartha
		<li>- notation for micro tones and gliding
	<li>Plays the notation file with specified raaga, micortones, gliding, instruments
		<li>Automatically generates percussion layer per specified thaaLa/jaathi combination
	<li> List of available carnatic instruments:
	<li> 	-	CARNATIC_INSTRUMENTS = ["Veena","Veena2","Flute","Sarod",]
	<li> 	-	DEFAULT_INSTRUMENTS = ["Violin","Sitar","Shenai","Piano","Guitar"]
	<li> 	-	PERCUSSION_INSTRUMENTS = ["Mridangam","EastWestMix"]
	
## Notations
### Comments
<li> Comments start with "{"
<li> Example: { This is a comment  

### Commands
<li> Commands start with "#" followed by a number or [[<number> with closing ]] somewhere in following lines
<li> #S<number> Speed of the song values 1 to 5 - Example:
<li> 	#S1
<LI> #M<number> Specify MElakaratha of the song values 1 to 72 - Example:
<li>	#M15
<li> #D<number> Duration - values 1 - 200. Example:
<li> 	#D60
<li> #T - specify thaaLa - values 1 to 7 (1-Eka ... 7-Dhurva ThaaLam). Example:
<li> 	#T4
<li> #J - specify jaathi - values 1 to 5 (1-Thisra ... 7-Samkeerna). Example:
<li> 	#J2
<li> [[<number> ThaaLam Speed values 1 to 3. If number is missing, it will be considered as to Exclude Percussion from this point onwards until closing ]
<li> Need not specify [[1 .. ]] - which is default
<li> [[3
<li> S R G M 
<li> ]]
<li> [[
<li> P D N S'
<li> ]]
<li> The notes S R G M will have percussion played along at thaaLam speed of 3 times
<li> The notes P D N S' will NOT have percussion played. only instrument

### Carnatic Notes
<li> Carnatic notes can be written as S R R1 R2 etc 
<li> Or can be written in lower case with/without numbers Example: s r1, g m pd n'
<li> Lower octaves should have "period"/"dot" . as a suffix. Example: S. R1. M2. etc
<li> Upper octave notes should have single quote ' or caret ^. Example: S' R1^ M1 ' etc
<li> Additional duration to notes can be using comma or semicolon. Example: s,, r;, etc
<li> Microtone notations can S>1 S>2 R1>3 - 10%, 20% 30% respectively more than the pitch of the note
<li> Similarly notations like G3<1 M2<4 have 10% 40% respectively less than the pitch of the note
<li> Gliding notes:  S / R - will glide from S to R and sustain at R for its duration
<li> Gliding notes:  M ! P - will glide down from M to P and sustain at P for its duration
<li> Shaking notes:  Suffix tilde symbol to notes to shake the note. Example: S~ R2~ P^~ etc


## Lessons
```
generate_lessons(lesson_type,arrange_notes_to_speed_and_thaaLa=True, raaga_name=None, thaaLa_name=None, jaathi_name=None):
    """
            - generating notations for music lessons for specified raaga and thaaLa
            - Lesson Names supported are: "SARALI_VARISAI", "JANTAI_VARISAI", "DHAATTU_VARISAI", "MELSTHAAYI_VARISAI", "KEEZHSTHAAYI_VARISAI"]
            @param    lesson_type    case not sensitive
            @param    arrange_notes_to_speed_and_thaaLa    True the notations generated will be fit to speed and thaaLa
            @param    raaga_name    If not specified default raaga from settings will be used
            @param    thaaLa_name   If not specified default thaaLa from settings will be used
            @param    jaathi_name   If not specified default jaathi from settings will be used
                       Use raaga.get_raaga_list() to get the list of raaga names
                       Use thaaLa.get_thaaLam_names() to get the list of thaaLa names
                       Use thaaLa.get_jaathi_names() to get the list of jaathi names
            :return:    notations for the selected lesson
    """

alankaara_varisai_from_book(arrange_notes_to_speed_and_thaaLa=True, raaga_name=None):
    """
        Generate alankaara varisai (from carnatic music lessons book) for the specified raaga
            @param    arrange_notes_to_speed_and_thaaLa    True the notations generated will be fit to speed and thaaLa
            @param    raaga_name    If not specified default raaga from settings will be used
            :return:   alankaara varisai for the selected raaga
    """
    
alankaara_varisai_from_algorithm(arrange_notes_to_speed_and_thaaLa=True, raaga_name=None, thaaLa_name=None, jaathi_name=None):
    """
        Generate alankaara varisai (from computer generated algorithm) for the specified raaga
            @param    arrange_notes_to_speed_and_thaaLa    True the notations generated will be fit to speed and thaaLa
            @param    raaga_name    If not specified default raaga from settings will be used
            @param    thaaLa_name   If not specified default thaaLa from settings will be used
            @param    jaathi_name   If not specified default jaathi from settings will be used
                       Use raaga.get_raaga_list() to get the list of raaga names
                       Use thaaLa.get_thaaLam_names() to get the list of thaaLa names
                       Use thaaLa.get_jaathi_names() to get the list of jaathi names
            :return:   alankaara varisai for the selected raaga
    """
    
```
## cparser
```
parse_file(file_name,arrange_notes_to_speed_and_thaaLa = True):
    """
        To parse a notation file and generate SCAAMP list
        @param    file_name: Notations file - see help for notation syntax
        @param    arrange_notes_to_speed_and_thaaLa    True the notations generated will be fit to speed and thaaLa
        @return:  file_carnatic_note_array     SCAMP notes list [ "Carnatic Note", ["Instrument", Volume_float, Duration_float], ...]
        @return:  result lines of notations
    """
    
parse_solkattu(solkattu_list):
    """
        To parse solkattu phrases of percussion instrument and  generate SCAAMP list
        @param    solkattu_list
        @param    arrange_notes_to_speed_and_thaaLa    True the notations generated will be fit to speed and thaaLa
        @return:  result     SCAMP notes list [ "Carnatic Note", ["Instrument", Volume_float, Duration_float], ...]
    """
    
```
## cplayer
```
get_instrument_list(include_percussion_instruments=False):
    """
        Get list of available instruments
        @param include_percussion_instruments: True / False whether to include list of percussion instruments available
        @return: List of available instruments
    """
    
play_notes(scamp_note_list,include_percussion_layer=False):
    """
        To play notes
        @param scamp_note_list            SCAMP notes list [ "Carantic Note", ["Instrument", Volume_float, Duration_float], ...]
                                            notes list can be obtained from cparser.parser_file function
        @param include_percussion_layer    True: Includes Percussion according to the set ThaaLam and Jaathi
                                            ThaaLam and Jaathi can be set using thaaLa.set_thaaLam(thaaLam_Name, Jaathi_Name) 
                                            or using thaaLam.set_thaaLam_index(thaaLam_index, jaathi_index)
    """
    
play_notations_from_file(notation_file,instrument=None,include_percussion_layer=False):
    """
        To play notes from the notation file
        @param notation_file    File containing commands, notations - see help
        @param instrument:             Play using the instrument specified. 
                                    Will be overwritten by instruments if specified in the notation_file 
        @param include_percussion_layer    True: Includes Percussion according to the set ThaaLam and Jaathi
                                            ThaaLam and Jaathi can be set using thaaLa.set_thaaLam(thaaLam_Name, Jaathi_Name) 
    """
    
```
## Examples:
#### raaga - Example
```
from carnatic import raaga
raaga_list = raaga.get_raaga_list()
print(raaga_list)
raagas = raaga.search_for_raaga_by_name(search_str="kalyani", is_exact=False)
print(raagas)
raagam = raaga.search_for_raaga_by_name(search_str="mohanam", is_exact=True)
raaga_id = raagam[0][0]
raaga_name = raagam[0][1]
print(raaga_id,raaga_name)
print('Mohanam - aroganam',raaga.get_aroganam(raaga_id), 'Mohanam - avaroganam',raaga.get_avaroganam(raaga_id))
parent_raaga_id, parent_raaga_name = raaga.get_parent_raaga(raaga_id)
print('parent raaga',parent_raaga_name,parent_raaga_id)
print('Janya Raagas:',raaga.get_janya_raagas(parent_raaga_id))
""" 
    Get List of melakartha raagas using multiple filter conditions
    List of raagas that have 6 notes both in aroganam and avaroganam
    or list of raaga that have M1 and M2 in aroganam and avaroganam
"""
filter_options = {'Aroganam Note Count' : 6, "Avaroganam Note Count":6}
six_note_raagas = raaga.search_for_raaga_by_attributes(attribute_value_dictionary=filter_options,is_exact=True)
print(six_note_raagas)
filter_options = {'Aroganam' : "M1 M2", "Avaroganam":"M2 M1"}
spl_raagas = raaga.search_for_raaga_by_attributes(attribute_value_dictionary=filter_options,is_exact=False)
print(spl_raagas)
print(raaga.get_melakartha_raagas())
```
#### thaaLa - Example
```
from carnatic import thaaLa
""" Generate Beat Patterns 9beat-7beat-5beat-4beat """
tp = thaaLa.get_thaaLa_patterns_for_beat_string(thaaLa_beat_string="9754",generate_random=True)
print(tp)
""" Generate beat pattern for specific thaala jaathi nadai combination """
tp = thaaLa.get_thaaLa_patterns_for_thaaLa_jaathi_nadai(thaaLa_index=4,jaathi_index=2,nadai_index=2,generate_random=True)
print(tp)
""" Generate beat pattern for specified number of avarthanam """
tp = thaaLa.get_thaaLa_patterns_for_avarthanam(avarthanam_count=2,thaaLa_index=4,jaathi_index=2,nadai_index=2,generate_random=True)
print(tp)
```
#### lessons - Example
```
from carnatic import lessons
# Example - 1
result = lessons.generate_lessons("sarali_varisai",arrange_notes_to_speed_and_thaaLa=True, raaga_name="BhoopAlam",thaaLa_name="Jampa",jaathi_name="Sankeerna")
#
# Example - 2
result = lessons.alankaara_varisai_from_book(arrange_notes_to_speed_and_thaaLa=True, raaga_name="hamsadhwani")

# Example - 3
result =lessons.alankaara_varisai_from_algorithm(arrange_notes_to_speed_and_thaaLa=True, raaga_name="mohanam",thaaLa_name="ata",jaathi_name="misra")

print(result)
```
#### cplayer - Example
```
notation_file = "../Notes/PancharathnaKrithi-jagadhaandhakaaraka.cmn"
play_notations_from_file(notation_file,"Sarod")
```
#### Song - Example
```
s = Song()
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
```