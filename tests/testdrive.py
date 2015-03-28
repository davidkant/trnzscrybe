"""Transcribe test suite.

Tests the basic transcriber features. 

TODO:
- rewrite using NOSE!
- document usage and parameters
- write pdfs to file
- ipython notebook Tutorial integration (we could just call these but i want to see the code)

dkant, March 2015

"""

import trnzscrybe_master.trnzscrybe as xscribe
import abjad as abj
import random

#-------------------------------------------------------------------------------------------------#
# The snipper 
#-------------------------------------------------------------------------------------------------#

def snipper(snip, safe=True, headless=True):
    """ Transcribe a snippet. """

    # unpack
    foo, solution_string = snip
    notes, params = foo();

    # print
    print "{0}...".format(foo.__doc__),

    # yes safe
    if safe:

        # catch errors
        try:

            # transcribe
            staff_hat = xscribe.transcribe(notes, **params)

            # render lily
            if not headless: abj.show(make_lilyfile(staff_hat))

        # no go
        except Exception as inst:

            # fail!
            print "FAIL!"

            # what happened?
            print " --> ERROR! {0}".format(type(inst))

            # and return
            return 0

        # yes go
        else:

            # is it correct?
            correct = staff_hat.__format__() == solution_string

            # tell me about it
            print "PASS!" if correct else "FAIL!"
            
            # plot notes
            if not headless: xscribe.plot_notes(notes, figsize=(12,3))

            # and return
            return correct

    # no safe
    else: 

        # transcribe
        staff_hat = xscribe.transcribe(notes, **params)

        # render lily
        if not headless: abj.show(make_lilyfile(staff_hat))

        # is it correct?
        correct = staff_hat.__format__() == solution_string

        # tell me about it
        print "PASS!" if correct else "FAIL!"
        
        # plot notes
        if not headless: plot_notes(notes, figsize=(12,3))

        # and return
        return correct

#-------------------------------------------------------------------------------------------------#
# The snippets 
#-------------------------------------------------------------------------------------------------#

snips = []

#-----------------------------------------------#

def foo():
    """just a bunch of quarter notes"""

    # params
    tempi = [60.0]
    time_sigs = [(4,4)]

    # notes
    notes = []
    notes += xscribe.make_note(0.00, 60, 1.00)
    notes += xscribe.make_note(1.00, 62, 1.00)
    notes += xscribe.make_note(2.00, 64, 1.00)
    notes += xscribe.make_note(3.00, 65, 1.00)
    notes += xscribe.make_note(4.00, 67, 1.00)
    notes += xscribe.make_note(5.00, 69, 1.00)
    notes += xscribe.make_note(6.00, 71, 1.00)
    notes += xscribe.make_note(7.00, 72, 1.00)

    # return it
    return notes, {'tempi': tempi, 'time_signatures': time_sigs}

solution_string = "\\new Staff {\n\t{\n\t\t\\time 4/4\n\t\t{\n\t\t\tc'4\n\t\t}\n\t\t{\n\t\t\td'4\n\t\t}\n\t\t{\n\t\t\te'4\n\t\t}\n\t\t{\n\t\t\tf'4\n\t\t}\n\t}\n\t{\n\t\t{\n\t\t\tg'4\n\t\t}\n\t\t{\n\t\t\ta'4\n\t\t}\n\t\t{\n\t\t\tb'4\n\t\t}\n\t\t{\n\t\t\tc''4\n\t\t}\n\t}\n\t{\n\t\t{\n\t\t\tr1\n\t\t}\n\t}\n}"

snips += [(foo, solution_string)]

#-----------------------------------------------#

def foo():
    """not just quarter notes"""

    # params
    tempi = [60.0]
    time_sigs = [(4,4)]

    # notes
    notes = []
    notes += xscribe.make_note(0.00, 60, 1.00)
    notes += xscribe.make_note(1.00, 62, 0.50)
    notes += xscribe.make_note(1.50, 64, 0.50)
    notes += xscribe.make_note(2.00, 65, 0.25)
    notes += xscribe.make_note(2.25, 60, 0.25)
    notes += xscribe.make_note(2.50, 62, 0.25)
    notes += xscribe.make_note(2.75, 64, 0.25)
    notes += xscribe.make_note(3.00, 65, 1.00)
    notes += xscribe.make_note(4.00, 70, 2.00)

    # return it
    return notes, {'tempi': tempi, 'time_signatures': time_sigs}

solution_string = "\\new Staff {\n\t{\n\t\t\\time 4/4\n\t\t{\n\t\t\tc'4\n\t\t}\n\t\t{\n\t\t\td'8\n\t\t\te'8\n\t\t}\n\t\t{\n\t\t\tf'16\n\t\t\tc'16\n\t\t\td'16\n\t\t\te'16\n\t\t}\n\t\t{\n\t\t\tf'4\n\t\t}\n\t}\n\t{\n\t\t{\n\t\t\tas'2\n\t\t}\n\t\t{\n\t\t\tr2\n\t\t}\n\t}\n}"

snips += [(foo, solution_string)]

#-----------------------------------------------#

def foo():
    """let's make the rhythm a bit more complex"""

    # params
    tempi = [60.0]
    time_sigs = [(4,4)]

    # make notes
    random.seed(1)

    notes = []
    note_durs = [1.0/4, 1.0/2, 1.0/1, 1.0/0.5]
    curr_time = 0
    total_time = 8.0

    while curr_time < total_time:

        note_dur = note_durs[random.randint(0, len(note_durs)-1)]
        
        if random.randint(0,1) == 0:
            note_pitch = random.randint(58,72)
            notes += xscribe.make_note(curr_time, note_pitch, note_dur)
            curr_time += note_dur
            
        else:
            curr_time += note_dur

    # return it
    return notes, {'tempi': tempi, 'time_signatures': time_sigs}

