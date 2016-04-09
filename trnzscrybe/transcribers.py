"""Transcription functions."""

# import classes
# import settings
# import tree
# import utilities

from classes import *
from tree import *
from settings import *
from utilities import *

import numpy as np
import copy
import itertools
import abjad as abj

"""

Transcribe Hierarchy

THINK ON:::
  
  -> wait a minute offs are here somewhere right b/c rests do happen...
  -> we don't need to return push from transcribe_tuplet

"""


#-------------------------------------------------------------------------------------------------#
# UTILITIES 
#-------------------------------------------------------------------------------------------------#
"""this should be in utilities"""

def mid_2_lil(mid):

        mid = int(round(mid))

        # pitch_classes = ['c', 'cs', 'd', 'ds', 'e', 'f', 'fs', 'g', 'gs', 'a', 'as', 'b']
        # pitch_classes = ['c', 'cs!', 'd', 'ds!', 'e', 'f', 'fs!', 'g', 'gs!', 'a', 'as!', 'b']
        # pitch_classes = ['c', 'cs!', 'd', 'ef!', 'e', 'f', 'fs!', 'g', 'af!', 'a', 'bf!', 'b']
        pitch_classes = ['c', 'df', 'd', 'ef', 'e', 'f', 'fs', 'g', 'af', 'a', 'bf', 'b']
        pitch_octaves = [',,,,', ',,,', ',,', ',', '', '\'', '\'\'', '\'\'\'', '\'\'\'\'', '\'\'\'\'\'']

        pitch_class = pitch_classes[mid%12]
        pitch_octave = pitch_octaves[mid/12]

        return pitch_class + pitch_octave

#-------------------------------------------------------------------------------------------------#
# TRANSCRIBE: TUPLET
#-------------------------------------------------------------------------------------------------#

#--- helpers -----------------------------------#

def spell_rhythm(num, base, dur_map, verbose=False):

    # subtraction, not modulo, b/c 1.0/0.5
    # will it always be 1? NO! (10, 1.0)
    
    if verbose:
        print '\nREDUCING'
        print 'num: {0}'.format(num)
        print 'base: {0}'.format(base)
        print 'dur: {0}'.format(num*base)
    
    rhythms = dur_map.keys()
    newbase = max([x for x in rhythms if x <= num*base])
    newnum = int(math.floor((num*base)/newbase))
    remainder = (num*base)-(newnum*newbase)
    
    if verbose:
        print '=> newnum: {0}'.format(newnum)
        print '=> new base: {0}'.format(newbase)
        print '=> remainder: {0}'.format(remainder)
    
    return [(newnum, newbase)] if remainder == 0 else [(newnum, newbase)] + \
        spell_rhythm(remainder/base, base, dur_map, verbose=verbose)

def apply_rhythm(this_notes, spelled_rhythm, rhythm_strings, notes_with_lily_features):

    #print 'notes_with_lily_features {0}'.format(notes_with_lily_features)

    lily_features = map(lambda n: filter(lambda f:f[0]=='lily', n.features), notes_with_lily_features)[0] if notes_with_lily_features else []
    #print lily_features
    lily_features = map(lambda x:x[1], lily_features)
    #print lily_features
    lily_features = reduce(lambda x,y: x+y, lily_features) if lily_features else ""
    #print 'lily_features {0}'.format(lily_features)
    subnotes = []

    for (num,base) in spelled_rhythm:
        for i in range(num):
        
            # FUCKING (efficiency) this all happens for each num. can do it outside just once

            # empty => rest
            if this_notes == []:
                thisone = abj.Rest('r' + rhythm_strings(base) + '\mp')

            # one note 
            elif len(this_notes) == 1:
                thisone = abj.Note(mid_2_lil(this_notes[0].pitch) + rhythm_strings(base) + lily_features)

            # chord
            else:
                thisone = abj.Chord("<" + reduce(lambda x,y: x+" "+y, [mid_2_lil(n.pitch) for n in this_notes]) + ">" + rhythm_strings(base) + lily_features)

            # append to subnotes
            subnotes.append(thisone)

    # if more than one subnote then tie them all up
    # first count how many
    # then reach back into subnotes and tie themup
    # wait this shouldn't work... meaning it probs doesn't...

    how_many = sum([x for (x,y) in spelled_rhythm])

    #print how_many

    if how_many > 1:
        #print "tieing"
        abj.attach(abj.Tie(), subnotes[how_many*-1::])
    
    return subnotes

