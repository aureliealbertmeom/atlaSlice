#! /usr/bin/env python
import sys
import pandas as pd

def check(item, list_items, message):
    """
    Check if the given item is in the list. If not, exit the script with the provided error message.

    Parameters:
    - item: The item to check in the list.
    - list_items: The list to check for the item.
    - message: The error message to display if the item is not in the list.

    Returns:
    None
    """
    if item not in list_items:
        sys.exit(message)

def concatenate_all_names_in_list(listnames):
    """
    Concatenate names in the given list into a single string separated by '-'.

    Parameters:
    - listnames: A list of names to concatenate.

    Returns:
    str: The concatenated string of names.
    """
    if len(listnames)==1:
        allnames=listnames[0]
    elif len(listnames)==2:
        allnames=listnames[0]+'-'+listnames[1]
    elif len(listnames)>2:
        allnames=''
        lv=len(listnames)
        ll=0
        for var in listnames:
            ll+=1
            allnames=allnames+var
            if ll < lv:
                allnames=allnames+'-'
    return allnames

def duration_from_string(ffreq):
    match ffreq[-1]:
        case 'h':
            dur=pd.Timedelta(hours=int(ffreq[:-1]))
        case 'd':
            dur=pd.Timedelta(days=int(ffreq[:-1]))
        case 'm':
            dur=pd.Timedelta(months=int(ffreq[:-1]))
        case 'y':
            dur=pd.Timedelta(years=int(ffreq[:-1]))
    return dur

def maskname(vardim,filetyp):
    match vardim:
        case '2D':
            match filetyp:
                case 'gridT' | 'gridT-2D' | 'icemod' | 'flxT':
                    maskname='tmaskutil'
                case 'gridU' | 'gridU-2D':
                    maskname='umaskutil'
                case 'gridV' | 'gridV-2D':
                    maskname='vmaskutil'
        case '3D':
            match filetyp:
                case 'gridT' | 'gridW':
                    maskname='tmask'
                case 'gridU':
                    maskname='umask'
                case 'gridV':
                    maskname='vmask'

    return maskname

def tag_from_string_date(date,style):
    if style == 'aalbert_gda':
        year=pd.Timestamp(date).year
        month=pd.Timestamp(date).month
        day=pd.Timestamp(date).day
        hour=pd.Timestamp(date).hour
        mm="{:02d}".format(month)
        dd="{:02d}".format(day)
        hh="{:02d}".format(hour)
        tag='y'+str(year)+'m'+str(mm)+'d'+str(dd)+'h'+str(hh)
    return tag


