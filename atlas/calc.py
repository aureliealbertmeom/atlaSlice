import sys, getopt
import argparse

import numpy as np
import numpy.ma as ma

import xarray as xr

def vorticity(u,v,e1v,e2u):
    return dx(v)/e1v - dy(u)/e2u

def dx(var):
    return var.shift(x=1)-var

def dy(var):
    return var.shift(y=1)-var

def module(u,v):
    return np.sqrt(u*u + v*v)
