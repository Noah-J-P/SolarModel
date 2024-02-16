# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 11:11:29 2024

@author: noahj
"""

import pvlib
from pvlib import pvsystem
import numpy as np

cec_mod_db = pvsystem.retrieve_sam('CECmod')


### manufacturer specifications
TOPBiop=10.91
TOPBvop=41.6
TOPBPmax=454

BYDiop=10.42
BYDvop=28.3
BYDPmax=294.8

TQPiop=7.53
TQPvop=38.29
TQPPmax=288.15
## Put the characteristics from data sheet below


module_dataBYDNLK395 = {'Technology': 'monocrystalline Q.ANTUM solar half cells', # technology
               'STC': 395, # STC power
               'PTC': 294.8, # PTC power
               'v_mp': 30.32, # Maximum power voltage under STC
               'i_mp': 13.03, # Maximum power current under STC
               'v_oc': 36.9, # Open-circuit voltage under STC
               'i_sc': 13.71, # Short-circuit current under STC
               'alpha_sc': 0.042, # Temperature Coeff. Short Circuit Current [A/C]
               'beta_voc': -0.254, # Temperature Coeff. Open Circuit Voltage [V/C]
               'gamma_pmp': -0.328, # Temperature coefficient of power at maximum point [%/C]
               'N_s': 108, # Number of cells in series
               'temp_ref': 25}  # Reference temperature conditions
module_dataTOPBiHiKu600 = {'Technology':'TOPCon cells', # technology
     'STC': 600, # STC power
     'PTC': 454, # PTC power
     'v_mp': 44, # Maximum power voltage under STC
     'i_mp': 13.64, # Maximum power current under STC
     'v_oc': 51.8, # Open-circuit voltage under STC
     'i_sc': 14.54, # Short-circuit current under STC
     'alpha_sc': 0.05, # Temperature Coeff. Short Circuit Current [A/C]
     'beta_voc': -0.25, # Temperature Coeff. Open Circuit Voltage [V/C]
     'gamma_pmp': -0.29, # Temperature coefficient of power at maximum point [%/C]
     'N_s': 144, # Number of cells in series
     'temp_ref': 25}  # Reference temperature conditions

module_dataTQPeakDuo385 = {'Technology': 'monocrystalline Q.ANTUM solar half cells', # technology
               'STC': 385, # STC power
               'PTC': 288.3, # PTC power
               'v_mp': 40.24, # Maximum power voltage under STC
               'i_mp': 9.57, # Maximum power current under STC
               'v_oc': 49.57, # Open-circuit voltage under STC
               'i_sc': 10.05, # Short-circuit current under STC
               'alpha_sc': 0.04, # Temperature Coeff. Short Circuit Current [A/C]
               'beta_voc': -0.27, # Temperature Coeff. Open Circuit Voltage [V/C]
               'gamma_pmp': -0.35, # Temperature coefficient of power at maximum point [%/C]
               'N_s': 144, # Number of cells in series
               'temp_ref': 25}  # Reference temperature conditions

cec_fit_paramsTQP = pvlib.ivtools.sdm.fit_cec_sam('monoSi', module_dataTQPeakDuo385['v_mp'], module_dataTQPeakDuo385['i_mp'],
                                  module_dataTQPeakDuo385['v_oc'], module_dataTQPeakDuo385['i_sc'], module_dataTQPeakDuo385['alpha_sc'],
                                  module_dataTQPeakDuo385['beta_voc'], module_dataTQPeakDuo385['gamma_pmp'], 
                                  module_dataTQPeakDuo385['N_s'], module_dataTQPeakDuo385['temp_ref'])


cec_fit_paramsTOPB = pvlib.ivtools.sdm.fit_cec_sam('monoSi', module_dataTOPBiHiKu600['v_mp'], module_dataTOPBiHiKu600['i_mp'],
                                  module_dataTOPBiHiKu600['v_oc'], module_dataTOPBiHiKu600['i_sc'], module_dataTOPBiHiKu600['alpha_sc'],
                                  module_dataTOPBiHiKu600['beta_voc'], module_dataTOPBiHiKu600['gamma_pmp'], 
                                  module_dataTOPBiHiKu600['N_s'], module_dataTOPBiHiKu600['temp_ref'])

cec_fit_paramsBYD395 = pvlib.ivtools.sdm.fit_cec_sam('monoSi', module_dataBYDNLK395['v_mp'], module_dataBYDNLK395['i_mp'],
                                  module_dataBYDNLK395['v_oc'], module_dataBYDNLK395['i_sc'], module_dataBYDNLK395['alpha_sc'],
                                  module_dataBYDNLK395['beta_voc'], module_dataBYDNLK395['gamma_pmp'], 
                                  module_dataBYDNLK395['N_s'], module_dataBYDNLK395['temp_ref'])
irrad=np.array([800])
temp_amb=np.array([20])
temp_cell=temp_amb+(41-20)/800*irrad

# 2nd step: Apply model to estimate the 5 parameters of the single diode equation using the CEC model
diode_paramsTQP = pvlib.pvsystem.calcparams_cec(irrad, temp_cell, module_dataTQPeakDuo385['alpha_sc'], cec_fit_paramsTQP[4], 
                                            cec_fit_paramsTQP[0], cec_fit_paramsTQP[1], cec_fit_paramsTQP[3], 
                                            cec_fit_paramsTQP[2], cec_fit_paramsTQP[5])

diode_paramsTOPB = pvlib.pvsystem.calcparams_cec(irrad, temp_cell, module_dataTOPBiHiKu600['alpha_sc'], cec_fit_paramsTOPB[4], 
                                            cec_fit_paramsBYD395[0], cec_fit_paramsTOPB[1], cec_fit_paramsTOPB[3], 
                                            cec_fit_paramsTOPB[2], cec_fit_paramsTOPB[5])


diode_paramsBYD = pvlib.pvsystem.calcparams_cec(irrad, temp_cell, module_dataBYDNLK395['alpha_sc'], cec_fit_paramsBYD395[4], 
                                            cec_fit_paramsBYD395[0], cec_fit_paramsBYD395[1], cec_fit_paramsBYD395[3], 
                                            cec_fit_paramsBYD395[2], cec_fit_paramsBYD395[5])
# This returns the parameters needed for model
#print(diode_params)

iv_valuesTQP = pvlib.pvsystem.singlediode(diode_paramsTQP[0], 
                                        diode_paramsTQP[1], 
                                        diode_paramsTQP[2], 
                                        diode_paramsTQP[3], 
                                        diode_paramsTQP[4], 
                                        ivcurve_pnts=25,   # Number of points of the I-V curve (equally distributed)
                                        method='lambertw') # I-V using the Lambert W. function

iv_valuesTOPB = pvlib.pvsystem.singlediode(diode_paramsTOPB[0], 
                                        diode_paramsTOPB[1], 
                                        diode_paramsTOPB[2], 
                                        diode_paramsTOPB[3], 
                                        diode_paramsTOPB[4], 
                                        ivcurve_pnts=25,   # Number of points of the I-V curve (equally distributed)
                                        method='lambertw') # I-V using the Lambert W. function


iv_valuesBYD = pvlib.pvsystem.singlediode(diode_paramsBYD[0], 
                                        diode_paramsBYD[1], 
                                        diode_paramsBYD[2], 
                                        diode_paramsBYD[3], 
                                        diode_paramsBYD [4], 
                                        ivcurve_pnts=25,   # Number of points of the I-V curve (equally distributed)
                                        method='lambertw') # I-V using the Lambert W. function



### Checking percent difference between modeled and specified values
idif=100*(iv_valuesTOPB['i_mp']-TOPBiop)/TOPBiop
idif=str(idif)
vdif=100*(iv_valuesTOPB['v_mp']-TOPBvop)/TOPBvop
vdif=str(vdif)
pdif=100*(iv_valuesTOPB['p_mp']-TOPBPmax)/TOPBPmax
pdif=str(pdif)

print("The percent difference of I at max power for the TOPBiHiKu600 is " + idif +"%")

print("The percent difference of V at max power for the TOPBiHiKu600 is " + vdif +"%")

print("The percent difference of max power for the TOPBiHiKu600 is " + pdif +"%")

idif=100*(iv_valuesBYD['i_mp']-BYDiop)/BYDiop
idif=str(idif)
vdif=100*(iv_valuesBYD['v_mp']-BYDvop)/BYDvop
vdif=str(vdif)
pdif=100*(iv_valuesBYD['p_mp']-BYDPmax)/BYDPmax
pdif=str(pdif)

print("The percent difference of I at max power for the BYDNLK395 is " + idif +"%")

print("The percent difference of V at max power for the BYDNLK395 is " + vdif +"%")

print("The percent difference of max power for the BYDNLK395 is " + pdif +"%")

idif=100*(iv_valuesTQP['i_mp']-TQPiop)/TQPiop
idif=str(idif)
vdif=100*(iv_valuesTQP['v_mp']-TQPvop)/TQPvop
vdif=str(vdif)
pdif=100*(iv_valuesTQP['p_mp']-TQPPmax)/TQPPmax
pdif=str(pdif)

print("The percent difference of I at max power for the TQPeakDuo400 is " + idif +"%")

print("The percent difference of V at max power for the TQPeakDuo400 is " + vdif +"%")

print("The percent difference of max power for the TQPeakDuo400 is " + pdif +"%")