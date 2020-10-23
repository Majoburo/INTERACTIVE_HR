import pandas as pd
from scipy.interpolate import InterpolatedUnivariateSpline
import numpy as np
import matplotlib.pyplot as plt
import glob
from astropy.io import fits
from os import path

def get_sdssspec(f):
    hdu = fits.open(f)
    d = hdu[1].data
    h = hdu[0].header
    hdu.close()

    Nd = len(d)
    scale = float(h['BUNIT'][0:5])
    sdsswave = np.zeros(Nd)
    sdssflux = np.zeros(Nd)
    for s in range(Nd):
        sdsswave[s] = 10.0**(d[s][1])
        sdssflux[s] = d[s][0]*scale
        
    # Perform 3-point binning for blue arm
    num_bin = 3
    max_ind = int(np.floor(float(len(sdsswave))/num_bin) * num_bin)
    sdsswave = (sdsswave[0:max_ind:num_bin] + 
                sdsswave[1:max_ind:num_bin] + 
                sdsswave[2:max_ind:num_bin]) / num_bin
    sdssflux = (sdssflux[0:max_ind:num_bin] + 
                sdssflux[1:max_ind:num_bin] + 
                sdssflux[2:max_ind:num_bin]) / num_bin
    
    return sdsswave,sdssflux

files = glob.glob("DATA/*fits")

# Load in the Gaia-SDSS Crossmatched Sample
sdss_crossmatch = pd.read_csv("gaia_sdss30_match3.csv")
sdss_bprp = sdss_crossmatch.phot_bp_mean_mag.values - sdss_crossmatch.phot_rp_mean_mag.values
sdss_mag = sdss_crossmatch.phot_g_mean_mag.values + 5.0*np.log10(sdss_crossmatch.parallax/100.)
specnames = sdss_crossmatch.specname.values

stars = []
xy = []
wl1,_ = get_sdssspec(files[0])
stars.append(wl1) #making first row the wavelenght row
for i,fi in enumerate(specnames):
    if path.exists("DATA/"+fi):
        wl, data = get_sdssspec("DATA/"+fi)
        spl = InterpolatedUnivariateSpline(wl,data,ext=3)
        star = spl(wl1)
        star[star==0]=float('NaN')
        stars.append(spl(wl1))
        xy.append([sdss_mag[i],sdss_bprp[i]])
#Saving csv files with xy coordinates for CMD and spectral data.
np.savetxt("spectra.csv", np.array(stars), fmt="%.4e", delimiter=",", header="wavelenght flux")
np.savetxt("xy.csv", np.array(xy), fmt="%.2f", delimiter=",", header="x y")

