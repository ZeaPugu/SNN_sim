# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 10:25:39 2018

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
        frame['c'].grid(row=1, column=0, columnspan=2, sticky=N+S+E+W)
    
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
            fr['a'].columnconfigure(c, weight=1)
        for r in range(50):
            fr['a'].rowconfigure(r, weight=1)
        ##### SIMULATION #####
        def simulationModel():
            
            input_stim = inf.input_stimulus(float(aspinbox_meaninput.get()), float(aspinbox_STDinput.get()), 1, .0001, .5, int(aspinbox_orderinput.get()))
            figure(99)
            #plot(input_stim)
            N = 20
            N_tot = 200
            back_curr = inf.back_current(float(entry_meanback.get()), float(aspinbox_STDback.get()), 1.49, 1, .0001, .002, 20, int(aspinbox_orderback.get()))
            back_curr2 = inf.back_current(float(entry_meanback.get()), float(aspinbox_STDback.get()), 1.47, 1, .0001, .002, 180, int(aspinbox_orderback.get()))
            #input_stim = input_stimulus(0, 2000e-12, 1, .0001, .5, 1)
            I_back = TimedArray(back_curr, dt = 0.1*ms)
            I_back2 = TimedArray(back_curr2, dt = 0.1*ms)
            I_input = TimedArray(input_stim, dt = 0.1*ms)
            Vreversal = 0
            v0 = float(aspinbox_V0.get())
            R = float(aspinbox_resistance.get())
            tau = 5*ms
            taug = 5*ms
            C = tau/R
            
            ### Layer 1 Neuron Equation
            
            # No synaptic current input
        
            eqs_1 = '''
            dv/dt = (-v + I_input(t)*R + I_back(t, i)*R + v0 )/tau : 1 (unless refractory)
            '''
            
            ### Layers 2+ Neuron Equations
            # Conductance based synaptic current input
            eqs_2 = '''
            I_conductance = -g*(v-Vreversal) : 1
            dv/dt = (-v/(R*C) + I_back2(t, i)/(C) + v0/(R*C) - g*(v-Vreversal)/C) : 1 (unless refractory)
            dg/dt = -g/taug : 1
            '''
            
            M = NeuronGroup(N, eqs_1, threshold='v>-50e-3', reset='v = -60e-3', refractory=1*ms, method='euler', dt = 0.1*ms)
            M.v = -60e-3
            M1 = NeuronGroup(N*9, eqs_2, threshold='v>-50e-3', reset='v = -60e-3',refractory=1*ms,  method='euler', dt = 0.1*ms)
            M1.v = -60e-3
            M1.g = 0
            
            ### Layer 1 - Layer 2 Synapses
            s = Synapses(M, M1, on_pre='g_post += 9e-11') #9e-11
            s.connect(j = 'k for k in range(0, 20)')
            
            ### Layer 2 - Layer 3 Synapses
            s2 = Synapses(M1, M1, on_pre='g_post += 9e-11')
            for y in range(0, 20):
                s2.connect(i = y, j = range(20, 40))
            
            ### Layer 3 - Layer 4 Synapses
            for y in range(20, 40):
                s2.connect(i = y, j = range(40, 60))
            
            ### Layer 4 - Layer 5 Synapses
            for y in range(40, 60):
                s2.connect(i = y, j = range(60, 80))
                
            ### Layer 5 - Layer 6 Synapses
            for y in range(60, 80):
                s2.connect(i = y, j = range(80, 100))
                
            ### Layer 6 - Layer 7 Synapses
            for y in range(80, 100):
                s2.connect(i = y, j = range(100, 120))
                
            ### Layer 7 - Layer 8 Synapses
            for y in range(100, 120):
                s2.connect(i = y, j = range(120, 140))
                
            ### Layer 8 - Layer 9 Synapses
            for y in range(120, 140):
                s2.connect(i = y, j = range(140, 160))
                
            ### Layer 9 - Layer 10 Synapses
            for y in range(140, 160):
                s2.connect(i = y, j = range(160, 180))
                
            
            ### State Monitors
            Mv = StateMonitor(M, 'v', record=True)
            Mspk = SpikeMonitor(M)
            M1v = StateMonitor(M1, 'v', record=True)
            Mspk1 = SpikeMonitor(M1)
            M1_I_conductance = StateMonitor(M1, 'I_conductance', record = True)
            M1_g = StateMonitor(M1, 'g', record = True)
        
            run(int(aspinbox_Runtime.get())*ms)
            
            print(Mspk.i)
        #buttons------------------------------------------------
        astart = tk.Button(fr['a'],text="Simulate", bg="Green", fg="White",activeforeground="black", command=simulationModel)
        astart.config(font="Arial")
        astart.grid(row=50, column=0,columnspan=45, sticky=N+E+W+S, padx=(5,5), pady=(5,5))
        Label(fr['a'], 
                 text="""Choose your model:""",
                 justify = tk.LEFT,
                 padx = 5).grid(row=2, column=0)
        
        self.models = (  # Text, Value, Row, Column
            ('LIF', 1, 2, 1),
            ('HH', 2, 3, 1),
            ('Other', 3, 4, 1)
         )
        
        radiobuttons = []
        for _Text, _Value, _Row, _Column in self.models: # it will unpack the values during each iteration
            _Radio = Radiobutton(fr['a'], text = _Text, value = _Value)
            _Radio.config(anchor=W, justify = LEFT)
            _Radio.grid(row = _Row, column = _Column, sticky=W)
            radiobuttons.append(_Radio)
        #labels-------------------------------------------------
        alabel_neurons=Label(fr['a'], text="Enter Numer of neurons")
        alabel_neurons.grid(row=0, column=0, sticky=W, padx=(20,20))
        alabel_layers=Label(fr['a'], text="Enter Numer of layers")
        alabel_layers.grid(row=1, column=0, sticky=W, padx=(20,20))
        mean_backcurrent= Label(fr['a'], text="mean(background current(A))")
        mean_backcurrent.grid(row=5, column=0, sticky=W, padx=(20,20))
        std_backcurrent= Label(fr['a'], text="STD(background current(A))")
        std_backcurrent.grid(row=6, column=0, sticky=W, padx=(20,20))
        order_backcurrent= Label(fr['a'], text="order(background current)")
        order_backcurrent.grid(row=7, column=0, sticky=W, padx=(20,20))
        mean_input= Label(fr['a'], text="mean(input(A))")
        mean_input.grid(row=8, column=0, sticky=W, padx=(20,20))
        std_input= Label(fr['a'], text="STD(input(A))")
        std_input.grid(row=9, column=0, sticky=W, padx=(20,20))
        order_input= Label(fr['a'], text="order(input)#1")
        order_input.grid(row=10, column=0, sticky=W, padx=(20,20))
        V0= Label(fr['a'], text="V0(mV)")
        V0.grid(row=11, column=0, sticky=W, padx=(20,20))
        input_Resistence= Label(fr['a'], text="input_Resistence(Ohm)#100e6")
        input_Resistence.grid(row=12, column=0, sticky=W, padx=(20,20))
        Conductance= Label(fr['a'], text="Conductance(postsynaptic)")
        Conductance.grid(row=13, column=0, sticky=W, padx=(20,20))
        Run_Time= Label(fr['a'], text="Run_Time(ms)")
        Run_Time.grid(row=14, column=0, sticky=W, padx=(20,20))
        #Entries------------------------------------------------
        aspinbox_neuron = Spinbox(fr['a'], from_=0, to=20)
        aspinbox_neuron.grid(row=0, column=1)
        aspinbox_layer = Spinbox(fr['a'], from_=0, to=20)
        aspinbox_layer.grid(row=1, column=1)
        mb = StringVar(fr['a'], value='55e-12')
        entry_meanback = tk.Entry(fr['a'], textvariable=mb)
        entry_meanback.grid(column=1, row = 5, sticky=W)
        #aspinbox_meanback = Spinbox(fr['a'], from_=10e-12, to=80e-12)
        #aspinbox_meanback.grid(row=5, column=1)
        stb = StringVar(fr['a'], value='70e-12')
        aspinbox_STDback = tk.Entry(fr['a'], textvariable=stb)
        aspinbox_STDback.grid(row=6, column=1,sticky=W)
        aspinbox_orderback = Spinbox(fr['a'], from_=0, to=20)
        aspinbox_orderback.grid(row=7, column=1)
        mi = StringVar(fr['a'], value='0')
        aspinbox_meaninput = tk.Entry(fr['a'], textvariable=mi)
        aspinbox_meaninput.grid(row=8, column=1, sticky=W)
        sti = StringVar(fr['a'], value='2000e-12')
        aspinbox_STDinput = tk.Entry(fr['a'],textvariable=sti )
        aspinbox_STDinput.grid(row=9, column=1, sticky=W)
        aspinbox_orderinput = Spinbox(fr['a'], from_=0, to=20)
        aspinbox_orderinput.grid(row=10, column=1)
        v0 = StringVar(fr['a'], value='-60e-3')
        aspinbox_V0 = tk.Entry(fr['a'],textvariable=v0 )
        aspinbox_V0.grid(row=11, column=1, sticky=W)
        r = StringVar(fr['a'], value='100e6')
        aspinbox_resistance = tk.Entry(fr['a'], textvariable=r)
        aspinbox_resistance.grid(row=12, column=1, sticky=W)
        cond= StringVar(fr['a'], value='g_post += 9e-11')
        aspinbox_Conductance = tk.Entry(fr['a'],textvariable=cond )
        aspinbox_Conductance.grid(row=13, column=1, sticky=W)
        aspinbox_Runtime = Spinbox(fr['a'], from_=100, to=1000)
        aspinbox_Runtime.grid(row=14, column=1)
        
        # Populating b2a & b2b frames
    
        # Populating c1 frame
        for c2 in range(20):
            fr['c'].columnconfigure(c2, weight=1)
        for r2 in range(30):
            fr['c'].rowconfigure(r2, weight=1)
            
        rasterbutton = tk.Button(fr['c'], command=self.openFrame)
        rasterimagetemp=Image.open("raster.png")
        rasterimage = ImageTk.PhotoImage(rasterimagetemp)
        rasterbutton.config(image=rasterimage)
        rasterbutton.image=rasterimage
        rasterbutton.grid(row=0, column=0, padx=10, pady=10, sticky=N+E+W+S)
    
    #----------------------------------------------------------------------    
    def openFrame(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Graph(self.newWindow)
    #----------------------------------------------------------------------
class Graph():
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.f1 = Figure( figsize=(10, 9), dpi=80 )
        self.ax10 = self.f1.add_axes( (0.05, .05, .50, .50), axisbg=(.75,.75,.10), frameon=True)
        self.ax10.plot(np.max(np.random.rand(100,10)*10,axis=1),"r-")
        self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
        self.canvas = FigureCanvasTkAgg(self.f1, master=self.master)
        self.canvas.get_tk_widget().grid()
        self.canvas.show()
        self.quitButton.grid()
        self.frame.grid()
    def close_windows(self):
        self.master.destroy()
        


if __name__ == '__main__':  
    root=tk.Tk()
    root.geometry("1600x800")
    app=Simulator(root)
    root.update()
    root.deiconify()
    root.mainloop()