solution_string = "\\new Staff {\n\t{\n\t\t\\time 4/4\n\t\t{\n\t\t\tr16\n\t\t\tf'8. ~\n\t\t}\n\t\t{\n\t\t\tf'4 ~\n\t\t}\n\t\t{\n\t\t\tf'16\n\t\t\tr8\n\t\t\tas16 ~\n\t\t}\n\t\t{\n\t\t\tas4 ~\n\t\t}\n\t}\n\t{\n\t\t{\n\t\t\tas8.\n\t\t\ta'16 ~\n\t\t}\n\t\t{\n\t\t\ta'4 ~\n\t\t}\n\t\t{\n\t\t\ta'8.\n\t\t\tgs'16\n\t\t}\n\t\t{\n\t\t\tr16\n\t\t\tas8. ~\n\t\t}\n\t}\n\t{\n\t\t{\n\t\t\tas4 ~\n\t\t}\n\t\t{\n\t\t\tas16\n\t\t\tr8.\n\t\t}\n\t\t{\n\t\t\tr2\n\t\t}\n\t}\n}"

snips += [(foo, solution_string)]

#-----------------------------------------------#

def foo():
    """i assume you can do tuplets, too. all kinds yes?"""

    # params
    tempi = [60.0]
    time_sigs = [(4,4)]

    # notes
    notes = []

    notes += xscribe.make_note(0.0/3, 60, 1.0/3)
    notes += xscribe.make_note(1.0/3, 62, 1.0/3)
    notes += xscribe.make_note(2.0/3, 64, 1.0/3)

    notes += xscribe.make_note(1 + 0.0/5, 60, 1.0/5)
    notes += xscribe.make_note(1 + 1.0/5, 62, 1.0/5)
    notes += xscribe.make_note(1 + 2.0/5, 64, 1.0/5)
    notes += xscribe.make_note(1 + 3.0/5, 65, 1.0/5)
    notes += xscribe.make_note(1 + 4.0/5, 67, 1.0/5)

    notes += xscribe.make_note(2 + 0.0/6, 60, 1.0/6)
    notes += xscribe.make_note(2 + 1.0/6, 62, 1.0/6)
    notes += xscribe.make_note(2 + 2.0/6, 64, 1.0/6)
    notes += xscribe.make_note(2 + 3.0/6, 65, 1.0/6)
    notes += xscribe.make_note(2 + 4.0/6, 67, 1.0/6)
    notes += xscribe.make_note(2 + 5.0/6, 69, 1.0/6)

    notes += xscribe.make_note(3 + 0.0/7, 60, 1.0/7)
    notes += xscribe.make_note(3 + 1.0/7, 62, 1.0/7)
    notes += xscribe.make_note(3 + 2.0/7, 64, 1.0/7)
    notes += xscribe.make_note(3 + 3.0/7, 65, 1.0/7)
    notes += xscribe.make_note(3 + 4.0/7, 67, 1.0/7)
    notes += xscribe.make_note(3 + 5.0/7, 69, 1.0/7)
    notes += xscribe.make_note(3 + 6.0/7, 71, 1.0/7)

    # return it
    return notes, {'tempi': tempi, 'time_signatures': time_sigs}

solution_string = "\\new Staff {\n\t{\n\t\t\\time 4/4\n\t\t\\times 2/3 {\n\t\t\tc'8\n\t\t\td'8\n\t\t\te'8\n\t\t}\n\t\t\\times 4/5 {\n\t\t\tc'16\n\t\t\td'16\n\t\t\te'16\n\t\t\tf'16\n\t\t\tg'16\n\t\t}\n\t\t\\times 2/3 {\n\t\t\tc'16\n\t\t\td'16\n\t\t\te'16\n\t\t\tf'16\n\t\t\tg'16\n\t\t\ta'16\n\t\t}\n\t\t\\times 4/7 {\n\t\t\tc'16\n\t\t\td'16\n\t\t\te'16\n\t\t\tf'16\n\t\t\tg'16\n\t\t\ta'16\n\t\t\tb'16\n\t\t}\n\t}\n\t{\n\t\t{\n\t\t\tr1\n\t\t}\n\t}\n}"

snips += [(foo, solution_string)]

#-----------------------------------------------#

def foo():
    """this thing can handle ties right?"""

    # params
    tempi = [60.0]
    time_sigs = [(4,4)]

    # notes
    notes = []
    notes += xscribe.make_note(0.00, 69, 1.00)
    notes += xscribe.make_note(1.00, 63, 1.00)
    notes += xscribe.make_note(2.00, 64, 1.00)
    notes += xscribe.make_note(3.00, 66, 2.00)
    notes += xscribe.make_note(5.00, 67, 1.00)
    notes += xscribe.make_note(6.00, 69, 1.00)
    notes += xscribe.make_note(7.00, 73, 3.00)
    notes += xscribe.make_note(10.00, 72, 1.00)

    # return it
    return notes, {'tempi': tempi, 'time_signatures': time_sigs}

solution_string = "\\new Staff {\n\t{\n\t\t\\time 4/4\n\t\t{\n\t\t\ta'4\n\t\t}\n\t\t{\n\t\t\tds'4\n\t\t}\n\t\t{\n\t\t\te'4\n\t\t}\n\t\t{\n\t\t\tfs'4 ~\n\t\t}\n\t}\n\t{\n\t\t{\n\t\t\tfs'4\n\t\t}\n\t\t{\n\t\t\tg'4\n\t\t}\n\t\t{\n\t\t\ta'4\n\t\t}\n\t\t{\n\t\t\tcs''4 ~\n\t\t}\n\t}\n\t{\n\t\t{\n\t\t\tcs''2\n\t\t}\n\t\t{\n\t\t\tc''4\n\t\t}\n\t\t{\n\t\t\tr4\n\t\t}\n\t}\n}"

snips += [(foo, solution_string)]

#-----------------------------------------------#

def foo():
    """how about two notes at once"""

    # params
    tempi = [60.0]
    time_sigs = [(4,4)]

    # notes
    notes = []
    notes += xscribe.make_note(0.00, 63, 1.00)
    notes += xscribe.make_note(0.00, 67, 1.00)
    notes += xscribe.make_note(1.00, 62, 1.00)
    notes += xscribe.make_note(1.00, 70, 1.00)
    notes += xscribe.make_note(2.00, 67, 1.00)
    notes += xscribe.make_note(2.00, 72, 1.00)
    notes += xscribe.make_note(3.00, 69, 1.00)
    notes += xscribe.make_note(3.00, 60, 1.00)
    notes += xscribe.make_note(4.00, 68, 2.00)
    notes += xscribe.make_note(4.00, 61, 2.00)

    # return it
    return notes, {'tempi': tempi, 'time_signatures': time_sigs}

