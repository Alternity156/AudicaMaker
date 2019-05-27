'''file containing authoring_validation class which contains various checks to prevent potential issues'''

import json
import sys
from collections import OrderedDict
import os
import re

class authoringValidator():

    beginner_cues = ""
    moderate_cues = ""
    advanced_cues = ""
    expert_cues = ""
    
    def validate_cues(self):
        '''checks and fixes duplicate cues'''
    
        cue_files = [self.beginner_cues, self.moderate_cues,
                        self.advanced_cues, self.expert_cues]
        for cue_file in cue_files:
            if cue_file:
                with open(cue_file, 'r') as fd:
                    cue_data = json.load(fd, object_pairs_hook=OrderedDict)
                print("Checking for duplicates")
                tmp_cue_data = []
                for cue in cue_data["cues"]:
                    if cue not in tmp_cue_data:
                        tmp_cue_data.append(cue)
                
                if len(tmp_cue_data) < len(cue_data["cues"]):
                    cue_data["cues"] = tmp_cue_data
                    with open(cue_file+"tmp", 'w') as fd:
                        fd.write(re.sub(", ", ",", json.dumps(cue_data, sort_keys=False, indent=4)))
                    os.remove(cue_file)
                    os.rename(cue_file+"tmp", cue_file)
                    return 0
                else:
                    return 0
        
    def begin_validation(self):
        '''triggers start of validation/ verifications methods'''
        
        self.validate_cues()