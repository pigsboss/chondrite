#!/usr/bin/env python
"""Measure similarity of two spectra.
Syntax:
spec.py a.csv b.csv -f LAMBDA_0 -t LAMBDA_1 -r D_LAMBDA -n LAMBDA_n -p figure_name
a.csv and b.csv are the two spectra CSV files.
-f  LAMBDA_0 is minimum wavelength of spectral band.
-t  LAMBDA_1 is maximum wavelength of spectral band.
-r  D_LAMBDA is wavelength sampling resolution.
-n  LAMBDA_n is wavelength where two spectra are normalized.
-p  plot spectra and save as graphic file or show in GUI.
-h  print this message.
"""

import numpy as np
import csv
import sys
import matplotlib.pyplot as plt
from os import path
from getopt import gnu_getopt
from scipy.interpolate import interp1d

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei', 'Hiragino Sans GB']

def load_spec(csvfile):
    """load spectrum from CSV file.
"""
    wlst = []
    slst = []
    with open(csvfile,'r') as fp:
        specreader = csv.DictReader(fp)
        varname  = specreader.fieldnames[0]
        specname = specreader.fieldnames[1]
        for row in specreader:
            wlst.append(float(row[varname]))
            slst.append(float(row[specname]))
        print('{:d} {:s} records read from {:s}, spectral range: {:.1f} nm to {:.1f} nm.'.format(
            len(wlst), specname, csvfile, wlst[0], wlst[-1]))
    npts = len(wlst)
    wdat = np.double(wlst)
    sdat = np.double(slst)
    spec = interp1d(wdat, sdat, 'linear')
    return specname, spec

def spec_corr(x,y):
    return (np.sum(x*y) / np.sqrt(np.sum(x**2.)*np.sum(y**2.)))

if __name__ == "__main__":
    opts, args = gnu_getopt(sys.argv[1:], 'hf:t:r:n:p:')
    plotspec = False
    for opt, val in opts:
        if opt == '-h':
            print(__doc__)
            sys.exit()
        elif opt == '-f':
            lambda_0 = float(val)
        elif opt == '-t':
            lambda_1 = float(val)
        elif opt == '-r':
            d_lambda = float(val)
        elif opt == '-n':
            lambda_n = float(val)
        elif opt == '-p':
            plotspec = True
            plotname = val
    csvfile_a = path.normpath(path.abspath(path.realpath(args[0])))
    csvfile_b = path.normpath(path.abspath(path.realpath(args[1])))
    assert path.isfile(csvfile_a), csvfile_a+' does not exist.'
    assert path.isfile(csvfile_b), csvfile_b+' does not exist.'
    specname_a, spec_a = load_spec(csvfile_a)
    specname_b, spec_b = load_spec(csvfile_b)
    wrng = np.arange(lambda_0, lambda_1, d_lambda)
    arng = spec_a(wrng) / spec_a(lambda_n)
    brng = spec_b(wrng) / spec_b(lambda_n)
    print('Corr: {:.6f}'.format((spec_corr(arng, brng))))
    if plotspec:
        plt.close()
        plt.plot(wrng, arng, label=specname_a)
        plt.plot(wrng, brng, label=specname_b)
        plt.xlabel('wavelength, in nm')
        plt.ylabel('reflectance, normalized')
        plt.legend()
        if len(plotname) > 0:
            plt.savefig(plotname,dpi=800)
            plt.close()
        else:
            plt.show()
