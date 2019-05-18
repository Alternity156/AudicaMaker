from mutagen.oggvorbis import OggVorbis

import os

class errorChecker():

    ## FILES
    beginner_cues = ""
    moderate_cues = ""
    advanced_cues = ""
    expert_cues = ""
    midi = ""
    main_audio = ""
    extras_audio = ""
    sustain_l_audio = ""
    sustain_r_audio = ""
    
    main_pan_l = 0.0
    main_pan_r = 0.0
    main_vol_l = 0.0
    main_vol_r = 0.0
    main_lenght = 0.0
    main_channels = 0
    main_bitrate = 0
    main_sample_rate = 0
    
    sustain_l_pan = 0.0
    sustain_l_vol = 0.0
    sustain_l_lenght = 0.0
    sustain_l_channels = 0
    sustain_l_bitrate = 0
    sustain_l_sample_rate = 0
    
    sustain_r_pan = 0.0
    sustain_r_vol = 0.0
    sustain_r_lenght = 0.0
    sustain_r_channels = 0
    sustain_r_bitrate = 0
    sustain_r_sample_rate = 0
    
    extras_pan_l = 0.0
    extras_pan_r = 0.0
    extras_vol_l = 0.0
    extras_vol_r = 0.0
    extras_lenght = 0.0
    extras_channels = 0
    extras_bitrate = 0
    extras_sample_rate = 0
    
    songID = ""
    title = ""
    artist = ""
    fusionSpatialized = "fusion/guns/default/drums_default_spatial.fusion"
    fusionUnspatialized = "fusion/guns/default/drums_default_sub.fusion"
    tempo = 0.0
    songEndEvent = ""
    songEndPitchAdjust = 0.0
    prerollSeconds = 0.0
    previewStartSeconds = 0.0
    useMidiForCues = False
    hidden = False
    offset = 0
    author = ""
    
    autoSongID = False
    inGameAuthor = False
    ignoreMinorErrors = False
    midiToCues = False
    cuesToMidi = False
    
    minorErrors = []
    majorErrors = []
    
    audio_to_convert = []
    audio_to_silence = []
    
    def reset(self):
        self.minorErrors = []
        self.majorErrors = []
        self.audio_to_convert = []
        self.audio_to_silence = []
    
    def check_desc(self):
        if self.autoSongID == False:
            if self.songID == "":
                self.majorErrors.append("songID field must not be empty.")
        if self.title == "":
            self.majorErrors.append("Song Title field must not be empty.")
        if self.artist == "":
            self.majorErrors.append("Song Artist field must not be empty.")
        if isinstance(self.tempo, float) == False:
            self.majorErrors.append("Song Tempo must be float.")
        if self.tempo <= 0.0:
            self.majorErrors.append("Tempo must be higher than 0.")
        if self.songEndEvent not in ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]:
            self.majorErrors.append("Only \"A, A#, B, C, C#, D, D#, E, F, F#, G, G#\"")
            self.majorErrors.append("are allowed as End Event Key.")
        if isinstance(self.songEndPitchAdjust, float) == False:
            self.majorErrors.append("End Pitch Adjust must be float.")
        if isinstance(self.prerollSeconds, float) == False:
            self.majorErrors.append("Preroll Seconds must be float.")
        if self.prerollSeconds < 0.0:
            self.majorErrors.append("Preroll Seconds must be positive.")
        if isinstance(self.previewStartSeconds, float) == False:
            self.majorErrors.append("Preview Start Seconds must be float.")
        if self.previewStartSeconds < 0.0:
            self.majorErrors.append("Preview Start Seconds must be positive.")
        if isinstance(self.offset, int) == False:
            self.majorErrors.append("Offset must be integer value.")
        if self.author == "":
            self.majorErrors.append("Author(s) field is empty.")
        if self.hidden == True:
            self.minorErrors.append("Hidden is turned on, song will not show up in the song list.")
        if self.ignoreMinorErrors == True:
            self.minorErrors = []
    
    def check_data(self):
        midi = self.midi
        cues = [self.beginner_cues, self.moderate_cues, self.advanced_cues, self.expert_cues]
        checks = []
        if self.useMidiForCues == False:
            if os.path.isfile(midi) == False:
                self.minorErrors.append("MIDI file does not exist.")
            for file in cues:
                if os.path.isfile(file):
                    checks.append(True)
                else:
                    checks.append(False)
            if checks[0] == False and checks[1] == False and checks[2] == False and checks[3] == False:
                self.majorErrors.append("No cues file exists, need at least one.")
                self.majorErrors.append("If you are using MIDI for cues you must tick the checkbox.")
            else:
                if checks[0] == False:
                    self.minorErrors.append("Beginner cues does not exist.")
                if checks[1] == False:
                    self.minorErrors.append("Moderate cues does not exist.")
                if checks[2] == False:
                    self.minorErrors.append("Advanced cues does not exist.")
                if checks[3] == False:
                    self.minorErrors.append("Expert cues does not exist.")
        else:
            if os.path.isfile(midi) == False:
                self.majorErrors.append("MIDI file does not exist.")
        if self.ignoreMinorErrors == True:
            self.minorErrors = []
        return checks
    
    def check_audio(self):
        files = [self.main_audio, self.extras_audio, self.sustain_l_audio, self.sustain_r_audio]
        pans_and_vols = [self.main_pan_l, self.main_pan_r, self.main_vol_l, self.main_vol_r, self.sustain_l_pan, self.sustain_l_vol, self.sustain_r_pan, self.sustain_r_vol, self.extras_pan_l, self.extras_pan_r, self.extras_vol_l, self.extras_vol_r]
        checks = [] # 0: file exists (bool)
                    # 1: file is mogg (bool)
                    # 2: file is ogg (bool)
        for file in files:
            file_checks = []
            if os.path.isfile(file):
                file_checks.append(True)
                if file[-5:] == ".mogg":
                    file_checks.append(True)
                else:
                    file_checks.append(False)
                if file[-4:] == ".ogg":
                    file_checks.append(True)
                else:
                    file_checks.append(False)
                if file_checks[1] == False and file_checks[2] == False:
                    self.minorErrors.append("Only OGG and MOGG audio is supported.")
            else:
                file_checks.append(False)
                file_checks.append(False)
                file_checks.append(False)
            checks.append(file_checks)
        for data in pans_and_vols:
            if isinstance(data, float) == False:
                self.majorErrors.append("All Pans and Vols must be float values.")
                break
        if checks[0][0] == False:
            self.majorErrors.append("Main audio does not exist.")
        if checks[1][0] == False:
            self.minorErrors.append("Extras audio does not exist.")
            self.audio_to_silence.append(["_extras", self.extras_audio])
        if checks[2][0] == False:
            self.minorErrors.append("Left sustain audio does not exist.")
            self.audio_to_silence.append(["_sustain_l", self.sustain_l_audio])
        if checks[3][0] == False:
            self.minorErrors.append("Right sustain audio does not exist.")
            self.audio_to_silence.append(["_sustain_r", self.sustain_r_audio])
        if checks[0][2] == True:
            try:
                oggInfo = self.ogg_info(self.main_audio)
                self.main_lenght = oggInfo[0]
                self.main_channels = oggInfo[1]
                self.main_bitrate = oggInfo[2]
                self.main_sample_rate = oggInfo[3]
                self.audio_to_convert.append(["song", self.main_audio])
                if self.main_channels != 2:
                    self.minorErrors.append("Main audio does not have 2 channels.")
            except:
                self.majorErrors.append("Error while reading " + self.main_audio)
        if checks[1][2] == True:
            try:
                oggInfo = self.ogg_info(self.extras_audio)
                self.extras_lenght = oggInfo[0]
                self.extras_channels = oggInfo[1]
                self.extras_bitrate = oggInfo[2]
                self.extras_sample_rate = oggInfo[3]
                self.audio_to_convert.append(["_extras", self.extras_audio])
                if self.extras_channels != 2:
                    self.minorErrors.append("Extras audio does not have 2 channels.")
            except:
                self.majorErrors.append("Error while reading " + self.extras_audio)
        if checks[2][2] == True:
            try:
                oggInfo = self.ogg_info(self.sustain_l_audio)
                self.sustain_l_lenght = oggInfo[0]
                self.sustain_l_channels = oggInfo[1]
                self.sustain_l_bitrate = oggInfo[2]
                self.sustain_l_sample_rate = oggInfo[3]
                self.audio_to_convert.append(["_sustain_l", self.sustain_l_audio])
                if self.sustain_l_channels != 1:
                    self.minorErrors.append("Left sustain audio does not have 1 channel.")
            except:
                self.majorErrors.append("Error while reading " + self.sustain_l_audio)
        if checks[3][2] == True:
            try:
                oggInfo = self.ogg_info(self.sustain_r_audio)
                self.sustain_r_lenght = oggInfo[0]
                self.sustain_r_channels = oggInfo[1]
                self.sustain_r_bitrate = oggInfo[2]
                self.sustain_r_sample_rate = oggInfo[3]
                self.audio_to_convert.append("_sustain_r", self.sustain_r_audio)
                if self.sustain_r_channels != 1:
                    self.minorErrors.append("Right sustain audio does not have 1 channel.")
            except:
                self.majorErrors.append("Error while reading " + self.sustain_r_audio)
        if self.ignoreMinorErrors == True:
            self.minorErrors = []
        return checks
        
    def ogg_info(self, ogg_file):
        f = OggVorbis(ogg_file)
        length = f.info.length #length in seconds
        channels = f.info.channels
        bitrate = f.info.bitrate
        sample_rate = f.info.sample_rate
        return [length, channels, bitrate, sample_rate]
