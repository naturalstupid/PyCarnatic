from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer
import sys
class QtPlayer(QMediaPlayer):
    def __init__(self):
        super().__init__()
        self._playing_list = {}
        self._media_count = 0
        self._current_media_index = -1
        self._audio_output = QAudioOutput()
        self.setAudioOutput(self._audio_output)
    def play(self):
        if self._media_count >0 and super().playbackState() != QMediaPlayer.PlaybackState.PlayingState:
            if self._current_media_index == -1:
                self._current_media_index = 0
            media_location = list(self._playing_list.values())[self._current_media_index]
            print('playing',media_location)
            super().setSource(QUrl.fromLocalFile(media_location))
            super().play()
    def pause_resume(self):
        if self._media_count >0:
            if super().playbackState() == QMediaPlayer.PlaybackState.PlayingState:
                super().pause()
            elif super().playbackState() == QMediaPlayer.PlaybackState.PausedState:
                super().play()
    def previous(self):
        if self._media_count >0:
            self._current_media_index = (self._current_media_index+self._media_count-1)%self._media_count
            self.play()
    def next(self):
        if self._media_count >0:
            self._current_media_index = (self._current_media_index+self._media_count+1)%self._media_count
            self.play()
    def stop(self):
        if self._media_count >0 and super().playbackState() != QMediaPlayer.PlaybackState.StoppedState:
            super().stop()
    def set_playing_list(self,media_dict):
        self._playing_list = media_dict
        self._media_count = len(media_dict)
        #print('media_dict',media_dict)
    def set_playing_index(self,playing_index):
        if playing_index in range(0,self._media_count):
            self._current_media_index = playing_index