def beam_notes(notes, tuplet):

    # do not manually beam tuplets less than 1 beat //--> for now... add later
    if tuplet.duration_in_beats() < 1: return

    # split into groups of notes and rests
    for(key, group) in itertools.groupby(notes, lambda n: isinstance(n, abj.Note)): # and n.duration < 1

        # convert to list (b/c exhausts iterable)
        group = list(group)

        # if it is notes and not singleton, beam it
        # if key and len(group) > 1: abj.attach(abj.Beam(), group)

def filter_gracenotes(held_notes, new_notes):

    # filter grace note outs and pop from note list
    gracenotes = []

    held_ons = [n for n in held_notes if n.onoff == 'on']
    held_offs = [n for n in held_notes if n.onoff == 'off']
    new_ons = [n for n in new_notes if n.onoff == 'on']
    new_offs = [n for n in new_notes if n.onoff == 'off']

    for off in held_offs:
        if off.pitch in [on.pitch for on in held_ons]:                
            index = [on.pitch for on in held_ons].index(off.pitch) # earliest by default
            thenote = held_ons.pop(index)
            if thenote in new_notes:
                gracenotes += [thenote]
    # look will both turn on and off this cycle
    # recognize by both an off and on this cycle
    # if we find pop it to gracenotes lists
    # alternativelty: a grace note is one that is off and on within diff cycle
    return gracenotes
    # they

def attach_gracenotes(gracenotes, receiver, base, rhythm_strings):

    if gracenotes != []:

        grace_chord_delta = 0.00

        # if they fall within grace_chord_delta, make a gracechord
        if max(gracenotes, key=lambda n: n.time).time - \
            min(gracenotes, key=lambda n: n.time).time \
            <= grace_chord_delta:

            gracenotes_abj = [abj.Chord("<" + 
                reduce(lambda x,y: x+" "+y, [mid_2_lil(n.pitch) for n in gracenotes]) + 
                ">" + rhythm_strings(base/((min(3,len(gracenotes))+1)/2*2)))]

        # else, make separate gracenotes
        else:
            # gracenotes_abj = [abj.Note(mid_2_lil(gracenote.pitch) + 
            #     rhythm_strings(base/((min(3,len(gracenotes))+1)/2*2))) for gracenote in gracenotes] # <--// this min 3 thing is a hack...
            gracenotes_abj = [abj.Note(mid_2_lil(gracenote.pitch) + rhythm_strings(base/(2))) for gracenote in gracenotes]

        # add to container
        grace_container = abj.scoretools.GraceContainer(gracenotes_abj, kind='grace')

        # attach container to main note
        abj.attach(grace_container, receiver)

def tieitup(held_notes, staff):

    #print "tie held {0}".format(held_notes)

    # don't think i can tie before i add to staff b/c logical voice contiguity error
    # FUCKING for now tie is just <yes or no> b/c we can't specify a partial tie

    if held_notes:

        #print "doing one"

        # previous note: last leaf of the previus tuplet 
        # FUCKING hardcoded assumes everything is a tuplet.
        # not_first_beat = len(staff[-1])!=0
        not_first_beat = len(staff[-1])!=1
        # print not_first_beat
        # print len(staff)
        # print staff[-1][-1]
        # print 'no'
        last_prev = staff[-1 if not_first_beat else -2][-2 if not_first_beat else -1][-1]
        # last_prev = staff[-1 if not_first_beat else -2][-1 if not_first_beat else -1][-1]
        # print last_prev

        # current note: first leaf of the current tuplet
        firs_curr = staff[-1][-1][0]

        # tie them
        abj.attach(abj.Tie(), [last_prev, firs_curr])

#--- main --------------------------------------#

