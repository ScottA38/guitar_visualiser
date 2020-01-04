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
        index = int(self.l_widget.curselection()[0])
        return self.l_widget.get(index)

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
        for key in scales[scale_name].keys():
            self.l_widget.insert(END, key)

def draw_visualisation(fretboard, ScaleObj, RKeyObj, frame):
    """function to take all current input data and draw the fretboard to screen"""
    cur_scale = Scale("C", scales[ScaleObj.get_list_selection()][RKeyObj.get_list_selection()])
    cur_scale.impose(fretboard)

    c=0
    r=0
    for string in fretboard:
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
            Label(frame, text=fret, bg = background, fg=foreground, relief=RIDGE, width=5, height=2  ).grid(row=r, column=c)
            c += 1
        r += 1
        c=0

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

def redraw(event):
    """Method for event handling on click inside of header frame - MUST be called exclusively by the 'header' Frame"""
    print("event fired!")
    if event.widget.__class__.__name__ == "Frame":
        body.destroy()
        body = Frame(root, bd=2, relief=SUNKEN)
        body.pack(expand=True, fill="both")
        draw_visualisation(e_std, Obs_ScaleList, Obr_RKeyList, body)

root = Tk()
root.title("Fretboard_visualiser")

header = Frame(root, height=100,  bd=2, relief=SUNKEN)
header.pack(expand=True, fill="both")

body = Frame(root, bd=2, relief=SUNKEN)
body.pack(expand=True, fill="both")

scale_names = Listbox(header, height=4, exportselection=0, name="scale_names")
relative_key = Listbox(header, height=4, exportselection=0, name="relative_keys")

scale_names.pack()
relative_key.pack()

header.bind("<Button-1>", redraw)

for scale in scales.keys():
    scale_names.insert(END, scale)

for key in scales["pentatonic"].keys():
    relative_key.insert(END, key)

Obs_ScaleList = ScaleName(scale_names)
Obr_RKeyList = RelativeKey(relative_key)

Obs_ScaleList.addObserver(Obr_RKeyList)

e_std = Fretboard(['E', 'A', 'D', 'G', 'B', 'E'], 23)

draw_visualisation(e_std, Obs_ScaleList, Obr_RKeyList, body)

root.mainloop()
