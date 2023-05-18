from MediaPlayer import (MPMediaItemPropertyArtist,
                         MPMediaItemPropertyPlaybackDuration,
                         MPMediaItemPropertyTitle, 
                         MPMusicPlaybackStatePaused,
                         MPMusicPlaybackStatePlaying,
                         MPMusicPlaybackStateStopped,
                         MPNowPlayingInfoCenter,
                         MPRemoteCommandCenter)
from Foundation import NSMutableDictionary
from tooltils import length
from AppKit import NSSound
from time import sleep


class audio():
    def __init__(self):
        self.cmd  = MPRemoteCommandCenter.sharedCommandCenter()
        self.info = MPNowPlayingInfoCenter.defaultCenter()

        self.cmd.playCommand()           .addTargetWithHandler_(self.play)
        self.cmd.nextTrackCommand()      .addTargetWithHandler_(self.next)
        self.cmd.previousTrackCommand()  .addTargetWithHandler_(self.previous)
        self.cmd.togglePlayPauseCommand().addTargetWithHandler_(self.playpause)
    
    def infoPlay(self):
        nowplaying_info                                      = NSMutableDictionary.dictionary()
        nowplaying_info[MPMediaItemPropertyTitle]            = self.file.split('.')[0:-1]
        nowplaying_info[MPMediaItemPropertyArtist]           = self.author
        nowplaying_info[MPMediaItemPropertyPlaybackDuration] = length(self.file)

        self.info.setNowPlayingInfo_(nowplaying_info)
        self.info.setPlaybackState_(MPMusicPlaybackStatePlaying)

    def infoPause(self):
        self.info.setPlaybackState_(MPMusicPlaybackStatePaused)
    
    def infoStop(self):
        self.info.setPlaybackState_(MPMusicPlaybackStateStopped)

    def volume(self, volume: float=100.0):
        self.song.setVolume_(volume / 100.0)

    def play(self, event, file: str, volume: float=100.0):
        self.song        = NSSound.alloc().initWithContentsOfFile_byReference_(file, True)
        self.status: str = 'playing'
        self.volume(volume)
        self.song.setLoops_(False)
        self.song.play()
        try:
            self.infoPlay()
            sleep(self.song.duration())
        except KeyboardInterrupt:
            pass

    def playpause(self, event):
        if self.status == 'paused':
            self.status == 'playing'
            self.song.resume()
        elif self.status == 'playing':
            self.status == 'paused'
            self.song.pause()

    def next(self, event):
        self.status = 'stopped'
        self.song.stop()
        ...

    def previous(self, event):
        self.status = 'stopped'
        self.song.stop()
        ...