def transcribe_tuplet(tuplet, staff, time_signature, holdover=None, push=None, listeners=None, verbose=False):

    """Transcribe a tuplet."""

    if verbose: print "\ntranscribing tuplet"

    #--- confused ------------------------------#

    """some setting for possible quaver in here i 
    feel should prolly be inside beat division sc
    heme or just open in settings? should pass be
    at division cheme or settings as like an envi
    ronment"""

    dur_map = dict([(quaver.duration_in_beats(time_signature), quaver.value_str) 
        for quaver in [Quaver(q) for q in quavers]])

    def rhythm_strings(duration):
        """Quaver for this duration in this time sig."""
        return dur_map[duration] 

    #--- setup ---------------------------------#

    # init holdover and push
    if holdover == None: holdover = []  # notes still sounding
    if push == None: push = []          # notes pushed from previous tuplet

    # init leaves
    leaves = []  # accumulate tuplet leaves (attach to abj.score at the end)

    # init tie flag
    is_tied = False
    
    #--- transcribe events ---------------------#
   
    """how wait there will only be push the first 
    time. do we even need to return push from thi
    s orr we do cuz we can push notes tuplet to t
    uplet not just over the bar right?"""

    """step through the tuplet event by event and 
    accumulate transcribed elements in leaves:

        1. parse notes
        2. spell them 
        3. call listeners
        4. handle gracenotes

    """

    # scope tied notes outside of the loop
    tied_notes = []  # this is the grand list of pairs
    prev_tied_froms_abj = [] # this is prev frame passed along init to []

    for i,event in enumerate(tuplet.differentiate()):

        if verbose: print "\ntranscribing event {0}".format(i)

        #--- setup ---------------------------------#

        event_duration, event_notes = event  # unpack event duration and notes

        new_notes = event_notes + push  # new notes this event
        held_notes = holdover           # any notes holding over still sounding

        new_ons = [n for n in new_notes if n.onoff == 'on']    # separate ons and offs
        new_offs = [n for n in new_notes if n.onoff == 'off']  # separate ons and offs

        held_ons = [n for n in held_notes if n.onoff == 'on']    # separate ons and offs
        held_offs = [n for n in held_notes if n.onoff == 'off']  # don't think we need this...
       
        gracenotes = []  # accumulate gracenotes 
        turned_off = []  # accumulate notes turned off this event 

        if verbose:
            print "\n  held notes {0}".format(held_notes)
            print "  new notes {0}".format(new_notes)
            print "  tied notes {0}".format(tied_notes)

        #--- parse on/offs -------------------------#

        """look through note offs and find the corres
        ponding note on. parse note on/off pairs into 
        turned_off and gracenotes. a note is a grace
        note if it has an off and on this event. a no
        te is a turned_off if it was previously sound
        ing. we find the earliest match by the defaul
        t be havior of using List.index"""

        if verbose: print "\n  turning notes off..."

        for off in copy.deepcopy(new_offs):  # deepcopy b/c popping and looping same list

            if verbose: print "    looking for {0}".format(off)

            # match a held note -> turned_off 
            if off.pitch in [on.pitch for on in held_ons]:                
                index = [on.pitch for on in held_ons].index(off.pitch)
                popped = held_ons.pop(index)
                if verbose: print "    popping to turned off {0}".format(popped)
                index = [off.pitch for off in new_offs].index(off.pitch)
                popped_off = new_offs.pop(index)
                turned_off += [popped_off]

            # match a new note -> gracenote
            elif off.pitch in [on.pitch for on in new_ons]:
                index = [on.pitch for on in new_ons].index(off.pitch)
                popped = new_ons.pop(index)
                if verbose: print "    popping to gracenotes {0}".format(popped)
                index = [off.pitch for off in new_offs].index(off.pitch)
                gracenotes += [popped]
                new_offs.pop(index)

        if verbose:
            print "\n  still being held (THATS A TIE) {0}".format(held_ons)
            print "\n  gracenotes {0}".format(gracenotes) 

        #--- spell event ---------------------------#

        """this is where we convert from time in seco
        nds to time in music notation. spelling is th
        e duration in music notation. we get the dura
        tion spelling and apply it to the current not
        es."""
        
        # want to notate both held + new notes
        new_and_held_ons = held_ons + new_ons
        
        # get spelling
        spelling = spell_rhythm(event_duration, tuplet.base, dur_map)

        if verbose: print "\n  spelling {0}".format(spelling)

        """filter for notes with 'lily' features. it'
        s a little funny but we have to do it here be
        cause of the way abjad works. this will chang
        e when we switch from abjad classes to our ow
        n internal representation. 'lily' features ca
        n be attached to both note ons and note offs 
        so we filter a list of new_ons + turned_offs."""

        notes_with_lily_features = [n for n in (new_ons + turned_off) 
            if 'lily' in [f[0] for f in n.features]]

        # apply spelling
        subnotes = apply_rhythm(new_and_held_ons, spelling, rhythm_strings, notes_with_lily_features)

        #--- listeners -----------------------------#

        """call any listeners. currently listeners ca
        n be registered with 'new_note' events and wi
        thi 'tied_note' events for now. more later pr
        obably."""

        # listener: new_note
        new_notes_raw = new_ons
        new_notes_abj = subnotes[0]
        if new_notes_raw:
            if verbose: print "\n  new notes!"
            if listeners:
                for listener in [listener for (kind,listener) in listeners if kind=='new_note']:
                    listener(new_notes_raw, new_notes_abj, verbose=verbose)

        # listener: tied_note
        tied_notes_raw = held_ons
        tied_notes_abj = subnotes[0]
        if tied_notes_raw:
            if verbose: print "\n  new notes!"
            if listeners:
                for listener in [listener for (kind,listener) in listeners if kind=='tied_note']:
                    listener(tied_notes_raw, tied_notes_abj, verbose=verbose)

        #--- finally -------------------------------#
        
        # attach grace notes
        attach_gracenotes(gracenotes, subnotes[-1], spelling[0][1], rhythm_strings)
        
        # flag any ties
        if held_ons: is_tied = True

        # append to eaves
        leaves.extend(subnotes)

        #--- ties ----------------------------------#

        """if incoming tie check for correspond note
        an incoming tie is ay held note (still on)
        if it matches to a noteoff it's off and don't care
        but if it comes in held and does off we want to 
        tie it. shouldn't we be doins that aboe? before
        new and held has the new part?
        
        if held_ons grab them from subnotes and pass along in list
        held_ons are the notes that are tied_TO
        new_and_held_ons are the notes that are tied_FROM
        wait since held_ons is in new_and_held_ons aren't we 
        going to grab the same note twice?

        exactly, that logic is incorrect. held_ons is
        NOT the held_TO b/c notes that are turned off
        this tie can be held_TO. go back up top and revise.

        uhh i take it back again

        TIED_TO = held_ons (after b/ing filtered for offs)
        TIED_FROMS = new_and_held_ons 

        this means some notes are BOTH tos and froms
        
        1. identify tied_to/froms
        2. grab them from subnotes
        3. put them in the right lists/pairs
        4. pass along froms
        5. store to/from pairs
        
        """
        # # 1. identify tied_to/froms
        # curr_tied_tos = held_ons
        # curr_tied_froms = new_and_held_ons

        # # 2. grab abjad notes from subnotes: filter for same pitch
        # # and grab the last (most recent) matching subnote
        # curr_tied_tos_abj = [filter(
        #     lambda x:x.written_pitch.numbered_pitch.pitch_number+60 == p.pitch, 
        #     subnotes)[-1] for p in curr_tied_tos]
        # curr_tied_froms_abj = [filter(
        #     lambda x:x.written_pitch.numbered_pitch.pitch_number+60 == p.pitch, 
        #     subnotes)[-1] for p in curr_tied_froms]

        # # 3. pair any prev_tied_from_abj wth curr_tied_tos_abj
        # for prev_from in prev_tied_froms_abj:

        #     # look for a  match in curr_tied_tos_abj
        #     matches = [i for i,curr_to in enumerate(curr_tied_tos_abj) if 
        #                prev_from.written_pitch.numbered_pitch.pitch_number+60 == 
        #                curr_to.written_pitch.numbered_pitch.pitch_number+60]

        #     # if a match is found
        #     if index:
        #         # pop first match
        #         curr_to = curr_tied_tos_abj.pop(matches[0])
        #         # add it to tied_notes as tuple
        #         tied_notes += [(prev_from,curr_to)]

        # # 4. curr_tied_froms_abj get passed to next i
        # prev_tied_froms_abj = curr_tied_froms_abj

        #--- and  ----------------------------------#

        # pass along any holdover and push
        holdover = new_and_held_ons
        push = []

    #--- transcribe tuplet ---------------------#

    """OK, we're about done! create an abjad tupl
    et and append it to the current staff."""
    
    # manually beam beam_notes
    beam_notes(leaves, tuplet)

    # create tuplet
    this_tuplet = abj.Tuplet(abj.Multiplier(tuplet.multiply[1], tuplet.multiply[0]), leaves)

    # append it to the last measure
    staff[-1].append(this_tuplet)
    
    # and finally apply any ties 
    tieitup(is_tied, staff)

    #--- the end -------------------------------#

    # return any holdover and push
    return holdover, push

