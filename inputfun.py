# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 14:45:55 2018

@author: fung2
"""
from brian2 import *
from scipy import signal
import numpy as np

def back_current(mean, std, enhancement, runtime, dt, tau, N, order):
    sampling_rate = 1/dt
    nyquist = sampling_rate/2
    cutoff = 1/tau
    normalized_cutoff = cutoff/nyquist
    
    
    back_noise = np.random.normal(enhancement*mean, std, (int(runtime/dt), N))
    b, a = signal.butter(order, normalized_cutoff, btype='low', analog=False)
    back_noise_filt = signal.lfilter(b, a, back_noise[:,0])

    if(N > 1):
        for j in range(1, N):
            back_noise_filt = np.vstack((back_noise_filt, signal.lfilter(b, a, back_noise[:,j])))
    
    return back_noise_filt.T

def input_stimulus(mean, std, runtime, dt, tau, order):
    sampling_rate = 1/dt
    nyquist = sampling_rate/2
    cutoff = 1/tau
    normalized_cutoff = cutoff/nyquist

    input_noise= (np.random.normal(mean, std, int(runtime/dt)))
    
    b, a = signal.butter(order, normalized_cutoff, btype='low', analog=False)
    
    input_noise_filt = signal.lfilter(b, a, input_noise)
    
    for i in range(0, len(input_noise_filt)): 
        if(input_noise_filt[i] < 0):
            input_noise_filt[i] = 0
            
    return input_noise_filt

def psth(spike, lim, tbin):
    ## remove unwanted t from spike_t, spike_i index only within defined limit
    spike_i = []
    spike_t = []
    for j in range(0, size(spike.i)):
        if(spike.i[j] > lim[0] and spike.i[j] < lim[1]):
            spike_t.append(spike.t[j])
            spike_i.append(spike.i[j])
            
    t = 0
    count = 0
    freq = []
    tvec = []
    
    for k in range(0, size(spike_t)):
        while(spike_t[k] > t):
            freq.append(count/(20*tbin))
            count = 0;
            tvec.append(t)
            t += tbin;
            if(spike_t[k] <= t):
                count +=1;
        count +=1;
    
    return freq, tvec

def visualise_connectivity(S):
    Ns = len(S.source)
    Nt = len(S.target)
    figure(figsize=(10, 4))
    subplot(121)
    plot(zeros(Ns), arange(Ns), 'ok', ms=10)
    plot(ones(Nt), arange(Nt), 'ok', ms=10)
    for i, j in zip(S.i, S.j):
        plot([0, 1], [i, j], '-k')
    xticks([0, 1], ['Source', 'Target'])
    ylabel('Neuron index')
    xlim(-0.1, 1.1)
    ylim(-1, max(Ns, Nt))
    subplot(122)
    plot(S.i, S.j, 'ok')
    xlim(-1, Ns)
    ylim(-1, Nt)
    xlabel('Source neuron index')
    ylabel('Target neuron index')


