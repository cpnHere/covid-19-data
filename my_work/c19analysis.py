#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
********************************************
Created on Sat Mar 28 08:48:42 2020
by
Chamara Rajapakshe
(cpn.here@umbc.edu)
********************************************

"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import timedelta
import os
import cpnCommonlib as cpn
def savefig(fig,fig_ttl,path=None,rp=False):
    '''
    fig: Figure object matplotlib.figure.Figure
    fig_ttl: figure title string (some special characters will be removed from the file name)
    '''
    for ch in [' ','[',']']:
        if ch in fig_ttl:
            fig_ttl=fig_ttl.replace(ch,'_')
    fig_ttl=fig_ttl.replace('.','p')
    if path==None:
        filename=fig_ttl
    else:
        filename=path+fig_ttl
    if not(rp):
        if os.path.isfile(filename+'.png'):
            usr=input('Replace existing file?: ')
            if usr=='y':
                rp=True
        else:
            rp=True
    if rp:
        fig.savefig(filename+'.png', format='png', dpi=200)
        print(filename+'.png SAVED.')
def plot_counties(fips,fig1,ax1,lns='.-',alpha=0.5):
    for cnty in fips.keys():
        county = data.groupby('fips').get_group(fips[cnty])
        if cnty != county['county'].get_values()[0]:
            print('County name incompatibility!!!'+cnty)
        else:
            
            ax1.plot(pd.to_datetime(county['date']),county['cases'],lns,label=county['county'].get_values()[0],alpha=alpha)
            
        
    ax1.tick_params(axis='x',labelrotation=90)
    ax1.set_yscale('log')
    ax1.grid(which='both')
    return fig1,ax1
def plot_NYCity(fig1,ax1,daydelta=0):
    #st_date=pd.to_datetime('03/01/2020')
    #en_date=pd.to_datetime('03/18/2020')
    nyc = data.groupby('county').get_group('New York City')
    nyc['date']=pd.to_datetime(nyc['date'])
    #mask=(nyc['date']>st_date)&(nyc['date']<=en_date)
    #nyc_blast=nyc.loc[mask]
    delta=timedelta(days=daydelta)
    ax1.plot(nyc['date']+delta,nyc['cases'],'r--',alpha=0.5,label='NY+%ddays'%daydelta)
def plot_WashState(fig1,ax1,daydelta=0):
    st_date=pd.to_datetime('02/22/2020')
    wash = data_st.groupby('state').get_group('Washington')
    wash['date']=pd.to_datetime(wash['date'])
    mask=(wash['date']>st_date)
    wash_blast=wash.loc[mask]
    delta=timedelta(days=daydelta)
    ax1.plot(wash_blast['date']+delta,wash_blast['cases'],'b--',alpha=0.5,label='WA(st.)+%ddays'%daydelta)
def plot_State(fig1,ax1,state,daydelta=0):
    wash = data_st.groupby('state').get_group(state)
    wash['date']=pd.to_datetime(wash['date'])
    delta=timedelta(days=daydelta)
    ax1.plot(wash['date']+delta,wash['cases'],label=state+'+%ddays'%daydelta)
def confirmed_cases_vs_increase(data,cnty,fips,fig3,ax3,clr='k',lns='-',moving_window=1):
    '''
    moving_window=1 # change to consider moving average
    '''
    if np.isnan(fips):
        county =data.groupby('county').get_group('New York City')
    else:
        county = data.groupby('fips').get_group(fips)
    county['date']=pd.to_datetime(county['date'])
    x = county['cases'].to_numpy()   
    incr = x[1:]-x[0:-1]
    incr = np.append(0,incr)
    county['increase']=incr
    #ax3.plot(county['cases'],county['increase'],clr+lns,label=cnty)
    ax3.plot(cpn.movingaverage(county['cases'],moving_window),cpn.movingaverage(county['increase'],moving_window),clr+lns,label=cnty)

    #ax3.plot(county['cases'].array[-7],county['increase'].array[-7],clr+'^',label='-7days')
    #day7x=county['cases'].array[-8]
    #day7y=county['increase'].array[-8]
    #ax3.annotate('-7 days',xy=(day7x,day7y), xytext=(day7x,2),size=12,color=clr,arrowprops=dict(arrowstyle='->',color=clr))
    ax3.set_xscale('log')
    ax3.set_yscale('log')
