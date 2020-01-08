import itertools as it
from collections import deque

class Fretboard:

    def __init__(self, tuning, no_frets):
        self.strings = []
        for root in tuning:
            self.strings.append(String(root, no_frets))

    def __str__(self):
        out = ""
        for string in self.strings:
            out += "String " + str(self.strings.index(string)) + ": " + str(string) + "\n"
        return out

    #def getter for indexing object like self.strings
    def __getitem__(self, x):
        return self.strings[x]

class Note:

    def __init__(self, note, octave=2):
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
    #breaks DRY
    music_notes = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']

    def __init__(self, root_note, no_frets, root_octave=2):
        self.frets = []
        #find the position of the root within music notes list
        root_index = String.music_notes.index(root_note)
        root_first = deque(String.music_notes)
        root_first.rotate(-root_index) #use 'deque' to cycle list until it starts at the root note
        for note in it.cycle(root_first):
            self.frets.append(Note(note))
            if len(self.frets) >= no_frets:
                break
        self.root_index = self.music_notes.index(root_note)

    def __str__(self):
        out = " | "
        return out.join(self.frets)

    #def getter for indexing object as self.frets
    def __getitem__(self, x):
        return self.frets[x]


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
