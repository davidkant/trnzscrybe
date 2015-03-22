from classes import *
import abjad as abj
import matplotlib.pyplot as plt
import copy
import math

#--------------------------------------------------------------------------------------------------#
# Things that do things                                                                            #
#--------------------------------------------------------------------------------------------------#

def make_lilyfile(staff):
    """ Make lilypond file from staff. """
    
    # create lilypond file
    lilypond_file = abj.lilypondfiletools.make_basic_lilypond_file(staff)

    # global
    lilypond_file.global_staff_size = 20
    lilypond_file.default_paper_size = 'letter','portrait'
    
    # head block
    lilypond_file.header_block.items.append("tagline = \"\"")

    # layout block
    lilypond_file.layout_block.items.append("\\numericTimeSignature")

    return lilypond_file


def show(staff):
    """Render and show."""

    return abj.show(make_lilyfile(staff))

    
def plot(notes, pitch_range=(58,72), figsize=(20,5)):
    """ Plot notes. """
    
    # deep copy so we can alter them
    d_notes = copy.deepcopy(notes)
    
    # we'll need these
    ons = [n for n in d_notes if n.onoff=='on']
    offs = [n for n in d_notes if n.onoff=='off']
    offs_pitch = [n.pitch for n in d_notes if n.onoff=='off']
    
    # grab xlim b/f we start popping
    x_max = math.ceil(max([n.time for n in offs]))

    # loop through, find offs, and pop from list
    for note in ons:
        index = offs_pitch.index(note.pitch)
        note.off_time = offs[index].time
        offs_pitch.pop(index)
        offs.pop(index)

    # plot them
    fig = plt.figure(figsize=figsize)
    for note in ons: 
        plt.plot([note.time, note.off_time], [note.pitch, note.pitch], color='red')
        plt.scatter([note.time], [note.pitch], color='grey')
    plt.xlim([0.,x_max])
    plt.ylim(pitch_range)
    #fig.axes[0].get_xaxis().set_visible(False)
    #fig.axes[0].get_yaxis().set_visible(False)
    #fig.axes[0].set_xticklabels([])
    fig.axes[0].set_yticklabels([])
    plt.show()


def make_note(time, pitch, duration, features=None):
    """ time, pitch, duration -> note on + note off. """

    return [Note(time, pitch, 'on', features=features), Note(time+duration, pitch, 'off')]

