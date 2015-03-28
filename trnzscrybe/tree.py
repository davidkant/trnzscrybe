from classes import *
from settings import *


import numpy as np

"""A tree structure to enumerate all possible rhythmic paths through a measure
given a time signature and beat division scheme. There is no search optimization 
yet. The nomenclature is like this:"""

class Flower:
    
    def __init__(self, value, mtuplet=None, parent=None, error=None):
        self.value = value
        self.parent = parent
        self.error = None
        self.mtuplet = mtuplet

    def calculate(self, notes, tempo, verbose=False):
        
        # measure range this (parent) node
        sum_to_this_node = sum([n.value for n in self.parent.ancestors()]) * 60.0/tempo        
        sum_through_this_node = sum_to_this_node + self.parent.value * 60.0/tempo
        if verbose: print 'calculating {0} - {1}'.format(sum_to_this_node, sum_through_this_node)

        # filter notes in range
        notes_in_range = filter(lambda note: sum_to_this_node <= note.time < sum_through_this_node, notes)
        if verbose: print 'notes_in_range: {0}'.format(notes_in_range)
        
        # my hits
        hit_points = np.linspace(sum_to_this_node, sum_through_this_node, self.value+1)
        if verbose: print 'hit_points: {0}'.format(hit_points)
        
        # calc error

        delta = lambda a,b: abs(b - a)
        # delta = lambda a,b: (b - a)**2
        # delta = lambda a,b: abs(b - a)**0.5

        self.error = sum([min([delta(n.time, p) 
                               for p in hit_points]) 
                          for n in notes_in_range])

        error_unweighted  = self.error

        # check min required
        if len(filter(lambda n: n.onoff == 'on', notes_in_range)) < self.mtuplet.min_required: 
            self.error = 999.999        
            
        # apply weight
        self.error *= float(self.mtuplet.weight)

        if verbose: print 'error: {0}, min_required: {1}, weight: {2}, total error{3}'.format(
            error_unweighted, self.mtuplet.min_required, self.mtuplet.weight, self.error)
        
        # return self
        return self
        
    def __repr__(self):
        return 'Flower(val={0})'.format(self.value)

class Node:
    
    def __init__(self, value, parent=None, children=None, flowers=None):
        self.parent = parent # reference to parent
        self.children = children # reference to children
        self.value = value # this node value
        self.flowers = flowers
                
    def is_terminus(self):
        return self.children is None

    def ancestors(self):
        return self.parent.ancestors() + [self.parent] if self.parent is not None else []
    
    def descendents(self):
        return self.children + reduce(lambda x,y: x+y, map(lambda child: child.descendents(), self.children)) if self.children is not None else []    

    def depth(self):
        return len(self.ancestors())

    def termini(self):
        return ([self] if self.is_terminus() else []) + \
            (reduce(lambda x,y: x+y, map(lambda child: child.termini(), self.children)) 
            if self.children is not None else [])
     # //--> build in precaution for unterminated path
    
    def flower(self, beat_division_scheme, time_signature):
        
        # create a flower for each sublet
        #         self.flowers = [Flower(t.divisions, parent=self, mtuplet=t) 
        #                         for t in filter(lambda t: t.duration == self.value, beat_division_scheme.tuplets)
    
        self.flowers = map(lambda t: Flower(t.divisions, parent=self, mtuplet=t),
                           filter(lambda t: t.duration_in_beats() == self.value, 
                                  beat_division_scheme.tuplets))
    
    def branch(self, time_signature, beat_division_scheme, verbose=False):

        # measure length up through this node
        length_so_far = sum([self.value] + [n.value for n in self.ancestors()])
        if verbose: print 'length_so_far: {0}'.format(length_so_far)

        # time left in the measure
        time_remaining = time_signature.num_beats - length_so_far
        if verbose: print 'time_remaining: {0}'.format(time_remaining)

        # if there's time left
        if time_remaining > 0:

            # create and branch children for all values <= time_remaining
            divs = list(set([t.duration_in_beats() for t in beat_division_scheme.tuplets]))
            if verbose: print 'branching: {0}'.format(filter(lambda d: d <= time_remaining, divs))
            self.children = [Node(val, parent=self) for val in filter(lambda d: d <= time_remaining, divs)]
            # map(lambda child: child.branch(measure_length=measure_length, divs=divs, verbose=verbose), self.children)
            
        return self
        
    def grow(self, time_signature, beat_division_scheme):
        
        # flower self
        self.flower(beat_division_scheme, time_signature)
        
        # branch self
        self.branch(time_signature, beat_division_scheme)
                        
        # then grow children
        if not self.is_terminus(): map(lambda child: child.grow(time_signature, beat_division_scheme), self.children)
            
        return self
    
    def calculate(self, notes, tempo):
        
        # calculate itself (flowers)
        if self.flowers is not None: map(lambda flower: flower.calculate(notes, tempo), self.flowers)
        
        # map calculate children
        if not self.is_terminus(): map(lambda node: node.calculate(notes, tempo), self.children)
        
    def bouquet(self):
        
        # path of flowers with least error
        return [min(node.flowers, key=lambda flower: flower.error) 
                for node in self.ancestors()] + \
               [min(self.flowers, key=lambda flower: flower.error)]
        
    def bouquet_error(self):
        
        return sum([flower.error for flower in self.bouquet()])
        
    def measure(self):

        return [n.value for n in self.ancestors()] + [self.value]
    
    def to_path(self):
        
        return Path([flower.mtuplet for flower in self.bouquet()])

    def show(self):
        print '  '*self.depth() + str(self),
        if self.flowers is not None: print [f.value for f in self.flowers],
        if self.flowers is not None: print [f.error for f in self.flowers],
        if not self.is_terminus(): 
            print
            for child in self.children: child.show()
        else:
            print '||'   
        return self
        
    def __repr__(self):
        # return str(self.value)
        return 'Node(val={0})'.format(self.value)
    
