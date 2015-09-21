"LALALAL"

from . import classes
from . import settings
from . import tree
from . import transcribers
from . import test

reload(classes)
reload(settings)
reload(tree)
reload(transcribers)
reload(test)

from classes import *
from settings import *
from tree import *
from transcribers import *
from test import *
