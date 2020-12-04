#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: nicholasnewcomb
"""

#I_calc revision 1

import matplotlib.pyplot as plt
#import matplotlib.ticker as ticker
import numpy as np
import pandas as pd

#10.816 lbs for aluminum box LT2 size


B_Weight = 27
LB = 4.15
BB = 7.52
weight_1 = B_Weight+BB
weight_2 = B_Weight+2*BB
weight_3 = B_Weight+3*BB
track_cam = 0.3
depth_cam = 0.7
Nav = track_cam+depth_cam


###Big Batteries
weight_1
#Volume: 



r = 6.34/2 #wheel in inches
MaxRPM = 5676


#Torq Calculations:
GB = 36 #gearbox ratio (options for 4,12,16,20,36,48,64,80,100)
Tau_stall = 2.6*GB

RPM= pd.Series([0, 1000, 2000, 3000, 4000, 5000])
RPM = [w/GB for w in RPM]
w = np.linspace(0,5676/GB,num=2000)
Tau_Alex = pd.DataFrame(data=[2.6, 2.2, 1.6, 1.35, 0.8, 0.4],index=RPM)
Tau_Nick = pd.DataFrame(data=[2.6, 2.25,1.6, 1.35, 0.8, 0.4],index=RPM)
Tau_comb = Tau_Alex.append(Tau_Nick)
Tau_comb.sort_values(0,ascending=False,inplace=True)
Tau_cons, Tau_stall = np.polyfit(Tau_comb.index, Tau_comb[0], 1)
#current calcs
I_free = 1.8
I_stall = 105

def Current(w):
    I=(I_stall-I_free)/(0-MaxRPM/GB)*w+105
    return(I)

def Torq(w,GB):
    T=Tau_cons*w+Tau_stall
    T=GB*T
    return(T)



#%% Power Constants

SparkMax = 0.2*12 #motor controller
Roboteq = 0.3*22.8 #BMS
myRIO = 0.1*12 #Definitely would like backup on this one
NX = 0.53*19 #Nvidia Jetson NX
SignalLight = 0.02*5 #LED indicator 5V
D435i = 0.7*5 #Depth camera 5V
T265 = 0.3*5 #Tracking camera 5V
Encoder = 0.02*5 #Through bore 5V
ArduCam = 0.16*3.3 #Inspection Camera
PhantomKit = 0.52*12 #average use camera mount guess
LightRing = 0.1*12 #ring of LEDs
Router = 4*12 #wifi router

Pparts = SparkMax+Roboteq+myRIO+NX+SignalLight+D435i+T265+Encoder+ArduCam+PhantomKit+LightRing+Router
#%%
I = Current(w)
T = Torq(w,GB)


fig1, (ax,ax1,ax2,ax3,ax4) = plt.subplots(nrows=1,ncols=5)
ax = plt.subplot(221)
ax.set_ylim([0,max(T)*1.2])
ax.locator_params(axis='y',nbins=10)
ax.locator_params(axis='x',nbins=12)
ax.set_ylabel("Torque (N-m)")
ax.set_xlabel(r'RPM')
ax.set_title('Torque Curves')
ax.tick_params(axis='y', labelcolor='royalblue')
L1 = ax.plot(w,T,color='royalblue',label="Torque")
ax.grid(which='major', axis='both')


ax1 = ax.twinx()  # instantiate a second axes that shares the same x-axis\
ax1.set_ylim([0,max(I)*8])
ax1.locator_params(axis='y',nbins=10)
ax1.locator_params(axis='x',nbins=12)
ax1.set_ylabel("Current (Amps)")
ax1.tick_params(axis='y', labelcolor='purple')
L2 = ax1.plot(w,I,color='purple',label="Current")


fig1.legend([L1,L2],
           labels=["Torque","Current"],
           loc=[0.25,0.8]
           #prop={'size':13}
           )



TauCons = T/I #N-m per Amp
S=w*4*np.pi/12
ax2 = plt.subplot(222)
ax2.plot(S,TauCons, label="Torque Per Amp",color='goldenrod')
ax2.set_title(r'$\frac{Torque}{Amp}$ at Various RPM')
ax2.set_ylabel(r'$\frac{N-m}{A}$')
ax2.set_xlabel(r'Speed $\frac{feet}{min}$')
ax2.grid()

PND = T*8.85075/r #divide by radius and convert newtons to pounds force
ax3 = plt.subplot(223)
ax3.plot(S,PND, label="Lbs",color='red')
ax3.set_ylim([0,max(PND)*1.2])
ax3.locator_params(axis='y',nbins=8)
ax3.locator_params(axis='x',nbins=12)
ax3.set_title(r'Maximum Payload')
ax3.set_ylabel(r'Weight (lbs)')
ax3.set_xlabel(r'Speed $\frac{feet}{min}$')
ax3.grid()

print("Max Payload is: ",np.interp(150,S,PND))

PNDcons = I/PND #Amps/Pound
ax4 = plt.subplot(224)
ax4.plot(S,PNDcons, label="Amps Per Pound",color='green')
ax4.set_title(r'$\frac{Amps}{Pound}$ at Various RPM')
ax4.set_ylabel(r'$\frac{A}{lb}$')
ax4.set_xlabel(r'Speed $\frac{feet}{min}$')
ax4.grid()
plt.tight_layout()
plt.show()

#%%
fig2, ax5 = plt.subplots(nrows=1,ncols=1)

ax5.set_ylabel(r'Power Consumption $\frac{Watts}{hour}$')
ax5.set_xlabel(r'Speed $\frac{feet}{min}$')
ax5.set_title('Total Power Use')

Ptot=12*PNDcons*weight_1+Pparts
L6 = ax5.plot(S,Ptot,color='black',label="1 Batt Consumption")
Ptot2=12*PNDcons*weight_2+Pparts
L8 = ax5.plot(S,Ptot2,color='blue',label="2 Batt Consumption")
Ptot3=12*PNDcons*weight_3+Pparts
L10 = ax5.plot(S,Ptot3,color='green',label="3 Batt Consumption")
B1 = np.zeros(np.size(Ptot))
VB1=22.8
CapB1 = 14
CapB2 = 28
for value in range(np.size(B1)):
    B1[value]=VB1*CapB2
B2=B1*2
B3=B1*3
l7 = ax5.plot(S,B1,color='black',label='1 Batt Capacity',linestyle='-.')
l9 = ax5.plot(S,B2,color='blue',label='2 Batt Capacity',linestyle='-.')
l11 = ax5.plot(S,B3,color='green',label='3 Batt Capacity',linestyle='-.')
ax5.grid(which='major', axis='both')
fig2.legend(
           loc=[0.6,0.6]
           )
plt.tight_layout()
plt.show()


#%%
fig3, ax6 = plt.subplots(nrows=1,ncols=1)

ax6.set_ylabel('Operating Time \n (Hours)')
ax6.set_xlabel('Speed \n'+r'$\frac{feet}{min}$')
ax6.set_title('Total Operational Time')

L12 = ax6.plot(S,B1/Ptot,color='black',label="1 Batt Operating Time")
L13 = ax6.plot(S,B2/Ptot2,color='blue',label="2 Batt Operating Time")
L14 = ax6.plot(S,B3/Ptot3,color='green',label="3 Batt Operating Time")




EOL = 0.8

L15 = ax6.plot(S,B1/Ptot*EOL,color='black',label="1 Batt EOL",linestyle='-.')
L16 = ax6.plot(S,B2/Ptot2*EOL,color='blue',label="2 Batt EOL",linestyle='-.')
L17 = ax6.plot(S,B3/Ptot3*EOL,color='green',label="3 Batt EOL",linestyle='-.')

print("While Operating at 220ft/min")
print("Operating time for 1 Batt: ",np.interp(150,S,B1/Ptot))
print("EOL operating time for 1 Batt: ",np.interp(150,S,B1/Ptot*EOL))
print("Operating time for 2 Batt: ",np.interp(150,S,B2/Ptot2))
print("EOL operating time for 2 Batt: ",np.interp(150,S,B2/Ptot2*EOL))
print("Operating time for 3 Batt: ",np.interp(150,S,B3/Ptot3))
print("EOL operating time for 3 Batt: ",np.interp(150,S,B3/Ptot3*EOL))

ax6.grid(which='major', axis='both')
fig3.legend(
           loc=[0.2,0.65]
           )
plt.tight_layout()
plt.show()