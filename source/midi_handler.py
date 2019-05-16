## midi2cues and cues2midi were coded by Awwbees from Harmonix, slightly modified to fit my needs.

from collections import OrderedDict

import sys
import os
import midi
import json

def make_track_name(name):
    event = midi.TrackNameEvent()
    event.text = name
    for char in name:
        event.data.append(ord(char))
    return event

def make_midi_for_bpm(filename, bpm):
       
    pattern = midi.Pattern(resolution=480, format=1)

    HeaderTrack = midi.Track(tick_relative=False)
    RHTrack = midi.Track(tick_relative=False)
    LHTrack = midi.Track(tick_relative=False)
    EitherTrack = midi.Track(tick_relative=False)

    HeaderTrack.append(make_track_name(filename))
    RHTrack.append(make_track_name('Expert - RH'))
    LHTrack.append(make_track_name('Expert - LH'))
    EitherTrack.append(make_track_name('Expert - Either'))

    tempoEvent = midi.SetTempoEvent()
    tempoEvent.set_bpm(bpm)
    HeaderTrack.append(tempoEvent)

    HeaderTrack = midi.Track(sorted(HeaderTrack, key=lambda x: x.tick), tick_relative=False)
    RHTrack = midi.Track(sorted(RHTrack, key=lambda x: x.tick), tick_relative=False)
    LHTrack = midi.Track(sorted(LHTrack, key=lambda x: x.tick), tick_relative=False)
    EitherTrack = midi.Track(sorted(EitherTrack, key=lambda x: x.tick), tick_relative=False)

    HeaderTrack.append(midi.EndOfTrackEvent(tick=HeaderTrack[-1].tick))
    RHTrack.append(midi.EndOfTrackEvent(tick=RHTrack[-1].tick))
    LHTrack.append(midi.EndOfTrackEvent(tick=LHTrack[-1].tick))
    EitherTrack.append(midi.EndOfTrackEvent(tick=EitherTrack[-1].tick))

    HeaderTrack.make_ticks_rel()
    RHTrack.make_ticks_rel()
    LHTrack.make_ticks_rel()
    EitherTrack.make_ticks_rel()

    pattern.append(HeaderTrack)
    pattern.append(RHTrack)
    pattern.append(LHTrack)
    pattern.append(EitherTrack)

    midifile = filename
    midi.write_midifile(midifile, pattern)
    
def cues_to_midi(cuesfile):

    cues = json.load(open(cuesfile, 'r'))

    pattern = midi.Pattern(resolution=480, format=1)

    HeaderTrack = midi.Track(tick_relative=False)
    RHTrack = midi.Track(tick_relative=False)
    LHTrack = midi.Track(tick_relative=False)
    EitherTrack = midi.Track(tick_relative=False)

    HeaderTrack.append(make_track_name(cuesfile.replace('.cues','')))
    RHTrack.append(make_track_name('Community - RH'))
    LHTrack.append(make_track_name('Community - LH'))
    EitherTrack.append(make_track_name('Community - Either'))

    if "tempo" in cues:
        tempoEvent = midi.SetTempoEvent()
        tempoEvent.set_bpm(cues["tempo"])
        HeaderTrack.append(tempoEvent)

    for cue in cues["cues"]:
        if cue["handType"] == 1:
            track = RHTrack
        elif cue["handType"] == 2:
            track = LHTrack
        else:
            track = EitherTrack

        behavior = cue["behavior"]
        channel = 0
        if behavior == 2:
            channel = 1
        elif behavior == 1:
            channel = 2
        elif behavior == 4:
            channel = 3
        elif behavior == 5:
            channel = 4

        tick = cue["tick"]
        tickLength = cue["tickLength"]

        track.append(midi.NoteOnEvent(tick=tick, velocity=cue["velocity"], pitch=cue["pitch"], channel=channel))
        track.append(midi.NoteOffEvent(tick=tick+tickLength, velocity=0, pitch=cue["pitch"], channel=channel))

        if cue["gridOffset"]["x"] != 0:
            track.append(midi.ControlChangeEvent(tick=tick, control=16, value=int(cue["gridOffset"]["x"] * 64 + 64)))
        if cue["gridOffset"]["y"] != 0:
            track.append(midi.ControlChangeEvent(tick=tick, control=17, value=int(cue["gridOffset"]["y"] * 64 + 64)))

    if "repeaters" in cues:
        for repeater in cues["repeaters"]:
            if repeater["handType"] == 1:
                track = RHTrack
            elif repeater["handType"] == 2:
                track = LHTrack
            elif repeater["handType"] == 0:
                track = EitherTrack
            else:
                continue

            track.append(midi.NoteOnEvent(tick=repeater["tick"], velocity=repeater["velocity"], pitch=repeater["pitch"]))
            track.append(midi.NoteOffEvent(tick=repeater["tick"]+repeater["tickLength"], velocity=0, pitch=repeater["pitch"]))

    HeaderTrack = midi.Track(sorted(HeaderTrack, key=lambda x: x.tick), tick_relative=False)
    RHTrack = midi.Track(sorted(RHTrack, key=lambda x: x.tick), tick_relative=False)
    LHTrack = midi.Track(sorted(LHTrack, key=lambda x: x.tick), tick_relative=False)
    EitherTrack = midi.Track(sorted(EitherTrack, key=lambda x: x.tick), tick_relative=False)

    HeaderTrack.append(midi.EndOfTrackEvent(tick=HeaderTrack[-1].tick))
    RHTrack.append(midi.EndOfTrackEvent(tick=RHTrack[-1].tick))
    LHTrack.append(midi.EndOfTrackEvent(tick=LHTrack[-1].tick))
    EitherTrack.append(midi.EndOfTrackEvent(tick=EitherTrack[-1].tick))

    HeaderTrack.make_ticks_rel()
    RHTrack.make_ticks_rel()
    LHTrack.make_ticks_rel()
    EitherTrack.make_ticks_rel()

    pattern.append(HeaderTrack)
    pattern.append(RHTrack)
    pattern.append(LHTrack)
    pattern.append(EitherTrack)

    midifile = cuesfile.replace('.cues','.mid')
    print "writing midi file to " + midifile

    midi.write_midifile(midifile, pattern)
    
