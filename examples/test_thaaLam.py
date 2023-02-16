from carnatic import thaaLa, settings
""" Generate Beat Patterns 9beat-7beat-5beat-4beat """
thaaLa_index = 7
jaathi_index = 2
nadai_index = 2 #1=chathusram 2 = th
settings.THAALAM_SPEED = 3
""" Example - 1
print(thaaLa.total_beat_count(thaaLa_index, jaathi_index))
print(thaaLa.total_subbeat_count(thaaLa_index, jaathi_index, nadai_index))
"""
""" Example - 2
tp = thaaLa.get_thaaLa_patterns_for_beat_string(thaaLa_beat_string="9754",generate_random=True)
print(tp)
"""
#""" Example - 3 Generate beat pattern for specific thaala jaathi nadai combination
tp = thaaLa.get_thaaLa_patterns_for_thaaLa_jaathi_nadai(thaaLa_index=thaaLa_index,jaathi_index=jaathi_index,nadai_index=nadai_index,generate_random=True)
print(tp)
#"""
""" Example-4 Generate beat pattern for specified number of avarthanam
tp = thaaLa.get_thaaLa_patterns_for_avarthanam(avarthanam_count=2,thaaLa_index=4,jaathi_index=2,nadai_index=2,generate_random=True)
print(tp)
"""