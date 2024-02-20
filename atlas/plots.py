#! /usr/bin/env python

"""
This is a collection of plotting functions
==========================================
Written in 2024-02-07 by Aurelie Albert aurelie.albert@univ-grenoble-alpes.fr
"""


import sys, getopt
import argparse

import numpy as np
import numpy.ma as ma

import xarray as xr

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.util as cutil
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as mticker

import cmocean
import dask

plt.rcParams.update({'font.size': 20})

def one_map_noproj_notitle(fig, nx, ny, pos, data, unit, mask, cmap, vmin, vmax):

    datam=np.ma.array(data,mask=1-mask)
    cmapm=plt.get_cmap(cmap).copy()
    cmapm.set_bad('gray',1.)

    ax = fig.add_subplot(nx,ny,pos)

    pcolor=ax.imshow(datam,cmap=cmapm,vmin=vmin,vmax=vmax,interpolation='none')
    ax.invert_yaxis()

    cbar = plt.colorbar(pcolor,orientation='horizontal',label=unit)


def one_map_noproj_notitle_zoom(fig, nx, ny, pos, data, unit, mask, cmap, vmin, vmax,i1,i2,j1,j2):

    datam=np.ma.array(data,mask=1-mask)
    cmapm=plt.get_cmap(cmap).copy()
    cmapm.set_bad('gray',1.)

    ax = fig.add_subplot(nx,ny,pos)

    pcolor=ax.imshow(datam,cmap=cmapm,vmin=vmin,vmax=vmax,interpolation='none')
    ax.invert_yaxis()
    plt.xlim(i1, i2)
    plt.ylim(j1, j2)

    cbar = plt.colorbar(pcolor,orientation='horizontal',shrink=0.75, pad=0.1,label=unit)

def one_map_noproj(fig, nx, ny, pos, data, unit, mask, cmap, vmin, vmax, title):

    datam=np.ma.array(data,mask=1-mask)
    cmapm=plt.get_cmap(cmap).copy()
    cmapm.set_bad('gray',1.)

    ax = fig.add_subplot(nx,ny,pos)

    pcolor=ax.pcolormesh(datam,cmap=cmapm,vmin=vmin,vmax=vmax)
    fig.subplots_adjust(right=0.8)

    cbar = plt.colorbar(pcolor,orientation='horizontal',shrink=0.75, pad=0.1,label=unit)
    ax.set_title(title,size=20,y=1.08)

def one_map_noproj_zoom(fig, nx, ny, pos, data, unit, mask, cmap, vmin, vmax, title,xlim1,xlim2,ylim1,ylim2):

    datam=np.ma.array(data,mask=1-mask)
    cmapm=plt.get_cmap(cmap).copy()
    cmapm.set_bad('gray',1.)

    ax = fig.add_subplot(nx,ny,pos)

    pcolor=ax.pcolormesh(datam,cmap=cmapm,vmin=vmin,vmax=vmax)
    fig.subplots_adjust(right=0.8)
    plt.xlim(xlim1, xlim2)
    plt.ylim(ylim1, ylim2)

    cbar = plt.colorbar(pcolor,orientation='horizontal',shrink=0.75, pad=0.1,label=unit)
    ax.set_title(title,size=20,y=1.08)

def one_map_proj_ortho_global(fig, nx, ny, pos, lon, lat, data, unit, mask, cmap, vmin, vmax, title,cen_lat,cen_lon):

    datam=np.ma.array(data,mask=1-mask)
    cmapm=plt.get_cmap(cmap).copy()
    cmapm.set_bad('gray',1.)

    projection=ccrs.Orthographic(central_latitude=cen_lat, central_longitude=cen_lon)
    ax = fig.add_subplot(nx,ny,pos,projection=projection)

    gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='k', zorder=3)
    gl.top_labels   = False
    gl.right_labels = False
    gl.bottom_labels   = False
    gl.left_labels = False

    pcolor=ax.pcolormesh(lon,lat,datam,cmap=cmapm,vmin=vmin,vmax=vmax,shading='flat',transform=ccrs.PlateCarree())

    cbar = plt.colorbar(pcolor,orientation='horizontal',shrink=0.75, pad=0.1,label=unit)
    ax.set_title(title,size=20,y=1.08)




