import pygame
from pygame import mixer
import musicpy
mixer.init()
class sfplayer():
    def __init__(self,*args):
        super().__init__()
    def add_songs(self,song_list):
        pass
    def play_audio_file(self,audio_file):
        import os
        audio_file = os.path.abspath(audio_file)
        mixer.quit()
        mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
        mixer.music.load(audio_file)
        mixer.music.play(0)
        print('playing',audio_file,mixer.get_busy())
        assert mixer.get_busy()==True,"Mixer not working"
        import musicpy as mp
        while mixer.get_busy():
            print('playing')
            pygame.time.delay(10)
            pygame.event.poll()
        print('playing finished')
    def pause(self):
        mixer.music.pause()
    def resume(self):
        mixer.music.unpause()
    def stop(self):
        mixer.music.stop()

if __name__ == '__main__':
    import requests
    mp3 = requests.get('http://www.shivkumar.org/music/originals/05a-adamodi-charukesi-krithi-ssi-c01.mp3')
    temp_mp3_file='tmp/delme.mp3'
    with open(temp_mp3_file,"wb") as f:
        f.write(mp3.content)
    f.close()
    sfp = sfplayer()
    print('mixer state',mixer.get_busy())
    sfp.play_audio_file(temp_mp3_file)
    