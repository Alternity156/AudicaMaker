'''file containing authoring_validation class which contains various checks to prevent potential issues
TODO:
    integrate into main.py
    look at more effective way to validate_cues without as much memory or processor requirements'''

import json
import sys
from re import sub
from collections import OrderedDict
import os
import midi

class authoringValidator():

    error_messages = []
    major_error = False
    
    def add_error(self, message):
        '''handler to add a error to class'''
        
        if len(message) == 0:
            return None
        else:
            self.error_messages.append(message)
            return self.error_messages
            
    def validate_cues(self):
        '''checks and fixes duplicate cues'''
        
        cue_files = [self.beginner_cues, self.moderate_cues,
                        self.advanced_cues, self.expert_cues]
        # holds the edited version of any cue files that were edited
        cue_files_edited = []
        for cue_file_index, cue_file in enumerate(cue_files):
            if os.path.exists(cue_file):
                # using OrderedDict to preserve order
                with open(cue_file, 'r') as fd:
                    cue_data = json.load(fd, object_pairs_hook=OrderedDict)
                tmp_cue_data = []
                for cue in cue_data["cues"]:
                    if cue not in tmp_cue_data:
                        tmp_cue_data.append(cue)
                if len(tmp_cue_data) < len(cue_data["cues"]):
                    target_file = os.path.splitext(cue_file)[0]+"_tmp.cues"
                    cue_data["cues"] = tmp_cue_data
                    with open(target_file, 'w') as fd:
                        # stores index and file path for returning
                        # index used to know what difficulty file belongs to
                        cue_files_edited.append((cue_file_index, target_file))
                        fd.write(sub(", ", ",", json.dumps(cue_data, sort_keys=False, indent=4)))
        if len(cue_files_edited) == 0:
            return True
        else:
            cue_error_string = "Minor Errors in .cue file(s): Duplicate/Invalid notes detected\nAutomatic Resolution Implemented\n"
            self.add_error(cue_error_string)
            return False
                    
                    
    def validate_midi(self):
        '''loads midi and reports if there are duplicates in the same track'''
    
        if self.midi_file=="" or os.path.splitext(self.midi_file)[1] != ".mid":
            self.major_error = True
            self.add_error("FILE SPECIFIED FOR MIDI FILE IS NOT VALID:\n {midi_file}".format(midi_file=os.path.basename(self.midi_file)))
            return False
        self.midi_file_content = midi.read_midifile(self.midi_file)
        self.midi_file_content.make_ticks_abs()
        midi_errors_count = 0
        midi_errors_dict = {}
        get_next_event_type = lambda event_array, event_ind: \
                                event_array[event_ind+1][0]
        get_event_tick = lambda event: event.tick
        for track in self.midi_file_content:
            #type_indicators used to determine if valid, 1 is on, 2 is off, 0 is misc.
            type_indicators = map(lambda event: 1 if 
                isinstance(event,midi.NoteOnEvent) and event.data[0] < 107
                else 2 if isinstance(event, midi.NoteOffEvent) and 
                event.data[0] < 107 else 0, track[:])
            if any(type_indicators):
                type_track_list = zip(type_indicators, track)
                track_name = track[0].text
                for event_index, (event_type, event) in enumerate(type_track_list[:-1]):
                    if event_type and event_type == get_next_event_type(type_track_list, event_index):
                        #check if melee to disregard double melee positives
                        if "Melee" in track_name:
                            #check if both aren't the same kind
                            if event.data[0] != track[event_index+1].data[0] and \
                                event_type != get_next_event_type(
                                type_track_list, event_index+1):
                                continue
                        midi_errors_dict.setdefault(track_name,[])
                        midi_errors_dict[track_name].extend([
                            event.tick, 
                            track[event_index+1].tick])
                        midi_errors_count += 1
        for midi_track_name, midi_errors in midi_errors_dict.items():
            midi_errors_dict[midi_track_name] = sorted(set(midi_errors))
        if midi_errors_count > 0:
            self.major_error = True
            self.add_error("ERRORS DETECTED IN MIDI TRACK(S)")
            for midi_track_name, midi_errors in midi_errors_dict.items():
                # add error indicating location of midi errors
                self.add_error("\nMIDI TRACK NAME: {midi_track_name}\n"\
                    "ERROR(S) LOCATION: {midi_errors}".format(
                        midi_track_name=midi_track_name,
                        midi_errors=", ".join(map(str, midi_errors))))
        return False if midi_errors_count > 0 else True
            #return midi_errors_dict
        
    def __init__(self, beginner_cues="", moderate_cues="", advanced_cues="", expert_cues="", midi_file=""):
        self.beginner_cues = beginner_cues 
        self.moderate_cues = moderate_cues
        self.advanced_cues = advanced_cues
        self.expert_cues = expert_cues
        self.midi_file = midi_file
    
    def begin_validation(self):
        '''triggers start of validation/ verifications methods'''

        results = []
        self.error_messages = []
        results.append(self.validate_cues())
        results.append(self.validate_midi())
        self.error_messages = "".join(self.error_messages)
        return results