solution_string = "\\new Staff {\n\t{\n\t\t\\time 4/4\n\t\t{\n\t\t\t<ds' g'>4\n\t\t}\n\t\t{\n\t\t\t<d' as'>4\n\t\t}\n\t\t{\n\t\t\t<g' c''>4\n\t\t}\n\t\t{\n\t\t\t<c' a'>4\n\t\t}\n\t}\n\t{\n\t\t{\n\t\t\t<cs' gs'>2\n\t\t}\n\t\t{\n\t\t\tr2\n\t\t}\n\t}\n}"

snips += [(foo, solution_string)]

#-----------------------------------------------#

def foo():
    """what about really close notes? gracenotes"""

    # params
    tempi = [60.0]
    time_sigs = [(4,4)]

    # notes
    notes = []
    notes += xscribe.make_note(0.00, 63, 0.95)
    notes += xscribe.make_note(0.95, 67, 0.05)  # gracenote
    notes += xscribe.make_note(1.00, 66, 0.05)  # gracenote
    notes += xscribe.make_note(1.05, 72, 0.95)
    notes += xscribe.make_note(2.00, 70, 1.00)
    notes += xscribe.make_note(3.00, 68, 0.01)  # gracenote
    notes += xscribe.make_note(3.01, 64, 0.01)  # gracenote
    notes += xscribe.make_note(3.02, 66, 0.01)  # gracenote
    notes += xscribe.make_note(3.03, 62, 0.97)
    notes += xscribe.make_note(4.00, 71, 0.04)  # gracenote
    notes += xscribe.make_note(4.04, 72, 0.96)

    # return it
    return notes, {'tempi': tempi, 'time_signatures': time_sigs}

solution_string = "\\new Staff {\n\t{\n\t\t\\time 4/4\n\t\t{\n\t\t\tds'4\n\t\t}\n\t\t{\n\t\t\t\\grace {\n\t\t\t\tg'8\n\t\t\t\tfs'8\n\t\t\t}\n\t\t\tc''4\n\t\t}\n\t\t{\n\t\t\tas'4\n\t\t}\n\t\t{\n\t\t\t\\grace {\n\t\t\t\tgs'16\n\t\t\t\te'16\n\t\t\t\tfs'16\n\t\t\t}\n\t\t\td'4\n\t\t}\n\t}\n\t{\n\t\t{\n\t\t\t\\grace {\n\t\t\t\t<b'>8\n\t\t\t}\n\t\t\tc''4\n\t\t}\n\t\t{\n\t\t\tr4\n\t\t}\n\t\t{\n\t\t\tr2\n\t\t}\n\t}\n}"

snips += [(foo, solution_string)]

#-----------------------------------------------#

def foo():
    """let's change the tempo"""

    # params
    tempi = [70]
    time_sigs = [(4,4)]

    # notes
    notes = []
    notes += xscribe.make_note(0.00, 60, 1.00)
    notes += xscribe.make_note(1.00, 62, 1.00)
    notes += xscribe.make_note(2.00, 64, 1.00)
    notes += xscribe.make_note(3.00, 65, 1.00)
    notes += xscribe.make_note(4.00, 67, 1.00)
    notes += xscribe.make_note(5.00, 69, 1.00)
    notes += xscribe.make_note(6.00, 71, 1.00)
    notes += xscribe.make_note(7.00, 72, 1.00)

    # return it
    return notes, {'tempi': tempi, 'time_signatures': time_sigs}

solution_string = "\\new Staff {\n\t{\n\t\t\\time 4/4\n\t\t{\n\t\t\tc'4 ~\n\t\t}\n\t\t\\times 2/3 {\n\t\t\tc'16\n\t\t\td'4 ~\n\t\t\td'16 ~\n\t\t}\n\t\t\\times 2/3 {\n\t\t\td'8\n\t\t\te'4 ~\n\t\t}\n\t\t{\n\t\t\te'8\n\t\t\tf'8 ~\n\t\t}\n\t}\n\t{\n\t\t\\times 2/3 {\n\t\t\tf'4\n\t\t\tg'8 ~\n\t\t}\n\t\t\\times 2/3 {\n\t\t\tg'4 ~\n\t\t\tg'16\n\t\t\ta'16 ~\n\t\t}\n\t\t{\n\t\t\ta'4\n\t\t}\n\t\t{\n\t\t\tb'4 ~\n\t\t}\n\t}\n\t{\n\t\t\\times 2/3 {\n\t\t\tb'16\n\t\t\tc''4 ~\n\t\t\tc''16 ~\n\t\t}\n\t\t\\times 2/3 {\n\t\t\tc''8\n\t\t\tr4\n\t\t}\n\t\t{\n\t\t\tr2\n\t\t}\n\t}\n}"

snips += [(foo, solution_string)]

#-----------------------------------------------#

def foo():
    """multiple tempos(sp)?"""

    # params
    tempi = [120, 60, 30]
    time_sigs = [(4,4)]

    # notes
    notes = []
    notes += xscribe.make_note(0.00, 60, 1.00)
    notes += xscribe.make_note(1.00, 62, 1.00)
    notes += xscribe.make_note(2.00, 64, 1.00)
    notes += xscribe.make_note(3.00, 65, 1.00)
    notes += xscribe.make_note(4.00, 67, 1.00)
    notes += xscribe.make_note(5.00, 69, 1.00)
    notes += xscribe.make_note(6.00, 71, 1.00)
    notes += xscribe.make_note(7.00, 72, 1.00)

    # return it
    return notes, {'tempi': tempi, 'time_signatures': time_sigs}