def midi_to_cues(midifile):

    def make_custom_sort(orders):
        orders = [{k: -i for (i, k) in enumerate(reversed(order), 1)} for order in orders]
        def process(stuff):
            if isinstance(stuff, dict):
                l = [(k, process(v)) for (k, v) in stuff.items()]
                keys = set(stuff)
                for order in orders:
                    if keys.issuperset(order):
                        return OrderedDict(sorted(l, key=lambda x: order.get(x[0], 0)))
                return OrderedDict(sorted(l))
            if isinstance(stuff, list):
                return [process(x) for x in stuff]
            return stuff
        return process

    pattern = midi.read_midifile(midifile)

    active_notes = []
    targets = []
    repeaters = []
    tempo = -1

    pattern.make_ticks_abs()

    for track in pattern:
        if tempo == -1:
            for event in track:
                if type(event) is midi.SetTempoEvent:
                    tempo = event.get_bpm()
                    break

        handType = 0
        for event in track:
            if type(event) is midi.TrackNameEvent:
                if "RH" in event.text:
                    handType = 1
                    break
                if "LH" in event.text:
                    handType = 2
                    break

        ccs = []
        for event in track:
            if type(event) is midi.ControlChangeEvent:
                if event.get_control() == 16 or event.get_control() == 17:
                    ccs.append(event)

        for event in track:
            if type(event) is midi.NoteOnEvent:
                active_notes.append(event)
            if type(event) is midi.NoteOffEvent:
                for active_note in active_notes:
                    if active_note.get_pitch() == event.get_pitch():
                        if active_note.get_pitch() < 107:
                            target = {}

                            length = event.tick - active_note.tick
                            channel = event.channel

                            offsetX = 0
                            offsetY = 0
                            for cc in ccs:
                                if abs(active_note.tick - cc.tick) <= 10:
                                    if cc.get_control() == 16:
                                        offsetX = (cc.get_value() - 64) / 64.0
                                    if cc.get_control() == 17:
                                        offsetY = (cc.get_value() - 64) / 64.0

                            behavior = 0
                            if active_note.get_pitch() == 98 or active_note.get_pitch() == 99 or active_note.get_pitch() == 100 or active_note.get_pitch() == 101:
                                behavior = 6
                            elif length > 240:
                                behavior = 3
                            elif channel == 1:
                                behavior = 2
                            elif channel == 2:
                                behavior = 1
                            elif channel == 3:
                                behavior = 4
                            elif channel == 4:
                                behavior = 5

                            target["tick"] = active_note.tick
                            target["tickLength"] = length
                            target["pitch"] = active_note.get_pitch()
                            target["velocity"] = active_note.get_velocity()
                            target["gridOffset"] = {}
                            target["gridOffset"]["x"] = offsetX
                            target["gridOffset"]["y"] = offsetY
                            target["handType"] = handType
                            target["behavior"] = behavior

                            targets.append(target)
                        else:
                            repeater = {}
                            repeater["handType"] = handType
                            repeater["tick"] = active_note.tick
                            repeater["tickLength"] = event.tick - active_note.tick
                            repeater["pitch"] = active_note.get_pitch()
                            repeater["velocity"] = active_note.get_velocity()
                            repeaters.append(repeater)
                        for i in range(len(active_notes)): 
                            if active_notes[i].get_pitch() == active_note.get_pitch(): 
                                del active_notes[i] 
                                break
                        break

    sort = make_custom_sort([['tick', 'tickLength', 'pitch', 'velocity', 'gridOffset', 'handType', 'behavior']])
    targetsSorted = sort(targets)

    cues = {}
    cues['cues'] = sorted(targetsSorted, key=lambda x: x['tick'])
    cues['repeaters'] = repeaters
    if tempo != -1:
        cues['tempo'] = tempo

    cuesfile = midifile.replace('.mid','.cues')
    print "writing cues file to " + cuesfile

    with open(cuesfile, 'w') as outfile:  
        json.dump(cues, outfile, indent=4)