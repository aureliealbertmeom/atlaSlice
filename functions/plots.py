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
import matplotlib.dates as md
import matplotlib.path as mpath
theta = np.linspace(0, 2*np.pi, 100)
map_circle = mpath.Path(np.vstack([np.sin(theta), np.cos(theta)]).T * 0.5 + [0.5, 0.5])

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
#    cmapm.set_bad('gray',1.)

    projection=ccrs.Orthographic(central_latitude=cen_lat, central_longitude=cen_lon)
    ax = fig.add_subplot(nx,ny,pos,projection=projection)

#    gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='k', zorder=3)
#    gl.top_labels   = False
#    gl.right_labels = False
#    gl.bottom_labels   = False
#    gl.left_labels = False

    pcolor=ax.pcolormesh(lon,lat,datam,cmap=cmapm,vmin=vmin,vmax=vmax,transform=ccrs.PlateCarree())

    cbar = plt.colorbar(pcolor,orientation='horizontal',shrink=0.75, pad=0.1,label=unit)
    ax.set_title(title,size=20,y=1.08)

def one_map_proj_mollweide_global(fig, nx, ny, pos, lon, lat, data, unit, mask, cmap, vmin, vmax, title):

    datam=np.ma.array(data,mask=1-mask)
    cmapm=plt.get_cmap(cmap).copy()
    cmapm.set_bad('gray',1.)

    projection=ccrs.Mollweide()
    ax = fig.add_subplot(nx,ny,pos,projection=projection)

#    gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='k', zorder=3)
#    gl.top_labels   = False
#    gl.right_labels = False
#    gl.bottom_labels   = False
#    gl.left_labels = False

    pcolor=ax.pcolormesh(lon,lat,datam,cmap=cmapm,vmin=vmin,vmax=vmax,transform=ccrs.PlateCarree())

    cbar = plt.colorbar(pcolor,orientation='horizontal',shrink=0.75, pad=0.1,label=unit)
    ax.set_title(title,size=20,y=1.08)

def one_map_proj_south_stereo(fig, nx, ny, pos, lon, lat, data, unit, mask, cmap, vmin, vmax, title):

    datam=np.ma.array(data,mask=1-mask)
    cmapm=plt.get_cmap(cmap).copy()
#    cmapm.set_bad('gray',1.)

    projection=ccrs.SouthPolarStereo()
    ax = fig.add_subplot(nx,ny,pos,projection=projection)

    ax.set_extent([-180, 180, -90, -60], ccrs.PlateCarree())

    gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='k', zorder=3)
    gl.top_labels   = False
    gl.right_labels = False
    gl.bottom_labels   = False
    gl.left_labels = False

    pcolor=ax.pcolormesh(lon,lat,datam,cmap=cmapm,vmin=vmin,vmax=vmax,transform=ccrs.PlateCarree())

    cbar = plt.colorbar(pcolor,orientation='horizontal',shrink=0.75, pad=0.1,label=unit)
    ax.set_title(title,size=20,y=1.08)

def one_map_proj_north_stereo(fig, nx, ny, pos, lon, lat, data, unit, mask, cmap, vmin, vmax, title):

    datam=np.ma.array(data,mask=1-mask)
    cmapm=plt.get_cmap(cmap).copy()
    cmapm.set_bad('gray',1.)

    projection=ccrs.NorthPolarStereo()
    ax = fig.add_subplot(nx,ny,pos,projection=projection)

    ax.set_extent([-180, 180, 60, 90], ccrs.PlateCarree())

    gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='k', zorder=3)
    gl.top_labels   = False
    gl.right_labels = False
    gl.bottom_labels   = False
    gl.left_labels = False

    pcolor=ax.pcolormesh(lon,lat,datam,cmap=cmapm,vmin=vmin,vmax=vmax,transform=ccrs.PlateCarree())

    cbar = plt.colorbar(pcolor,orientation='horizontal',shrink=0.75, pad=0.1,label=unit)
    ax.set_title(title,size=20,y=1.08)

def one_map_proj_plate_carree_zoom(fig, nx, ny, pos, lon, lat, data, unit, mask, cmap, vmin, vmax, title, xlim1, xlim2, ylim1, ylim2):

    datam=np.ma.array(data,mask=1-mask)
    cmapm=plt.get_cmap(cmap).copy()
    cmapm.set_bad('gray',1.)

    projection=ccrs.PlateCarree(central_longitude=0)
    ax = fig.add_subplot(nx,ny,pos,projection=projection)

    ax.set_extent([xlim1, xlim2, ylim1, ylim2], ccrs.PlateCarree())

    gl = ax.gridlines(draw_labels=True, linewidth=0.5, color='k', zorder=3)
    gl.top_labels   = True
    gl.right_labels = True
    gl.bottom_labels   = True
    gl.left_labels = True

    pcolor=ax.pcolormesh(lon,lat,datam,cmap=cmapm,vmin=vmin,vmax=vmax,transform=ccrs.PlateCarree())
    fig.subplots_adjust(right=0.8)

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