solution_string = "\\new Staff {\n\t{\n\t\t\\time 4/4\n\t\t{\n\t\t\tc'2\n\t\t}\n\t\t{\n\t\t\td'2\n\t\t}\n\t}\n\t{\n\t\t{\n\t\t\te'4\n\t\t}\n\t\t{\n\t\t\tf'4\n\t\t}\n\t\t{\n\t\t\tg'4\n\t\t}\n\t\t{\n\t\t\ta'4\n\t\t}\n\t}\n\t{\n\t\t{\n\t\t\tb'8\n\t\t\tc''8\n\t\t}\n\t\t{\n\t\t\tr4\n\t\t}\n\t\t{\n\t\t\tr2\n\t\t}\n\t}\n}"

snips += [(foo, solution_string)]

#-----------------------------------------------#

def foo():
    """we can change the time signature too"""

    # params
    tempi = [60]
    time_sigs = [(3,4)]

    # notes
    notes = []
    notes += xscribe.make_note(0.00, 60, 1.00)
    notes += xscribe.make_note(1.00, 62, 1.00)
    notes += xscribe.make_note(2.00, 64, 1.00)
    notes += xscribe.make_note(3.00, 65, 1.00)
    notes += xscribe.make_note(4.00, 67, 1.00)
    notes += xscribe.make_note(5.00, 69, 1.00)
    notes += xscribe.make_note(6.00, 71, 1.00)
    notes += xscribe.make_note(7.00, 72, 1.00)

    # return it
    return notes, {'tempi': tempi, 'time_signatures': time_sigs}

solution_string = "\\new Staff {\n\t{\n\t\t\\time 3/4\n\t\t{\n\t\t\tc'4\n\t\t}\n\t\t{\n\t\t\td'4\n\t\t}\n\t\t{\n\t\t\te'4\n\t\t}\n\t}\n\t{\n\t\t{\n\t\t\tf'4\n\t\t}\n\t\t{\n\t\t\tg'4\n\t\t}\n\t\t{\n\t\t\ta'4\n\t\t}\n\t}\n\t{\n\t\t{\n\t\t\tb'4\n\t\t}\n\t\t{\n\t\t\tc''4\n\t\t}\n\t\t{\n\t\t\tr4\n\t\t}\n\t}\n}"

snips += [(foo, solution_string)]

#-----------------------------------------------#

def foo():
    """and not just once"""

    # params
    tempi = [60]
    time_sigs = [(3,4), (5,8)]

    # notes
    notes = []
    notes += xscribe.make_note(0.00, 60, 1.00)
    notes += xscribe.make_note(1.00, 62, 1.00)
    notes += xscribe.make_note(2.00, 64, 1.00)
    notes += xscribe.make_note(3.00, 65, 1.00)
    notes += xscribe.make_note(4.00, 67, 1.00)
    notes += xscribe.make_note(5.00, 69, 1.00)
    notes += xscribe.make_note(6.00, 71, 1.00)
    notes += xscribe.make_note(7.00, 72, 1.00)

    # return it
    return notes, {'tempi': tempi, 'time_signatures': time_sigs}

solution_string = "\\new Staff {\n\t{\n\t\t\\time 3/4\n\t\t{\n\t\t\tc'4\n\t\t}\n\t\t{\n\t\t\td'4\n\t\t}\n\t\t{\n\t\t\te'4\n\t\t}\n\t}\n\t{\n\t\t\\time 5/8\n\t\t{\n\t\t\tf'8\n\t\t}\n\t\t{\n\t\t\tg'8\n\t\t}\n\t\t{\n\t\t\ta'8\n\t\t}\n\t\t{\n\t\t\tb'8\n\t\t}\n\t\t{\n\t\t\tc''8\n\t\t}\n\t}\n\t{\n\t\t{\n\t\t\tr8\n\t\t}\n\t\t{\n\t\t\tr2\n\t\t}\n\t}\n}"

snips += [(foo, solution_string)]

#-----------------------------------------------#

def foo():
    """random notes, random tempi, random time sigs"""

    # notes
    random.seed(0)

    notes = []
    curr_time = 0
    total_time = 20.0

    while curr_time < total_time:

        note_dur = random.random()
        
        if random.randint(0,5) <= 4:
            note_pitch = random.randint(58,72)
            notes += xscribe.make_note(curr_time, note_pitch, note_dur)
            curr_time += note_dur
            
        else:
            curr_time += note_dur


    # params
    tempi = [random.random()*90 + 50 for i in range(7)]
    time_sigs = [(random.randint(4,6), random.randint(1,2)*4) for i in range(7)]

    # return it
    return notes, {'tempi': tempi, 'time_signatures': time_sigs}

