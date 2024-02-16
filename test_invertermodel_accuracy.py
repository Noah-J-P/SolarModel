# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 11:24:31 2024

@author: noahj
"""

import pvlib
from pvlib import pvsystem
import numpy as np

primo38kspecmax=3800
primo38kspecmin=1900
growattspecmax=7280
growattspecmin=4765
SEspecmax=3300
SEspecmin=2637.12
inverter_primo38k = {'Paco': 3800,   # AC Power rating  User provided
                 'Pso': 38, # power consumed by inverter 1% of Ac rating is reasonable 
                 'Pdco': 6000, # Dc power input resulting in Paco at reference voltage   User provided
                 'Vdco': 600, # dc reference voltage     User provided
                'C0': 0, #  (assumed 0 without experimental data)
                'C1': 0, #  (assumed 0 without experimental data)
                'C2': 0, # (assumed 0 without experimental data)
                'C3': 0, # (assumed 0 without experimental data)
                'Pnt': 1, # Power consumed at night
               } 

inverter_growatt = {'Paco': 7280,   # AC Power rating  User provided
                 'Pso': 72.8, # power consumed by inverter 1% of Ac rating is reasonable 
                 'Pdco': 16400, # Dc power input resulting in Paco at reference voltage   User provided
                 'Vdco': 400, # dc reference voltage     User provided
                'C0': 0, #  (assumed 0 without experimental data)
                'C1': 0, #  (assumed 0 without experimental data)
                'C2': 0, # (assumed 0 without experimental data)
                'C3': 0, # (assumed 0 without experimental data)
                'Pnt': 1, # Power consumed at night
               } 

inverter_SE3800H = {'Paco': 3300,   # AC Power rating  User provided
                 'Pso': 33, # power consumed by inverter 1% of Ac rating is reasonable 
                 'Pdco': 5100, # Dc power input resulting in Paco at reference voltage   User provided
                 'Vdco': 480, # dc reference voltage     User provided
                'C0': 0, #  (assumed 0 without experimental data)
                'C1': 0, #  (assumed 0 without experimental data)
                'C2': 0, # (assumed 0 without experimental data)
                'C3': 0, # (assumed 0 without experimental data)
                'Pnt': 2.5, # Power consumed at night
               } 


# Estimate AC power from DC power using the Sandia Model
acprimo38kmin = pvlib.inverter.sandia(410, # DC voltage input to the inverter
                                3000, # DC power input to the inverter
                                 inverter_primo38k) # Parameters for the inverter 

acprimo38kmax = pvlib.inverter.sandia(410, # DC voltage input to the inverter
                                6000, # DC power input to the inverter
                                 inverter_primo38k) # Parameters for the inverter 

acgrowattmin = pvlib.inverter.sandia(400, # DC voltage input to the inverter
                                10700, # DC power input to the inverter
                                 inverter_growatt) # Parameters for the inverter 

acgrowattmax = pvlib.inverter.sandia(400, # DC voltage input to the inverter
                                16400, # DC power input to the inverter
                                 inverter_growatt) # Parameters for the inverter 

acSEmin = pvlib.inverter.sandia(380, # DC voltage input to the inverter
                                4075, # DC power input to the inverter
                                 inverter_SE3800H) # Parameters for the inverter 

acSEmax = pvlib.inverter.sandia(380, # DC voltage input to the inverter
                                5100, # DC power input to the inverter
                                 inverter_SE3800H) # Parameters for the inverter 

primomindif=100*(acprimo38kmin-primo38kspecmin)/primo38kspecmin
primomindif=str(primomindif)
primomaxdif=100*(acprimo38kmax-primo38kspecmax)/primo38kspecmax
primomaxdif=str(primomaxdif)

growattmindif=100*(acgrowattmin-growattspecmin)/growattspecmin
growattmindif=str(growattmindif)
growattmaxdif=100*(acgrowattmax-growattspecmax)/growattspecmax
growattmaxdif=str(growattmaxdif)

SEmindif=100*(acSEmin-SEspecmin)/SEspecmin
SEmindif=str(SEmindif)
SEmaxdif=100*(acSEmax-SEspecmax)/SEspecmax
SEmaxdif=str(SEmaxdif)

print("The percent difference of the maximum output AC power for the Primo 3.8-1 inverter is " + primomaxdif +"%")
print("The percent difference of the minimum output AC power for the Primo 3.8-1 inverter is " + primomindif +"%")

print("The percent difference of the maximum output AC power for the Growatt 8200TL-XH-US inverter is " + growattmaxdif +"%")
print("The percent difference of the minimum output AC power for the Growatt 8200TL-XH-US inverter is " + growattmindif +"%")

print("The percent difference of the maximum output AC power for the SE3800H-US inverter is " + SEmaxdif +"%")
print("The percent difference of the minimum output AC power for the SE3800H-US inverter is " + SEmindif +"%")