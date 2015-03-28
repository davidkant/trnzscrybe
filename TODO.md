#TODO

### todo
these are the major ones:

* **search optimization:** the transcriber is currently NOT OPTIMIZED. i wanted to first make sure it's getting the correct solution, then optimize it.

* **internal representation:** current music represntation uses abjad, which makes the code a little messy. i should roll my own, and export to abjad at the very last stage, but it's a 
bit of a major rewrite.

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

* __stats / feedback:__ some feedback on complexity would be nice. like, min_required +/or weights shifted these many tuplets. or a way to diff two transcriptions. just to know how much we're compressing the maximum complexity / undweighted solution.


### raw
not yet coherently formulated:

* __complexity:__ 
  - complexity measure
  - complexity weight
  - over a window

* wait i shouldn't need push at the tuplet level should i. can't measure pair it when it does it.

* min_required. seems like should be different if starts on the first beat versus not. like, rest / tie feels different than start on downbeat but they count to the same.

* distance function options

* error calculation: do on/offs count twice?

* __tree refactoring__
  - instead of passing refs to time sig and bds around maybe top level tree has them and we pass a ref to the top level tree and then ask it for this stuff when needed
  - add a refactor note that if it's under min we set to 999.999 not a real value! could flag instead. which would help keep track for stats / feedback
  - in general feel like passing a lot of data where i could maybe be passing refs
  - optimization
    - it's a litle weird that it's min by node first rather than all one big list. b/c we call min twice

  
* something a little funny with the tempo change / time sig / and tuplets: don't think i allowed 64th notes but one shows up. in ring of fire at the 2/4 bar. in fact it's all off by a factor of 2.