solution_string = "\\new Staff {\n\t{\n\t\t\\time 6/4\n\t\t{\n\t\t\te'4 ~\n\t\t}\n\t\t\\times 4/7 {\n\t\t\te'8\n\t\t\te'8.\n\t\t\tf'8 ~\n\t\t}\n\t\t{\n\t\t\tf'4\n\t\t}\n\t\t\\times 4/7 {\n\t\t\tr4.\n\t\t\ta'16 ~\n\t\t}\n\t\t\\times 2/3 {\n\t\t\ta'4\n\t\t\tb'8 ~\n\t\t}\n\t\t\\times 4/5 {\n\t\t\tb'8.\n\t\t\tb'8 ~\n\t\t}\n\t}\n\t{\n\t\t{\n\t\t\tb'4 ~\n\t\t}\n\t\t\\times 4/7 {\n\t\t\tb'8\n\t\t\tb'4\n\t\t\tb2 ~\n\t\t}\n\t\t\\times 4/7 {\n\t\t\tb16\n\t\t\tb'4 ~\n\t\t\tb'16\n\t\t\tas'16 ~\n\t\t}\n\t\t{\n\t\t\tas'4 ~\n\t\t}\n\t\t\\times 4/7 {\n\t\t\tas'4\n\t\t\tfs'8.\n\t\t}\n\t}\n\t{\n\t\t\\time 4/8\n\t\t{\n\t\t\t\\grace {\n\t\t\t\t<ds'>16\n\t\t\t}\n\t\t\tas8 ~\n\t\t}\n\t\t\\times 4/5 {\n\t\t\tas8\n\t\t\tr32\n\t\t}\n\t\t\\times 2/3 {\n\t\t\tr8\n\t\t\tr32\n\t\t\tb'32 ~\n\t\t}\n\t\t\\times 4/5 {\n\t\t\tb'16\n\t\t\tcs'16\n\t\t\te'32 ~\n\t\t}\n\t}\n\t{\n\t\t{\n\t\t\te'8\n\t\t}\n\t\t\\times 4/7 {\n\t\t\tf'32\n\t\t\tfs'8. ~\n\t\t}\n\t\t{\n\t\t\tfs'32\n\t\t\tas'16. ~\n\t\t}\n\t\t\\times 4/7 {\n\t\t\tas'32\n\t\t\tr8\n\t\t\te'16 ~\n\t\t}\n\t}\n\t{\n\t\t\\time 6/8\n\t\t\\times 4/7 {\n\t\t\te'8 ~\n\t\t\te'32\n\t\t\tfs'16 ~\n\t\t}\n\t\t\\times 4/7 {\n\t\t\tfs'8.\n\t\t\tc'8\n\t\t\tf'8 ~\n\t\t}\n\t\t\\times 4/5 {\n\t\t\tf'16.\n\t\t\tb'32\n\t\t\tr32\n\t\t}\n\t\t{\n\t\t\tr4\n\t\t}\n\t}\n\t{\n\t\t\\time 6/4\n\t\t\\times 2/3 {\n\t\t\tr4\n\t\t\tgs'8 ~\n\t\t}\n\t\t{\n\t\t\tgs'16\n\t\t\tas'16\n\t\t\tc''8 ~\n\t\t}\n\t\t\\times 4/5 {\n\t\t\tc''8\n\t\t\tg'8.\n\t\t}\n\t\t{\n\t\t\tr4\n\t\t}\n\t\t\\times 4/5 {\n\t\t\tg'4\n\t\t\tr4.\n\t\t}\n\t}\n}"

snips += [(foo, solution_string)]

#-----------------------------------------------#

def foo():
    """how do we change possible subdivisions?"""

    # params
    tempi = [60]
    time_sigs = [(4,4)]

    # BeatDivisionScheme
    bds = xscribe.BeatDivisionScheme()

    # duration 4 beats
    # bds.add_tuplet((1,1), 4.0)    # /1 whole note
    # bds.add_tuplet((3,2), 2.0)    # /3 half note triplet
    # bds.add_tuplet((5,4), 1.0)    # /5 quarter note quintuplet
    # bds.add_tuplet((7,4), 1.0)    # /5 quarter note septuplet

    # duration 2 beats
    # bds.add_tuplet((1,1), 2.0)    # /1 half note
    bds.add_tuplet((3,2), 1.0)      # /3 quarter note triplet
    # bds.add_tuplet((5,4), 1.0/2)  # /5 eighth note quintuplet
    # bds.add_tuplet((7,4), 1.0/2)  # /7 eighth note septuplet

    # duration 1 beat
    # bds.add_tuplet((1,1), 1.0)    # /1 quarter note
    # bds.add_tuplet((2,2), 1.0/2)  # /2 eighth note
    # bds.add_tuplet((3,2), 1.0/2)  # /3 eighth note triplet
    # bds.add_tuplet((4,4), 1.0/4)  # /4 sixteenth note
    # bds.add_tuplet((5,4), 1.0/4)  # /5 quintuplet
    # bds.add_tuplet((6,4), 1.0/4)  # /6 sextuplet
    # bds.add_tuplet((7,4), 1.0/4)  # /7 septuplet

    # notes
    notes = []
    notes += xscribe.make_note(0.00, 60, 1.00)
    notes += xscribe.make_note(1.00, 62, 1.00)
    notes += xscribe.make_note(2.00, 64, 1.00)
    notes += xscribe.make_note(3.00, 65, 1.00)
    notes += xscribe.make_note(4.00, 67, 1.00)
    notes += xscribe.make_note(5.00, 69, 1.00)
    notes += xscribe.make_note(6.00, 71, 1.00)
    notes += xscribe.make_note(7.00, 72, 1.00)

    # return it
    return notes, {'tempi': tempi, 'time_signatures': time_sigs, 'beat_division_scheme': bds}

solution_string = "\\new Staff {\n\t{\n\t\t\\time 4/4\n\t\t\\times 2/3 {\n\t\t\tc'2\n\t\t\td'4\n\t\t}\n\t\t\\times 2/3 {\n\t\t\te'2\n\t\t\tf'4\n\t\t}\n\t}\n\t{\n\t\t\\times 2/3 {\n\t\t\tg'2\n\t\t\ta'4\n\t\t}\n\t\t\\times 2/3 {\n\t\t\tb'2\n\t\t\tc''4\n\t\t}\n\t}\n\t{\n\t\t\\times 2/3 {\n\t\t\tr2.\n\t\t}\n\t\t\\times 2/3 {\n\t\t\tr2.\n\t\t}\n\t}\n}"

snips += [(foo, solution_string)]

#-----------------------------------------------#

def foo():
    """extensibility? listeners and callbacks"""

    # params
    tempi = [60]
    time_sigs = [(4,4)]

    # notes
    notes = []
    notes += xscribe.make_note(0.00, 69, 1.00)
    notes += xscribe.make_note(1.00, 63, 1.00)
    notes += xscribe.make_note(2.00, 64, 1.00)
    notes += xscribe.make_note(3.00, 66, 2.00)
    notes += xscribe.make_note(5.00, 67, 1.00)
    notes += xscribe.make_note(6.00, 69, 1.00)
    notes += xscribe.make_note(7.00, 73, 3.00)
    notes += xscribe.make_note(10.00, 72, 1.00)

    def apply_cent_deviations(notes_raw, notes_abj, verbose=False):
        """Attach cent deviations to note(s)."""

        if verbose: print "\n  attaching cent deviations"

        for note_raw in notes_raw:
            markup = abj.markuptools.Markup(r'\fontsize #-4 "{0}"'.format(note_raw.pitch), direction=None)
            abj.attach(markup, notes_abj)
            
    def apply_bonk_deviations(notes_raw, notes_abj, verbose=False):
        """Attach ** to note(s)."""

        if verbose: print "\n  attaching bonk deviations"

        for note_raw in notes_raw:
            markup = abj.markuptools.Markup(r'\fontsize #-2 "**"', direction=None)
            abj.attach(markup, notes_abj)
            
    listeners = [('new_note', apply_cent_deviations), ('tied_note', apply_bonk_deviations)]

    # return it
    return notes, {'tempi': tempi, 'time_signatures': time_sigs, 'listeners': listeners}