def plot_time_series(fig,time,var,unit,title):
    ax = fig.add_subplot(111)
    plt.plot(time,var,color='darkblue', marker='+', linestyle='dashed',linewidth=2, markersize=4)
    plt.ylabel(unit)
    ax.set_title(title,size=20,y=1.08)
    plt.xticks( rotation=25 )
    xfmt = md.DateFormatter('%Y-%m-%d %H')
    ax.xaxis.set_major_formatter(xfmt)

def plot_time_series_min_max(fig,time,mean_var,min_var,max_var,unit,title):
    ax = fig.add_subplot(311)
    plt.plot(time,mean_var,color='darkblue', marker='.', linestyle='solid',linewidth=1, markersize=4)
    plt.ylabel(unit)
    ax.set_title(title,size=20,y=1.08)
    plt.xticks( rotation=25 )
    xfmt = md.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(xfmt)
    ax = fig.add_subplot(313)
    plt.plot(time,min_var,color='darkblue', marker='.', linestyle='solid',linewidth=1, markersize=4)
    plt.ylabel(unit)
    plt.xticks( rotation=25 )
    xfmt = md.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(xfmt)
    ax = fig.add_subplot(312)
    plt.plot(time,max_var,color='darkblue', marker='.', linestyle='solid',linewidth=1, markersize=4)
    plt.ylabel(unit)
    plt.xticks( rotation=25 )
    xfmt = md.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(xfmt)

def plot_hovmuller_lon(fig,time,lon,var,vmin,vmax,unit,cmap,title):
    ax = fig.add_subplot(111)
    lon0=lon
    if (np.mean(np.diff(lon))<0):
        lon[np.where(lon<0)]=lon[np.where(lon<0)]+360
    pcolor=ax.pcolormesh(lon,time,var,cmap=cmap,vmin=vmin,vmax=vmax, shading='nearest')
    ax.invert_yaxis()
    plt.xlabel('longitude °E')
    xfmt = md.DateFormatter('%Y-%m-%d')
    ax.yaxis.set_major_formatter(xfmt)
    locs, labels = plt.xticks()  
    print('locs = ',locs)
    print('labels = ',labels)
    new_labels=labels
    for ind in np.arange(len(locs)):
        print(locs[ind])
        if locs[ind] > 180.:
            new_labels[ind]=locs[ind]-360
        else:
            new_labels[ind]=locs[ind]
    print('new labels = ',new_labels)
    ax.set_xticks(locs) # choose which x locations to have ticks
    ax.set_xticklabels(new_labels)
    cbar = plt.colorbar(pcolor,orientation='vertical',shrink=0.75, pad=0.1,label=unit)
    ax.set_title(title,size=20,y=1.08)

def plot_hovmuller_lat(fig,time,lat,var,vmin,vmax,unit,cmap,title):
    ax = fig.add_subplot(111)
    pcolor=ax.pcolormesh(time,lat,var,cmap=cmap,vmin=vmin,vmax=vmax, shading='nearest')
    plt.ylabel('latitude °N')
    plt.xticks( rotation=25 )
    xfmt = md.DateFormatter('%Y-%m-%d')
    ax.xaxis.set_major_formatter(xfmt)
    cbar = plt.colorbar(pcolor,orientation='horizontal',shrink=0.75, pad=0.1,label=unit)
    ax.set_title(title,size=20,y=1.08)

def plot_zy(fig,dep,lat,var,vmin,vmax,unit,cmap,title):
    ax = fig.add_subplot(111)
    fig.set_frameon('False')
    pcolor=ax.pcolormesh(lat,dep,var,cmap=cmap,vmin=vmin,vmax=vmax, shading='nearest')
    #pcolor=ax.contourf(lat,dep,var,levels=np.arange(vmin,vmax,5),cmap=cmap)
    ax.invert_yaxis()
    plt.xlabel('latitude °N')
    plt.ylabel('depth in m')
    cbar = plt.colorbar(pcolor,orientation='horizontal',shrink=0.75, pad=0.1,label=unit)
    ax.set_title(title,size=20,y=1.08)

