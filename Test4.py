# -*- coding: utf-8 -*-
"""
Created on Thu Mar  8 12:44:23 2018

@author: fung2
"""
import SSreset as ssr
ssr.__reset__()
################################################################
from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from brian2 import *
import networkx as nx
import numpy as np
from scipy import signal
import inputfun as inf
###############################################################
class OtherFrame(tk.Toplevel):
    """"""
    #----------------------------------------------------------------------
    def __init__(self, master):
        """Constructor"""
        self.original_frame = master
        tk.Toplevel.__init__(self)
        self.geometry("400x300")
        self.title("otherFrame")
        backbutton = Button(self, text="Done", color = "red", command=self.onClose)
        backbutton.grid()
    #----------------------------------------------------------------------
    def onClose(self):
        """"""
        self.destroy()
        self.original_frame.show()
###############################################################
class Simulator(tk.Frame):
    
    def __init__(self, master):
        Frame.__init__(self, master)
        self.master=master
        self.init_window()

    def init_window(self):
        self.master.title("Network Constructor v1.0")
        self.master.grid()
        
        framelay=self.setup_frames()
        self.populate_frames(framelay)
        
    def setup_frames(self):
        frame = {}
        # Parental Frames
        frame['a'] = Frame(self.master, width=300, height=600, borderwidth=2, relief='groove')
        frame['b'] = Frame(self.master, width=1300, height=600, borderwidth=2, relief='groove')
        frame['c'] = Frame(self.master, width=1600, height=200, borderwidth=2, relief='groove')
    
        frame['a'].grid(row=0, column=0, sticky=N+S+E+W)
        frame['b'].grid(row=0, column=1, sticky=N+S+E+W)
        frame['c'].grid(row=1, column=0, columnspan=2)
    
        # Progeny 0 Frames:
        frame['b1'] = Frame(frame['b'], width=1000, height=500, bg ='black', borderwidth=12, relief='sunken')
        frame['b2'] = Frame(frame['b'], width=300, height=100, borderwidth=2, relief='groove')
    
        frame['b1'].grid(row=0, column=0, sticky=N+S+E+W)
        frame['b2'].grid(row=1, column=0, sticky=N+S+E+W,)
    


    
        # Weighting
        frame['b'].grid_rowconfigure(0, weight=1)
        frame['b'].grid_columnconfigure(0, weight=1)
    
        return frame
    def populate_frames(self, fr):
    
        # Populating 'a' frame
        for c in range(35):
            fr['a'].columnconfigure(c, weight=5)
        for r in range(50):
            fr['a'].rowconfigure(r, weight=5)
        #buttons------------------------------------------------
        astart = tk.Button(fr['a'],text="Simulate", bg="Green", fg="white",activeforeground="black")
        astart.config(font="Arial")
        astart.grid(row=50, column=0,columnspan=45, sticky=N+E+W+S, padx=(5,5), pady=(5,5))
        v = tk.IntVar()
        v.set(1)  # initializing the choice, i.e. Python
        
        models = [
                ("LIF",1),
                ("HH",2),
                ("Other",3)
        ]

        def ShowChoice():
            print(v.get())

        Label(fr['a'], 
                 text="""Choose your model:""",
                 justify = tk.LEFT,
                 padx = 20).grid()
        
        for val, model in enumerate(models):
            tk.Radiobutton(root, 
                          text=model,
                          padx = 20, 
                          variable=v, 
                          command=ShowChoice,
                          value=val).grid()
        
            
        
        
        #labels-------------------------------------------------
        alabel_neurons=Label(fr['a'], text="Enter Numer of neurons")
        alabel_neurons.grid(row=0, column=0, sticky=N+E+W+S)
        
        alabel_layers=Label(fr['a'], text="Enter Numer of layers")
        alabel_layers.grid(row=1, column=0, sticky=N+E+W+S)
        #Entries------------------------------------------------
        aspinbox_neuron = Spinbox(fr['a'], from_=0, to=20)
        aspinbox_neuron.grid(row=0, column=1)
        aspinbox_layer = Spinbox(fr['a'], from_=0, to=20)
        aspinbox_layer.grid(row=1, column=1)
        # Populating b2a & b2b frames
    
        # Populating c1 frame
        for c2 in range(60):
            fr['a'].columnconfigure(c2, weight=5)
        for r2 in range(30):
            fr['a'].rowconfigure(r2, weight=5)
        cnew_window = tk.Button(fr['c'], text="Open in new Frame", command=self.openFrame)
        cnew_window.grid(row=30, column=60, sticky=N+E+W+S)
        #----------------------------------------------------------------------
    def hide(self):
        """"""
        self.master.withdraw()
    #----------------------------------------------------------------------
    def openFrame(self):
        """"""
        self.hide()
        subFrame = OtherFrame(self)
    #----------------------------------------------------------------------
    def show(self):
        """"""
        self.master.update()
        self.master.deiconify()

if __name__ == '__main__':  
    root=Tk()
    root.geometry("1600x800")
    app=Simulator(root)
    root.mainloop()
    print("asdasd")