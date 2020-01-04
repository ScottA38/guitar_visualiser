from tkinter import *
from guitar_visualiser import Fretboard, String, Scale, Note
from Util.synchronization import Synchronization, synchronize, synchronized
from Util.observer import Observer, Observable

class ScaleName(Observable):
    def __init__(self, l_widget):
        Observable.__init__(self)
        self.l_widget = l_widget

    def get_list_selection(self):
        index = int(self.l_widget.curselection()[0])
        return list_widget.get(index)

    def notifyObservers(self):
        self.setChanged()
        scale_name = self.get_list_selection()
        Observable.notifyObservers(self, scale_name)

class RelativeKey(Observer):
    def __init__(self, l_widget):
        Observer.__init__(self)

    def update(self, observable, arg):



def draw(fretboard, scale, relative_key, frame):
    #affecting the values of another class :(
    scale.impose(fretboard)

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

root = Tk()
root.title("Fretboard_visualiser")

header = Frame(root, height=100,  bd=2, relief=SUNKEN)
header.pack(expand=True, fill="both")

body = Frame(root, bd=2, relief=SUNKEN)
body.pack(expand=True, fill="both")


scale_names = Frame(header, height=4, exportselection=0, name="scale_names")
relative_key = Frame(header, height=4, exportselection=0, name="relative_keys")

scale_names.pack()
relative_key.pack()

for scale in scales.keys():
    scale_names.insert(END, scale)

e_std = Fretboard(['E', 'A', 'D', 'G', 'B', 'E'], 23)

d_pent = Scale("D", scales["pentatonic"]["minor"])
c_natural_maj = Scale("C", scales["natural"]["major"])
f_maj_pent = Scale("F", scales["pentatonic"]["major"])

#print(d_pent.degrees)

root.mainloop()
