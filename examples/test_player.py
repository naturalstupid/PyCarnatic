from carnatic import cplayer, thaaLa, cparser, settings
thaaLa_index=4
jaathi_index=2
nadai_index=3
thaaLa.set_thaaLam_index(thaaLa_index, jaathi_index, nadai_index)
""" Example - 1 Play one avarthanam of mridangam solkattu for a thaaLa/Jaathi  """
#"""
solkattu_list = thaaLa.get_thaaLa_patterns_for_avarthanam(avarthanam_count=1,thaaLa_index=thaaLa_index,jaathi_index=jaathi_index,nadai_index=nadai_index,generate_random=True)
print(solkattu_list)
scamp_note_list = cparser.parse_solkattu(solkattu_list)
print(scamp_note_list)
# since SCAMP notes are already percussion, include_percussion_layer can be True or False does not matter
cplayer.play_notes(scamp_note_list, include_percussion_layer=False)
#"""
""" Example 2"""
"""
notation_file = settings._APP_PATH + "/Notes/PancharathnaKrithi-jagadhaandhakaaraka.cmn"
cplayer.play_notations_from_file(notation_file,"Flute",include_percussion_layer=False)
"""
""" Example 3 playing solkattu file """
"""
solkattu_file = settings._APP_PATH + "/Lessons/Percussion/mrid_lessons_8.cmn"
cplayer.play_solkattu_from_file(solkattu_file)
"""