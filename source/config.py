import json

class config():

    configFilename = "config.json"
    
    songID = ""
    title = ""
    artist = ""
    midiFile = ""
    fusionSpatialized = "fusion/guns/default/drums_default_spatial.fusion"
    fusionUnspatialized = "fusion/guns/default/drums_default_sub.fusion"
    tempo = 0.0
    songEndEvent = ""
    songEndPitchAdjust = 0.0
    prerollSeconds = 0.0
    previewStartSeconds = 0.0
    useMidiForCues = False
    hidden = False
    author = ""
    
    main_audio = ""
    main_pan_l = 0.0
    main_pan_r = 0.0
    main_vol_l = 0.0
    main_vol_r = 0.0
    
    sustain_l_audio = ""
    sustain_l_pan = 0.0
    sustain_l_vol = 0.0
    
    sustain_r_audio = ""
    sustain_r_pan = 0.0
    sustain_r_vol = 0.0
    
    extras_audio = ""
    extras_pan_l = 0.0
    extras_pan_r = 0.0
    extras_vol_l = 0.0
    extras_vol_r = 0.0
    
    beginner_cues = ""
    moderate_cues = ""
    advanced_cues = ""
    expert_cues = ""
    
    autoSongID = False
    inGameAuthor = False
    ignoreMinorErrors = False
    convertCuesToMidi = False
    
    def load_config(self):
        f = open(self.configFilename, 'r')
        desc_file = json.load(f)
        self.songID = desc_file["songID"]
        self.title = desc_file["title"]
        self.artist = desc_file["artist"]
        self.midiFile = desc_file["midiFile"]
        self.fusionSpatialized = desc_file["fusionSpatialized"]
        self.fusionUnspatialized = desc_file["fusionUnspatialized"]
        self.tempo = desc_file["tempo"]
        self.songEndEvent = desc_file["songEndEvent"]
        self.songEndPitchAdjust = desc_file["songEndPitchAdjust"]
        self.prerollSeconds = desc_file["prerollSeconds"]
        self.previewStartSeconds = desc_file["previewStartSeconds"]
        self.useMidiForCues = desc_file["useMidiForCues"]
        self.hidden = desc_file["hidden"]
        self.author = desc_file["author"]
        self.main_audio = desc_file["main_audio"]
        self.main_pan_l = desc_file["main_pan_l"]
        self.main_pan_r = desc_file["main_pan_r"]
        self.main_vol_l = desc_file["main_vol_l"]
        self.main_vol_r = desc_file["main_vol_r"]
        self.sustain_l_audio = desc_file["sustain_l_audio"]
        self.sustain_l_pan = desc_file["sustain_l_pan"]
        self.sustain_l_vol = desc_file["sustain_l_vol"]
        self.sustain_r_audio = desc_file["sustain_r_audio"]
        self.sustain_r_pan = desc_file["sustain_r_pan"]
        self.sustain_r_vol = desc_file["sustain_r_vol"]
        self.extras_audio = desc_file["extras_audio"]
        self.extras_pan_l = desc_file["extras_pan_l"]
        self.extras_pan_r = desc_file["extras_pan_r"]
        self.extras_vol_l = desc_file["extras_vol_l"]
        self.extras_vol_r = desc_file["extras_vol_r"]
        self.beginner_cues = desc_file["beginner_cues"]
        self.moderate_cues = desc_file["moderate_cues"]
        self.advanced_cues = desc_file["advanced_cues"]
        self.expert_cues = desc_file["expert_cues"]
        self.autoSongID = desc_file["autoSongID"]
        self.inGameAuthor = desc_file["inGameAuthor"]
        self.ignoreMinorErrors = desc_file["ignoreMinorErrors"]
        self.convertCuesToMidi = desc_file["convertCuesToMidi"]
        f.close()
        
    def save_config(self):
        line = "{\n"
        line = line + "\t\"songID\": " + json.dumps(self.songID) + ",\n"
        line = line + "\t\"title\": " + json.dumps(self.title) + ",\n"
        line = line + "\t\"artist\": " + json.dumps(self.artist) + ",\n"
        line = line + "\t\"midiFile\": " + json.dumps(self.midiFile) + ",\n"
        line = line + "\t\"fusionSpatialized\": " + json.dumps(self.fusionSpatialized) + ",\n"
        line = line + "\t\"fusionUnspatialized\": " + json.dumps(self.fusionUnspatialized) + ",\n"
        line = line + "\t\"tempo\": " + json.dumps(self.tempo) + ",\n"
        line = line + "\t\"songEndEvent\": " + json.dumps(self.songEndEvent) + ",\n"
        line = line + "\t\"songEndPitchAdjust\": " + json.dumps(self.songEndPitchAdjust) + ",\n"
        line = line + "\t\"prerollSeconds\": " + json.dumps(self.prerollSeconds) + ",\n"
        line = line + "\t\"previewStartSeconds\": " + json.dumps(self.previewStartSeconds) + ",\n"
        line = line + "\t\"useMidiForCues\": " + json.dumps(self.useMidiForCues) + ",\n"
        line = line + "\t\"hidden\": " + json.dumps(self.hidden) + ",\n"
        line = line + "\t\"author\": " + json.dumps(self.author) + ",\n"
        line = line + "\t\"main_audio\": " + json.dumps(self.main_audio) + ",\n"
        line = line + "\t\"main_pan_l\": " + json.dumps(self.main_pan_l) + ",\n"
        line = line + "\t\"main_pan_r\": " + json.dumps(self.main_pan_r) + ",\n"
        line = line + "\t\"main_vol_l\": " + json.dumps(self.main_vol_l) + ",\n"
        line = line + "\t\"main_vol_r\": " + json.dumps(self.main_vol_r) + ",\n"
        line = line + "\t\"sustain_l_audio\": " + json.dumps(self.sustain_l_audio) + ",\n"
        line = line + "\t\"sustain_l_pan\": " + json.dumps(self.sustain_l_pan) + ",\n"
        line = line + "\t\"sustain_l_vol\": " + json.dumps(self.sustain_l_vol) + ",\n"
        line = line + "\t\"sustain_r_audio\": " + json.dumps(self.sustain_r_audio) + ",\n"
        line = line + "\t\"sustain_r_pan\": " + json.dumps(self.sustain_r_pan) + ",\n"
        line = line + "\t\"sustain_r_vol\": " + json.dumps(self.sustain_r_vol) + ",\n"
        line = line + "\t\"extras_audio\": " + json.dumps(self.extras_audio) + ",\n"
        line = line + "\t\"extras_pan_l\": " + json.dumps(self.extras_pan_l) + ",\n"
        line = line + "\t\"extras_pan_r\": " + json.dumps(self.extras_pan_r) + ",\n"
        line = line + "\t\"extras_vol_l\": " + json.dumps(self.extras_vol_l) + ",\n"
        line = line + "\t\"extras_vol_r\": " + json.dumps(self.extras_vol_r) + ",\n"
        line = line + "\t\"beginner_cues\": " + json.dumps(self.beginner_cues) + ",\n"
        line = line + "\t\"moderate_cues\": " + json.dumps(self.moderate_cues) + ",\n"
        line = line + "\t\"advanced_cues\": " + json.dumps(self.advanced_cues) + ",\n"
        line = line + "\t\"expert_cues\": " + json.dumps(self.expert_cues) + ",\n"
        line = line + "\t\"autoSongID\": " + json.dumps(self.autoSongID) + ",\n"
        line = line + "\t\"inGameAuthor\": " + json.dumps(self.inGameAuthor) + ",\n"
        line = line + "\t\"ignoreMinorErrors\": " + json.dumps(self.ignoreMinorErrors) + ",\n"
        line = line + "\t\"convertCuesToMidi\": " + json.dumps(self.convertCuesToMidi) + "\n"
        line = line + "}"
        
        f = open(self.configFilename, "w")
        f.write(line)
        f.close()
        