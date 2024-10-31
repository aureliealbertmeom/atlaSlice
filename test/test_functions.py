#! /usr/bin/env python
  
import sys,getopt,os
from pathlib import Path
import argparse
import pandas as pd
import shutil
import subprocess
import math as ma
import numpy as np

#Make sure the path to the package is in the PYTHONPATH
from atlas import functions as f

def test_check():
    assert f.item_in_list('toto',['toto','tutu','titi']) == True
    assert f.item_in_list('fifi',['toto','tutu','titi']) == False

def test_real_time_data2D():
    a=np.array([3600,7200,10800,21600,28800])
    b=np.array([[1,2],[5,6],[8,4],[4,6],[8,9]])
    abis=np.array([ 3600.,  7200., 10800., 14400., 18000., 21600., 25200., 28800.])
    bbis=np.array([[ 1.,  2.],[ 5.,  6.],[ 8.,  4.],[np.nan, np.nan],[np.nan, np.nan],[ 4.,  6.],[np.nan, np.nan],[ 8.,  9.]])
    a_result,b_result=f.real_time_data2D(a,b)
    np.testing.assert_array_equal(a_result, abis)
    np.testing.assert_array_equal(b_result, bbis)
    assert np.sum(a_result-abis) == 0
    assert np.nansum(b_result-bbis) == 0
   
def test_get_ind_xtrac_month_in_year():
    assert f.get_ind_xtrac_month_in_year(2009,'01','3h') == (1, 248)
    assert f.get_ind_xtrac_month_in_year(2009,'01','24h') == (1, 31)
    assert f.get_ind_xtrac_month_in_year(2009,'12','3h') == (2673, 2920)

def test_get_ind_xtrac_day_in_month():
    assert f.get_ind_xtrac_day_in_month('01','3h') == (1, 8)
    assert f.get_ind_xtrac_day_in_month('01','1h') == (1, 24)
    assert f.get_ind_xtrac_day_in_month('02','3h') == (9, 16)

def test_get_ind_xtrac_day_in_5days():
    assert f.get_ind_xtrac_day_in_5days('01','01','05','1h') == (1, 24)
    assert f.get_ind_xtrac_day_in_5days('02','01','05','1h') == (25, 48)