def one_map_noproj_nolim(fig, nx, ny, pos, data, unit, mask, cmap, title):

    datam=np.ma.array(data,mask=1-mask)
    cmapm=plt.get_cmap(cmap).copy()
    cmapm.set_bad('gray',1.)

    ax = fig.add_subplot(nx,ny,pos)

    pcolor=ax.pcolormesh(datam,cmap=cmapm)
    fig.subplots_adjust(right=0.8)

    cbar = plt.colorbar(pcolor,orientation='horizontal',shrink=0.75, pad=0.1,label=unit)
    ax.set_title(title,size=20,y=1.08)

def one_map_noproj_nolim_zoom(fig, nx, ny, pos, data, unit, mask, cmap, title,xlim1, xlim2,ylim1, ylim2):

    datam=np.ma.array(data,mask=1-mask)
    cmapm=plt.get_cmap(cmap).copy()
    cmapm.set_bad('gray',1.)

    ax = fig.add_subplot(nx,ny,pos)

    pcolor=ax.pcolormesh(datam,cmap=cmapm)
    plt.xlim(xlim1, xlim2)
    plt.ylim(ylim1, ylim2)
    fig.subplots_adjust(right=0.8)

    cbar = plt.colorbar(pcolor,orientation='horizontal',shrink=0.75, pad=0.1,label=unit)
    ax.set_title(title,size=20,y=1.08)

def sections_latitude(ax,seclat,seclon1,seclon2,data,mask,navlon,navlev,cmap,deplim,vmin,vmax,unit,title):
    datam=np.ma.array(data,mask=1-mask)
    lon=navlon[seclat,seclon1:seclon2]
    if (np.mean(np.diff(lon))<0):
        lon[np.where(lon<0)]=lon[np.where(lon<0)]+360
    pcolor=ax.pcolormesh(lon,navlev,datam[:,seclat,seclon1:seclon2],vmin=vmin,vmax=vmax,cmap=cmap)
    ax.set_ylim([0,deplim])
    ax.invert_yaxis()
    plt.xlabel('longitude °E')
    cbar = plt.colorbar(pcolor,orientation='horizontal',shrink=0.75, pad=0.1,label=unit)
    ax.set_title(title,size=20,y=1.08)

def sections_longitude(ax,seclon,seclat1,seclat2,data,mask,navlat,navlev,cmap,deplim,vmin,vmax,unit,title):
    datam=np.ma.array(data,mask=1-mask)
    lat=navlat[seclat1:seclat2,seclon]
    pcolor=ax.pcolormesh(lat,navlev,datam[:,seclat1:seclat2,seclon],vmin=vmin,vmax=vmax,cmap=cmap)
    ax.set_ylim([0,deplim])
    ax.invert_yaxis()
    plt.xlabel('latitude °N')
    cbar = plt.colorbar(pcolor,orientation='horizontal',shrink=0.75, pad=0.1,label=unit)
    ax.set_title(title,size=20,y=1.08)

def sections_latitude_nolims(ax,seclat,seclon1,seclon2,datam,navlon,navlev,cmap,deplim,unit,title):
    lon=navlon[seclat,seclon1:seclon2]
    if (np.mean(np.diff(lon))<0):
        lon[np.where(lon<0)]=lon[np.where(lon<0)]+360
    pcolor=ax.pcolormesh(lon,navlev,datam[:,seclat,seclon1:seclon2],cmap=cmap, shading='nearest')
    ax.set_ylim([0,deplim])
    ax.invert_yaxis()
    plt.xlabel('longitude °E')
    cbar = plt.colorbar(pcolor,orientation='horizontal',shrink=0.75, pad=0.1,label=unit)
    ax.set_title(title,size=20,y=1.08)

def sections_longitude_nolims(ax,seclon,seclat1,seclat2,datam,navlat,navlev,cmap,deplim,unit,title):
    lat=navlat[seclat1:seclat2,seclon]
    pcolor=ax.pcolormesh(lat,navlev,datam[:,seclat1:seclat2,seclon],cmap=cmap, shading='nearest')
    ax.set_ylim([0,deplim])
    ax.invert_yaxis()
    plt.xlabel('latitude °N')
    cbar = plt.colorbar(pcolor,orientation='horizontal',shrink=0.75, pad=0.1,label=unit)
    ax.set_title(title,size=20,y=1.08)