solution_string = "\\new Staff {\n\t{\n\t\t\\time 4/4\n\t\t{\n\t\t\ta'4\n\t\t\t\t- \\markup {\n\t\t\t\t\t\\fontsize\n\t\t\t\t\t\t#-4\n\t\t\t\t\t\t69\n\t\t\t\t\t}\n\t\t}\n\t\t{\n\t\t\tds'4\n\t\t\t\t- \\markup {\n\t\t\t\t\t\\fontsize\n\t\t\t\t\t\t#-4\n\t\t\t\t\t\t63\n\t\t\t\t\t}\n\t\t}\n\t\t{\n\t\t\te'4\n\t\t\t\t- \\markup {\n\t\t\t\t\t\\fontsize\n\t\t\t\t\t\t#-4\n\t\t\t\t\t\t64\n\t\t\t\t\t}\n\t\t}\n\t\t{\n\t\t\tfs'4 ~\n\t\t\t\t- \\markup {\n\t\t\t\t\t\\fontsize\n\t\t\t\t\t\t#-4\n\t\t\t\t\t\t66\n\t\t\t\t\t}\n\t\t}\n\t}\n\t{\n\t\t{\n\t\t\tfs'4\n\t\t\t\t- \\markup {\n\t\t\t\t\t\\fontsize\n\t\t\t\t\t\t#-2\n\t\t\t\t\t\t**\n\t\t\t\t\t}\n\t\t}\n\t\t{\n\t\t\tg'4\n\t\t\t\t- \\markup {\n\t\t\t\t\t\\fontsize\n\t\t\t\t\t\t#-4\n\t\t\t\t\t\t67\n\t\t\t\t\t}\n\t\t}\n\t\t{\n\t\t\ta'4\n\t\t\t\t- \\markup {\n\t\t\t\t\t\\fontsize\n\t\t\t\t\t\t#-4\n\t\t\t\t\t\t69\n\t\t\t\t\t}\n\t\t}\n\t\t{\n\t\t\tcs''4 ~\n\t\t\t\t- \\markup {\n\t\t\t\t\t\\fontsize\n\t\t\t\t\t\t#-4\n\t\t\t\t\t\t73\n\t\t\t\t\t}\n\t\t}\n\t}\n\t{\n\t\t{\n\t\t\tcs''2\n\t\t\t\t- \\markup {\n\t\t\t\t\t\\fontsize\n\t\t\t\t\t\t#-2\n\t\t\t\t\t\t**\n\t\t\t\t\t}\n\t\t}\n\t\t{\n\t\t\tc''4\n\t\t\t\t- \\markup {\n\t\t\t\t\t\\fontsize\n\t\t\t\t\t\t#-4\n\t\t\t\t\t\t72\n\t\t\t\t\t}\n\t\t}\n\t\t{\n\t\t\tr4\n\t\t}\n\t}\n}"

snips += [(foo, solution_string)]

#-----------------------------------------------#

def foo():
    """lily markup features"""

    # params
    tempi = [60]
    time_sigs = [(4,4)]

    # notes
    notes = []
    notes += xscribe.make_note(0.00, 69, 1.50, [('lily', '\\accent'), ('lily', '\mf')]) 
    notes += xscribe.make_note(1.50, 63, 1.00, [('lily', '\\turn')])
    notes += xscribe.make_note(3.00, 64, 1.00, [('lily', '\\fermata'), ('lily', '\ppp')])

    # return it
    return notes, {'tempi': tempi, 'time_signatures': time_sigs}

solution_string = "\\new Staff {\n\t{\n\t\t\\time 4/4\n\t\t{\n\t\t\ta'4 -\\accent \\mf ~\n\t\t}\n\t\t{\n\t\t\ta'8\n\t\t\tds'8 -\\turn ~\n\t\t}\n\t\t{\n\t\t\tds'8\n\t\t\tr8\n\t\t}\n\t\t{\n\t\t\te'4 -\\fermata \\ppp\n\t\t}\n\t}\n\t{\n\t\t{\n\t\t\tr1\n\t\t}\n\t}\n}"

snips += [(foo, solution_string)]

#-----------------------------------------------#

def foo():
    """tuplet complexity: min required"""

    # params
    tempi = [60]
    time_sigs = [(4,4)]

    # create an empty BeatDivsionScheme and add to it
    bds = xscribe.BeatDivisionScheme()

    # duration 4 beats
    bds.add_tuplet((1,1), 4.0)    # /1 whole note
    bds.add_tuplet((3,2), 2.0)    # /3 half note triplet
    bds.add_tuplet((5,4), 1.0)    # /5 quarter note quintuplet
    bds.add_tuplet((7,4), 1.0)    # /5 quarter note septuplet

    # duration 2 beats
    bds.add_tuplet((1,1), 2.0)    # /1 half note
    bds.add_tuplet((3,2), 1.0)    # /3 quarter note triplet
    bds.add_tuplet((5,4), 1.0/2)  # /5 eighth note quintuplet
    bds.add_tuplet((7,4), 1.0/2)  # /7 eighth note septuplet

    # duration 1 beat
    bds.add_tuplet((1,1), 1.0)    # /1 quarter note
    bds.add_tuplet((2,2), 1.0/2)  # /2 eighth note
    bds.add_tuplet((3,2), 1.0/2)  # /3 eighth note triplet
    bds.add_tuplet((4,4), 1.0/4)  # /4 sixteenth note
    bds.add_tuplet((5,4), 1.0/4, min_required=3)  # /5 quintuplet
    bds.add_tuplet((6,4), 1.0/4, min_required=3)  # /6 sextuplet
    bds.add_tuplet((7,4), 1.0/4, min_required=3)  # /7 septuplet

    # notes
    notes = []
    notes += xscribe.make_note(0.00, 60, 1.00)
    notes += xscribe.make_note(1.00, 62, 1.0/5)       # 2 quintuplets
    notes += xscribe.make_note(1.00+1.0/5, 64, 4.0/5)
    notes += xscribe.make_note(2.00, 65, 1.0/6)       # 2 sextuplets
    notes += xscribe.make_note(2.00+1.0/6, 67, 5.0/6)
    notes += xscribe.make_note(3.00, 69, 1.0/7)       # 2 septuplets
    notes += xscribe.make_note(3.00+1.0/7, 71, 6.0/7)

    # return it
    return notes, {'tempi': tempi, 'time_signatures': time_sigs, 'beat_division_scheme': bds}

