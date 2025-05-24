# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 15:06:25 2023

@author: bilal
"""

from serial import *
import numpy as np
import time
from matplotlib import pyplot as plt

#funcstions

def initial_cond(dg):
    # voltsweep(fp, dg)
    dg.write('TRAT 4e4\r'.encode())

    #Syncing the pulses
    dg.write('DLAY 2,0,0\r'.encode())
    dg.write('DLAY 4,2,0\r'.encode())
    dg.write('DLAY 6,2,0\r'.encode())
    dg.write('DLAY 8,2,0\r'.encode())

    #Assign voltages
    dg.write('LAMP 1,%f \r'.encode() % (2.2)) #for AB
    dg.write('LAMP 2,%f \r'.encode() % (2.2)) #for CD
    dg.write('LAMP 3,%f \r'.encode() % (2.2)) #for EF
    dg.write('LAMP 4,%f \r'.encode() % (2.2)) #for GH

    # Assign pulse widths
    dg.write('DLAY 3,2, 10e-9\r'.encode())
    dg.write('DLAY 5,4, 10e-9\r'.encode())
    dg.write('DLAY 7,6, 10e-9\r'.encode())
    dg.write('DLAY 9,8, 10e-9\r'.encode())
    
    return 0

def plottin(labels, x, y ):
    
    plt.clf()
    plt.figure(figsize=(8, 6))
    plt.scatter(x,y)
    plt.xlabel(labels[0])
    plt.ylabel(labels[1])
    plt.title(labels[2])
    plt.grid()
    
    plt.savefig(labels[3] + '.svg')
    plt.savefig(labels[3] + '.png')
    

def GetData(s, time = 1 , exp_rate = 40000):
    data_points = exp_rate*time
    data = s.read(10)
    # print(s.in_waiting)
    dets = []
    counts = np.array([data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]])
    
    dets.append([data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]])
    for i in range(int(data_points)-1):
        data = s.read(10)
        if data[0] + data[1]+ data[2]+ data[3]+ data[4]+ data[5]+ data[6]+ data[7]+ data[8] > 0:
            dets.append([data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]])
        counts = counts + np.array([data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]])
    
    return dets, counts    

def voltsweep(fp, dg):
    
    counts = []
    
    steps = np.arange(0.5, 3.3, 0.01)
    
    triggers = steps
    
    A = []
    B =  []
    BP =  []
    AP =  []
    AB =  []
    ABP =  []
    APB =  []
    APBP =  []
    ABBP =  []
    
    data_fid = []
    
    for i in steps:
        
        dg.write('LAMP 1,%f \r'.encode() % (i)) #for AB
        dg.write('LAMP 2,%f \r'.encode() % (i)) #for CD
        dg.write('LAMP 3,%f \r'.encode() % (i)) #for EF
        dg.write('LAMP 4,%f \r'.encode() % (i)) #for GH
        dg.write('DISP 12,3\r'.encode()) 

        data_counts, counting = GetData(fp)
        counts = [counting]
        A.append(counts[0][0])
        B.append(counts[0][1])
        BP.append(counts[0][2])
        AP.append(counts[0][3])
        AB.append(counts[0][4])
        ABP.append(counts[0][5])
        APB.append(counts[0][6])
        APBP.append(counts[0][7])
        ABBP.append(counts[0][8])
        
        data_fid += data_counts
    
    
    #For channels
    plottin(["Voltage (V)", "Detections on A", "Voltage Sweep","VoltA" ], triggers, A)
    plottin(["Voltage (V)", "Detections on B", "Voltage Sweep","VoltB" ], triggers, B)
    plottin(["Voltage (V)", "Detections on BP", "Voltage Sweep","VoltB'"], triggers, BP)
    plottin(["Voltage (V)", "Detections on AP", "Voltage Sweep","VoltA'" ], triggers, AP)
    
    plottin(["Voltage (V)", "Detections on AB", "Voltage Sweep","VoltAB" ], triggers, AB)
    plottin(["Voltage (V)", "Detections on AB'", "Voltage Sweep","VoltAB'" ], triggers, ABP)
    plottin(["Voltage (V)", "Detections on A'B", "Voltage Sweep","VoltA'B"], triggers, APB)
    plottin(["Voltage (V)", "Detections on A'B'", "Voltage Sweep","VoltA'B'"], triggers, APBP)
    plottin(["Voltage (V)", "Detections on ABB'", "Voltage Sweep","VoltABB'" ], triggers, ABBP)
    
    #print(data_fid)
    #data = [A, B , BP, AP, AB, ABP, APB, APBP, ABBP]
    np.savetxt('Voltage_Sweep.txt', data_fid)
            
    return 0


# main
fp = Serial("COM11", 4000000)
dg = Serial("COM4", 9600)

fp.set_buffer_size(1000000)

while True:    
    pos_head = fp.read(1)
    
    if pos_head[0] == 47:
        break

# voltsweep(fp, dg)
initial_cond(dg)

try:
    voltsweep(fp, dg)
    print("chillz")

except:    
    print('sads')


fp.close()
dg.close()
