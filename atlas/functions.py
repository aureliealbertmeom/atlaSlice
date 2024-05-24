#! /usr/bin/env python
import sys
import pandas as pd
import numpy as np
import shutil
import subprocess
import calendar

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
    if not item_in_list(item,list_items):
        sys.exit(message)

def item_in_list(item,list_items):
    """
    Check if the given item is in the list.
    Return True or False

    Parameters:
    - item: The item to check in the list.
    - list_items: The list to check for the item.

    Returns:
    Boolean
    """
    if item not in list_items:
        return False
    else:
        return True


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
                case 'gridT' | 'gridT-2D' | 'icemod' | 'flxT' | 'domain_noisf_v2_4.2':
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

def __build_colormap__(MC, log_ctrl=0, exp_ctrl=0):

    import matplotlib.colors as mplc

    [ nc, n3 ] = np.shape(MC)

    # Make x vector :
    x =[]
    for i in range(nc): x.append(255.*float(i)/((nc-1)*255.0))
    x = np.array(x)
    if log_ctrl > 0: x = np.log(x + log_ctrl)
    if exp_ctrl > 0: x = np.exp(x * exp_ctrl)
    rr = x[nc-1] ; x  = x/rr

    y =np.zeros(nc)
    for i in range(nc): y[i] = x[nc-1-i]

    x = 1 - y ; rr = x[nc-1] ; x  = x/rr

    vred  = [] ; vblue = [] ; vgreen = []

    for i in range(nc):
        vred.append  ([x[i],MC[i,0],MC[i,0]])
        vgreen.append([x[i],MC[i,1],MC[i,1]])
        vblue.append ([x[i],MC[i,2],MC[i,2]])

    cdict = {'red':vred, 'green':vgreen, 'blue':vblue}

    my_cm = mplc.LinearSegmentedColormap('my_colormap',cdict,256)

    return my_cm

def home_made_cmap(name):
    match name:
        case 'on3':
            M = np.array( [
                [ 0.,0.,0. ],               # noir
                [ 0.,138./255.,184./255. ], # bleu
                [ 1.,1.,1. ],               # blanc
                [ 1.,237./255.,0 ],         # jaune
            ] )
        case 'on2':
            M = np.array( [
                [ 0.,0.,0. ],               # noir
                [ 0.,138./255.,184./255. ], # bleu
                [ 1.,1.,1. ],               # blanc
            ] )

    my_cmap = __build_colormap__(M, log_ctrl=0, exp_ctrl=0)
    return my_cmap

def real_time_data2D(time,var):
    """
    From an interrupted time vector and an associated 2D variable
    return a continuous time vector and the associated 2D variable 
    filled with Nan values where data is missing

    Parameters:
    - time: a time vector (not a datetime)
    - var: a 2D field with one dimension being identical to time

    Returns:
    Bigger time and var arrays 
    """
    if np.ndim(var) != 2: print('ERROR in size var is not 2D');  sys.exit(0)
    (d1,d2)=np.shape(var)
    if len(time) != d1: print('ERROR in size length of time vector and variable does not match'); sys.exit(0)
    tinit=time[0]
    tend=time[-1]
    nbh=int((tend-tinit)/3600)+1
    real_time=np.zeros((nbh))
    real_var=np.zeros((nbh,d2))
    ind=0
    for t in np.arange(nbh):
        tt=tinit+t*3600
        if time[ind] == tt:
            real_time[t]=time[ind]
            real_var[t,:]=var[ind,:]
            ind=ind+1
        else:
            real_time[t]=tt
            real_var[t,:]=np.nan*np.ones((1,d2))

    return real_time,real_var

def use_template(tempname, scriptname, dict_strings_values):
    """
    Copy a template script and replace a list of strings by chosen arguments in it
    Parameters :
     - name of the template script
     - name of the resulting script
     - a dictionary that match default string and the corresponding value we want to replace it
    Returns :
    None
    """
    shutil.copyfile(tempname,scriptname)
    for string in dict_strings_values:
        subprocess.call(["sed", "-i", "-e",  's%'+str(string)+'%'+str(dict_strings_values[string])+'%g',scriptname])

def get_ind_xtrac_month_in_year(year, month, freq):
    """
    Get the temporal indexes bounding a given month for a yearly file with a given freqency of output
    Parameters :
      - year
      - month
      - frequency of the time axis
    Returns :
      - ti and tf the bounding indexes for the month considered
    """
    if calendar.isleap(int(year)):
        nb_day_in_month=[31,29,31,30,31,30,31,31,30,31,30,31]
    else:
        nb_day_in_month=[31,28,31,30,31,30,31,31,30,31,30,31]

    nb_per_day=int(24/int(freq[:-1]))
    m=int(month)
    mm1=m-1
    if mm1==0:
        ti=1
        tf=31*nb_per_day
    else:
        tt=1
        while mm1 > 0:
            tt=tt+nb_per_day*nb_day_in_month[mm1-1]
            mm1=mm1-1
        ti=tt
        tf=tt+nb_per_day*nb_day_in_month[m-1]-1

    return ti,tf

def get_ind_xtrac_day_in_month(day, freq):
    """
    Get the temporal indexes bounding a given day for a monthly file with a given freqency of output
    Parameters :
      - day
      - frequency of the time axis
    Returns :
      - ti and tf the bounding indexes for the day considered
    """

    nb_per_day=int(24/int(freq[:-1]))
    d=int(day)
    ti=(d-1)*nb_per_day+1
    tf=d*nb_per_day

    return ti,tf
