import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.filechooser import FileChooserListView
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.config import Config

from threading import Thread
from subprocess import check_output
from zipfile import ZipFile

from config import config
from audica import desc, sustain, song, extras
from error_checker import errorChecker
from midi_handler import make_midi_for_bpm

import re
import os
import shutil
import time
import datetime

Config.set('graphics', 'fullscreen', 0)
Config.set('graphics', 'borderless', 0)
Config.set('graphics', 'height', 576)
Config.set('graphics', 'width', 1024)
Config.set('graphics','resizable',0)
Config.write()

class KeyInput(TextInput):

    def insert_text(self, substring, from_undo=False):
        s = substring.upper()
        text = self.text + s
        if text in ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]:
            return super(KeyInput, self).insert_text(s, from_undo=from_undo)

class IntInput(TextInput):

    pat = re.compile('[^0-9]')
    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        s = re.sub(pat, '', substring)
        if substring == "-":
            s = substring
        return super(IntInput, self).insert_text(s, from_undo=from_undo)

class FloatInput(TextInput):

    pat = re.compile('[^0-9]')
    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        if substring == "-":
            s = substring
        return super(FloatInput, self).insert_text(s, from_undo=from_undo)

class MainApp(FloatLayout):

    title = "Audica Maker"
    value = os.getcwd()

    ## AUDIO

    audioLabel = Label(text="AUDIO", pos=(-465,275), bold=True, font_size=30)
    
    mainAudioLabel = Label(text="Main Audio File", pos=(-458,255))
    mainAudioInput = TextInput(multiline=False, pos=(1,507), size_hint=(.2,.05))
    
    mainAudioLeftPanLabel = Label(text="Pan L", pos=(-285,255))
    mainAudioLeftPanInput = FloatInput(text="0.0", multiline=False, pos=(208,507), size_hint=(.04,.05))
    
    mainAudioRightPanLabel = Label(text="Pan R", pos=(-243,255))
    mainAudioRightPanInput = FloatInput(text="0.0", multiline=False, pos=(250,507), size_hint=(.04,.05))
    
    mainAudioLeftVolLabel = Label(text="Vol L", pos=(-201,255))
    mainAudioLeftVolInput = FloatInput(text="0.0", multiline=False, pos=(292,507), size_hint=(.04,.05))
    
    mainAudioRightVolLabel = Label(text="Vol R", pos=(-159,255))
    mainAudioRightVolInput = FloatInput(text="0.0", multiline=False, pos=(334,507), size_hint=(.04,.05))
    
    extrasAudioLabel = Label(text="Extras Audio File", pos=(-454,210))
    extrasAudioInput = TextInput(multiline=False, pos=(1,462), size_hint=(.2,.05))
    
    extrasAudioLeftPanLabel = Label(text="Pan L", pos=(-285,210))
    extrasAudioLeftPanInput = FloatInput(text="0.0", multiline=False, pos=(208,462), size_hint=(.04,.05))
    
    extrasAudioRightPanLabel = Label(text="Pan R", pos=(-243,210))
    extrasAudioRightPanInput = FloatInput(text="0.0", multiline=False, pos=(250,462), size_hint=(.04,.05))
    
    extrasAudioLeftVolLabel = Label(text="Vol L", pos=(-201,210))
    extrasAudioLeftVolInput = FloatInput(text="0.0", multiline=False, pos=(292,462), size_hint=(.04,.05))
    
    extrasAudioRightVolLabel = Label(text="Vol R", pos=(-159,210))
    extrasAudioRightVolInput = FloatInput(text="0.0", multiline=False, pos=(334,462), size_hint=(.04,.05))
    
    leftSustainAudioLabel = Label(text="Left Sustain Audio File", pos=(-435,165))
    leftSustainAudioInput = TextInput(multiline=False, pos=(1,417), size_hint=(.2,.05))
    
    leftSustainAudioPanLabel = Label(text="Pan", pos=(-264,165))
    leftSustainAudioPanInput = FloatInput(text="0.0", multiline=False, pos=(229,417), size_hint=(.04,.05))
    
    leftSustainAudioVolLabel = Label(text="Vol", pos=(-180,165))
    leftSustainAudioVolInput = FloatInput(text="0.0", multiline=False, pos=(312,417), size_hint=(.04,.05))
    
    rightSustainAudioLabel = Label(text="Right Sustain Audio File", pos=(-430,120))
    rightSustainAudioInput = TextInput(multiline=False, pos=(1,372), size_hint=(.2,.05))
    
    rightSustainAudioPanLabel = Label(text="Pan", pos=(-264,120))
    rightSustainAudioPanInput = FloatInput(text="0.0", multiline=False, pos=(229,372), size_hint=(.04,.05))
    
    rightSustainAudioVolLabel = Label(text="Vol", pos=(-180,120))
    rightSustainAudioVolInput = FloatInput(text="0.0", multiline=False, pos=(312,372), size_hint=(.04,.05))
    
    ## DATA
    
    dataLabel = Label(text="DATA", pos=(-472,70), bold=True, font_size=30)
    
    midiFileLabel = Label(text="MIDI File", pos=(-480,49))
    midiFileInput = TextInput(multiline=False, pos=(1,301), size_hint=(.2,.05))
    
    beginnerCuesLabel = Label(text="Beginner Cues File", pos=(-448,4))
    beginnerCuesInput = TextInput(multiline=False, pos=(1,256), size_hint=(.2,.05))
    
    moderateCuesLabel = Label(text="Moderate Cues File", pos=(-445,-41))
    moderateCuesInput = TextInput(multiline=False, pos=(1,211), size_hint=(.2,.05))
    
    advancedCuesLabel = Label(text="Advanced Cues File", pos=(-445,-86))
    advancedCuesInput = TextInput(multiline=False, pos=(1,166), size_hint=(.2,.05))
    
    expertCuesLabel = Label(text="Expert Cues File", pos=(-456,-131))
    expertCuesInput = TextInput(multiline=False, pos=(1,121), size_hint=(.2,.05))
    
    ## DESC
    
    descLabel = Label(text="DESC", pos=(-98,275), bold=True, font_size=30)
    
    songIDLabel = Label(text="songID", pos=(-110,255))
    songIDInput = TextInput(multiline=False, pos=(376,507), size_hint=(.2,.05))
    
    titleLabel = Label(text="Song Title", pos=(-100,210))
    titleInput = TextInput(multiline=False, pos=(376,462), size_hint=(.2,.05))
    
    artistLabel = Label(text="Song Artist", pos=(-97,165))
    artistInput = TextInput(multiline=False, pos=(376,417), size_hint=(.2,.05))
    
    tempoLabel = Label(text="Song Tempo", pos=(-92,120))
    tempoInput = FloatInput(text="0.0", multiline=False, pos=(376,372), size_hint=(.2,.05))
    
    endEventLabel = Label(text="End Event Key", pos=(-88,75))
    endEventInput = KeyInput(text="A", multiline=False, pos=(376,327), size_hint=(.2,.05))
    
    endPitchAdjustLabel = Label(text="End Pitch Adjust", pos=(-80,30))
    endPitchAdjustInput = FloatInput(text="0.0", multiline=False, pos=(376,282), size_hint=(.2,.05))
    
    prerollSecondsLabel = Label(text="Preroll Seconds", pos=(-82,-15))
    prerollSecondsInput = FloatInput(text="0.0", multiline=False, pos=(376,237), size_hint=(.2,.05))
    
    previewStartSecondsLabel = Label(text="Preview Start Seconds", pos=(-60,-60))
    previewStartSecondsInput = FloatInput(text="0.0", multiline=False, pos=(376,192), size_hint=(.2,.05))
    
    offsetLabel = Label(text="Offset (Only used by Edica)", pos=(-45,-105))
    offsetInput = IntInput(text="0", multiline=False, pos=(376,147), size_hint=(.2,.05))
    
    authorLabel = Label(text="Map Author(s)", pos=(-87,-150))
    authorInput = TextInput(multiline=False, pos=(376,102), size_hint=(.2,.05))
    
    useMidiForCuesLabel = Label(text="Use MIDI for Cues", pos=(-222,68))
    useMidiForCuesCheckbox = CheckBox(pos=(205,350), size_hint=(.025,.025))
    
    hiddenLabel = Label(text="Hidden", pos=(-260,44))
    hiddenCheckbox = CheckBox(pos=(205,325), size_hint=(.025,.025))
    
    ## OPTIONS
    
    autoSongIDLabel = Label(text="Automatic songID", pos=(-222,20))
    autoSongIDCheckbox = CheckBox(pos=(205,300), size_hint=(.025,.025))
    
    inGameAuthorLabel = Label(text="In-game Author", pos=(-232,-5))
    inGameAuthorCheckbox = CheckBox(pos=(205,275), size_hint=(.025,.025))
    
    ignoreMinorErrorsLabel = Label(text="Ignore Minor Errors", pos=(-218,-30))
    ignoreMinorErrorsCheckbox = CheckBox(pos=(205,250), size_hint=(.025,.025))
    
    convertMidiToCuesLabel = Label(text="Convert MIDI to Cues", pos=(-212,-55))
    convertMidiToCuesCheckbox = CheckBox(pos=(205,225), size_hint=(.025,.025))
    
    convertCuesToMidiLabel = Label(text="Convert Cues to MIDI", pos=(-212,-80))
    convertCuesToMidiCheckbox = CheckBox(pos=(205,200), size_hint=(.025,.025))
    
    ## BUTTONS
    
    saveButton = Button(text="Save Project", pos=(1,1), size_hint=(.2,.1))
    loadButton = Button(text="Load Project", pos=(1,60), size_hint=(.2,.1))
    importDescButton = Button(text="Import .desc", pos=(376,1), size_hint=(.2,.1725))
    makeAudicaButton = Button(text="Make .audica", pos=(205,1), size_hint=(.16725,.1725))
    
    ## LOGBOX
    
    messageTextbox = TextInput(multiline=True, pos=(582,3), size_hint=(.43,.99), readonly=True)
    
    ## 
    
    current_message_row = 0
    
    config_file = config()
    desc_file = desc()
    sustain_file = sustain()
    song_file = song()
    extras_file = extras()
    error_checker = errorChecker()

    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        
        self.add_widget(self.audioLabel)
        self.add_widget(self.mainAudioLabel)
        self.add_widget(self.mainAudioInput)
        self.add_widget(self.mainAudioLeftPanLabel)
        self.add_widget(self.mainAudioLeftPanInput)
        self.add_widget(self.mainAudioRightPanLabel)
        self.add_widget(self.mainAudioRightPanInput)
        self.add_widget(self.mainAudioLeftVolLabel)
        self.add_widget(self.mainAudioLeftVolInput)
        self.add_widget(self.mainAudioRightVolLabel)
        self.add_widget(self.mainAudioRightVolInput)
        self.add_widget(self.extrasAudioLabel)
        self.add_widget(self.extrasAudioInput)
        self.add_widget(self.extrasAudioLeftPanLabel)
        self.add_widget(self.extrasAudioLeftPanInput)
        self.add_widget(self.extrasAudioRightPanLabel)
        self.add_widget(self.extrasAudioRightPanInput)
        self.add_widget(self.extrasAudioLeftVolLabel)
        self.add_widget(self.extrasAudioLeftVolInput)
        self.add_widget(self.extrasAudioRightVolLabel)
        self.add_widget(self.extrasAudioRightVolInput)
        self.add_widget(self.leftSustainAudioLabel)
        self.add_widget(self.leftSustainAudioInput)
        self.add_widget(self.leftSustainAudioPanLabel)
        self.add_widget(self.leftSustainAudioPanInput)
        self.add_widget(self.leftSustainAudioVolLabel)
        self.add_widget(self.leftSustainAudioVolInput)
        self.add_widget(self.rightSustainAudioLabel)
        self.add_widget(self.rightSustainAudioInput)
        self.add_widget(self.rightSustainAudioPanLabel)
        self.add_widget(self.rightSustainAudioPanInput)
        self.add_widget(self.rightSustainAudioVolLabel)
        self.add_widget(self.rightSustainAudioVolInput)
        self.add_widget(self.dataLabel)
        self.add_widget(self.midiFileLabel)
        self.add_widget(self.midiFileInput)
        self.add_widget(self.beginnerCuesLabel)
        self.add_widget(self.beginnerCuesInput)
        self.add_widget(self.moderateCuesLabel)
        self.add_widget(self.moderateCuesInput)
        self.add_widget(self.advancedCuesLabel)
        self.add_widget(self.advancedCuesInput)
        self.add_widget(self.expertCuesLabel)
        self.add_widget(self.expertCuesInput)
        self.add_widget(self.descLabel)
        self.add_widget(self.songIDLabel)
        self.add_widget(self.songIDInput)
        self.add_widget(self.titleLabel)
        self.add_widget(self.titleInput)
        self.add_widget(self.artistLabel)
        self.add_widget(self.artistInput)
        self.add_widget(self.tempoLabel)
        self.add_widget(self.tempoInput)
        self.add_widget(self.endEventLabel)
        self.add_widget(self.endEventInput)
        self.add_widget(self.endPitchAdjustLabel)
        self.add_widget(self.endPitchAdjustInput)
        self.add_widget(self.prerollSecondsLabel)
        self.add_widget(self.prerollSecondsInput)
        self.add_widget(self.previewStartSecondsLabel)
        self.add_widget(self.previewStartSecondsInput)
        self.add_widget(self.offsetLabel)
        self.add_widget(self.offsetInput)
        self.add_widget(self.authorLabel)
        self.add_widget(self.authorInput)
        self.add_widget(self.useMidiForCuesLabel)
        self.add_widget(self.useMidiForCuesCheckbox)
        self.add_widget(self.hiddenLabel)
        self.add_widget(self.hiddenCheckbox)
        self.add_widget(self.autoSongIDLabel)
        self.add_widget(self.autoSongIDCheckbox)
        self.add_widget(self.inGameAuthorLabel)
        self.add_widget(self.inGameAuthorCheckbox)
        self.add_widget(self.ignoreMinorErrorsLabel)
        self.add_widget(self.ignoreMinorErrorsCheckbox)
        #self.add_widget(self.convertMidiToCuesLabel)
        #self.add_widget(self.convertMidiToCuesCheckbox)
        #self.add_widget(self.convertCuesToMidiLabel)
        #self.add_widget(self.convertCuesToMidiCheckbox)
        self.add_widget(self.saveButton)
        self.add_widget(self.loadButton)
        self.add_widget(self.importDescButton)
        self.add_widget(self.makeAudicaButton)
        self.add_widget(self.messageTextbox)
        
        self.loadButton.bind(on_release=lambda i:self._create_popup(i))
        self.saveButton.bind(on_release=lambda i:self.save_project())
        self.importDescButton.bind(on_release=lambda i:self._create_popup(i))
        self.makeAudicaButton.bind(on_release=lambda i:Thread(target=self.save_audica).start())
        
        self.mainAudioInput.bind(on_double_tap=self.on_double_click)
        self.extrasAudioInput.bind(on_double_tap=self.on_double_click)
        self.leftSustainAudioInput.bind(on_double_tap=self.on_double_click)
        self.rightSustainAudioInput.bind(on_double_tap=self.on_double_click)
        self.midiFileInput.bind(on_double_tap=self.on_double_click)
        self.beginnerCuesInput.bind(on_double_tap=self.on_double_click)
        self.moderateCuesInput.bind(on_double_tap=self.on_double_click)
        self.advancedCuesInput.bind(on_double_tap=self.on_double_click)
        self.expertCuesInput.bind(on_double_tap=self.on_double_click)
        
        self.autoSongIDCheckbox.bind(active=self.autoSongIDHandler)
        
        Thread(target=self.welcome_message).start()
        
    def autoSongIDHandler(self, checkbox, value):
        if value:
            self.songIDInput.text = ""
            self.songIDInput.readonly = True
        else:
            self.songIDInput.readonly = False
        
    def welcome_message(self):
        time.sleep(1)
        self.send_message("====================================================")
        self.send_message("BASIC INFORMATION")
        self.send_message("")
        self.send_message("To open a file browser double click on the text input box.")
        self.send_message("")
        self.send_message("Can use ogg or mogg for audio.")
        self.send_message("")
        self.send_message("Main Audio is required but the other files are optionnal.")
        self.send_message("")
        self.send_message("Pans and Vols can be negative.")
        self.send_message("")
        self.send_message("MIDI file can only have a single BPM marker.")
        self.send_message("")
        self.send_message("The BPM of the MIDI file and the desc file must match.")
        self.send_message("")
        self.send_message("If you are using cues files and no MIDI file one will be generated")
        self.send_message("")
        self.send_message("Only \"A, A#, B, C, C#, D, D#, E, F, F#, G, G#\"")
        self.send_message("are allowed as End Event Key.")
        self.send_message("")
        self.send_message("Pans, Vols, Tempo, Pitch Adjust, Preroll Seconds and ")
        self.send_message("Preview Start Seconds must be float.")
        self.send_message("")
        self.send_message("Offset must be integer, only used by Edica.")
        self.send_message("")
        self.send_message("Automatic songID will make the songID \"authorsongname\".")
        self.send_message("")
        self.send_message("In-game author will display author under artist in the song list.")
        self.send_message("")
        self.send_message("Project is saved in the OUTPUT folder with songID as filename.")
        
    def send_message(self, message):
        message = message + "\n"
        self.messageTextbox.cursor = (len(self.messageTextbox.text), self.current_message_row)
        self.messageTextbox.readonly = False
        self.messageTextbox.insert_text(message, from_undo=False)
        self.messageTextbox.readonly = True
        self.messageTextbox.cursor = (len(self.messageTextbox.text), self.current_message_row)
        self.current_message_row = self.current_message_row + 1
        f = open("log.txt", "a")
        f.write("[" + str(datetime.datetime.fromtimestamp(time.time()).isoformat()) + "] " + message)
        
    def import_desc(self, file):
        self.send_message("====================================================")
        self.send_message("IMPORTING DESC...")
        self.desc_file.load_desc_file(file)
        self.songIDInput.text = self.desc_file.songID
        self.titleInput.text = self.desc_file.title
        self.artistInput.text = self.desc_file.artist
        self.tempoInput.text = str(self.desc_file.tempo)
        self.endEventInput.text = self.desc_file.songEndEvent
        self.endPitchAdjustInput.text = str(self.desc_file.songEndPitchAdjust)
        self.prerollSecondsInput.text = str(self.desc_file.prerollSeconds)
        self.previewStartSecondsInput.text = str(self.desc_file.previewStartSeconds)
        self.useMidiForCuesCheckbox.active = self.desc_file.useMidiForCues
        self.hiddenCheckbox.active = self.desc_file.hidden
        self.authorInput.text = self.desc_file.author
        self.send_message("DESC IMPORTED")
        
    def load_project(self, file):
        self.send_message("====================================================")
        self.send_message("LOADING PROJECT...")
        self.config_file.configFilename = file
        self.config_file.load_config()
        self.songIDInput.text = self.config_file.songID
        self.titleInput.text = self.config_file.title
        self.artistInput.text = self.config_file.artist
        self.midiFileInput.text = self.config_file.midiFile
        self.midiFileInput.cursor = (len(self.midiFileInput.text), 0)
        self.tempoInput.text = str(self.config_file.tempo)
        self.endEventInput.text = self.config_file.songEndEvent
        self.endPitchAdjustInput.text = str(self.config_file.songEndPitchAdjust)
        self.prerollSecondsInput.text = str(self.config_file.prerollSeconds)
        self.previewStartSecondsInput.text = str(self.config_file.previewStartSeconds)
        self.useMidiForCuesCheckbox.active = self.config_file.useMidiForCues
        self.hiddenCheckbox.active = self.config_file.hidden
        self.authorInput.text = self.config_file.author
        self.mainAudioInput.text = self.config_file.main_audio
        self.mainAudioInput.cursor = (len(self.mainAudioInput.text), 0)
        self.mainAudioLeftPanInput.text = str(self.config_file.main_pan_l)
        self.mainAudioRightPanInput.text = str(self.config_file.main_pan_r)
        self.mainAudioLeftVolInput.text = str(self.config_file.main_vol_l)
        self.mainAudioRightVolInput.text = str(self.config_file.main_vol_r)
        self.extrasAudioInput.text = self.config_file.extras_audio
        self.extrasAudioInput.cursor = (len(self.extrasAudioInput.text), 0)
        self.extrasAudioLeftPanInput.text = str(self.config_file.extras_pan_l)
        self.extrasAudioRightPanInput.text = str(self.config_file.extras_pan_r)
        self.extrasAudioLeftVolInput.text = str(self.config_file.extras_vol_l)
        self.extrasAudioRightVolInput.text = str(self.config_file.extras_vol_r)
        self.leftSustainAudioInput.text = self.config_file.sustain_l_audio
        self.leftSustainAudioInput.cursor = (len(self.leftSustainAudioInput.text), 0)
        self.leftSustainAudioPanInput.text = str(self.config_file.sustain_l_pan)
        self.leftSustainAudioVolInput.text = str(self.config_file.sustain_l_vol)
        self.rightSustainAudioInput.text = self.config_file.sustain_r_audio
        self.rightSustainAudioInput.cursor = (len(self.rightSustainAudioInput.text), 0)
        self.rightSustainAudioPanInput.text = str(self.config_file.sustain_r_pan)
        self.rightSustainAudioVolInput.text = str(self.config_file.sustain_r_vol)
        self.beginnerCuesInput.text = self.config_file.beginner_cues
        self.beginnerCuesInput.cursor = (len(self.beginnerCuesInput.text), 0)
        self.moderateCuesInput.text = self.config_file.moderate_cues
        self.moderateCuesInput.cursor = (len(self.moderateCuesInput.text), 0)
        self.advancedCuesInput.text = self.config_file.advanced_cues
        self.advancedCuesInput.cursor = (len(self.advancedCuesInput.text), 0)
        self.expertCuesInput.text = self.config_file.expert_cues
        self.expertCuesInput.cursor = (len(self.expertCuesInput.text), 0)
        self.autoSongIDCheckbox.active = self.config_file.autoSongID
        self.inGameAuthorCheckbox.active = self.config_file.inGameAuthor
        self.ignoreMinorErrorsCheckbox.active = self.config_file.ignoreMinorErrors
        self.send_message("PROJECT LOADED")
        
    def save_project(self):
        self.send_message("====================================================")
        self.send_message("SAVING PROJECT...")
        
        if self.autoSongIDCheckbox.active == True:
            pattern = re.compile('\W')
            self.songIDInput.readonly = False
            self.songIDInput.text = re.sub(pattern, "", self.authorInput.text + self.titleInput.text).lower()
            self.songIDInput.readonly = True
        
        projects_folder = os.getcwd() + os.sep + "PROJECTS"
        project_filename = projects_folder + os.sep + self.songIDInput.text + ".json"
        
        if os.path.exists(projects_folder) == True:
            if os.path.isfile(project_filename):
                os.remove(project_filename)
        else:
            os.mkdir(projects_folder)
        
        self.config_file.configFilename = project_filename
        self.config_file.songID = self.songIDInput.text
        self.config_file.title = self.titleInput.text
        self.config_file.artist = self.artistInput.text
        self.config_file.midiFile = self.midiFileInput.text
        self.config_file.tempo = float(self.tempoInput.text)
        self.config_file.songEndEvent = self.endEventInput.text
        self.config_file.songEndPitchAdjust = float(self.endPitchAdjustInput.text)
        self.config_file.prerollSeconds = float(self.prerollSecondsInput.text)
        self.config_file.previewStartSeconds = float(self.previewStartSecondsInput.text)
        self.config_file.useMidiForCues = self.useMidiForCuesCheckbox.active
        self.config_file.hidden = self.hiddenCheckbox.active
        self.config_file.author = self.authorInput.text
        self.config_file.main_audio = self.mainAudioInput.text
        self.config_file.main_pan_l = float(self.mainAudioLeftPanInput.text)
        self.config_file.main_pan_r = float(self.mainAudioRightPanInput.text)
        self.config_file.main_vol_l = float(self.mainAudioLeftVolInput.text)
        self.config_file.main_vol_r = float(self.mainAudioRightVolInput.text)
        self.config_file.extras_audio = self.extrasAudioInput.text
        self.config_file.extras_pan_l = float(self.extrasAudioLeftPanInput.text)
        self.config_file.extras_pan_r = float(self.extrasAudioRightPanInput.text)
        self.config_file.extras_vol_l = float(self.extrasAudioLeftVolInput.text)
        self.config_file.extras_vol_r = float(self.extrasAudioRightVolInput.text)
        self.config_file.sustain_l_audio = self.leftSustainAudioInput.text
        self.config_file.sustain_l_pan = float(self.leftSustainAudioPanInput.text)
        self.config_file.sustain_l_vol = float(self.leftSustainAudioVolInput.text)
        self.config_file.sustain_r_audio = self.rightSustainAudioInput.text
        self.config_file.sustain_r_pan = float(self.rightSustainAudioPanInput.text)
        self.config_file.sustain_r_vol = float(self.rightSustainAudioVolInput.text)
        self.config_file.beginner_cues = self.beginnerCuesInput.text
        self.config_file.moderate_cues = self.moderateCuesInput.text
        self.config_file.advanced_cues = self.advancedCuesInput.text
        self.config_file.expert_cues = self.expertCuesInput.text
        self.config_file.autoSongID = self.autoSongIDCheckbox.active
        self.config_file.inGameAuthor = self.inGameAuthorCheckbox.active
        self.config_file.ignoreMinorErrors = self.ignoreMinorErrorsCheckbox.active
        self.config_file.save_config()
        self.send_message("PROJECT SAVED")
        
    def disable_all_buttons(self):
        self.loadButton.disabled = True
        self.saveButton.disabled = True
        self.makeAudicaButton.disabled = True
        self.importDescButton.disabled = True
        
    def enable_all_buttons(self):
        self.loadButton.disabled = False
        self.saveButton.disabled = False
        self.makeAudicaButton.disabled = False
        self.importDescButton.disabled = False

    def save_audica(self):
        self.disable_all_buttons()
        if self.autoSongIDCheckbox.active == True:
            pattern = re.compile('\W')
            self.songIDInput.readonly = False
            self.songIDInput.text = re.sub(pattern, "", self.authorInput.text + self.titleInput.text).lower()
            self.songIDInput.readonly = True
        if self.check_for_errors() == True:
            if self.make_audica_file() == True:
                self.send_message("====================================================")
                self.send_message("DONE!")
        else:
            self.send_message("====================================================")
            self.send_message("FOUND MAJOR ERRORS, CANCELING...")
        self.enable_all_buttons()
    
    def check_for_errors(self):
        self.error_checker.reset()
        self.error_checker.beginner_cues = self.beginnerCuesInput.text
        self.error_checker.moderate_cues = self.moderateCuesInput.text
        self.error_checker.advanced_cues = self.advancedCuesInput.text
        self.error_checker.expert_cues = self.expertCuesInput.text
        self.error_checker.midi = self.midiFileInput.text
        self.error_checker.main_audio = self.mainAudioInput.text
        self.error_checker.extras_audio = self.extrasAudioInput.text
        self.error_checker.sustain_l_audio = self.leftSustainAudioInput.text
        self.error_checker.sustain_r_audio = self.rightSustainAudioInput.text
        self.error_checker.main_pan_l = float(self.mainAudioLeftPanInput.text)
        self.error_checker.main_pan_r = float(self.mainAudioRightPanInput.text)
        self.error_checker.main_vol_l = float(self.mainAudioLeftVolInput.text)
        self.error_checker.main_vol_r = float(self.mainAudioRightVolInput.text)
        self.error_checker.sustain_l_pan = float(self.leftSustainAudioPanInput.text)
        self.error_checker.sustain_l_vol = float(self.leftSustainAudioVolInput.text)
        self.error_checker.sustain_r_pan = float(self.rightSustainAudioPanInput.text)
        self.error_checker.sustain_r_vol = float(self.rightSustainAudioVolInput.text)
        self.error_checker.extras_pan_l = float(self.extrasAudioLeftPanInput.text)
        self.error_checker.extras_pan_r = float(self.extrasAudioRightPanInput.text)
        self.error_checker.extras_vol_l = float(self.extrasAudioLeftVolInput.text)
        self.error_checker.extras_vol_r = float(self.extrasAudioRightVolInput.text)
        self.error_checker.songID = self.songIDInput.text
        self.error_checker.title = self.titleInput.text
        self.error_checker.artist = self.artistInput.text
        self.error_checker.tempo = float(self.tempoInput.text)
        self.error_checker.songEndEvent = self.endEventInput.text
        self.error_checker.songEndPitchAdjust = float(self.endPitchAdjustInput.text)
        self.error_checker.prerollSeconds = float(self.prerollSecondsInput.text)
        self.error_checker.previewStartSeconds = float(self.previewStartSecondsInput.text)
        self.error_checker.useMidiForCues = self.useMidiForCuesCheckbox.active
        self.error_checker.hidden = self.hiddenCheckbox.active
        self.error_checker.offset = int(self.offsetInput.text)
        self.error_checker.author = self.authorInput.text
        self.error_checker.autoSongID = self.autoSongIDCheckbox.active
        self.error_checker.inGameAuthor = self.inGameAuthorCheckbox.active
        self.error_checker.ignoreMinorErrors = self.ignoreMinorErrorsCheckbox.active
        self.error_checker.midiToCues = self.convertMidiToCuesCheckbox.active
        self.error_checker.cuesToMidi = self.convertCuesToMidiCheckbox.active
        
        self.send_message("====================================================")
        self.send_message("BEGINNING CHECK...")
        
        self.send_message("====================================================")
        self.send_message("CHECKING USER INPUT...")
        self.error_checker.check_audio()
        self.error_checker.check_data()
        self.error_checker.check_desc()
        if len(self.error_checker.majorErrors) > 0:
            self.send_message("====================================================")
            self.send_message("MAJOR ERRORS")
            self.send_message("")
            for message in self.error_checker.majorErrors:
                self.send_message(message)
            return False
        else:
            self.send_message("No major errors, continuing...")
        if len(self.error_checker.minorErrors) > 0:
            self.send_message("====================================================")
            self.send_message("MINOR ERRORS")
            self.send_message("")
            for message in self.error_checker.minorErrors:
                self.send_message(message)
                
        self.send_message("====================================================")
        self.send_message("CHECK PASSED")
        return True
        
    def make_audica_file(self):
    
        files = []
    
        temp_dir = os.getcwd() + os.sep + self.songIDInput.text
        
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.mkdir(temp_dir)
            
        silent_audio_file = os.getcwd() + os.sep + "silent_audio.mogg"
            
        main_audio_mogg = temp_dir + os.sep + self.songIDInput.text + ".mogg"
        extras_audio_mogg = temp_dir + os.sep + self.songIDInput.text + "_extras.mogg"
        sustain_l_audio_mogg = temp_dir + os.sep + self.songIDInput.text + "_sustain_l.mogg"
        sustain_r_audio_mogg = temp_dir + os.sep + self.songIDInput.text + "_sustain_r.mogg"
        main_audio_moggsong = temp_dir + os.sep + self.songIDInput.text + ".moggsong"
        extras_audio_moggsong = temp_dir + os.sep + self.songIDInput.text + "_extras.moggsong"
        sustain_l_audio_moggsong = temp_dir + os.sep + self.songIDInput.text + "_sustain_l.moggsong"
        sustain_r_audio_moggsong = temp_dir + os.sep + self.songIDInput.text + "_sustain_r.moggsong"
        midi_file = temp_dir + os.sep + self.songIDInput.text + ".mid"
        
        mainAudioMoggReady = False
        extrasAudioMoggReady = False
        sustainlAudioMoggReady = False
        sustainrAudioMoggReady = False
        mainAudioMoggsongReady = False
        extrasAudioMoggsongReady = False
        sustainlAudioMoggsongReady = False
        sustainrAudioMoggsongReady = False
        descFileReady = False
        midiFileReady = False
        beginnerCuesReady = False
        moderateCuesReady = False
        advancedCuesReady = False
        expertCuesReady = False
        
        self.send_message("====================================================")
        self.send_message("CREATING MOGGSONG FILES...")
        
        self.song_file.moggPath = main_audio_mogg.split(os.sep)[-1]
        self.song_file.midiPath = midi_file.split(os.sep)[-1]
        self.song_file.pansL = float(self.mainAudioLeftPanInput.text)
        self.song_file.pansR = float(self.mainAudioRightPanInput.text)
        self.song_file.volsL = float(self.mainAudioLeftVolInput.text)
        self.song_file.volsR = float(self.mainAudioRightVolInput.text)
        self.song_file.save_file(main_audio_moggsong)
        
        files.append(main_audio_moggsong)
        mainAudioMoggsongReady = True
        self.send_message("CREATED " + main_audio_moggsong.split(os.sep)[-1])
        
        self.extras_file.moggPath = extras_audio_mogg.split(os.sep)[-1]
        self.extras_file.midiPath = midi_file.split(os.sep)[-1]
        self.extras_file.pansL = float(self.extrasAudioLeftPanInput.text)
        self.extras_file.pansR = float(self.extrasAudioRightPanInput.text)
        self.extras_file.volsL = float(self.extrasAudioLeftVolInput.text)
        self.extras_file.volsR = float(self.extrasAudioRightVolInput.text)
        self.extras_file.save_file(extras_audio_moggsong)
        
        files.append(extras_audio_moggsong)
        extrasAudioMoggsongReady = True
        self.send_message("CREATED " + extras_audio_moggsong.split(os.sep)[-1])
        
        self.sustain_file.moggPathL = sustain_l_audio_mogg.split(os.sep)[-1]
        self.sustain_file.moggPathR = sustain_r_audio_mogg.split(os.sep)[-1]
        self.sustain_file.midiPath = midi_file.split(os.sep)[-1]
        self.sustain_file.pansL = float(self.leftSustainAudioPanInput.text)
        self.sustain_file.pansR = float(self.rightSustainAudioPanInput.text)
        self.sustain_file.volsL = float(self.leftSustainAudioVolInput.text)
        self.sustain_file.volsR = float(self.rightSustainAudioVolInput.text)
        
        self.sustain_file.save_file_l(sustain_l_audio_moggsong)
        files.append(sustain_l_audio_moggsong)
        sustainlAudioMoggsongReady = True
        self.send_message("CREATED " + sustain_l_audio_moggsong.split(os.sep)[-1])
        
        self.sustain_file.save_file_r(sustain_r_audio_moggsong)
        files.append(sustain_r_audio_moggsong)
        sustainrAudioMoggsongReady = True
        self.send_message("CREATED " + sustain_r_audio_moggsong.split(os.sep)[-1])
        
        self.send_message("MOGGSONG CREATION DONE")
        
        if len(self.error_checker.audio_to_convert) > 0:
            self.send_message("====================================================")
            self.send_message("CONVERTING OGG FILES TO MOGG...")
            for file in self.error_checker.audio_to_convert:
                input_file = file[1]
                if file[0] == "song":
                    output_file = temp_dir + os.sep + self.songIDInput.text + ".mogg"
                else:
                    output_file = temp_dir + os.sep + self.songIDInput.text + file[0] + ".mogg"
                converter_output = check_output("ogg2mogg.exe \"" + input_file + "\" \"" + output_file + "\"")
                if converter_output != "":
                    self.send_message("ERROR CONVERTING " + output_file.split(os.sep)[-1])
                    self.send_message(converter_output)
                else:
                    if file[0] == "song":
                        mainAudioMoggReady = True
                    elif file[0] == "_extras":
                        extrasAudioMoggReady = True
                    elif file[0] == "_sustain_l":
                        sustainlAudioMoggReady = True
                    elif file[0] == "_sustain_r":
                        sustainrAudioMoggReady = True
                    files.append(output_file)
                    self.send_message("CREATED " + output_file.split(os.sep)[-1])
            self.send_message("MOGG CREATION DONE")
            
        if len(self.error_checker.audio_to_silence) > 0:
            self.send_message("====================================================")
            self.send_message("PREPARING SILENT MOGG FILES...")
            for file in self.error_checker.audio_to_silence:
                input_file = silent_audio_file
                if file[0] == "song":
                    output_file = temp_dir + os.sep + self.songIDInput.text + ".mogg"
                else:
                    output_file = temp_dir + os.sep + self.songIDInput.text + file[0] + ".mogg"
                shutil.copyfile(input_file, output_file)
                #converter_output = check_output("ogg2mogg.exe \"" + input_file + "\" \"" + output_file + "\"")
                if file[0] == "_extras":
                    extrasAudioMoggReady = True
                elif file[0] == "_sustain_l":
                    sustainlAudioMoggReady = True
                elif file[0] == "_sustain_r":
                    sustainrAudioMoggReady = True
                files.append(output_file)
                self.send_message("CREATED " + output_file.split(os.sep)[-1])
            self.send_message("SILENT AUDIO PREPARATION DONE")
            
        audio_file_checks = [mainAudioMoggReady, extrasAudioMoggReady, sustainlAudioMoggReady, sustainrAudioMoggReady]
        
        if False in audio_file_checks:
            self.send_message("====================================================")
            self.send_message("COPYING MOGG FILES...")
            if mainAudioMoggReady == False:
                if self.mainAudioInput.text[-5:] == ".mogg":
                    shutil.copyfile(self.mainAudioInput.text, temp_dir + os.sep + self.songIDInput.text + ".mogg")
                    files.append(temp_dir + os.sep + self.songIDInput.text + ".mogg")
                    mainAudioMoggReady = True
                    self.send_message("CREATED " + self.songIDInput.text + ".mogg")
            if extrasAudioMoggReady == False:
                if self.extrasAudioInput.text[-5:] == ".mogg":
                    shutil.copyfile(self.extrasAudioInput.text, temp_dir + os.sep + self.songIDInput.text + "_extras.mogg")
                    files.append(temp_dir + os.sep + self.songIDInput.text + "_extras.mogg")
                    extrasAudioMoggReady = True
                    self.send_message("CREATED " + self.songIDInput.text + "_extras.mogg")
            if sustainlAudioMoggReady == False:
                if self.leftSustainAudioInput.text[-5:] == ".mogg":
                    shutil.copyfile(self.leftSustainAudioInput.text, temp_dir + os.sep + self.songIDInput.text + "_sustain_l.mogg")
                    files.append(temp_dir + os.sep + self.songIDInput.text + "_sustain_l.mogg")
                    sustainlAudioMoggReady = True
                    self.send_message("CREATED " + self.songIDInput.text + "_sustain_l.mogg")
            if sustainrAudioMoggReady == False:
                if self.rightSustainAudioInput.text[-5:] == ".mogg":
                    shutil.copyfile(self.rightSustainAudioInput.text, temp_dir + os.sep + self.songIDInput.text + "_sustain_r.mogg")
                    files.append(temp_dir + os.sep + self.songIDInput.text + "_sustain_r.mogg")
                    sustainrAudioMoggReady = True
                    self.send_message("CREATED " + self.songIDInput.text + "_sustain_r.mogg")
                    
        audio_file_checks = [mainAudioMoggReady, extrasAudioMoggReady, sustainlAudioMoggReady, sustainrAudioMoggReady]
        
        if False in audio_file_checks:
            self.send_message("====================================================")
            self.send_message("ERROR PREPARING AUDIO FILES, CANCELING...")
            return False
                    
        self.send_message("====================================================")
        self.send_message("CREATING DESC FILE...")
        
        self.desc_file.songID = self.songIDInput.text
        self.desc_file.moggSong = self.songIDInput.text + ".moggsong"
        self.desc_file.title = self.titleInput.text
        self.desc_file.artist = self.artistInput.text + "\n" + self.authorInput.text
        self.desc_file.midiFile = self.songIDInput.text + ".mid"
        self.desc_file.sustainSongRight = self.songIDInput.text + "_sustain_r.moggsong"
        self.desc_file.sustainSongLeft = self.songIDInput.text + "_sustain_l.moggsong"
        self.desc_file.fxSong = self.songIDInput.text + "_extras.moggsong"
        self.desc_file.tempo = float(self.tempoInput.text)
        self.desc_file.songEndEvent = self.endEventInput.text
        self.desc_file.songEndPitchAdjust = float(self.endPitchAdjustInput.text)
        self.desc_file.prerollSeconds = float(self.prerollSecondsInput.text)
        self.desc_file.previewStartSeconds = float(self.previewStartSecondsInput.text)
        self.desc_file.useMidiForCues = self.useMidiForCuesCheckbox.active
        self.desc_file.hidden = self.hiddenCheckbox.active
        self.desc_file.offset = int(self.offsetInput.text)
        self.desc_file.author = self.authorInput.text
        self.desc_file.save_desc_file(temp_dir + os.sep + "song.desc")
        files.append(temp_dir + os.sep + "song.desc")
        descFileReady = True
        
        self.send_message("DESC FILE CREATED")
        
        self.send_message("====================================================")
        self.send_message("PREPARING DATA FILES...")
        
        if self.useMidiForCuesCheckbox.active == True:
            if os.path.isfile(self.midiFileInput.text) == True:
                shutil.copyfile(self.midiFileInput.text, midi_file)
                files.append(midi_file)
                midiFileReady = True
                self.send_message("CREATED " + midi_file.split(os.sep)[-1])
            else:
                return False
        
            
        
        if os.path.isfile(self.beginnerCuesInput.text) == True:
            shutil.copyfile(self.beginnerCuesInput.text, temp_dir + os.sep + "beginner.cues")
            files.append(temp_dir + os.sep + "beginner.cues")
            beginnerCuesReady = True
            self.send_message("CREATED beginner.cues")
        if os.path.isfile(self.moderateCuesInput.text) == True:
            shutil.copyfile(self.moderateCuesInput.text, temp_dir + os.sep + "moderate.cues")
            files.append(temp_dir + os.sep + "moderate.cues")
            moderateCuesReady = True
            self.send_message("CREATED moderate.cues")
        if os.path.isfile(self.advancedCuesInput.text) == True:
            shutil.copyfile(self.advancedCuesInput.text, temp_dir + os.sep + "advanced.cues")
            files.append(temp_dir + os.sep + "advanced.cues")
            advancedCuesReady = True
            self.send_message("CREATED advanced.cues")
        if os.path.isfile(self.expertCuesInput.text) == True:
            shutil.copyfile(self.expertCuesInput.text, temp_dir + os.sep + "expert.cues")
            files.append(temp_dir + os.sep + "expert.cues")
            expertCuesReady = True
            self.send_message("CREATED expert.cues")
        if self.useMidiForCuesCheckbox.active == False:
            if True in [beginnerCuesReady, moderateCuesReady, advancedCuesReady, expertCuesReady]:
                if midiFileReady == False:
                    self.send_message("No MIDI file selected, creating blank MIDI file with BPM.")
                    make_midi_for_bpm(midi_file, float(self.tempoInput.text))
                    files.append(midi_file)
                    midiFileReady = True
                    self.send_message("CREATED " + midi_file.split(os.sep)[-1])
                self.send_message("DATA FILES PREPARATION DONE")
            else:
                return False
        else:
            self.send_message("DATA FILES PREPARATION DONE")
        
        self.send_message("====================================================")
        self.send_message("MAKING AUDICA FILE...")
        
        audica_output_folder = os.getcwd() + os.sep + "OUTPUT"
        audica_filename = audica_output_folder + os.sep + self.songIDInput.text + ".audica"
        
        if os.path.exists(audica_output_folder) == True:
            if os.path.isfile(audica_filename):
                os.remove(audica_filename)
        else:
            os.mkdir(audica_output_folder)
        
        f = ZipFile(audica_filename, "w")
        for file in files:
            f.write(file, file.split(os.sep)[-1])
        f.close()
        
        shutil.rmtree(temp_dir)
        
        self.send_message("AUDICA FILE COMPLETED, SAVED IN OUTPUT FOLDER!")
        
        return True
        
    def on_double_click(self, instance):
        self._create_popup(instance)
        
    def _dismiss(self, *largs):
        if self.textinput:
            self.textinput.focus = False
        if self.popup:
            self.popup.dismiss()
        self.popup = None
 
    def _validate(self, instance):
        self._dismiss()
        value = self.textinput.selection
 
        if not value:
            return
 
        self.value = os.path.realpath(value[0])
        if instance.text == "Load Project":
            self.load_project(self.value)
        elif instance.text == "Import .desc":
            self.import_desc(self.value)
        else:
            instance.text = self.value
            instance.cursor = (len(instance.text), 0)
        
    def _create_popup(self, instance):
        # create popup layout
        content = BoxLayout(orientation='vertical', spacing=5)
        popup_width = min(10, 10)
        self.popup = popup = Popup(
            title=self.title, content=content, size_hint=(0.9, 0.9),
            width=popup_width)
 
        # create the filechooser
        self.textinput = textinput = FileChooserListView(
            path=self.value, size_hint=(1, 1), dirselect=True)
        textinput.bind(on_path=self._validate)
        self.textinput = textinput
 
        # construct the content
        content.add_widget(textinput)
 
        # 2 buttons are created for accept or cancel the current value
        btnlayout = BoxLayout(size_hint_y=None, height='50dp', spacing='5dp')
        btn = Button(text='Ok')
        btn.bind(on_release=lambda i:self._validate(instance))
        btnlayout.add_widget(btn)
        btn = Button(text='Cancel')
        btn.bind(on_release=self._dismiss)
        btnlayout.add_widget(btn)
        content.add_widget(btnlayout)
 
        # all done, open the popup !
        popup.open()

class MyApp(App):

    def build(self):
        return MainApp()


if __name__ == '__main__':
    MyApp().run()
        

