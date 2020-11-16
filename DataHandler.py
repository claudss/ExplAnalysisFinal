# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 14:48:10 2020

@author: cseid
"""

import pandas as pd
import numpy as np

#first order of business: acquire all data from its various CSV file sources
#we also extract certain columns from each CSV so we only have to deal with the most pertinent information

snapdata18 = pd.read_csv("Data/SnapPoliticalAds_2018.csv")
snapdata19 = pd.read_csv("Data/SnapPoliticalAds_2019.csv")
snapdata20 = pd.read_csv("Data/SnapPoliticalAds_2020.csv")
bigsnap = pd.concat([snapdata18, snapdata19, snapdata20])

#snapcols = ['OrganizationName', 'Spend', 'Impressions', 'Gender', 'AgeBracket', 'Regions(Included)', 'Interests', 'Advanced Demographics']
snapcols = [3, 4, 5, 6, 7, 10, 11, 12, 14, 26, 30]
snapsub = bigsnap[bigsnap.columns[snapcols]]

googledata1 = pd.read_csv("Data/google-political-ads-creative-stats.csv")
googledata2 = pd.read_csv("Data/google-political-ads-advertiser-stats.csv")

#gd1cols = ['Advertiser_Name', 'Advertiser_ID', 'Date_Range_Start', 'Date_Range_End', 'Impressions', 'Spend_USD']
gd1cols = [4, 5, 7, 8, 9, 10, 11]
gd1sub = googledata1[googledata1.columns[gd1cols]]

# MONEY RELATED
#gd2cols = ['Regions', 'Total_Creatives', 'Spend_USD', 'Advertiser_ID', 'Advertiser_Name']
gd2cols = [0, 1, 3, 5, 6]
gd2sub = googledata2[googledata2.columns[gd2cols]]


facebookdata = pd.read_csv("Data/FacebookData.csv")
fbcols = [2, 3, 4]
fbsub = facebookdata[facebookdata.columns[fbcols]]

officialnames = ["DONALD J. TRUMP FOR PRESIDENT, INC.", "TRUMP MAKE AMERICA GREAT AGAIN COMMITTEE", 
                 "WARREN FOR PRESIDENT, INC.", "PETE FOR AMERICA, INC.", "PETE FOR AMERICA EXPLORATORY", 
                 "BIDEN FOR PRESIDENT", "BERNIE 2020", "TULSI NOW", "TULSI NOW INC", 
                 "FRIENDS OF ANDREW YANG", "MARIANNE WILLIAMSON FOR PRESIDENT", 
                 "WELD 2020 PRESIDENTIAL CAMPAIGN COMMITTEE, INC.", "MIKE BLOOMBERG 2020 INC", 
                 "MIKE BLOOMBERG 2020", "PETE FOR AMERICA", "WARREN FOR PRESIDENT", "KAMALA HARRIS FOR THE PEOPLE"]

spending_goog = pd.DataFrame()
spending_snap = pd.DataFrame()
spending_fb = pd.DataFrame()
impressions_goog = pd.DataFrame()
for name in officialnames:
    spending_goog = spending_goog.append(gd2sub[gd2sub['Advertiser_Name'].str.lower().str.contains(name.lower())])
    impressions_goog = impressions_goog.append(gd1sub[gd1sub['Advertiser_Name'].str.lower().str.contains(name.lower())])
    #spending_snap = spending_snap.append(snapsub[snapsub['OrganizationName'].str.lower().str.contains(name.lower())]) 
    spending_snap = spending_snap.append(snapsub[snapsub['PayingAdvertiserName'].str.lower().str.contains(name.lower())]) 
    spending_fb = spending_fb.append(fbsub[fbsub['Disclaimer'].str.lower() == name.lower()]) 

impressions_goog.drop_duplicates(keep='first', inplace=True)
spending_goog.drop_duplicates(keep='first', inplace=True)
spending_snap.drop_duplicates(keep='first', inplace=True)
spending_fb.drop_duplicates(keep='first', inplace=True)

# create impressions csv for google data - edit all committee names to be consistent
impressions_goog['Advertiser_Name'] = impressions_goog['Advertiser_Name'] .replace({'PETE FOR AMERICA':'PETE FOR AMERICA, INC.', 'PETE FOR AMERICA EXPLORATORY':'PETE FOR AMERICA, INC.'})
impressions_goog['Advertiser_Name']  = impressions_goog['Advertiser_Name'] .replace({'WARREN FOR PRESIDENT':'WARREN FOR PRESIDENT, INC.'})
impressions_goog['Advertiser_Name']  = impressions_goog['Advertiser_Name'] .replace({'TULSI NOW':'TULSI NOW INC'})
impressions_goog['Advertiser_Name']  = impressions_goog['Advertiser_Name'] .replace({'TRUMP MAKE AMERICA GREAT AGAIN COMMITTEE':'DONALD J. TRUMP FOR PRESIDENT, INC.'})
impressions_goog.to_csv("google_impressions.csv")

# organize google spending data into our uniform format
spending_goog['Advertiser_Name'] = spending_goog['Advertiser_Name'].str.upper()
spending_goog1 = spending_goog.groupby('Advertiser_Name', as_index=False).sum()
spending_snap1 = spending_snap.groupby('PayingAdvertiserName', as_index=False).sum()
spending_goog1 = spending_goog1.append(['Impressions', 'App'])
spending_goog1['App'] = 'Google'
spending_goog1['Impressions'] = np.nan
spending_goog1 = spending_goog1[['Advertiser_Name', 'Spend_USD', 'Impressions', 'Total_Creatives', 'App']]
spending_goog1.columns =  ['Organization', 'Spent', 'Impressions', 'AdTotal', 'App']

# organize snapchat spending data
spending_snap = spending_snap.reset_index()
spending_snap = spending_snap.drop(columns= ['index'])

# count how many advertisements by each candidate we see
snapcount = spending_snap.groupby('PayingAdvertiserName')['PayingAdvertiserName'].transform('count')
adname = []
for index in snapcount.index:
    adname.append(spending_snap.iloc[index, 5])
snapcount['AdName'] = adname
snapcount.drop_duplicates(keep='first', inplace=True)
snapcount = snapcount.reset_index()
snapcount = snapcount.drop(columns= ['index', 'AdName'])

# set up snapchat information in our uniform format
spending_snap1['PayingAdvertiserName'] = spending_snap1['PayingAdvertiserName'].str.upper()
spending_snap1['Count'] = snapcount
spending_snap1['App'] = 'Snapchat'
spending_snap1.columns =  ['Organization', 'Spent', 'Impressions', 'AdTotal', 'App']

#due to case differences, everything must be made consistent/uppercase in the Disclaimer section of FB data
spending_fb['Disclaimer'] = spending_fb['Disclaimer'].str.upper() 
spending_fb['Amount Spent (USD)'] = pd.to_numeric(spending_fb['Amount Spent (USD)'])
spending_fb['Number of Ads in Library'] = pd.to_numeric(spending_fb['Number of Ads in Library'])
spending_fb1 = spending_fb.groupby('Disclaimer', as_index=False).sum()
spending_fb1 = spending_fb1.append(['Impressions', 'App'])
spending_fb1['App'] = 'Facebook'
spending_fb1['Impressions'] = np.nan
spending_fb1 = spending_fb1[['Disclaimer', 'Amount Spent (USD)', 'Impressions', 'Number of Ads in Library', 'App']]
spending_fb1.columns =  ['Organization', 'Spent', 'Impressions', 'AdTotal', 'App']

# we drop duplicates again to make sure no extra ads are counted
spending_goog1.drop_duplicates(keep='first', inplace=True)
spending_goog1 = spending_goog1.dropna(subset=['Organization'])
spending_snap1.drop_duplicates(keep='first', inplace=True)
spending_fb1.drop_duplicates(keep='first', inplace=True)
spending_fb1 = spending_fb1[:-1]

# spending, count, and impressions CSVs created
spendcsv = pd.DataFrame(columns = ['Organization', 'Spent', 'Impressions', 'AdTotal', 'App'])

spendcsv = pd.concat([spending_goog1, spending_snap1, spending_fb1])
spendcsv['Organization'] = spendcsv['Organization'].replace({'PETE FOR AMERICA':'PETE FOR AMERICA, INC.', 'PETE FOR AMERICA EXPLORATORY':'PETE FOR AMERICA, INC.'})
spendcsv['Organization'] = spendcsv['Organization'].replace({'WARREN FOR PRESIDENT':'WARREN FOR PRESIDENT, INC.'})
spendcsv['Organization'] = spendcsv['Organization'].replace({'TULSI NOW':'TULSI NOW INC'})
spendcsv['Organization'] = spendcsv['Organization'].replace({'TRUMP MAKE AMERICA GREAT AGAIN COMMITTEE':'DONALD J. TRUMP FOR PRESIDENT, INC.'})
spendcsv.to_csv("ad_spending.csv")
