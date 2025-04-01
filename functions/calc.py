import sys, getopt
import argparse

import numpy as np
import numpy.ma as ma

import xarray as xr

sys.path.insert(0,'/summer/meom/workdir/alberta/xscale')
import xscale

def vorticity(u,v,e1v,e2u):
    return dx(v)/e1v - dy(u)/e2u

def dx(var):
    return var.shift(x=1)-var

def dy(var):
    return var.shift(y=1)-var

def dx_var(data,e1):
    dx_var = (data.shift(x=-1) - data)/e1
    return dx_var

def dy_var(data,e2):
    dy_var = (data.shift(y=-1) - data)/e2
    return dy_var

def dz_var(data,e3,dimdep):
    if dimdep == 'deptht':
        dz_var = (data.shift(deptht=-1) - data)/e3
    if dimdep == 'depthu':
        dz_var = (data.shift(depthu=-1) - data)/e3
    if dimdep == 'depthv':
        dz_var = (data.shift(depthv=-1) - data)/e3
    if dimdep == 'depthw':
        dz_var = (data.shift(depthw=-1) - data)/e3
    return dz_var

def module(u,v):
    return np.sqrt(u*u + v*v)

def filt(w):
    win_box2D = w.window
    win_box2D.set(window='hann', cutoff=20, dim=['x', 'y'], n=[30, 30],chunks={})
    bw = win_box2D.boundary_weights(drop_dims=[])
    w_LS = win_box2D.convolve(weights=bw)
    w_SS=w-w_LS
    return w_SS

