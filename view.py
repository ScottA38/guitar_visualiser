from tkinter import *
from guitar_visualiser import Fretboard, String, Scale, Note

class Lb(Listbox):
    def __init__(self, l_items, *args, **kwargs):
        Listbox.__init__(self, *args, **kwargs)
        self.items = l_items
        self.repop()

    def current_sel(self):
        """helper function for extracting list index selection"""
        try:
            index = int(self.curselection()[0])
            return self.get(index)
        except IndexError:
            raise IndexError(f"'get' current selection of Tk.Listbox {str(self).split('.')[-1]} failed. \nThe current selection is: {self.curselection()}")
        except:
            raise Exception()

    def repop(self):
        self.delete(0, END)
        for item in self.items:
            self.insert(END, item)
        self.selection_set( first = 0 )

class App(Tk):
    scales = {
                "pentatonic":
                {
                    "minor": [3, 2, 2, 3],
                    "major": [2, 2, 3, 2]
                },
                "natural":
                {
                    "minor": [2, 1, 2, 2, 1, 2],
                    "major": [2, 2, 1, 2, 2, 2]
                },
                "harmonic":
                {
                    "minor": [2, 1, 2, 2, 1, 3],
                    "major": [2, 2, 1, 2, 1, 3]
                },
                "melodic":
                {
                    "minor ascending": [2, 1, 2, 2, 2, 2],
                    "minor descending": [2, 2, 1, 2, 2, 1]
                }
            }
    tunings = {
        "standard": {
            "intervals": [5, 5, 5, 4, 5],
            "roots": ["F", "Gb", "G", "Ab", "A", "Bb", "B", "C", "Cb", "D", "Db", "E"]
        },
        "open": {
            "A": ["E", "A", "Db", "E", "A", "E"],
            "B": ["B", "Gb", "B", "Gb", "B", "D"],
            "D": ["D", "A", "D", "Gb", "A", "D"],
            "F": [],
            "G": []
        },
        "drop": {
            "intervals": [],
            "roots": ["Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "C", "Db", "D"]
        },
        "double-drop": {
            "intervals": [],
            "roots": ["E", "F", "Gb", "G", "Ab", "A", "Bb", "C", "Db"]
        }
    }

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Fretboard Visualiser")

        #declare widgets to live inside of root
        self.header = Frame(self, height=100,  bd=2, relief=SUNKEN)
        self.body = Frame(self, bd=2, relief=SUNKEN)
        self.scale_root = Lb(String.music_notes, self.header, height=4, exportselection=0, name="scale_root")
        self.scale_names = Lb(App.scales.keys(), self.header, height=4, exportselection=0, name="scale_names")
        self.rkey_list = Lb(App.scales[self.scale_names.current_sel()].keys(), self.header, height=4, exportselection=0, name="relative_keys")

        #bind events
        self.scale_names.bind("<Double-Button-1>", self.redraw_rkey_list)
        self.rkey_list.bind("<Double-Button-1>", self.redraw_body)

        #pack everything in order
        self.header.pack(expand = True, fill="both")
        self.body.pack(expand = True, fill="both")
        self.scale_root.pack(side=LEFT)
        self.scale_names.pack(side=LEFT)
        self.rkey_list.pack(side=LEFT)

        #create fretboard object
        self.fretboard = Fretboard(['E', 'A', 'D', 'G', 'B', 'E'], 23)
        self.scale = None #initialised when selection is made
        self.current_selection = App.scales[self.scale_names.current_sel()][self.rkey_list.current_sel()]
        self._draw_visualisation()


    def _draw_visualisation(self):
        """function to take all current input data and draw the fretboard to screen"""
        self.fretboard = Fretboard(['E', 'A', 'D', 'G', 'B', 'E'], 23)
        self.scale = Scale(self.scale_root.current_sel(), App.scales[self.scale_names.current_sel()][self.rkey_list.current_sel()])
        self.scale.impose(self.fretboard)

        c=0
        r=0
        for string in self.fretboard:
            for fret in string:
                background = "brown"
                foreground = "black"
                if c == 0:
                    background = "white"
                if fret.degree != None:
                    #print(f"view.py says fret.degree of fret {fret} is: {fret.degree}") DEBUG
                    if fret.degree == 0:
                        foreground = "blue"
                    else:
                        foreground = "green"
                Label(self.body, text=fret, bg = background, fg=foreground, relief=RIDGE, width=5, height=2  ).grid(row=r, column=c)
                c += 1
            r += 1
            c=0

    def redraw_body(self, event):
        """Reconstruct body when click event is fired """
        self.body.destroy()
        self.body = Frame(self, bd=2, relief=SUNKEN)
        self.body.pack(expand=True, fill="both")
        self._draw_visualisation()

    def redraw_rkey_list(self, event):
        self.rkey_list.items = App.scales[self.scale_names.current_sel()].keys()
        self.rkey_list.repop()



app = App()
app.mainloop()
