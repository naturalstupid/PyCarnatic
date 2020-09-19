# PyCarnatic / Carnatic Music Guru - V0.6.0
## This package was inspired from the Java Application: JRaaga / Carnatic Music Guru
** https://sourceforge.net/projects/carnaticmusicguru/ **

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
<li> { Comments start with "{"
<li> { Commands start with "#" followed by a number
<li> { #S<number> Speed of the song values 1 to 5 - Example:
<li> #S1
<LI> { #M<number> Specify MElakaratha of the song values 1 to 72 - Example:
<li>#M15
<li> { #D<number> Duration - values 1 - 200. Example:
<li> #D60
<li> { #T - specify thaala - values 1 to 7 (1-Eka ... 7-Dhurva ThaaLam). Example:
<li> #T4
<li> { #J - specify jaathi - values 1 to 5 (1-Thisra ... 7-Samkeerna). Example:
<li> #T2
<li> Carnatic notes can be written as S R R1 R2 etc 
<li> Lower octaves should have "period"/"dot" . as a suffix. Example: S. R1. M2. etc
<li> Upper octave notes should have single quote ' or caret ^. Example: S' R1^ M1 ' etc


## Lessons
```
generate_lessons(lesson_type,fit_notes_to_speed_and_thaaLa=False, raaga_name=None, thaaLa_name=None, jaathi_name=None) 
    """
            - generating notations for music lessons for specified raaga and thaaLa
            - Lesson Names supported are: "SARALI_VARISAI", "JANTAI_VARISAI", "DHAATTU_VARISAI", "MELSTHAAYI_VARISAI", "KEEZHSTHAAYI_VARISAI"]
            :param:    lesson_type    case not sensitive
            :param:    fit_notes_to_speed_and_thaaLa    True the notations generated will be fit to speed and thaaLa
            :param:    raaga_name    If not specified default raaga from settings will be used
            :param:    thaaLa_name   If not specified default thaaLa from settings will be used
            :param:    jaathi_name   If not specified default jaathi from settings will be used
                       Use raaga.get_raaga_list() to get the list of raaga names
                       Use thaaLa.get_thaaLam_names() to get the list of thaaLa names
                       Use thaaLa.get_jaathi_names() to get the list of jaathi names
            :return:    notations for the selected lesson
    """
alankaara_varisai_from_book(fit_notes_to_speed_and_thaaLa=False, raaga_name=None)
    """
        Generate alankaara varisai (from carnatic music lessons book) for the specified raaga
            :param:    fit_notes_to_speed_and_thaaLa    True the notations generated will be fit to speed and thaaLa
            :param:    raaga_name    If not specified default raaga from settings will be used
            :return:   alankaara varisai for the selected raaga
    """
alankaara_varisai_from_algorithm(fit_notes_to_speed_and_thaaLa=False, raaga_name=None, thaaLa_name=None, jaathi_name=None)
    """
        Generate alankaara varisai (from computer generated algorithm) for the specified raaga
            :param:    fit_notes_to_speed_and_thaaLa    True the notations generated will be fit to speed and thaaLa
            :param:    raaga_name    If not specified default raaga from settings will be used
            :param:    thaaLa_name   If not specified default thaaLa from settings will be used
            :param:    jaathi_name   If not specified default jaathi from settings will be used
                       Use raaga.get_raaga_list() to get the list of raaga names
                       Use thaaLa.get_thaaLam_names() to get the list of thaaLa names
                       Use thaaLa.get_jaathi_names() to get the list of jaathi names
            :return:   alankaara varisai for the selected raaga
    """
```
## cparser
```
parse_file(file_name,fit_notes_to_speed_and_thaaLa = False)
    """
        To parse a notation file and generate SCAAMP list
        :param:    file_name: Notations file - see help for notation syntax
        :param:    fit_notes_to_speed_and_thaaLa    True the notations generated will be fit to speed and thaaLa
        :return:   file_carnatic_note_array     SCAMP notes list [ "Carntic Note", ["Instrument", "Volume", "Duration"], ...]
        :return:   result lines of notations
    """
parse_solkattu(solkattu_list)
    """
        To parse solkattu phrases of percussion instrument and  generate SCAAMP list
        :param:    solkattu_list
        :param:    fit_notes_to_speed_and_thaaLa    True the notations generated will be fit to speed and thaaLa
        :return:   result     SCAMP notes list [ "Carntic Note", ["Instrument", "Volume", "Duration"], ...]
    """
```
## cplayer
```
play_notes(scamp_note_list,include_percussion_layer=False)
    """
        To play notes
        :param: scamp_note_list            SCAMP notes list [ "Carntic Note", ["Instrument", "Volume", "Duration"], ...]
                                            notes list can be obtained from cparser.parser_file function
        :param: include_percussion_layer    True: Includes Percussion according to the set ThaaLam and Jaathi
                                            ThaaLam and Jaathi can be set using thaaLa.set_thaaLam(thaaLam_Name, Jaathi_Name) 
    """
play_notations_from_file(notation_file,instrument="Flute")
    """
        To play notes from the notation file
        :param: notation_file    File containing commands, notations - see help
        :instrument:             Play using the instrument specified. 
                                    Will be overwritten by instruments if specified in the notation_file 
    """
```
## Examples:
#### lessons
```
    result = generate_lessons("sarali_varisai",fit_notes_to_speed_and_thaaLa=True)
    print(result)
    result = alankaara_varisai_from_book(fit_notes_to_speed_and_thaaLa=False, raaga_name="mohanam")
    print(result)
    result = alankaara_varisai_from_algorithm(fit_notes_to_speed_and_thaaLa=False, raaga_name="mohanam",thaaLa_name="Thriputai ThaaLa", jaathi_name="Chathusra Jaathi")
    print(result)
```
#### cplayer
```
    notation_file = "../Notes/PancharathnaKrithi-jagadhaandhakaaraka.cmn"
    play_notations_from_file(notation_file,"Sarod")
```