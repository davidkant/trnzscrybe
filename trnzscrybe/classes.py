"""Transcriber classes to the rescue!"""

from transcribers import *
from settings import *

import copy
import abjad as abj


class TimeSignature:
    """A time signaure."""

    def __init__(self, num_beats, beat):
        self.num_beats = num_beats
        self.beat = Quaver(str(beat))

    def to_abj(self):
        """Returns itself as an Abjad Time Signature."""
        return abj.TimeSignature((self.num_beats, int(self.beat.value_num)))  #//--> loks like abjad can't put dotted in time sig? ok.

    # def duration(self):
    #     return num_beats * 4.0/beat

class Quaver:
    """A Quaver.

    Init value is a string:

        '1'    whole
        '2.'   dotted half
        '2'    half
        '4.'   dotted quarter
        '4'    quarter
        '8.'   dotted eight
        '8'    eighth
        '16.'  dotted sixteenth
        '16'   sixteenth
        '32'   thirty-second
        '64'   sixty-fourth

    """

    def __init__(self, value):
        self.value_str = value
        self.value_num = int(self.value_str.split('.')[0]) * (1.0 if '.' not in self.value_str else 1.0/1.5)

    def duration_in_beats(self, time_signature): 
        """Quaver duration in beats."""
        return time_signature.beat.value_num/self.value_num

    # def duration_in_seconds(time_signature, tempo):
    #     """Quaver duration in seconds."""
    #     return tempo * self.duration_in_beats(time_signature)

class Note:
    """I am a note."""
    
    def __init__(self, time, pitch, onoff, prev=None, features=None):
        self.time = time
        self.pitch = pitch
        self.onoff = onoff
        self.features = features if features else []
    
    def __repr__(self):
        return 'Note({0}: time={1:.2f}, pitch={2})'.format(self.onoff, self.time, self.pitch)

class Tuplet:
    """Division of a beat(s)."""
    
    def __init__(self, multiply, base, min_required=0, weight=1):
        self.multiply = multiply
        self.base = base
        # self.duration = self.multiply[1]*self.base # now in beats
        self.divisions = self.multiply[0]
        self.min_required = min_required
        self.weight = weight
        self.hits = dict()

    # def duration_in_beats(self, time_signature):
    #     return self.base.duration_in_beats(time_signature) * self.multiply[1]

    def duration_in_beats(self):
        return self.multiply[1]*self.base

    def differentiate(self):
        diffthis = self.hits
        if 0 not in self.hits.keys(): diffthis[0] =  []   # //--> type this so not have hits[0] is ugly duder
        if self.divisions not in self.hits.keys(): diffthis[self.divisions] =  None  # //--> i thiiiink this one can be none
        keys_sorted = sorted(diffthis.keys())
        temp = [(y-x, diffthis[x]) for (x,y) in zip(keys_sorted[:-1], keys_sorted[1:])]# //--> put here: if y[0]-x[0] != 0
        return temp

    def transcribe(self, staff, time_signature, holdover=None, push=None, listeners=None, verbose=False):
        return transcribe_tuplet(self, staff, time_signature, holdover=holdover, push=push, listeners=listeners, verbose=verbose)

    def __repr__(self):
        return "Tuplet(multiply=%r, base=%r)" % \
            (self.multiply, self.base)
    
    def __str__(self):
        return "%r-er %r-let" % (self.base, self.divisions)

class Measure:
    """Time signaturea and some notes."""

    def __init__(self, time_signature=None, tempo=None, notes=None, measure_number=None, start_time=None):
        self.time_signature = time_signature
        self.tempo = tempo
        self.notes = notes if notes != None else []
        self.measure_number = measure_number
        self.start_time = start_time
        self.end_time = self.duration_in_seconds() + self.start_time

    def duration_in_seconds(self):
        """Measure duration in seconds."""
        return self.time_signature.num_beats * 60.0/self.tempo
    
    def append(self, new_notes):
        """Append notes."""
        self.notes.append(new_notes)

    def to_abj(self):
        """Returns an empty Abjad Measure."""
        return abj.Measure(self.time_signature.to_abj())

    def transcribe(self, staff, holdover=None, push=None, beat_division_scheme=None, listeners=None, verbose=False):
        return transcribe_measure(self, staff, holdover=holdover, push=push, beat_division_scheme=beat_division_scheme, listeners=listeners, verbose=verbose)

class RhythmTemplate:
    """Division of a measure."""
    
    def __init__(self, duration, divisions):
        self.duration = duration
        self.divisions = divisions
        
    def __repr__(self):
        return "RhythmTemplate(duration=%r, divisions=%r)" % \
            (self.duration, self.divisions)
    
    def __str__(self):
        return "RhythmTemplate(%r, %r)" % \
            (self.duration, self.divisions)

class Path:
    """Divsion of a measure."""

    def __init__(self, tuplets):
        self.tuplets = tuplets

    def integrate(self):
        return [0.0] + np.cumsum(reduce(lambda x,y: x+y, 
            [[float(t.duration_in_beats())/t.divisions]*t.divisions for t in self.tuplets])).tolist()
 
    def duplicate(self):
        return Path([Tuplet(t.multiply, t.base) for t in self.tuplets])
        # //--> or use deep copy, bro

class BeatDivisionScheme():

    def __init__(self):
        self.tuplets = []
        
    def clear_tuplets(self):
        self.tuplets = []

    def add_tuplet(self, multiply, base, min_required=0, weight=1):
        self.tuplets.append(Tuplet(multiply, base, min_required=min_required, weight=weight))
