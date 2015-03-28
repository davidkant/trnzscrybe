# dev notes [by topic]
---
...b/c i often forget why i did things a certain way:

### how does this thing even work
* the transcriber searches the space of all possible rhythms given allowable subdivisions of the beat(s). it finds the simplest (smallest number of subdisions) best fit solution (according to some distance function) 

### input
* transcriber input is a list of Transcribe.Note objects. each Note contains at least   
  1. a time (in seconds)
  2. a pitch (midi pitch value, not integer -> cents)
  3. either a note "on" or "off"
  4. may also contain further features for transcription, such as LilyPond markup or features for listener callback functions.

### output
* transcriber output is an abjad staff object. use abjad to render and write it to file.

### transcription parameters
* notes list
* tempo list
* time signature list
* beat division scheme list

---

### api
* i want to expose as little as possible—really just the Note object and the main transcriber call.

###### Tuplet
* min_required counts number of note onsets


---

### transcription hierarchy
* **transcribe(notes)** given a list of Notes with time specified in seconds, it steps through the list parsing the time stamps into measures and calls transcribe on each measure.  
 
* **Measure.transcribe()** finds the optimal rhythmic subdivision of the beat(s) for that measure. it associates each Note with the corresponding tuplet subdivsion and steps through the list of tuplets calling transcribe on each tuplet. this is where we do all the thinking about optimal rhythmic subdivisions, but we search only the length of a measure at a time. effectively, the measure is the border between tuplets (subdivisions of the beat[s])—tuplets do no span over the barline.  

* **Tuplet.transcribe()** writes the tuplet in music notation, converting to abjad objects and extending the current abjad staff. this involves all sorts of boring and tedious things about music notation like proper rhythm spelling, keeping track of ties, and beaming. this is also where we register various transcriber events—note added, note held, note offed and filter grace notes (notes that are too short for the rhythmic resolution). this is also where we implement any listener callback functions.

---

### measure
* notes, start and end time, and a bunch of transcription parameters
* important note: when Notes are parsed into measures, their time information is converted to local time (0:00@ the beginning of this measure). maybe i should keep the absolute time around, too?  
* sometimes these feel a bit heavyweight to me but it's nice to have all this information stored.

### holdover
* anything still on from the previous measure. when we transcribe measures they return holdover to pass along to the next one  
* we need this b/c when a note remains on we don't know when it actually ends until we transcribe the next measure. it might hold over into the next measure or it might get turned off immediatley on the first beat. it depends on how far it holds into the next measure and how that measure is transcribed.

### push
* stuff that is close enough to the end of a measure that it is transcribed on the first beat of the next measure instead of at the end of the previous measure, that is, the closest subdivision is the downbeat of the next measure   
* holdover is notes still on, push is notes that get bumped to the next measure

### grace notes
* if a note has an on and off within the same subdivision
* their duration us beyond (smaller than)the resolution of the transcriber to express
* grace note rendering is customizable by overriding the grace note function because we may want to treat them differently at different times—grace chords, multiple grace note, no grace notes at all, etc.
* what rhythmic value should they have? right now i half the value of the main note for each gracenote. if one, then half, but if two then quarter it.
* grace notes isn't quite same as sqeezing notes with min dur because it also depends how they fall into the beats (not just duratio, but placement as well)


### ties
* this is messy because we don't know whether or not to tie a held note until the next measure is transcribed (see holdover for explanation). this means we have to wait and then reach back into the previous tuplet and tie it up. this involves making some assumptions that feel funny, namely we assume the tie will be between the last element of the previous tuplet and the first element of the new tuplet, which maybe is okay, but in code feels weird. 
* this is only the case for ties between tuplets. ties within tuplets is handled by the rhythm speller

### beams
* beam any consecutive notes within a tuplet
* here's another place where i want transcription and notation to be separate
* note: we do it to list of notes, not to a tuplet, so we don't have to rely on abjad groupby tools
* do not manually beams tuplets less than 1 beat b/c want to connect them --> fix this. b/c have to rely on auto beaming when less than 1

 