class Tree:
    
    def __init__(self, time_signature, tempo, beat_division_scheme):

        self.time_signature = time_signature # need this later?
        self.tempo = tempo # need this later?
        self.beat_division_scheme = beat_division_scheme # need this later?
        self.grow(self.time_signature, self.beat_division_scheme)

    def grow(self, time_signature, beat_division_scheme):
        
        # create and grow limbs
        self.limbs = [Node(div).grow(time_signature, beat_division_scheme)
                      for div in list(set([t.duration_in_beats() 
                      for t in beat_division_scheme.tuplets]))]

        # print list(set([t.duration_in_beats() for t in beat_division_scheme.tuplets]))
        
        # grow limbs
        # map(lambda node: node.grow(time_signature, beat_division_scheme), self.limbs)
        # //--> this or that?
        
        # return self
        return self
    
    def termini(self):
    
        return reduce(lambda x,y: x+y, map(lambda node: node.termini(), self.limbs))
    
    def calculate(self, notes):
        
        # calculate limbs
        map(lambda node: node.calculate(notes, self.tempo), self.limbs)
        
    def optimal_bouquet(self):
        
        # the terminus with minimum bouquet error
        
        # calc error for all paths (b/c we'll need em more than once)
        all_errors = [(node.bouquet_error(), node) for node in self.termini()]

        # the terminus with minimum bouquet error
        best_error, best_node = min(all_errors, key=lambda (error,node): error)
        
        # look for duplicates by filtering within epsilon of best
        bests = [elem for elem in all_errors if abs(elem[0] - best_error) < 0.00001] # that's my thresh for equality
        # print 'there are {0} bests'.format(len(bests))

        # take the simplest (fewest divisions) OR tree way to know that?
        best_simplest = min(bests, key=lambda (error,node): sum([flower.value for flower in node.bouquet()]))    
        # simplest could also correspond to tree position from the left
        # one with fewest divsions is simplest and we want
        # (it should be the case that enumeration order gives it first, but we minimize for extra security)
        # //--> verbose should say how many, how close (epsilon) and if any have same num divisions
        
        return best_simplest

        
    def show(self):
        map(lambda node: node.show(), self.limbs)