#-------------------------------------------------------------------------------------------------#
# TRANSCRIBE: MEASURE
#-------------------------------------------------------------------------------------------------#

#--- helpers -----------------------------------#

def quanitze_2_path(notes, to_path, tempo):
    """Quantize."""
    
    push = [] # push an excess to next measure
    path = to_path.duplicate() # duplicate for storage
 
    # integrate 
    integrated = path.integrate()

    # tempo sacle
    integrated = map(lambda x: x * 60.0/tempo, integrated)
    
    # associate (None,None) to catch pushes
    associated = zip(integrated, (reduce(lambda x,y: x+y, [[(t,d) for d in range(t.divisions)]for t in path.tuplets])) + [(None,None)])

    # find closest and add hits to tuplet
    for note in notes:

        # find closest: return associate elem
        closest = min(associated, key=lambda (p,(t,h)): abs(note.time-p))

        # unpack
        (p,(t,h)) = closest
        
        # add hits to elem
        if p != integrated[-1]: # if not last
            if h in t.hits: t.hits[h] += [note]
            else: t.hits[h] = [note]
        else: # else push it
            push += [note]
            
    return path, push

#--- main --------------------------------------#

def transcribe_measure(measure, staff, holdover=None, push=None, beat_division_scheme=None, listeners=None, verbose=False):

    """Transcribe a measure."""

    if verbose: print "\ntranscribing measure {0}".format(measure.measure_number)

    #--- setup ---------------------------------#
    
    # init holdover
    if holdover == None: holdover = []
    if push == None: push = []

    #--- parse measure into tuplets ------------#

    # find best fit
    tree = Tree(measure.time_signature, measure.tempo, beat_division_scheme)
    tree.calculate(measure.notes)
    best_error, best_node = tree.optimal_bouquet()

    # convert to path
    best_path = best_node.to_path()

    # quantize to it        
    quantized_path, mpush = quanitze_2_path(measure.notes, best_path, measure.tempo)

    #--- transcribe tuplets --------------------#

    # add measure to Abjad staff
    staff.append(measure.to_abj())

    tholdover = holdover
    tpush = push

    if verbose:
        print "\n  best path {0}".format(best_node)
        print "  error {0}".format(best_error)

    # and transcribe to it
    for t in quantized_path.tuplets:
        tholdover, tpush = t.transcribe(staff, measure.time_signature, holdover=tholdover, push=tpush, listeners=listeners, verbose=verbose)

    #--- verbose -------------------------------#

    if verbose:
        print "\nreturns:"
        print "holdover {0}".format(tholdover)
        print "push {0}".format(mpush + tpush)

    #--- the end -------------------------------#

    # return any holdover or push
    return tholdover, (mpush + tpush)

