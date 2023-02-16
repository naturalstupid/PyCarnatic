from carnatic import lessons, cdeeplearn, raaga, settings, thaaLa
""" Example - 1
raagam = "mohanam" # "KanakAngi"
#thaaLa_name=settings.THAALA_NAMES.MATHYA
#jaathi_name=settings.JAATHI_NAMES.CHATHUSRA
result = lessons.generate_lessons("melsthaayi_varisai",arrange_notes_to_speed_and_thaaLa=True, raaga_name=raagam)#,thaaLa_name=thaaLa_name,jaathi_name=jaathi_name)
"""
""" Example - 2
thaaLa_name="ata"
jaathi_name="misra"
result = lessons.alankaara_varisai_from_book(arrange_notes_to_speed_and_thaaLa=True, raaga_name="mohanam",thaaLa_name=thaaLa_name,jaathi_name=jaathi_name)
"""
""" Example - 3
thaaLa_name="ata"
jaathi_name="misra"
result =lessons.alankaara_varisai_from_algorithm(arrange_notes_to_speed_and_thaaLa=True, raaga_name="mohanam",thaaLa_name=thaaLa_name,jaathi_name=jaathi_name)
"""
""" Example - 4
notations_file = "../carnatic/Lessons/Varnam/Kamboji_Sarasijaanbha.cmn"
notations_file = "../carnatic/Lessons/Varnam/Mohanam_Ninnukori.cmn"
result = lessons.generate_kalpana_swaram(raaga_notations_file=notations_file,starting_note='S',ending_note='D',length=160,line_break_at=16,jraaga_notation=True)
"""
#""" Example - 5 - generate kalapna swaram from corpus notation files
thaaLa_index=settings.THAALA_NAMES.MATHYA
jaathi_index=settings.JAATHI_NAMES.CHATHUSRA
nadai_index=settings.NADAI_NAMES.THISRA
#thaaLa.set_thaaLam(thaaLa_index, jaathi_index, nadai_index)
#print(thaaLa.get_thaaLa_positions(thaaLa_index, jaathi_index, as_string=True))
method = "markov"
if method == "deeplearn":
    cdeeplearn.set_parameters(batch_size=20, number_of_epochs=100, model_weights_folder="../carnatic/model_weights/")
raagam= "mohanam"
jraaga_notation=False
notations_files = ["../data/varnam.txt", "../data/varaveena.txt", "../data/valachi_vacchi.txt"]
result = lessons.generate_kalpana_swarams(method=method, raaga_name=raagam, corpus_files=notations_files,
                                          starting_note='s',ending_note='p',
                                          jraaga_notation=jraaga_notation, save_to_file="../score_output.txt",
                                          width=1,thaaLa_index=thaaLa_index,jaathi_index=jaathi_index,nadai_index=nadai_index)
#"""
""" Example - 6 - generate kalapna swaram from music lessons of the raga
method = "markov"
lesson_types_for_kalpana_swaram=["ALANKAARA_VARISAI_FROM_BOOK"]
perform_training = False
jraaga_notation=True
raagam= "mohanam"
thaaLa_name="Mathya"
jaathi_name="Chathusra"
if method == "deeplearn":
    cdeeplearn.set_parameters(batch_size=20, number_of_epochs=100, model_weights_folder="../carnatic/model_weights/")
result = lessons.generate_kalpana_swarams(method=method, raaga_name=raagam, thaaLa_name=thaaLa_name, jaathi_name=jaathi_name,
                                            starting_note="S R2",ending_note="G3 P", length=160,arrange_notes_to_thaaLa=True,
                                            jraaga_notation=jraaga_notation, save_to_file="../score_output.txt",
                                            perform_training=perform_training,width=2)
"""
""" Example - 7 - Generate kalpana swaram for a list of raagas and their varnam files
raaga_file_dictionary = {"mohanam":"../carnatic/Lessons/Varnam/Mohanam_Ninnukori.cmn",
                        #"Bhairavi":"../carnatic/Lessons/Varnam/Bhairavi_Viriboni.cmn", ##notation has ( and )
                        #"Begada":"../carnatic/Lessons/Varnam/Begada_indha_chalamu.cmn",
                        #"Hamsadhwani":"../carnatic/Lessons/Varnam/Hamsadhvani_Jalajaakshi.cmn",
                        #"Abhogi":"../carnatic/Lessons/Varnam/abhogi_evvari_bodhana.cmn",
                        #"SAranga":"../carnatic/Lessons/Varnam/Saaranga_indha_modi.cmn",
                        #"Kaanada":"../carnatic/Lessons/Varnam/Kaanada_NinneKoriyunnadhi.cmn",
                        #"Arabhi":"../carnatic/Lessons/Varnam/Aarabi_Sarasija.cmn",
                        }
method = "deeplearn"
lesson_types_for_kalpana_swaram=["ALANKAARA_VARISAI_FROM_BOOK"]
perform_training = True
jraaga_notation=True
thaaLa_name="Mathya"
jaathi_name="Chathusra"
width = 4 #This is same as chord_length in deep learning model
filter_options = {'Aroganam Note Count' : 8, "Avaroganam Note Count":8}
sampoorna_raagas = raaga.search_for_raaga_by_attributes(attribute_value_dictionary=filter_options,is_exact=True)
for raagam in raaga_file_dictionary.keys():
#for _,raagam in sampoorna_raagas:
    save_to_file = raagam+"_kalpana_swaram.txt"
    print("Creating kalpana swaram for raagam: "+raagam+" ...")
    corpus_file = [raaga_file_dictionary[raagam]]
    if method == "deeplearn":
        raaga.write_json_file_for_raaga(model_weights_folder="../carnatic/model_weights/",json_file=raagam+"_corpus.json")
        cdeeplearn.set_parameters(batch_size=20, number_of_epochs=100, model_weights_folder="../carnatic/model_weights/",
                                      json_file=raagam+"_corpus.json", model_weights_file=raagam+"_corpus.h5",chord_length=width)
        #  NOTE: chord_length=width argument is specific to DEEPLEARN method 
        result = lessons.generate_kalpana_swarams(method=method, corpus_files=corpus_file, raaga_name=raagam, thaaLa_name=thaaLa_name, jaathi_name=jaathi_name,
                    starting_note="R",ending_note="D", length=160,arrange_notes_to_thaaLa=True,
                    jraaga_notation=jraaga_notation, save_to_file=save_to_file,
                    perform_training=perform_training)
    else:
        #  NOTE: width=width argument is specific to MARKOV method
        result = lessons.generate_kalpana_swarams(method=method, corpus_files=corpus_file, raaga_name=raagam, thaaLa_name=thaaLa_name, jaathi_name=jaathi_name,
            starting_note=None,ending_note=None, length=160,arrange_notes_to_thaaLa=True,
            jraaga_notation=jraaga_notation, save_to_file=save_to_file,
            perform_training=perform_training, width=width)

    print("kalpana swaram for raagam: "+raagam+" saved in "+save_to_file)
"""
print(result)
