# -*- coding: utf-8 -*-
"""
Created on Fri May 08 09:30:57 2015

@author: tallon
"""

sepChg = False #True if chg/dsg power path are separated

numCell = 1 #Number of Li/Ion cells in serial
nomVolt = 3.6*numCell #Nominal cell voltage
minVolt = 2.5*numCell #Minimal cell voltage
maxVolt = 4.2*numCell #Maximum allowed cell voltage

opTemp = [10, 25, 45] #Critical operating temperature

resMOStyp = [(10.0, 0.076), (10.0, 0.092)] #[(Vgs (V), Rdson (Ohm))]
resMOSmax = [(2.5, 0.128), (2.5, 0.166)] #[(Vgs (V), Rdson (Ohm))]
junct2Amb = [85, 125] #Die thermal resistance range
currMOS = 0.1 #Current flowing in the MOS
parrMOS = 1 #Number of MOS in parallel

"""
Compute the final temperature range with respect to a range of defined
MOSFET Rdson (resMOStyp OR resMOSmax) and a range of operating temperatures
Print everything in a formatted way
"""
def compute(resRange, tempRange):
    resMOS = []
    if not sepChg:
        for t in resRange:
            resMOS.append((t[0], (t[1]*2)/parrMOS))
    else:
        for t in resRange:
             resMOS.append((t[0], t[1]/parrMOS))
    for i in resMOS:
        power = i[1]*(currMOS**2)
        tempRise = [junct2Amb[0]*power, junct2Amb[1]*power]
        print("**********V={0}V**********".format(i[0]))
        print("Power @{0}A....\t{2}W".format(currMOS, i[0], power))
        print("TºC rising....\t{0}ºC ~ {1}ºC".format(tempRise[0], tempRise[1]))
        for t in tempRange:
            temp = [t+tempRise[0], t+tempRise[1]]
            print("From {0}ºC....\t{1}ºC ~ {2}ºC".format(t, temp[0], temp[1]))

compute(resMOStyp, opTemp)
compute(resMOSmax, opTemp)