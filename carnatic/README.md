# PyCarnatic / Carnatic Music Guru - V1.3.0
## This package was inspired from the Java Application: [JRaaga / Carnatic Music Guru](https://sourceforge.net/projects/carnaticmusicguru/)
<br>
<br>This provides a python package to <br>
	<li>Generate Music Lessons (SaraLi, Jantai, Dhaattu, Keezh/mEl sthaayi and Alankaaram) for about 400 raagas
	<li> Generate kalpana swarams using either Markov or Deep Learning <b>(V0.7.5)</b>
	<li>Defines a notation system for carnatic music notes
		<li>- Will automatically use appropriate notes according to the melakartha
		<li>- notation for micro tones and gliding
	<li>Plays the notation file with specified raaga, micortones, gliding, instruments
		<li>Automatically generates percussion layer per specified thaaLa/jaathi combination
	<li> List of available carnatic instruments:
	<li> 	-	CARNATIC_INSTRUMENTS = ["Veena","Veena2","Flute","Sarod",]
	<li> 	-	DEFAULT_INSTRUMENTS = ["Violin","Sitar","Shenai","Piano","Guitar"]
	<li> 	-	PERCUSSION_INSTRUMENTS = ["Mridangam","EastWestMix"]

### Release History 
#### V1.3.0 
	See diff-with-0.7.5 folder for changes since V0.7.5
	UI folder with PyQt UI files added.
	Two Player SF2_LOADER and SCAMP are supported
	SF2_LOADER can pause/resume the player but does not support gamaka notations
	SCAMP Player supports gamaka notations - but does not support resume/pause player
	Instrument Thavil Added. Instrument EastWestMix removed
	
#### V0.7.6 
<li> Create JSON FILE from Aarogana and Avarogana of the raaga

#### V0.7.5 
<li> A bug in raaga.get_previous_note fixed
<li> cparser.parse_command() #S command will also set thaaLam speed to be the same
<li> cparser._get_notes_from_file() added and used in cmarkov and cdeeplearn modules
<li> cparser._arrange_notes_to_thaaLa() play_speed=settings.PLAY_SPEED argument added
<li> lessons - LESSON_TYPES changed from list to dictionary
<li> save_to_file=None argument added for methods of lessons modules
<li> lessons.generate_kalpana_swaram() function added
<li> cmarkov and cdeeplearn modules added to support generating kalpana swaram
 
