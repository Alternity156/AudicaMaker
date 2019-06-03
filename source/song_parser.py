from zipfile import ZipFile

import os
import json

class audica_song_parser():

    audica_location = "F:\\Steam\\SteamApps\\common\\Audica"

    songs_location = "Audica_Data\\StreamingAssets\\HmxAudioAssets\\songs"

    audica_songlist = ["adrenaline.audica",
                       "boomboom.audica",
                       "breakforme.audica",
                       "collider.audica",
                       "destiny.audica",
                       "gametime.audica",
                       "golddust.audica",
                       "hr8938cephei.audica",
                       "ifeellove.audica",
                       "iwantu.audica",
                       "lazerface.audica",
                       "overtime.audica",
                       "popstars.audica",
                       "predator.audica",
                       "raiseyourweapon_noisia.audica",
                       "resistance.audica",
                       "smoke.audica",
                       "splinter.audica",
                       "synthesized.audica",
                       "thespace.audica",
                       "tutorial.audica"]

    songs = []
    
    song_ammount = 0
    
    def reset(self):
        self.songs = []
        self.song_ammount = 0
    
    def audica_path_check(self):
        
        try:
            for r, d, f in os.walk(audica_location + os.sep + songs_location):
                for file in f:
                    if "Audica.exe" in file:
                        return True
        except:
            return False
    
    def parse_all_songs(self):
    
        audica_files = []
        
        if self.audica_path_check:
            for r, d, f in os.walk(self.audica_location + os.sep + self.songs_location):
                for file in f:
                    if ".audica" in file:
                        audica_files.append(r + os.sep + file)
                    
            for file in audica_files:
                self.parse_song(file)
    
    def parse_audica_songs(self):
        
        if self.audica_path_check:
            for file in self.audica_songlist:
                f = self.audica_location + os.sep + self.songs_location + os.sep + file
                self.parse_song(f)
            
    def parse_song(self, file):
        desc = json.load(ZipFile(file).open("song.desc"))
        
        s = self.song()
        
        s.filename = file.split(os.sep)[-1:]
        
        try:
            s.beginner_cues = json.load(ZipFile(file).open("beginner.cues"))
        except:
            pass
        try:
            s.moderate_cues = json.load(ZipFile(file).open("moderate.cues"))
        except:
            pass
        try:
            s.advanced_cues = json.load(ZipFile(file).open("advanced.cues"))
        except:
            pass
        try:
            s.expert_cues = json.load(ZipFile(file).open("expert.cues"))
        except:
            pass
        
        s.songID = desc["songID"]
        s.moggSong = desc["moggSong"]
        s.title = desc["title"]
        s.artist = desc["artist"]
        s.midiFile = desc["midiFile"]
        s.fusionSpatialized = desc["fusionSpatialized"]
        try:
            s.fusionUnspatialized = desc["fusionUnspatialized"]
        except:
            pass
        s.sustainSongRight = desc["sustainSongRight"]
        s.sustainLeft = desc["sustainSongLeft"]
        s.fxSong = desc["fxSong"]
        s.tempo = desc["tempo"]
        s.songEndEvent = desc["songEndEvent"]
        try:
            s.songEndPitchAdjust = desc["songEndPitchAdjust"]
        except:
            pass
        s.prerollSeconds = desc["prerollSeconds"]
        try:
            s.previewStartSeconds = desc["previewStartSeconds"]
        except:
            pass
        s.useMidiForCues = desc["useMidiForCues"]
        s.hidden = desc["hidden"]
        try:
            s.offset = desc["offset"]
        except:
            pass
        try:
            s.author = desc["author"]
        except:
            for song in self.audica_songlist:
                if song in file:
                    s.author = "Harmonix"
        
        self.songs.append(s)
                          
        self.song_ammount = len(self.songs)
        
    class song():
        songID = ""
        moggSong = ""
        title = ""
        artist = ""
        midiFile = ""
        fusionSpatialized = ""
        fusionUnspatialized = ""
        sustainSongRight = ""
        sustainSongLeft = ""
        fxSong = ""
        tempo = 0.0
        songEndEvent = ""
        songEndPitchAdjust = 0.0
        prerollSeconds = 0.0
        previewStartSeconds = 0.0
        useMidiForCues = False
        hidden = False
        offset = 0
        author = ""
        beginner_cues = {}
        moderate_cues = {}
        advanced_cues = {}
        expert_cues = {}
        filename = ""
    
#parser = audica_song_parser()
#parser.parse_all_songs()
#for song in parser.songs:
    #print song.title + "-" + str(song.tempo) + "bpm"