# Louis Maez
# 05/04/2026
# V783 Cyg, Kepler KIC 5559631
# Measured Period: 0.620733899203742 d


import lightkurve as lk
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
from astropy import units as u
import warnings
warnings.filterwarnings('ignore')

search_result = lk.search_lightcurve('KIC 5559631',
                                     mission = 'KEPLER')

lc_collection = search_result[0:19].download_all()

#fig, ax = plt.subplots(figsize = (20,5))
for curve in lc_collection:
    #curve.flux = curve['sap_flux']
    curve = curve.normalize()
    curve = curve.remove_nans()
    
lc_stitched = lc_collection.stitch(
    corrector_func=lambda x: x.normalize().flatten().remove_outliers(
        sigma = 3))

#lc_stitched.scatter()
#plt.show()

pgram = lc_stitched.to_periodogram(method = 'lombscargle')
#pgram.plot()
#plt.show()

#pgram.plot(view = 'period', scale = 'log')
#plt.show()
##
#print(pgram.period)
#print(pgram.power)
#print(pgram.period_at_max_power)
##
##lc_folded = lc_stitched.fold(period=pgram.period_at_max_power)
##lc_folded.scatter()
##plt.show()

peaks, properties = find_peaks(lc_stitched.flux, prominence = 0.5, distance = 0.6206798800670955)

peaks.plot()
plt.show()

##print("here")
##df = lc_stitched.to_pandas()
##df.to_csv("V783Cyg_LightCurve_Data.csv")
###lc_stitched.to_csv('V783Cyg_LightCurve_Data.csv')
##print("Exported lightcurve as .csv")

