from tkinter import *
from guitar_visualiser import Fretboard, String, Scale, Note


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

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Fretboard Visualiser")

        #declare widgets to live inside of root
        self.header = Frame(self, height=100,  bd=2, relief=SUNKEN)
        self.body = Frame(self, bd=2, relief=SUNKEN)
        self.scale_names = Listbox(self.header, height=4, exportselection=0, name="scale_names")
        self.rkey_list = Listbox(self.header, height=4, exportselection=0, name="relative_keys")

        #populate Listboxes
        for scale in App.scales.keys():
            self.scale_names.insert(END, scale)
        for key in App.scales["pentatonic"].keys():
            self.rkey_list.insert(END, key)

        self.scale_names.selection_set( first = 0 )
        self.rkey_list.selection_set( first = 0 )

        #bind events
        self.scale_names.bind("<Button-1>", self.listbox_click)
        self.rkey_list.bind("<Button-1>", self.listbox_click)

        #pack everything in order
        self.header.pack(expand = True, fill="both")
        self.body.pack(expand = True, fill="both")
        self.scale_names.pack(side=LEFT)
        self.rkey_list.pack(side=LEFT)

        #create fretboard object
        self.fretboard = Fretboard(['E', 'A', 'D', 'G', 'B', 'E'], 23)
        self.scale = None #initialised when selection is made
        self.current_selection = App.scales[self.get_list_selection(self.scale_names)][self.get_list_selection(self.rkey_list)]
        self._draw_visualisation()


    def _draw_visualisation(self):
        """function to take all current input data and draw the fretboard to screen"""
        self.fretboard = Fretboard(['E', 'A', 'D', 'G', 'B', 'E'], 23)
        self.scale = Scale("C", App.scales[self.get_list_selection(self.scale_names)][self.get_list_selection(self.rkey_list)])
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



    def listbox_click(self, event):
        event.widget.activate(event.widget.curselection()[0 ])
        w_name = str(event.widget).split('.')[-1]
        if w_name == "relative_keys":
            self.redraw_body()
        elif w_name == "scale_names":
            self.redraw_rkey_list()
        else:
            raise Exception("The widget event passed to 'App.listbox_click' does not pertain to a 'Tk.Listbox' instance")

    def redraw_body(self):
        """Reconstruct body when click event is fired """
        self.body.destroy()
        self.body = Frame(self, bd=2, relief=SUNKEN)
        self.body.pack(expand=True, fill="both")
        self._draw_visualisation()

    def redraw_rkey_list(self):
        scale_name = self.get_list_selection(self.scale_names)
        self.rkey_list.delete(0, END)
        for key in App.scales[scale_name].keys():
            self.rkey_list.insert(END, key)
        self.rkey_list.selection_set( first = 0 )

    def get_list_selection(self, widget):
        try:
            #"""helper function for extracting list index selection
            index = int(widget.curselection()[0])
            return widget.get(index)
        except IndexError:
            raise IndexError(f"When attempting to get the current selection of Tk.Listbox {str(widget).split('.')[-1]} it failed. \nThe current selection is: {widget.curselection()}")
        except:
            raise Exception()


app = App()
app.mainloop()
