# Tamil Prosody Analyzer / தமிழ் இயற்பா செயலி
This provides a python package to analyze Tamil poems and find out the poem types.  
இயற்றமிழ் என்பது நினைத்த கருத்தை உணர்த்துவதையே நோக்கமாகக் கொண்டு நடப்பது, பேச்சும், உரையும் செய்யுளும் இதில் அடங்கும். இயற்றமிழ்ச் செய்யுளை இயற்பா என்பர்.

இசைத்தமிழ் என்பது இசையின்பம் அளித்தலையே முதன்மை நோக்கமாகக் கொண்டு நடப்பது; சொற்பொருள் இன்பங்களையும் கொடுக்கக் கூடியது. இசைத்தமிழ் நூல்கள்; தேவாரம், திருவாசகம், நாலாயிரப் பனுவலில் (நாலாயிர திவ்விய பிரபந்தம்) முதலாயிரம், பெரிய திருமொழி, திருவாய்மொழி ஆகியன; திருப்புகழ் முதலியன.

Tamil poems are of two types namely:

1. இயற்பா  
1.1 வெண்பா மற்றும் வெண்பாவினம்  
1.2 ஆசிரியப்பா மற்றும் வெண்பாவினம்  
1.3 வஞ்சிப்பா மற்றும் வெண்பாவினம்  
1.4 கலிப்பா மற்றும் வெண்பாவினம்  
1.5 மருட்பா (மருள் - மயக்கம்; கலத்தல். வெண்பாவும் ஆசிரியப்பாவும் கலந்து அமைவது) <b>(Not Implemented)</b>  
2. இசைப்பா <b>(Not Implemented)</b>  
2.1 வண்ணப்பா  
2.2 சந்தப்பா  
2.2 சிந்துப்பா  
2.4 உருப்படிகள்  

This package contains five classes namely Ezhuthu, Sol, Adi, Yiyarpaa and Yaappu:
1. Ezhuthu:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; This class accepts a Tamil character and analyzes the character types. Provides methods such as is\_nedil(), is\_kuril(), is\_kutriyalugarm() etc.  
2. Sol:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; This class accepts a Tamil word (and calls internally Ezhuthu). Provides methods such as asaigaL() **Note: upper case L, thodai\_matches(with\_another\_word\_text) etc.  
3. Adi:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; This class accepts a Tamil sentence (and calls internally Sol). Provides methods such as sandha\_ozhungu(), seer\_thodai\_words() etc.  
4. Yiyarpu:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; This class accepts a Tamil Poem (and calls internally Adi). Provides methods such as sandha\_seergal(), thaLaigaL(), osaigaL(), vikarpam() etc.  
5. Yaappu:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; This class accepts a Tamil Poem (and calls internally Yiyarpu). Provides methods such as check\_for\_venpaa(), check\_for\_venpaavinam(), check\_for\_asiriyapaa() etc.  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; In addition it also accepts two optional arguments namely:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;treat\_aaydham\_as\_kuril=False/True and   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;treat\_kutriyaligaram\_as\_otru=False/True    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; It provides a method <b> analyze() </b> with two optional arguments namely:   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>poem\_type\_enum</b> and   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<b>get\_individual\_poem\_analysis=False/True</b>    

##Usage  
Sample code:  

<code>
    ty = Yiyarpa("மாதவா போதி வரதா வருளமலா\nபாதமே யோத சுரரைநீ - தீதகல\nமாயா நெறியளிப்பா யின்றன் பகலாச்சீர்த்\nதாயே யலகில்லா டாம்")  
	
	ty.analyze()  
</code>
	<b> OR </b>  <br>
<code>  	
	[poem_check, poem_analysis] =  ty.analyze(utils.POEM_TYPES.VEPAA,get_individual_poem_analysis=True)
	
	print(poem_check[0]) # print poem type   
	
</code>

There is a test code provided testing all classes and methods.  
The main function also checks whether all 1330 thirukurals  from <b>thiukural.txt</b> are of type குறள் வெண்பா  






செயலி