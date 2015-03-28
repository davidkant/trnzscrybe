"""Transcriber settings."""

from classes import *
from tree import *

import math


# default beat division scheme
def default_beat_division_scheme(weights=False):

    # new beat division scheme
    bds = BeatDivisionScheme()

    if not weights:

        # duration 4 beats
        bds.add_tuplet((1,1), 4.0)    # /1 whole note
        bds.add_tuplet((3,2), 2.0)    # /3 half note triplet
        bds.add_tuplet((5,4), 1.0)    # /5 quarter note quintuplet
        bds.add_tuplet((7,4), 1.0)    # /7 quarter note septuplet

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
        bds.add_tuplet((5,4), 1.0/4)  # /5 quintuplet
        bds.add_tuplet((6,4), 1.0/4)  # /6 sextuplet
        bds.add_tuplet((7,4), 1.0/4)  # /7 septuplet

    else:

        # duration 4 beats
        bds.add_tuplet((1,1), 4.0)    # /1 whole note
        bds.add_tuplet((3,2), 2.0)    # /3 half note triplet
        bds.add_tuplet((5,4), 1.0)    # /5 quarter note quintuplet
        bds.add_tuplet((7,4), 1.0)    # /7 quarter note septuplet

        # duration 2 beats
        bds.add_tuplet((1,1), 2.0)    # /1 half note
        bds.add_tuplet((3,2), 1.0)    # /3 quarter note triplet
        bds.add_tuplet((5,4), 1.0/2, weight=1*1*5.0/4)  # /5 eighth note quintuplet
        bds.add_tuplet((7,4), 1.0/2, weight=1*1*7.0/4)  # /7 eighth note septuplet

        # duration 1 beat
        bds.add_tuplet((1,1), 1.0)    # /1 quarter note
        bds.add_tuplet((2,2), 1.0/2)  # /2 eighth note
        bds.add_tuplet((3,2), 1.0/2)  # /3 eighth note triplet
        bds.add_tuplet((4,4), 1.0/4)  # /4 sixteenth note
        bds.add_tuplet((5,4), 1.0/4, weight=2*1*5.0/4)  # /5 quintuplet
        bds.add_tuplet((6,4), 1.0/4, weight=2*2*6.0/4)  # /6 sextuplet
        bds.add_tuplet((7,4), 1.0/4, weight=2*3*7.0/4)  # /7 septuplet

    return bds


# think about adding these...

  # bds.add_tuplet((8,8), 1.0/8)  # /8 thirty-second notes

  # duration 1/2 beat
  # bds.add_tuplet((4,4), 1.0/8)  # /4 thirty-second notes


# possible quavers
quavers = ['1', '2.', '2', '4.', '4', '8.', '8', '16.', '16', '32.', '32', '64.', '64', '128.', '128']