## Notations
### Comments
<li> Comments start with "{"
<li> Example: { This is a comment  

### Commands
<li> Commands start with "#" followed by a number or [[<number> with closing ]]
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
<li> #N - specify Nadai - values 1 to 7 (1-1st Kalai, 2-2nd Kalai, 3-Thisra, 4-Chathusra/3rd Speed, 5-Khanda, 6-Misra, 7-Samkeerna). Example:
<li> 	#N4

### Carnatic Notes
<li> Carnatic notes can be written as S R R1 R2 etc 
<li> Or can be written in lower case with/without numbers Example: s r1, g m pd n'
<li> Note: If a raaga has both R1 and R2 or M1 and M2 etc - then you should suffix with corresponding numbers.
<li> Lower octaves should have "period"/"dot" . as a suffix. Example: S. R1. M2. etc
<li> Upper octave notes should have single quote ' or caret ^. Example: S' R1^ M1 ' etc
<li> Additional duration to notes can be using comma or semicolon. Example: s,, r;, etc
<li> Microtone notations: S>1 S>2 R1>3 - 10%, 20% 30% respectively more than the pitch of the note
<li> Similarly notations like G3<1 M2<4 have 10% 40% respectively less than the pitch of the note
<li> Gliding notes:  S / R - will glide from S to R and sustain at R for its duration
<li> Gliding notes:  M ! P - will glide down from M to P and sustain at P for its duration
<li> Shaking notes:  Suffix tilde symbol to notes to shake the note. Example: S~ R2~ P^~ etc
<li> !!! NOTE: Gliding/Shaking notes will only work with SCAMP Player !!!

## Kalpana Swaram Generation (V0.7.5)  
In this version, three new modules have been added namely, cmarkov, cmarkovn and cdeeplearn. 
Both these modules have a function called generate_notes_from_corpus.
These model functions are called by he lessons module function
generate_kalpana_swarams function
which has an argument "method" which should be either "markov" or "deeplearn". 
The kalpana swaram can be generated also either using user's own corpus files that contain note sequences OR using the lessons such saraLi, jantai, alankaaram etc. The former needs corpus_files argument and the latter instead requires raagam_name and lesson_types to be used for generating kalpana swaram.  
<b> A note of caution: This is just an experimental stuff. The notes generated may not represent the "signature of the raaga". </b>

method="markov" generates kalpana swaram using the Markov model  
method="deeplearn" generates kalpana swaram using deep learning LSTM

### cmarkov code  

```
generate_notes_from_corpus(corpus_files:list,starting_note:str, ending_note:str, length:int=32, save_to_file=None):
    """
    Generate note sequence of defined length from corpus text files
    @param corpus_files: List of corpus file paths that contain sequence of notes
    @param starting_note: Starting note (should be one of aarognam/avaroganam notes). Default=None
    @param ending_note: Ending note (should be one of aarognam/avaroganam notes). Default=None
    @param length: desired length of notes to be generated. 
            Note: Not always exact number of notes may be generated
    @param save_to_file: File name to which generated notes are to be written. Default=None
    """
```
### cmarkovn code. 
This has addtional parameter width.  

```
generate_notes_from_corpus(corpus_files,starting_note=None, ending_note=None, length:int=32, width:int=4, save_to_file=None):
    """
    Generate note sequence of defined length from corpus text files
    @param corpus_files: List of corpus file paths that contain sequence of notes
    @param starting_note: Starting note (should be one of aarognam/avaroganam notes). Default=None
    @param ending_note: Ending note (should be one of aarognam/avaroganam notes). Default=None
    @param length: desired length of notes to be generated. 
            Note: Not always exact number of notes may be generated
    @param save_to_file: File name to which generated notes are to be written. Default=None
    @param width: integer. 1 means single note pair, 2 means two-note pair (SR RG GM), 4 means four note pair (SRGM RGMD) etc.
        Avoid specifying more than 4  
    """
```
### cdeeplearn code.  
```
set_parameters(batch_size=None, number_of_epochs=None,model_weights_folder= None,
                   json_file=None, model_weights_file=None):
    """
    Set parameters of deep learning method:
    @param batch_size: Batch size for training. Default=16
    @param number_of_epochs: Default 90
    @param model_weights_folder: Default: "model_weights/"
    @param json_file: File containing dictionary of unique notes. Default:"<raagam_name>_corpus|lessons.json"
    @param model_weights_file: File containing trained weights. Default:"<raagam_name>_corpus|lessons.h5"
    """
    
generate_notes_from_corpus(corpus_files:list,starting_note:str, ending_note:str, length:int=32, save_to_file=None,perform_training=False):
    """
    Generate note sequence of defined length from corpus text files
    @param corpus_files: List of corpus file paths that contain sequence of notes
    @param starting_note: Starting note (should be one of aarognam/avaroganam notes). Default=None
    @param ending_note: Ending note (should be one of aarognam/avaroganam notes). Default=None
    @param length: desired length of notes to be generated. 
            Note: Not always exact number of notes may be generated
    @param save_to_file: File name to which generated notes are to be written. Default=None
    @param perform_training: True/False. Default = False. 
        If True, training weights are generated even if model weight file is found  
    """
```


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
<b>New to V0.7.5</b> 
 
```
generate_kalpana_swarams(method="markov", corpus_files=None, raaga_name=None, thaaLa_name=None, jaathi_name=None, 
                                          song_speed=3, save_to_file=None, \
                                          starting_note='S',ending_note=None,length=160,line_break_at=32, \
                                          arrange_notes_to_thaaLa=True,jraaga_notation=True,
                                          lesson_types_for_kalpana_swaram = ["JANTAI_VARISAI", "DHAATTU_VARISAI", "MELSTHAAYI_VARISAI", 
                                                                             "KEEZHSTHAAYI_VARISAI","ALANKAARA_VARISAI_FROM_BOOK"],
                                          perform_training=False, width=1
                                          ):
    """
            - generating kalpana swaram either from the corpus notation files
                Or from music lessons for specified raaga and thaaLa.
            @param method: method="deeplearn" will use deep learning to learn the notation - slower method
                           method="markov" will use markov chain random walk - default
            @param corpus_files: List of notation file names to be used for learning 
                If you specify corpus files you need not specify thaaLa and song speed arguments
                Instead of corpus files you can generate from music lessons in which case you should specify
                raaga, thaaLam, jaathi and song speed arguments 
            @param    raaga_name    If not specified default raaga from settings will be used
            @param    thaaLa_name   If not specified default thaaLa from settings will be used
            @param    jaathi_name   If not specified default jaathi from settings will be used
                       Use raaga.get_raaga_list() to get the list of raaga names
                       Use thaaLa.get_thaaLam_names() to get the list of thaaLa names
                       Use thaaLa.get_jaathi_names() to get the list of jaathi names
            @param    song_speed    Song Speed 1 .. 3 - default = 3
            @param    save_to_file - File name (if specified) to save the results to.
            @param    starting_note    Starting note - default = "S". 
                      If you specify raaga_name the default will be first note of arogana
            @param    ending_note    ending note - default = None
                      If you specify raaga_name the default will be last note of arogana
                      If specified ending notes are not in corpus they are randomly chosen from corpus
            @param    length    number of notes to be generated - default = 160
                      Preferably be multiple of thaLa count (avarthana)
            @param    line_break_at    insert line break at - default at thaaLa end
                      this is needed only for generating using corpus text files and
                      this argument makes sense on if arrange_notes_to_thaaLa is set to False 
            @param    arrange_notes_to_thaaLa True/False - Default = True
            @param    jraaga_notation  True/False - default True
            @param    lesson_types_for_kalpana_swaram list of lesson types that should be used to generate kalpana swarams
                      Default: ["JANTAI_VARISAI", "DHAATTU_VARISAI", "MELSTHAAYI_VARISAI", 
                                "KEEZHSTHAAYI_VARISAI","ALANKAARA_VARISAI_FROM_BOOK"]
            @param perform_training: True/False. Force perfoming training even if model weights are found. 
                    Default = False. Applicable only for method="deeplearn"
            @param width: Number of adjacent notes to be used for prediction. Only applicable for markov model
            :return:    kalpana swaram for the specified raaga/thaaLa
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

""" Example - 4
notations_file = "../carnatic/Lessons/Varnam/Kamboji_Sarasijaanbha.cmn"
notations_file = "../carnatic/Lessons/Varnam/Mohanam_Ninnukori.cmn"
result = lessons.generate_kalpana_swaram(raaga_notations_file=notations_file,starting_note='S',ending_note='D',length=160,line_break_at=16,jraaga_notation=True)
"""
""" Example - 5 - generate kalapna swaram from corpus notation files
method = "deeplearn"
cdeeplearn.set_parameters(batch_size=20, number_of_epochs=100, model_weights_folder="../carnatic/model_weights/")
raagam= "mohanam"
jraaga_notation=False
notations_files = ["../data/varnam.txt", "../data/varaveena.txt", "../data/valachi_vacchi.txt"]
result = lessons.generate_kalpana_swarams(method=method, raaga_name=raagam,
					corpus_files=notations_files,starting_note='s',ending_note='d',length=160,
					line_break_at=16,jraaga_notation=jraaga_notation)
"""
#""" Example - 6 - generate kalapna swaram from music lessons of the raga
method = "deeplearn"
perform_training = False
jraaga_notation=True
raagam= "mohanam"
thaaLa_name="Mathya"
jaathi_name="Chathusra"
cdeeplearn.set_parameters(batch_size=20, number_of_epochs=100, model_weights_folder="../carnatic/model_weights/")
result = lessons.generate_kalpana_swarams(method=method, raaga_name=raagam, thaaLa_name=thaaLa_name,
 		jaathi_name=jaathi_name,starting_note='R',ending_note='G',length=160,
 		arrange_notes_to_thaaLa=True, jraaga_notation=jraaga_notation, 
 		save_to_file="../score_output.txt", perform_training=perform_training)
#"""
print(result)
```
#### cplayer - Example
```
notation_file = settings._APP_PATH + "/Notes/PancharathnaKrithi-jagadhaandhakaaraka.cmn"
play_notations_from_file(notation_file,"Sarod")
```
#### Song - Example
```
from carnatic import settings, song, cparser
""" Example building a song from scratch ...
s = song.Song()
ss = "S R1     G2 M1 P D2 N3 S^"
#print(s._overline(ss))
#ss = ' '.join(["S.~", "R.~", "G.~", "M.~", "P.~", "D.~", "N.~", "S~", "R~", "G~", "M~",  "P~","D~", "N~", "S^~", "R^~", "G^~", "M^~", "P^~", "D^~", "N^~"])
s.set_melakartha(15)
s.set_tempo(60)
s.set_thaaLam_index(4,2)
s.add_instrument("Veena")
s.set_speed(1)
s.set_notation_type(1)
s.add_comment("This is a comment")
s.add_notes(ss)
s.play()
s.save("delme.txt")
"""
#""" Example reading a song from a notation file and play 
song_file = settings._APP_PATH + "/Notes/PancharathnaKrithi-jagadhaandhakaaraka.cmn"
s = song.Song()
s.read(song_file)
s.play(instrument="Flute",include_percussion_layer=True)
#"""
```