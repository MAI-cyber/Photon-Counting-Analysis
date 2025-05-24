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
    dg.write('TRAT 1e4\r'.encode())

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
    dg.write('DLAY 3,2, 20e-9\r'.encode())
    dg.write('DLAY 5,4, 20e-9\r'.encode())
    dg.write('DLAY 7,6, 20e-9\r'.encode())
    dg.write('DLAY 9,8, 20e-9\r'.encode())
    
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
    

def resolution(fp, dg):
    
    
    counts = []
    
    steps = np.arange(40, 1, -0.1)
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
        
        dg.write('DLAY  3,2, %fe-9 \r'.encode() % (i)) #B with respect to A
        dg.write('DLAY  5,4, %fe-9 \r'.encode() % (i)) #D with respect to C
        dg.write('DLAY  7,6, %fe-9 \r'.encode() % (i)) #F with respect to E
        dg.write('DLAY  9,8, %fe-9 \r'.encode() % (i)) #H with respect to g
        
        dg.write('DISP 11,3\r'.encode()) 
        
        # print(i)


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
    plottin(["Pulse width", "Detections on A", "Resolutions","ResoA" ], triggers, A)
    plottin(["Pulse width", "Detections on B", "Resolutions","ResoB" ], triggers, B)
    plottin(["Pulse width", "Detections on BP", "Resolutions","ResoB'"], triggers, BP)
    plottin(["Pulse width", "Detections on AP", "Resolutions","ResoA'" ], triggers, AP)
    
    plottin(["Pulse width", "Detections on AB", "Resolutions","ResoAB" ], triggers, AB)
    plottin(["Pulse width", "Detections on AB'", "Resolutions","ResoAB'" ], triggers, ABP)
    plottin(["Pulse width", "Detections on A'B", "Resolutions","ResoA'B"], triggers, APB)
    plottin(["Pulse width", "Detections on A'B'", "Resolutions","ResoA'B'"], triggers, APBP)
    plottin(["Pulse width", "Detections on ABB'", "Resolutions","ResoABB'" ], triggers, ABBP)
    
    #print(data_fid)
    #data = [A, B , BP, AP, AB, ABP, APB, APBP, ABBP]
    np.savetxt('Resolutions_Sweep.txt', data_fid)
            
    return 0

def GetData(s, time = 0.5 , exp_rate = 40000):
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

# main
fp = Serial("COM11", 4000000)
dg = Serial("COM4", 9600)

fp.set_buffer_size(1000000)

flag = False

for i in range (1000):    
    pos_head = fp.read(1)
    
    if pos_head[0] == 47:
        print("HEad found")
        flag = True
        break
    
    
if flag:
    try:
        
        initial_cond(dg)
    
        resolution(fp, dg)
        
        print("chillz")
    
    except:
        
        print('sads')
else:
    print("head never found")

fp.close()
dg.close()
