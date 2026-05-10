# Louis Maez
# 05/04/2026
# PECCARY Analysis of V783Cyg Kepler Light Curve

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from peccary import peccary
from peccary import HCplots
from peccary import utils
from peccary.timeseries import Timeseries
import peccary.utils as utils

RawData = pd.read_csv('V783Cyg_LightCurve_Data.csv')
PruneData = RawData.dropna(subset = ['pdcsap_flux'])    #Discard NaN values from pdcsap_flux
#print(PruneData.head())

timeSet = PruneData['time']
tArray = timeSet.to_numpy().flatten()
fluxSet = PruneData['pdcsap_flux']
fluxArray = fluxSet.to_numpy().flatten()
tSeries = Timeseries(t = tArray, x = fluxArray)
print(tArray, fluxArray)

length = len(tArray)

pecc = peccary(tSeries, attr = 'x')
#pattern = peccary.tPat(1, sampInt = 500)
#idealInt = utils.tpat2ell(50, dt=1, n=3)
#print(idealInt)

H, C, ells = pecc.calcHCcurves(min_sampInt = 1,
                               max_sampInt = 40000, step_sampInt = 500)

HCplots.HCplane(H, C)
plt.show()

HCplots.HCcurves(H=H, C=C, sampInts = ells)
plt.show()
