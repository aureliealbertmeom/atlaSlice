#! /usr/bin/env python

"""
This is a collection of data management functions
==========================================
Written in 2024-02-10 by Aurelie Albert aurelie.albert@univ-grenoble-alpes.fr
"""

import sys, getopt, os, glob
import argparse

import numpy as np
import numpy.ma as ma

import xarray as xr
import dask

from functions import calc as ca
from functions import functions as f
from params import simulations_dict as params

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

def get_mdata2D_all_chunks(filei,varname,lev,maskfile,maskvar):
    """
    Open a file and the corresponding maskfile
    to retrieve a 2D field, at the surface or a given vertical level
    and mask it according to the cooresponding maskfile
    To be provided :
      - the name of the containing the variable to retrieve = filei
      - the nem of the variable = varname
      - the level at which to extract the 2D fiels = lev, if = -1 it means that the file in 2D entirely
      - the name of the mask file = maskfile
      - the name of the mask variable = maskvar
    Returns :
      - 2D xarray.DataArray
    """
    ds=xr.open_dataset(filei,chunks={'time_counter':1,'x':10000,'y':1000})
    dsmask=xr.open_dataset(maskfile,chunks={'time_counter':1,'x':10000,'y':1000})

    if (lev == -1):
        data=ds[varname][:].squeeze()
    else:
        data=ds[varname][:,lev].squeeze()
    mask=dsmask[maskvar].squeeze()
    datam=data.where(mask==1)
    return datam


def get_data3D(filei,var):
    ds=xr.open_dataset(filei)
    data=ds[var][:].squeeze()
    return data

def get_data3D_all_chunks(filei,var,dep):
    ds=xr.open_dataset(filei,chunks={'time_counter':1,dep:1,'x':10000,'y':1000})
    data=ds[var][:].squeeze()
    return data

def get_compute_2var2D_all_chunks(filei1,filei2,var,varname1,varname2,maskname,lev):
    ds1=xr.open_dataset(filei1,chunks={'time_counter':1,'x':10000,'y':1000})
    ds2=xr.open_dataset(filei2,chunks={'time_counter':1,'x':10000,'y':1000})

    if (lev == -1):
        data1=ds1[varname1][:].squeeze()
        data2=ds2[varname2][:].squeeze()
    else:
        data1=ds1[varname1][:,lev].squeeze()
        data2=ds2[varname2][:,lev].squeeze()
#to do : mask data with specific mask

    match var:
        case 'MOD':
            data=ca.module(data1,data2)
        case 'VORT':
            dsmask=xr.open_dataset(maskname,chunks={'time_counter':1,'x':10000,'y':1000})
            e1v=dsmask['e1v'][0]
            e2u=dsmask['e2u'][0]
            ff=dsmask['ff_t'][0]
            data=ca.vorticity(data1,data2,e1v,e2u)
            data=data/ff
    return data

def get_data2D_all(filei,var,lev):
    ds=xr.open_dataset(filei)
    if (lev == -1):
        data=ds[var][:].squeeze()
    else:
        data=ds[var][:,lev].squeeze()
    return data

def get_data2D_box(filei,var,imin,imax,jmin,jmax,k):
    ds=xr.open_dataset(filei,chunks={'time_counter':1,'x':1000,'y':1000})
    data_box=ds[var][:,jmin[k]-10:jmax[k]+10,imin[k]-10:imax[k]+10]
    return data_box

def get_data3D_box(filei,var,imin,imax,jmin,jmax,k):
    ds=xr.open_dataset(filei,chunks={'time_counter':1,'x':1000,'y':1000})
    data_box=ds[var][:,:,jmin[k]-10:jmax[k]+10,imin[k]-10:imax[k]+10]
    return data_box

