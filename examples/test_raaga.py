from carnatic import raaga
raaga_list = raaga.get_raaga_list()
print(raaga_list)
raagas = raaga.search_for_raaga_by_name(search_str="kalyani", is_exact=False)
print(raagas)
raagam = raaga.search_for_raaga_by_name(search_str="mohanam", is_exact=True)
raaga_id = raagam[0][0]
raaga_name = raagam[0][1]
print(raaga_id,raaga_name)
print('Mohanam - aroganam',raaga.get_aaroganam(raaga_id), 'Mohanam - avaroganam',raaga.get_avaroganam(raaga_id))
parent_raaga_id, parent_raaga_name = raaga.get_parent_raaga(raaga_id)
print('parent raaga',parent_raaga_name,parent_raaga_id)
print('Janya Raagas:',raaga.get_janya_raagas(parent_raaga_id))
raaga.write_json_file_for_raaga(model_weights_directory="../carnatic/model_weights/", json_file=raaga_name+"_corpus.json")
exit()
""" 
    Get List of melakartha raagas using multiple filter conditions
    List of raagas that have 6 notes both in aroganam and avaroganam
    or list of raaga that have M1 and M2 in aroganam and avaroganam
"""
"""
filter_options = {'Aroganam Note Count' : 6, "Avaroganam Note Count":6}
six_note_raagas = raaga.search_for_raaga_by_attributes(attribute_value_dictionary=filter_options,is_exact=True)
print(six_note_raagas)
exit()
filter_options = {'Aroganam' : "M1 M2", "Avaroganam":"M2 M1"}
spl_raagas = raaga.search_for_raaga_by_attributes(attribute_value_dictionary=filter_options,is_exact=False)
print(spl_raagas)
print(raaga.get_melakartha_raagas())
"""