#! /usr/bin/env python

"""
This is a collection of data management functions
==========================================
Written in 2024-02-10 by Aurelie Albert aurelie.albert@univ-grenoble-alpes.fr
"""

import sys, getopt
import argparse

import numpy as np
import numpy.ma as ma

import xarray as xr
import dask

def get_data2D(filei,var,ttime,lev):
    ds=xr.open_dataset(filei)
    if (lev == -1):
        data=ds[var][ttime].squeeze()
    else:
        data=ds[var][ttime,lev].squeeze()
    return data

def get_data2D_all_chunks(filei,var,lev):
    ds=xr.open_dataset(filei,chunks={'time_counter':1,'x':10000,'y':1000})
    if (lev == -1):
        data=ds[var][:].squeeze()
    else:
        data=ds[var][:,lev].squeeze()
    return data

def get_data2D_all(filei,var,lev):
    ds=xr.open_dataset(filei)
    if (lev == -1):
        data=ds[var][:].squeeze()
    else:
        data=ds[var][:,lev].squeeze()
    return data

