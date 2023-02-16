import threading, time
from carnatic import cplayer, cparser
class PlayerThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(PlayerThread, self).__init__(*args, **kwargs)
        self.__flag = threading.Event() # The flag used to pause the thread
        self.__flag.set() # Set to True
        self.__running = threading.Event() # Used to stop the thread identification
        self.__running.set() # Set running to True
    def run(self):
        print('running')
        while self.__running.isSet():
            self.__flag.wait() # return immediately when it is True, block until the internal flag is True when it is False
            #print(time.time())
            play()
            #time.sleep(1)
    def pause(self):
        self.__flag.clear() # Set to False to block the thread
        print('paused')

    def resume(self):
        self.__flag.set() # Set to True, let the thread stop blocking
        print('resumed')

    def stop(self):
        self.__flag.set() # Resume the thread from the suspended state, if it is already suspended
        self.__running.clear() # Set to False
        print('stopped')

def play():
    print('playing',time.time())
    #"""
    #lesson_file = "Notes/PancharathnaKrithi-jagadhaandhakaaraka.cmn"
    lesson_file = "../test_notes.inp"
    scamp_note_list,_= cparser.parse_notation_file(lesson_file)
    print(scamp_note_list)
    cplayer.play_notes(scamp_note_list,False)
    #"""
if __name__ == '__main__':
    pt = PlayerThread(target=play,name='PlayingThread')
    t = 5
    pt.start()
    time.sleep(t)
    pt.pause()
    time.sleep(t)
    pt.resume()
    time.sleep(t)
    pt.stop()
    