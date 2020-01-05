from tkinter import *
from guitar_visualiser import Fretboard, String, Scale, Note
from Util.synchronization import Synchronization, synchronize, synchronized
from Util.observer import Observer, Observable

class ScaleName(Observable):
    def __init__(self, l_widget):
        Observable.__init__(self)
        self.l_widget = l_widget
        self.l_widget.selection_set( first = 0 )
        self.l_widget.bind("<Button-1>", self.notifyObservers)

    def get_list_selection(self):
        try:
            index = int(self.l_widget.curselection()[0])
            return self.l_widget.get(index)
        except IndexError:
            print()
            raise IndexError(f"Error occurred trying to get the current listbox selection for wrapper class {self.__class__.__name__}.\nThis is likely because a selection has not been set yet.")
        except:
            raise Exception(f"Unknown exception encountered when trying to get the current Listbox selection in wrapper class {self.__class__.__name__} ")

    def notifyObservers(self, *args):
        self.setChanged()
        print("notifying!")
        scale_name = self.get_list_selection()
        Observable.notifyObservers(self, scale_name)

class RelativeKey(Observer):
    def __init__(self, l_widget):
        Observer.__init__(self)
        self.l_widget = l_widget
        self.l_widget.selection_set( first = 0 )

    def get_list_selection(self):
        index = int(self.l_widget.curselection()[0])
        return self.l_widget.get(index)

    def update(self, observable, arg):
        print(f"updating! arg: {arg}")
        self.draw_list(arg)

    def draw_list(self, scale_name):
        self.l_widget.delete(0, END)
        for key in App.scales[scale_name].keys():
            self.l_widget.insert(END, key)

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
        self.title("Fretboard_visualiser")

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

        #bind events
        self.scale_names.bind("<Button-1>", )
        self.rkey_list.bind("<Button-1>", self.redraw_body)

        #Listbox Observable/Observer objects
        self.Obs_scale = ScaleName(self.scale_names)
        self.Obr_rkey = RelativeKey(self.rkey_list)
        #attach observer
        self.Obs_scale.addObserver(self.Obr_rkey)

        #pack everything in order
        self.header.pack(expand = True, fill="both")
        self.body.pack(expand = True, fill="both")
        self.scale_names.pack()
        self.rkey_list.pack()

        #create fretboard objects
        self.fretboard = Fretboard(['E', 'A', 'D', 'G', 'B', 'E'], 23)
        self.scale = None #initialised when selection is made
        self.current_selection = App.scales[self.Obs_scale.get_list_selection()][self.Obr_rkey.get_list_selection()]
        self._draw_visualisation()


    def _draw_visualisation(self):
        """function to take all current input data and draw the fretboard to screen"""
        self.scale = Scale("C", App.scales[self.Obs_scale.get_list_selection()][self.Obr_rkey.get_list_selection()])
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

    def redraw_body(event):
        """Reconstruct body when click event is fired """
        body.destroy()
        body = Frame(root, bd=2, relief=SUNKEN)
        body.pack(expand=True, fill="both")
        self._draw_visualisation(e_std, Obs_ScaleList, Obr_RKeyList, body)

app = App()
app.mainloop()
