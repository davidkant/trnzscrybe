#Transcribe
---
super alpha—i.e., not yet for public consumption!!!

### what does this thing even do?
* trnzscrybe is a Python package for music transcription. its job is to convert from time-in-seconds to time-in-music-notation. 

### extensibility
1. lily markup can be attached to a note and passed right through
2. standard and custom listeners and callback functions for writing lily markup

### depends on
* LilyPond
* abjad
* matplotlib.pyplot (for test plotting)
* Python 2 (not yet tested for Python 3)

### tutorial
* there's an ipython notebook tutorial to demonstrate basic features and use.

### test suite
* there's a test suite to make sure we don't break things. this can be run from the terminal.

### dev branches
* __master__ is the current stable release
* __develop__ is the working development version for the next release
* __features__ are feature-specific development versions

__features__ are merged into __develop__ and __master__ is then updated through a release 
