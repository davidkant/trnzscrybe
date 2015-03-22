#TODO

### todo
these are the major ones:

* **search optimization:** the transcriber is currently NOT OPTIMIZED. i wanted to first make sure it's getting the correct solution, then optimize it.
* **internal representation:** current music represntation uses abjad, which makes the code a little messy. i should roll my own, and export to abjad at the very last stage, but it's a bit of a major rewrite.
* **extensibility** not fully implemented

### more todo
these are the less major ones:

* add cents from non-integer pitch values
* rewrite the test suite using NOSE
* Python 3 compatibility plz!
* optimizatino metrics: difference metrics and weights
* for tuplets min number allowed
* and add weights to certain tuplets
* beat division scheme should be dynamic like time sigs and tempo
* passing lots of stuff around... use dictionary like an environment
* suppress that extra measure
* push doesn't need to recurse all the way down now does it
* proper imports / package structure
* make a print log that is useful on verbose=True
* this includes printing best paths
* all defaults should be in settings.py... like deafault tempo and stuff... so we dont have to tear open the code base to find this stuff  
* pass dictionary of keword args instead of hard coding all the method signatures dummy!
* gracesnotes: what rhythmic value should they have? 

### raw
not yet coherently formulated:

* wait i shouldn't need push at the tuplet level should i. can't measure pair it when it does it.