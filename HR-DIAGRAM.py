
from scipy.interpolate import InterpolatedUnivariateSpline
import numpy as np
import matplotlib.pyplot as plt
import glob

# Spectra and corresponding wavelenght range
files = glob.glob("/Users/majoburo/Downloads/s_coelho07/*fits")
x = np.arange(3000,13000.1,0.2)
#SDSS filters
f = fits.open("/Users/majoburo/Downloads/filter_curves.fits")


#Desired spectra sampling 
xs = np.arange(2980.0,11230.0,10)

splines=[]

#Saving csv files with the SDSS filters info
for i in f[1:]:
    wl,a,_,_,_= zip(*i.data)
    spl = InterpolatedUnivariateSpline(wl,a,ext=1)
    splines.append(spl(xs))
    np.savetxt("%d_%d.csv"%(wl[0],wl[-1]), spl(xs), fmt="%.2f", delimiter=",", header="filter fraction")
f.close()

stars = []
xy = []
stars.append(xs) #making first row the wavelenght row

for i,fi in enumerate(files):
    with fits.open(fi,memmap=False) as hdu:
        data = hdu[0].data[:]
        if not np.any(np.isnan(data)):
            spl = InterpolatedUnivariateSpline(x,data,ext=1)
            y = spl(xs)
            g = np.trapz(y*splines[1])
            r = np.trapz(y*splines[2])
            #gr = np.log(g/r)/np.log(2.51)
            stars.append(y)
            xy.append([g-r,r])
            
#Saving csv files with xy coordinates for CMD and spectral data.
np.savetxt("spectra.csv", np.array(stars), fmt="%.2f", delimiter=",", header="wavelenght flux")
np.savetxt("xy.csv", np.array(xy), fmt="%.2f", delimiter=",", header="x y")


xy = np.array(xy)
plt.scatter(xy[:,0],xy[:,1])
plt.show()

