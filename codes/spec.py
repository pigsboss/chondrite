#!/usr/bin/env python
"""Measure similarity of two spectra.
Syntax:
spec.py a.csv b.csv
where a.csv and b.csv are the two spectra CSV files.

spec.py ab.xlsx
where ab.xlsx is the four-column Excel file that contains both spectra. 

Options:
-f  LAMBDA_0 is minimum wavelength of spectral band.
-t  LAMBDA_1 is maximum wavelength of spectral band.
-r  D_LAMBDA is wavelength sampling resolution.
-n  LAMBDA_n is wavelength where two spectra are normalized.
-p  PLOTNAME plot spectra and save as graphic file or show in GUI.
-s  SCALE (0, 1, 2, or 3) is the order of polynomial slope to be truncated
    before cross-correlating.
-h  print this message.
"""

import numpy as np
import pandas as pd
import csv
import sys
import matplotlib.pyplot as plt
from os import path
from getopt import gnu_getopt
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit

font = {'family': ['Hiragino Sans GB']}

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

def load_excel(excelfile):
    """Load spectra from Excel file.
"""
    df = pd.read_excel(excelfile, usecols=[0,1])
    specname_a = df.columns[1]
    valid_rows = np.logical_not(np.isnan(np.double(df[specname_a])))
    wdat,sdat = np.double(df)[valid_rows,:].transpose()
    spec = interp1d(wdat, sdat, 'linear')
    return specname_a, specname_b, spec_a, spec_b

def spec_corr(w, x, y, scale=0):
    func1 = lambda u,a,b: a*u+b
    func2 = lambda u,a,b,c: a*u**2.+b*u+c
    func3 = lambda u,a,b,c,d: a*u**3.+b*u**2.+c*u+d
    if scale==0:
        sx = np.mean(x)*np.ones_like(x)
        sy = np.mean(y)*np.ones_like(y)
    elif scale==1:
        popt,pcov = curve_fit(func1, w, x)
        sx = func1(w, *popt)
        popt,pcov = curve_fit(func1, w, y)
        sy = func1(w, *popt)
    elif scale==2:
        popt,pcov = curve_fit(func2, w, x)
        sx = func2(w, *popt)
        popt,pcov = curve_fit(func2, w, y)
        sy = func2(w, *popt)
    elif scale==3:
        popt,pcov = curve_fit(func3, w, x)
        sx = func3(w, *popt)
        popt,pcov = curve_fit(func3, w, y)
        sy = func3(w, *popt)
    vx = x - sx
    vy = y - sy
    return (np.sum(vx*vy) / np.sqrt(np.sum(vx**2.)*np.sum(vy**2.))), vx, vy, sx, sy

if __name__ == "__main__":
    opts, args = gnu_getopt(sys.argv[1:], 'hf:t:r:n:p:s:')
    plotspec = False
    lambda_0 = None
    lambda_1 = None
    d_lambda = 0.1
    lambda_n = None
    scale = 0
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
        elif opt == '-s':
            scale = int(val)
    if len(args)==2:
        csvfile_a = path.normpath(path.abspath(path.realpath(args[0])))
        csvfile_b = path.normpath(path.abspath(path.realpath(args[1])))
        assert path.isfile(csvfile_a), csvfile_a+' does not exist.'
        assert path.isfile(csvfile_b), csvfile_b+' does not exist.'
        specname_a, spec_a = load_csv(csvfile_a)
        specname_b, spec_b = load_csv(csvfile_b)
    else:
        excelfile = path.normpath(path.abspath(path.realpath(args[0])))
        assert path.isfile(excelfile), excelfile+' does not exist.'
        specname_a, specname_b, spec_a, spec_b = load_excel(excelfile)
    if lambda_0 is None:
        lambda_0 = max(spec_a.x[0], spec_b.x[0])
    if lambda_1 is None:
        lambda_1 = min(spec_a.x[-1], spec_b.x[-1])
    if lambda_n is None:
        lambda_n = (lambda_0 + lambda_1) / 2.
    wrng = np.arange(lambda_0, lambda_1, d_lambda)
    arng = spec_a(wrng) / spec_a(lambda_n)
    brng = spec_b(wrng) / spec_b(lambda_n)
    corr,va,vb,sa,sb = spec_corr(wrng, arng, brng, scale=scale)
    print('Corr: {:.6f}'.format(corr))
    print('S.A.: {:.6f} degrees'.format(np.rad2deg(np.arccos(corr))))
    if plotspec:
        plt.close()
        plt.plot(wrng, arng, label=specname_a)
        plt.plot(wrng, brng, label=specname_b)
        if scale>0:
            plt.plot(wrng, va, label=specname_a+' 变化值')
            plt.plot(wrng, vb, label=specname_b+' 变化值')
            plt.plot(wrng, sa, '-.', label=specname_a+' 平均值')
            plt.plot(wrng, sb, '-.', label=specname_b+' 平均值')
        plt.xlabel('wavelength, in nm')
        plt.ylabel('reflectance, normalized')
        plt.legend(prop=font)
        if len(plotname) > 0:
            plt.savefig(plotname,dpi=800)
            plt.close()
        else:
            plt.show()