#-------------------------------------------------------------------------------------------------#
# TRANSCRIBE: NOTE LIST
#-------------------------------------------------------------------------------------------------#

def transcribe(notes, staff=None, time_signatures=None, tempi=None, beat_division_scheme=None, listeners=None, verbose=False):

    """Transcribe takes the totally raw $&i* and makes music."""

    #--- setup ---------------------------------#

    # default params
    if staff == None: staff = abj.Staff()
    if time_signatures == None: time_signatures = [(4,4)]
    if tempi == None: tempi = [60.0]
    if beat_division_scheme == None: beat_division_scheme = default_beat_division_scheme()

    # init
    measure_number = 1  # start counting mm. from 1 (like in music!)
    measures = []       # list of measures

    # convert time signature tuples to classes
    if time_signatures != None: time_signatures = [TimeSignature(x,y) for (x,y) in time_signatures]

    # make a deep copy of notes so we can modify it
    notes = copy.deepcopy(notes)

    # sort notes by time
    notes.sort(key=lambda n: n.time)

    #--- parse notes into measures -------------#
    
    # create the first measure and add to list
    measures.append(Measure(
        time_signature=time_signatures[0],  # time sig 0
        tempo=tempi[0],                     # tempo 0
        measure_number=measure_number,      # measure number
        start_time=0)                       # start at 0.0 seconds
    )
    
    # loop thru notes and add them to measures
    while notes: 

        # current measure is the last in the list
        curr_measure = measures[-1]

        # if the note falls in current measure, add to measure and pop from notes list
        if notes[0].time < curr_measure.end_time:

            # pop and add to measure
            note = notes.pop(0)                   # pop it
            note.time -= curr_measure.start_time  # offset to local time
            curr_measure.append(note)             # add to measure

        # if the note does not fall in current measure, make a new measure
        else:

            # next measure params
            time_signature = time_signatures[min(measure_number, len(time_signatures)-1)]  # this or last
            tempo = tempi[min(measure_number, len(tempi)-1)]                               # this or last
            measure_number += 1                                                            # incr measure num
            start_time = curr_measure.end_time                                             # end of previous

            # create new measure
            measures.append(Measure(                                           
                time_signature=time_signature,
                tempo=tempo,
                measure_number=measure_number,
                start_time=start_time)
            )

    #--- transcribe measures -------------------#

    # progress bar?
    num_measures = len(measures)

    # init holdover
    holdover = None
    push = None

    # loop thru measures and transcribe them
    for measure in measures:

        print '\r{0}/{1}'.format(measure.measure_number,num_measures),

        holdover, push = measure.transcribe(staff, 
            holdover=holdover, 
            push=push,
            beat_division_scheme=beat_division_scheme, listeners=listeners, verbose=verbose)

    #--- the end -------------------------------#

    return staff