solution_string = "\\new Staff {\n\t{\n\t\t\\time 4/4\n\t\t{\n\t\t\tc'4\n\t\t}\n\t\t{\n\t\t\td'16\n\t\t\te'8.\n\t\t}\n\t\t{\n\t\t\tf'16\n\t\t\tg'8.\n\t\t}\n\t\t{\n\t\t\ta'16\n\t\t\tb'8.\n\t\t}\n\t}\n\t{\n\t\t{\n\t\t\tr1\n\t\t}\n\t}\n}"

snips += [(foo, solution_string)]

#-----------------------------------------------#

def foo():
    """tuplet complexity: weighting"""

    # params
    tempi = [60]
    time_sigs = [(4,4)]

    # create an empty BeatDivsionScheme and add to it
    bds = xscribe.BeatDivisionScheme()

    # duration 4 beats
    bds.add_tuplet((1,1), 4.0)    # /1 whole note
    bds.add_tuplet((3,2), 2.0)    # /3 half note triplet
    bds.add_tuplet((5,4), 1.0)    # /5 quarter note quintuplet
    bds.add_tuplet((7,4), 1.0)    # /5 quarter note septuplet

    # duration 2 beats
    bds.add_tuplet((1,1), 2.0)    # /1 half note
    bds.add_tuplet((3,2), 1.0)    # /3 quarter note triplet
    bds.add_tuplet((5,4), 1.0/2)  # /5 eighth note quintuplet
    bds.add_tuplet((7,4), 1.0/2, weight=1*7.0/4)  # /7 eighth note septuplet

    # duration 1 beat
    bds.add_tuplet((1,1), 1.0)    # /1 quarter note
    bds.add_tuplet((2,2), 1.0/2)  # /2 eighth note
    bds.add_tuplet((3,2), 1.0/2)  # /3 eighth note triplet
    bds.add_tuplet((4,4), 1.0/4)  # /4 sixteenth note
    bds.add_tuplet((5,4), 1.0/4, weight=2*5.0/4)  # /5 quintuplet
    bds.add_tuplet((6,4), 1.0/4, weight=4*6.0/4)  # /6 sextuplet
    bds.add_tuplet((7,4), 1.0/4, weight=6*7.0/4)  # /7 septuplet

    # notes
    random.seed(0)

    notes = []
    curr_time = 0
    total_time = 20.0

    while curr_time < total_time:

        note_dur = random.random()
        
        if random.randint(0,5) <= 4:
            note_pitch = random.randint(58,72)
            notes += xscribe.make_note(curr_time, note_pitch, note_dur)
            curr_time += note_dur
            
        else:
            curr_time += note_dur

    # return it
    return notes, {'tempi': tempi, 'time_signatures': time_sigs, 'beat_division_scheme': bds}

solution_string = "\\new Staff {\n\t{\n\t\t\\time 4/4\n\t\t\\times 4/7 {\n\t\t\te'4.\n\t\t\te'8\n\t\t\tf'4.\n\t\t}\n\t\t{\n\t\t\tr8\n\t\t\ta'8\n\t\t}\n\t\t\\times 4/5 {\n\t\t\tb'8.\n\t\t\tb'8 ~\n\t\t}\n\t}\n\t{\n\t\t{\n\t\t\tb'8\n\t\t\tb'8\n\t\t}\n\t\t\\times 4/7 {\n\t\t\tb4\n\t\t\tb'8.\n\t\t}\n\t\t{\n\t\t\tas'4\n\t\t}\n\t\t{\n\t\t\tfs'16\n\t\t\t\\grace {\n\t\t\t\t<ds'>16.\n\t\t\t}\n\t\t\tas8.\n\t\t}\n\t}\n\t{\n\t\t{\n\t\t\tr8\n\t\t\tb'16\n\t\t\tcs'16\n\t\t}\n\t\t{\n\t\t\te'4\n\t\t}\n\t\t{\n\t\t\t\\grace {\n\t\t\t\t<f'>8\n\t\t\t}\n\t\t\tfs'4\n\t\t}\n\t\t\\times 2/3 {\n\t\t\tas'4\n\t\t\tr8\n\t\t}\n\t}\n\t{\n\t\t\\times 4/7 {\n\t\t\tr8\n\t\t\te'4\n\t\t\tfs'4\n\t\t\tc'8\n\t\t\tf'8 ~\n\t\t}\n\t\t\\times 2/3 {\n\t\t\tf'8\n\t\t\t\\grace {\n\t\t\t\t<b'>8\n\t\t\t}\n\t\t\tr4\n\t\t}\n\t\t{\n\t\t\tr4\n\t\t}\n\t}\n\t{\n\t\t{\n\t\t\tr16\n\t\t\tgs'8\n\t\t\tas'16\n\t\t}\n\t\t{\n\t\t\tc''4\n\t\t}\n\t\t{\n\t\t\tg'8\n\t\t\tr8\n\t\t}\n\t\t{\n\t\t\tr8\n\t\t\tg'8 ~\n\t\t}\n\t}\n\t{\n\t\t\\times 2/3 {\n\t\t\tg'8\n\t\t\tr4\n\t\t}\n\t\t{\n\t\t\tr4\n\t\t}\n\t\t{\n\t\t\tr2\n\t\t}\n\t}\n}"

snips += [(foo, solution_string)]

#-----------------------------------------------#