def confirmed_cases_vs_increase_state(data_st,state,fig3,ax3,clr='k',lns='-',moving_window=1):
    '''
    moving_window=1 # change to consider moving average
    '''
    county = data_st.groupby('state').get_group(state)
    county['date']=pd.to_datetime(county['date'])
    x = county['cases'].to_numpy()   
    incr = x[1:]-x[0:-1]
    incr = np.append(0,incr)
    county['increase']=incr
    #ax3.plot(county['cases'],county['increase'],clr+lns,label=state+'(state)')
    if state == 'Washington':
        ax3.plot(cpn.movingaverage(county['cases'],moving_window),cpn.movingaverage(county['increase'],moving_window),clr+lns,label=state+'(state)')
    else:
        ax3.plot(cpn.movingaverage(county['cases'],moving_window),cpn.movingaverage(county['increase'],moving_window),clr+lns,label=state)
    #day7x=county['cases'].array[-8]
    #day7y=county['increase'].array[-8]
    #ax3.annotate('-7 days',xy=(day7x,day7y), xytext=(day7x,2),size=12,color=clr,arrowprops=dict(arrowstyle='->',color=clr))
    ax3.set_xscale('log')
    ax3.set_yscale('log')   
def confirmed_cases_vs_increase_US(data_st,ax3,moving_window=1):
    '''
    moving_window=1 # change to consider moving average
    '''
    us_cum_cases=np.array([])
    #us_cum_deaths=np.array([])
    for dt in data_st['date'].unique():
        us_cum_cases = np.append(us_cum_cases,data_st.groupby('date').get_group(dt)['cases'].sum())
        #us_cum_deaths = np.append(us_cum_deaths,data_st.groupby('date').get_group(dt)['deaths'].sum())
    incr = us_cum_cases[1:]-us_cum_cases[0:-1]
    incr = np.append(0,incr)
    #incrd = us_cum_deaths[1:]-us_cum_deaths[0:-1]
    #incrd = np.append(0,incrd)
    #ax3.plot(us_cum_cases,incr,'.-',color='grey',label='US total')
    ax3.plot(cpn.movingaverage(us_cum_cases,moving_window),cpn.movingaverage(incr,moving_window),'.-',color='grey',label='US total')
    #ax3.plot(us_cum_deaths,incrd,'^',color='grey',alpha=0.5,label='US (deaths vs. cases)')

