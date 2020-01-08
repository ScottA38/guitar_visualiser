from tkinter import *
import tkinter as tk
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

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        #declare widgets to live inside of root
        self.header = Frame(self, height=100,  bd=2, relief=SUNKEN)
        self.body = Frame(self, bd=2, relief=SUNKEN)
        self.lb_frames = {
            "scale_root": lambda: String.music_notes,
            "scale_names": App.scales.keys,
            "rkey_list": lambda: App.scales[self.scale_names.current_sel()].keys(), #has to be declared as lambda else the value is not ascertainable yet
        }
        for title, l_items in self.lb_frames.items():
            self.lb_frames[title] = self.contain_lb(self.header, title, l_items())
            #should be getting the listbox widget from the constructor
            setattr(self, title, self.lb_frames[title].nametowidget(title))
            self.lb_frames[title].pack(side=LEFT)

        self.scale_frame = self.contain_scale(self.header, "number_frets", 12, 46)
        self.scale_frame.pack(side=LEFT)
        self.no_frets = self.scale_frame.nametowidget("number_frets")

        #bind events
        self.scale_names.bind("<Double-Button-1>", self.redraw_rkey_list)
        self.rkey_list.bind("<Double-Button-1>", self.redraw_body)
        self.no_frets.bind("<B1-Motion>", self.redraw_body)

        #pack everything in order
        self.header.pack(expand = True, fill="both")
        self.body.pack(expand = True, fill="both")

        #create fretboard object
        self.fretboard = None #initialised on first call to _draw_visualisation
        self.scale = None #initialised on first call to _draw_visualisation
        self._draw_visualisation()


    def _draw_visualisation(self):
        """function to take all current input data and draw the fretboard to screen"""
        self.fretboard = Fretboard(['E', 'A', 'D', 'G', 'B', 'E'], self.no_frets.get())
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

    def contain_lb(self, master, title, lb_values):
        container = Frame(master, bd=2, relief=SUNKEN)
        heading = Label(container, justify=CENTER, text=title)
        lb = Lb(lb_values, container, height=4, exportselection=0, name=title)
        heading.pack(expand=True, fill=BOTH)
        lb.pack(expand=True, fill=BOTH)
        return container

    def contain_scale(self, master, title, min, max):
        container = Frame(master, bd=2, relief=SUNKEN)
        heading = Label(container, justify=CENTER, text=title)
        scale = tk.Scale(container, from_=min, to=max, orient=HORIZONTAL, name=title)
        heading.pack(expand=True, fill=BOTH)
        scale.pack(expand=True, fill=BOTH)
        return container


app = App()
app.mainloop()
