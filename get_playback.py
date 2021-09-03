import vlc, pafy    

class Playback():
    def __init__(self, url):
        self.url = url

    def get_playback(self):
        video = pafy.new(self.url)
        best = video.getbest(preftype="mp4")
        media = vlc.MediaPlayer(best.url)
        #media.set_mrl('rtp://@224.1.1.1')
        media.play()
   
