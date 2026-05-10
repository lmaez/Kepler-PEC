# Louis Maez
# 05/02/2026
# https://lightkurve.github.io/lightkurve/tutorials/1-getting-started/searching-for-data-products.html
# https://lightkurve.github.io/lightkurve/tutorials/1-getting-started/using-light-curve-file-products.html
# V783 Cyg, Kepler KIC 5559631

import lightkurve as lk
import matplotlib.pyplot as plt
import numpy as np
from lightkurve.correctors import PLDCorrector
import warnings
warnings.filterwarnings('ignore')

#Search for NGC 1501 in TESS data and print table 
#search_result = lk.search_lightcurve('KIC 5559631', mission = 'KEPLER')
search_result = lk.search_targetpixelfile('KIC 5559631', mission = 'KEPLER')
#print(search_result)
tpf_collection = search_result[:19].download_all()

bg_mask = np.zeros(tpf_collection[6].shape[1:], dtype = bool) #tpf_collection[6].create_threshold_mask(threshold = 3)
bg_mask[3:5, 1:2] = True
bg_mask[0:3, 4:5] = True
bg_mask[0:2, 0:1] = True

pld_mask = np.zeros(tpf_collection[6].shape[1:], dtype = bool)
pld_mask[1:3, 2:4] = True

pld = PLDCorrector(tpf_collection[6])
pld = tpf_collection[6].to_corrector()
test = pld.correct(restore_trend = True, aperture_mask = pld_mask,
                   pld_aperture_mask = pld_mask,
                   background_aperture_mask = bg_mask)
#test = tpf_collection[6].to_corrector('pld').correct()
sap_test = tpf_collection[6].to_lightcurve()
ax = sap_test.normalize().plot(label = 'sap_flux', color = 'red')
test.normalize().remove_outliers().plot(ax = ax, label = 'PLD Corrected')


##for curve in tpf_collection:
##    curve = curve.to_corrector('pld').correct()
##
##lc_collection = lk.LightCurveCollection([tpf.to_lightcurve(aperture_mask='pip') for tpf in tpf_collection])  
##lc_stitched = lc_collection.stitch()
##lc_stitched.plot()
plt.show()

uncorrected_cdpp = sap_test.estimate_cdpp()
corrected_cdpp = test.estimate_cdpp()
print(f"Uncorrected CDPP = {uncorrected_cdpp:.0f}")
print(f"Corrected CDPP = {corrected_cdpp:.0f}")

pld.diagnose()
pld.diagnose_masks()
plt.show()


