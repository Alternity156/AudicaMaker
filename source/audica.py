from zipfile import ZipFile

import json

class desc():
    
    songID = ""
    moggSong = ""
    title = ""
    artist = ""
    midiFile = ""
    fusionSpatialized = "fusion/guns/default/drums_default_spatial.fusion"
    fusionUnspatialized = "fusion/guns/default/drums_default_sub.fusion"
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
        
    def load_desc_file(self, file):
        f = open(file, 'r')
        desc_file = json.load(f)
        self.songID = desc_file["songID"]
        self.moggSong = desc_file["moggSong"]
        self.title = desc_file["title"]
        self.artist = desc_file["artist"]
        self.midiFile = desc_file["midiFile"]
        self.fusionSpatialized = desc_file["fusionSpatialized"]
        self.fusionUnspatialized = desc_file["fusionUnspatialized"]
        self.sustainSongRight = desc_file["sustainSongRight"]
        self.sustainSongLeft = desc_file["sustainSongLeft"]
        self.fxSong = desc_file["fxSong"]
        self.tempo = desc_file["tempo"]
        self.songEndEvent = desc_file["songEndEvent"][25:]
        try:
            self.songEndPitchAdjust = desc_file["songEndPitchAdjust"]
        except:
            pass
        self.prerollSeconds = desc_file["prerollSeconds"]
        try:
            self.previewStartSeconds = desc_file["previewStartSeconds"]
        except:
            pass
        self.useMidiForCues = desc_file["useMidiForCues"]
        self.hidden = desc_file["hidden"]
        try:
            self.offset = desc_file["offset"]
        except:
            pass
        try:
            self.author = desc_file["author"]
        except:
            pass
        f.close()
        
    def save_desc_file(self, file):
        line = "{\n"
        line = line + "\t\"songID\": " + json.dumps(self.songID) + ",\n"
        line = line + "\t\"moggSong\": " + json.dumps(self.moggSong) + ",\n"
        line = line + "\t\"title\": " + json.dumps(self.title) + ",\n"
        line = line + "\t\"artist\": " + json.dumps(self.artist) + ",\n"
        line = line + "\t\"midiFile\": " + json.dumps(self.midiFile) + ",\n"
        line = line + "\t\"fusionSpatialized\": " + json.dumps(self.fusionSpatialized) + ",\n"
        line = line + "\t\"fusionUnspatialized\": " + json.dumps(self.fusionUnspatialized) + ",\n"
        line = line + "\t\"sustainSongRight\": " + json.dumps(self.sustainSongRight) + ",\n"
        line = line + "\t\"sustainSongLeft\": " + json.dumps(self.sustainSongLeft) + ",\n"
        line = line + "\t\"fxSong\": " + json.dumps(self.fxSong) + ",\n"
        line = line + "\t\"tempo\": " + json.dumps(self.tempo) + ",\n"
        line = line + "\t\"songEndEvent\": " + json.dumps("event:/song_end/song_end_" + self.songEndEvent) + ",\n"
        line = line + "\t\"songEndPitchAdjust\": " + json.dumps(self.songEndPitchAdjust) + ",\n"
        line = line + "\t\"prerollSeconds\": " + json.dumps(self.prerollSeconds) + ",\n"
        line = line + "\t\"previewStartSeconds\": " + json.dumps(self.previewStartSeconds) + ",\n"
        line = line + "\t\"useMidiForCues\": " + json.dumps(self.useMidiForCues) + ",\n"
        line = line + "\t\"hidden\": " + json.dumps(self.hidden) + ",\n"
        line = line + "\t\"offset\": " + json.dumps(self.offset) + ",\n"
        line = line + "\t\"author\": " + json.dumps(self.author) + "\n"
        line = line + "}"
        
        f = open(file, "w")
        f.write(line)
        f.close()
        

class sustain():
    
    moggPathL = ""
    moggPathR = ""
    midiPath = ""
    pansL = 0.0
    pansR = 0.0
    volsL = 0.0
    volsR = 0.0
        
    def save_file_l(self, file):
        line = "(mogg_path \"" + self.moggPathL + "\")\n"
        line = line + "(midi_path \"" + self.midiPath + "\")\n"
        line = line + "\n"
        line = line + "(tracks\n"
        line = line + "  (\n"
        line = line + "    (sustain_l 0 event:/gameplay/sustain_left)\n"
        line = line + "  )\n"
        line = line + ")\n"
        line = line + "(pans (" + str(self.pansL) + "))\n"
        line = line + "(vols (" + str(self.volsL) + "))\n"
        f = open(file, "w")
        f.write(line)
        f.close()
        
    def save_file_r(self, file):
        line = "(mogg_path \"" + self.moggPathR + "\")\n"
        line = line + "(midi_path \"" + self.midiPath + "\")\n"
        line = line + "\n"
        line = line + "(tracks\n"
        line = line + "  (\n"
        line = line + "    (sustain_r 0 event:/gameplay/sustain_right)\n"
        line = line + "  )\n"
        line = line + ")\n"
        line = line + "(pans (" + str(self.pansR) + "))\n"
        line = line + "(vols (" + str(self.volsR) + "))\n"
        f = open(file, "w")
        f.write(line)
        f.close()
        
       
class song():
    
    moggPath = ""
    midiPath = ""
    pansL = 0.0
    pansR = 0.0
    volsL = 0.0
    volsR = 0.0
        
    def save_file(self, file):
        line = "(mogg_path \"" + self.moggPath + "\")\n"
        line = line + "(midi_path \"" + self.midiPath + "\")\n"
        line = line + "\n"
        line = line + "(tracks\n"
        line = line + "  (\n"
        line = line + "    (mix (0 1) event:/gameplay/song_audio)\n"
        line = line + "  )\n"
        line = line + ")\n"
        line = line + "(pans (" + str(self.pansL) + " " + str(self.pansR) + "))\n"
        line = line + "(vols (" + str(self.volsL) + " " + str(self.volsR) + "))\n"
        f = open(file, "w")
        f.write(line)
        f.close()
        
class extras():
    
    moggPath = ""
    midiPath = ""
    pansL = 0.0
    pansR = 0.0
    volsL = 0.0
    volsR = 0.0
        
    def save_file(self, file):
        line = "(mogg_path \"" + self.moggPath + "\")\n"
        line = line + "(midi_path \"" + self.midiPath + "\")\n"
        line = line + "\n"
        line = line + "(tracks\n"
        line = line + "  (\n"
        line = line + "    (mix (0 1) event:/gameplay/song_fx_audio)\n"
        line = line + "  )\n"
        line = line + ")\n"
        line = line + "(pans (" + str(self.pansL) + " " + str(self.pansR) + "))\n"
        line = line + "(vols (" + str(self.volsL) + " " + str(self.volsR) + "))\n"
        f = open(file, "w")
        f.write(line)
        f.close()