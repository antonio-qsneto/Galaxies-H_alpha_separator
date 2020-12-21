"""
    Purpose: Separate spectra from active galaxies with H-alpha
    @author: Antonio Neto
"""


from astropy.table import Table
from astropy.io import fits as pyfits
from matplotlib import pyplot
import matplotlib.pyplot as plt
import io, os
import numpy as np
import shutil

os.mkdir('agn')
os.mkdir('normal')
path = os.getcwd()
tree1 = path+'/agn/'
tree2 = path+'/normal/'

# Programa para separação de espectros h_alpha de N dimensões

for filename in os.listdir('galaxies/'):
    if filename.endswith('.fits'):
        fit = pyfits.open('galaxies/' + filename)
        
        header = fit[0].header
        flux_test = fit[0].data
        flux = fit[0].data
        flux = flux[0]
        
        start_wave = int(header['CRVAL1'])
        step = header['CDELT1']
        
        w0, dw, n = start_wave, step, len(flux)
        w = start_wave + step * n
        wave = np.linspace(w0, w, n, endpoint=False)
        data = Table([wave, flux], names=(str(header['CRVAL1']), str(step)))

        until = 6561 - start_wave
        until = until/step

        u = int(until)
        j = (flux[0:u])
        media1 = sum(flux[0:u])/len(j)
        media1 = media1+100
        inc = u + 5
        k = (flux[u:inc])
        media_h = sum(flux[u:inc])/len(k)

        hdu_name = fit
        name  = hdu_name[0].header['TARGET']
        ra_fit = hdu_name[0].header['OBSRA']
        dec_fit = hdu_name[0].header['OBSDEC']
        t = str(ra_fit)+str(dec_fit)
        m = max(k)+100
        
#------------------------------------------------------------------------------------#

        if (media_h > media1):
            shutil.copy('galaxies/' + filename, 'agn/' + filename)
        else:
            shutil.copy('galaxies/' + filename, 'normal/' + filename)