def foo():
    """FIXED: measure push"""

    # params
    tempi = [60]
    time_sigs = [(4,4)]

    # notes
    notes = []
    notes += xscribe.make_note(0.00, 60, 1.95)
    notes += xscribe.make_note(1.95, 60, 1.05)
    notes += xscribe.make_note(3.00, 60, 0.95)
    notes += xscribe.make_note(3.95, 60, 1.05)

    # return it
    return notes, {'tempi': tempi, 'time_signatures': time_sigs}

solution_string = "\\new Staff {\n\t{\n\t\t\\time 4/4\n\t\t{\n\t\t\tc'2\n\t\t}\n\t\t{\n\t\t\tc'4\n\t\t}\n\t\t{\n\t\t\tc'4\n\t\t}\n\t}\n\t{\n\t\t{\n\t\t\tc'4\n\t\t}\n\t\t{\n\t\t\tr4\n\t\t}\n\t\t{\n\t\t\tr2\n\t\t}\n\t}\n}"

snips += [(foo, solution_string)]

#-----------------------------------------------#

def foo():
    """FIXED: ties"""

    # params
    tempi = [60]
    time_sigs = [(4,4)]

    # notes
    notes = []
    notes += xscribe.make_note(0.00, 60, 0.33)
    notes += xscribe.make_note(0.33, 60, 0.33)
    notes += xscribe.make_note(0.66, 60, 1.33)
    notes += xscribe.make_note(2.00, 60, 1.00)
    notes += xscribe.make_note(3.00, 60, 2.00)

    # return it
    return notes, {'tempi': tempi, 'time_signatures': time_sigs}

solution_string = "\\new Staff {\n\t{\n\t\t\\time 4/4\n\t\t\\times 2/3 {\n\t\t\tc'8\n\t\t\tc'8\n\t\t\tc'8 ~\n\t\t}\n\t\t{\n\t\t\tc'4\n\t\t}\n\t\t{\n\t\t\tc'4\n\t\t}\n\t\t{\n\t\t\tc'4 ~\n\t\t}\n\t}\n\t{\n\t\t{\n\t\t\tc'4\n\t\t}\n\t\t{\n\t\t\tr4\n\t\t}\n\t\t{\n\t\t\tr2\n\t\t}\n\t}\n}"

snips += [(foo, solution_string)]

#-----------------------------------------------#

def foo():
    """FIXED: why these tied?"""

    # params
    tempi = [60]
    time_sigs = [(4,4)]

    # notes
    notes = []
    notes += xscribe.make_note(0.00, 60, 0.2)
    notes += xscribe.make_note(0.2, 60, 0.2)
    notes += xscribe.make_note(0.4, 60, 0.4)
    notes += xscribe.make_note(0.8, 60, 0.2)
    notes += xscribe.make_note(1.00, 60, 1.00)
    notes += xscribe.make_note(2.00, 60, 1.00)
    notes += xscribe.make_note(3.00, 60, 1.00)

    # return it
    return notes, {'tempi': tempi, 'time_signatures': time_sigs}

solution_string = "\\new Staff {\n\t{\n\t\t\\time 4/4\n\t\t\\times 4/5 {\n\t\t\tc'16\n\t\t\tc'16\n\t\t\tc'8\n\t\t\tc'16\n\t\t}\n\t\t{\n\t\t\tc'4\n\t\t}\n\t\t{\n\t\t\tc'4\n\t\t}\n\t\t{\n\t\t\tc'4\n\t\t}\n\t}\n\t{\n\t\t{\n\t\t\tr1\n\t\t}\n\t}\n}"

snips += [(foo, solution_string)]

#-----------------------------------------------#

def foo():
    """FIXED: and this second note not tied?"""

    # params
    tempi = [60]
    time_sigs = [(4,4)]

    # notes
    notes = []
    notes += xscribe.make_note(0.00, 60, 1.50)
    notes += xscribe.make_note(1.50, 60, 1.00)

    # return it
    return notes, {'tempi': tempi, 'time_signatures': time_sigs}

solution_string = "\\new Staff {\n\t{\n\t\t\\time 4/4\n\t\t{\n\t\t\tc'4 ~\n\t\t}\n\t\t{\n\t\t\tc'8\n\t\t\tc'8 ~\n\t\t}\n\t\t{\n\t\t\tc'8\n\t\t\tr8\n\t\t}\n\t\t{\n\t\t\tr4\n\t\t}\n\t}\n}"

snips += [(foo, solution_string)]

#-----------------------------------------------#

def foo():
    """FIXED: ties within diffs! you do need em!"""

    # params
    tempi = [60]
    time_sigs = [(6,4)]

    # notes
    notes = []
    notes += xscribe.make_note(0.00, 68, 5.0/4)
    notes += xscribe.make_note(5.0/4, 64, 3.0/4+1.0/7)
    notes += xscribe.make_note(2+1.0/7, 72, 6.0/7+1.0/6)
    notes += xscribe.make_note(3+1.0/6, 61, 5.0/6)
    notes += xscribe.make_note(4, 58, 2.0/7*5)

    # return it
    return notes, {'tempi': tempi, 'time_signatures': time_sigs}

solution_string = "\\new Staff {\n\t{\n\t\t\\time 6/4\n\t\t{\n\t\t\tgs'4 ~\n\t\t}\n\t\t{\n\t\t\tgs'16\n\t\t\te'8. ~\n\t\t}\n\t\t\\times 4/7 {\n\t\t\te'16\n\t\t\tc''4. ~\n\t\t}\n\t\t\\times 2/3 {\n\t\t\tc''16\n\t\t\tcs'4 ~\n\t\t\tcs'16\n\t\t}\n\t\t\\times 4/7 {\n\t\t\tas2 ~\n\t\t\tas8\n\t\t\tr4\n\t\t}\n\t}\n}"

snips += [(foo, solution_string)]

#-------------------------------------------------------------------------------------------------#
# Test drive!
#-------------------------------------------------------------------------------------------------#

print "\nTesting Testing Get Out the Way!\n"

num_correct = 0
for snip in snips:
    num_correct += snipper(snip)

print "\nPassed {0}/{1}\n".format(num_correct, len(snips))