if __name__=='__main__':
    today = pd.to_datetime('07/30/2020')
    filename = 'us-counties_0730.csv'
    fnamesta = 'us-states_0730.csv'
    data=pd.read_csv(filename,error_bad_lines=False)
    data_st=pd.read_csv(fnamesta,error_bad_lines=False)
    OH_sur = {'Lorain':39093,'Medina':39103,'Summit':39153,'Portage':39133,'Geauga':39055,'Lake':39085}
    our_sur ={'Harford':24025,'Baltimore city':24510,	'Carroll':24013,'Howard':24027,'Anne Arundel':24003,'York':42133,'Montgomery':24031} #York in PA
    
    
    #Cuyahoga
    fig1,ax1 = plt.subplots()
    fig1_ttl = filename.split('.',1)[0]+'_Cuyahoga'
    plot_counties(OH_sur,fig1,ax1)
    plot_counties({'Cuyahoga':39035},fig1,ax1,'k.-',alpha=1)
    plot_counties({'Baltimore':24005},fig1,ax1,'k.--')
    plot_NYCity(fig1,ax1,daydelta=8)
    plot_WashState(fig1,ax1,daydelta=14)
    #ax1.plot(pd.to_datetime('03/31/2020'),527,'k*',label='Today')
    ax1.legend()
    fig1.suptitle(fig1_ttl)
    #ax1.set_yscale('linear')
    fig1.tight_layout(rect=[0,0,1,0.98]);savefig(fig1,fig1_ttl);
    fig1.show()
    
    #Baltimore
    fig2,ax2 = plt.subplots()
    fig2_ttl = filename.split('.',1)[0]+'_Baltimore'
    plot_counties(our_sur,fig2,ax2)
    plot_counties({'Baltimore':24005},fig2,ax2,'k.-',alpha=1)
    plot_counties({'Cuyahoga':39035},fig2,ax2,'k.--',alpha=0.5)
    plot_NYCity(fig2,ax2,daydelta=10)
    plot_WashState(fig2,ax2,daydelta=16)
    #ax2.plot(pd.to_datetime('03/31/2020'),227,'k*',label='Today')
    ax2.legend()
    fig2.suptitle(fig2_ttl)
    fig2.tight_layout(rect=[0,0,1,0.98]);savefig(fig2,fig2_ttl);
    fig2.show()
    
    #Containment (Summit)
    fig3,ax3 = plt.subplots(figsize=(12,5))
    fig3_ttl = str(today.date())+'_containment_test'
    confirmed_cases_vs_increase(data,'Summit',39153,fig3,ax3,clr='c',lns='.-')
    confirmed_cases_vs_increase(data,'Cuyahoga',39035,fig3,ax3,clr='k',lns='.-')
    confirmed_cases_vs_increase(data,'New York City',np.nan,fig3,ax3,clr='r',lns='.--')
    confirmed_cases_vs_increase_state(data_st,'Washington',fig3,ax3,clr='b',lns='.--')
    confirmed_cases_vs_increase_US(data_st,ax3)
    ax3.axvline(16.5e6,ls=':',color='grey')
    ax3.annotate('2018/19 flu cases (reported to health providers)',xy=(17e6,2),color='grey',rotation=90)
    ax3.set_xlabel('confirmed cases')
    ax3.set_ylabel('daily increase')
    ax3.legend()
    fig3.suptitle(fig3_ttl)
    fig3.tight_layout(rect=[0,0,1,0.98])
    fig3.show()
    savefig(fig3,fig3_ttl)
    
    #Containment (Baltimore)
    fig3,ax3 = plt.subplots(figsize=(12,5))
    fig3_ttl = str(today.date())+'_containment_test_2'
    confirmed_cases_vs_increase(data,'Baltimore',24005,fig3,ax3,clr='c',lns='.-')
    confirmed_cases_vs_increase(data,'Cuyahoga',39035,fig3,ax3,clr='k',lns='.-')
    confirmed_cases_vs_increase(data,'New York City',np.nan,fig3,ax3,clr='r',lns='.--')
    confirmed_cases_vs_increase_state(data_st,'Washington',fig3,ax3,clr='b',lns='.--')
    confirmed_cases_vs_increase_US(data_st,ax3)
    ax3.axvline(16.5e6,ls=':',color='grey')
    ax3.annotate('2018/19 flu cases (reported to health providers)',xy=(17e6,2),color='grey',rotation=90)
    ax3.set_xlabel('confirmed cases')
    ax3.set_ylabel('daily increase')
    ax3.legend()
    fig3.suptitle(fig3_ttl)
    fig3.tight_layout(rect=[0,0,1,0.98])
    fig3.show()
    savefig(fig3,fig3_ttl)
    
    
    #States
    fig4,ax4 = plt.subplots()
    fig4_ttl = fnamesta.split('.',1)[0]
    st_list = ['Tennessee', 'Ohio', 'South Carolina', 'North Carolina', 'Illinois', 'Iowa', 'Texas', 'Georgia', 'Indiana','Arkansas']
    for stt in st_list:
        plot_State(fig4,ax4,stt)
    ax4.tick_params(axis='x',labelrotation=90)
    ax4.set_yscale('log')
    ax4.grid(which='both')
    ax4.legend()
    fig4.suptitle(fig4_ttl)
    fig4.tight_layout(rect=[0,0,1,0.98])
    savefig(fig4,fig4_ttl)
    fig4.show()



