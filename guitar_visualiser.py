import itertools as it
from collections import deque
import data

class Note:

    def __init__(self, note, octave):
        assert note in data.objs['notes'], "Note {} passed to note constructor not recognised in core data {}".format(note, data.objs['notes'])
        self.note = note
        self.marker = False
        self.degree = None
        self.octave = octave

    def __eq__(self, other):
        return self.note == other

    def __str__(self):
        return self.note

    def __repr__(self):
        return repr(self.note)

class String:

    def __init__(self, root_note, no_frets, root_octave):
        self.root_index = data.objs['notes'].index(root_note)
        self.frets = []
        #keep track of the octave of the note
        octave = root_octave
        iterator = note_iterator(root_note)
        current_note = ""
        while len(self.frets) > no_frets:
            current_note = next(iterator)
            if note == root_note:
                octave += 1
            self.frets.append(Note(note, octave))


    def __str__(self):
        out = " | "
        return out.join(self.frets)

    #def getter for indexing object as self.frets
    def __getitem__(self, x):
        return self.frets[x]


class Fretboard:

    def __init__(self, tuning, no_frets):
        assert len(tuning) == 6, "Unexpected number of strings passed to Fretboard constructor"
        assert all(isinstance(elem, Note) for elem in tuning), "Not all notes of tuning note list are recognised"
        self.strings = []
        for root, octave in tuning.items():
            self.strings.append(String(root, no_frets, octave))

    def __str__(self):
        out = ""
        for string in self.strings:
            out += "String " + str(self.strings.index(string)) + ": " + str(string) + "\n"
        return out

    #def getter for indexing object like self.strings
    def __getitem__(self, x):
        return self.strings[x]


class Scale:
    def __init__(self, root_note, intervals):
        self.root = root_note
        self.degrees = [root_note]
        root_index = String.music_notes.index(root_note)
        current_index = root_index
        for i in intervals:
            current_index += i
            next_degree = current_index % len(String.music_notes)
            print(f"next_degree is: {next_degree}")
            self.degrees.append(String.music_notes[next_degree])

    def __str__(self):
        return self.degrees

    def __repr__(self):
        return repr(self.degrees)

    def impose(self, board):
        assert isinstance(board, Fretboard), "The 'fretboard' argument supplied to Scale.impose() was of type %s not 'Fretboard'" % (fretboard.__class__.__name__)
        for a_string in board:
            for nt in a_string:
                if nt in self.degrees:
                    nt.degree = self.degrees.index(nt)
                    print(f"Degree index of note {nt}: {self.degrees.index(nt)}")


class FretboardFactory:

    base = ['E', 'A', 'D', 'G', 'B', 'E']

    def __init__(self, name, root):
        assert hasattr(self, "_" + name), "the tuning name {} passed to {} is unrecognised".format(name, self.__class__.__name__)
        self.tuning = data.objs['tunings'][name]
        assert root in self.tuning['roots']
        self.root_index = data.objs['notes'].index(root)

    def _open(self):
        """Function to generate the tuning pattern for a given 'open' tuning note"""
        tuning = []
        base_indexes = list(map(lambda note: data.objs['notes'].index(note), FretboardFactory.base))
        print("base_indexes: {}".format(base_indexes))
        degrees = [self.root_index, ((self.root_index + 4) % 12), ((self.root_index + 7) % 12)] #assumed open is scale major intervals
        for n in base_indexes:
            closest = list(map(lambda degree: abs(degree - n), degrees))
            closest_degree = degrees[closest.index(min(closest))]
            tuning.append(data.objs['notes'][closest_degree])
        return tuning

    def standard(self):
        """Function to generate standard tuning. Assumed that tuning intervals exist"""
        tuning = [root]
        prev_index = data.objs['notes'].index(tuning[0])
        for interval in self.tuning:
            new_index = (prev_index + interval) % 12
            #calculate the new next note in the tuning
            tuning.append(data.objs['notes'][new_index])
            prev = data.objs['notes'].index(new_note)
        return tuning

    def _drop(self):
        """Function to algorithimcally generate drop tunings"""
        tuning = FretboardFactory.base
        tuning[0] = data.objs['notes'][root_index] #TODO: manually set the octave of the root note
        return tuning

    def _double_drop(self):
        """Alrogrithmic function to generate double-drop tunings"""
        tuning = FretboardFactory.base
        tuning[0] = data.objs['notes'][root_index] #TODO: manually set the octave of the root note
        return tuning


def note_iterator(root_note):
    #find the position of the root within music notes list
    root_index = data.objs['notes'].index(root_note)
    root_first = deque(data.objs['notes'])
    root_first.rotate(-root_index) #use 'deque' to cycle list until it starts at the root note
    return it.cycle(root_first)
