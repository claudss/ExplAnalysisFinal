# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 21:02:33 2020

@author: cseid
"""

import pandas as pd

officialnames = ["DONALD J. TRUMP FOR PRESIDENT, INC.", "TRUMP MAKE AMERICA GREAT AGAIN COMMITTEE", 
                 "WARREN FOR PRESIDENT, INC.", "PETE FOR AMERICA, INC.", "PETE FOR AMERICA EXPLORATORY", 
                 "BIDEN FOR PRESIDENT", "BERNIE 2020", "TULSI NOW", "TULSI NOW INC", 
                 "FRIENDS OF ANDREW YANG", "MARIANNE WILLIAMSON FOR PRESIDENT", 
                 "WELD 2020 PRESIDENTIAL CAMPAIGN COMMITTEE, INC.", "MIKE BLOOMBERG 2020 INC", 
                 "MIKE BLOOMBERG 2020", "PETE FOR AMERICA", "WARREN FOR PRESIDENT", "KAMALA HARRIS FOR THE PEOPLE"]

geogoog = pd.read_csv("Data/google-political-ads-geo-spend.csv")
googcols = [0, 1, 2, 3]

# get google demographics
demogoog = pd.read_csv("Data/google-political-ads-campaign-targeting.csv")
#gd4cols = ['Campaign_ID', 'Age_Targeting', 'Gender_Targeting', 'Geo_Targeting_Included']
democols = [0, 1, 2, 3, 5, 6, 8, 9]
demosub = demogoog[demogoog.columns[democols]]
demogoog2 = pd.DataFrame()

for name in officialnames:
    demogoog2 = demogoog2.append(demosub[demosub['Advertiser_Name'].str.lower().str.contains(name.lower())])
    
demogoog2['Advertiser_Name'] = demogoog2['Advertiser_Name'].replace({'PETE FOR AMERICA':'PETE FOR AMERICA, INC.', 'PETE FOR AMERICA EXPLORATORY':'PETE FOR AMERICA, INC.'})
demogoog2['Advertiser_Name'] = demogoog2['Advertiser_Name'].replace({'WARREN FOR PRESIDENT':'WARREN FOR PRESIDENT, INC.'})
demogoog2['Advertiser_Name'] = demogoog2['Advertiser_Name'].replace({'TULSI NOW':'TULSI NOW INC'})
demogoog2['Advertiser_Name'] = demogoog2['Advertiser_Name'].replace({'TRUMP MAKE AMERICA GREAT AGAIN COMMITTEE':'DONALD J. TRUMP FOR PRESIDENT, INC.'})

demogoog2.to_csv("google_demographic.csv")


bigsnap = pd.concat([pd.read_csv("Data/SnapPoliticalAds_2018.csv"), pd.read_csv("Data/SnapPoliticalAds_2019.csv"), pd.read_csv("Data/SnapPoliticalAds_2020.csv")])

# get google's overall location data
googsub = geogoog[geogoog.columns[googcols]]
googsub = googsub.loc[googsub['Country'] == 'US']
googsub["Country_Subdivision_Primary"] = googsub["Country_Subdivision_Primary"].str.replace("US-", "")
googsub['Country_Subdivision_Secondary'] = googsub['Country_Subdivision_Secondary'].str.split('-').str[-1].str.strip()
googsub["Country_Subdivision_Secondary"] = googsub["Country_Subdivision_Secondary"].str.replace("AT LARGE", "0")

googsub.to_csv("google_geographic.csv")

# get particular columns from snapchat
#snapcols = ['OrganizationName', 'Spend', 'Impressions', 'Gender', 'AgeBracket', 'Regions(Included)', 'Interests', 'Advanced Demographics']
snapcols = [3, 4, 5, 6, 7, 10, 11, 12, 14, 26, 30]
snapsub = bigsnap[bigsnap.columns[snapcols]]
snapsub2 = pd.DataFrame()

for name in officialnames:
    snapsub2 = snapsub2.append(snapsub[snapsub['PayingAdvertiserName'].str.lower().str.contains(name.lower())])
    
snapsub2['PayingAdvertiserName'] = snapsub2['PayingAdvertiserName'].replace({'PETE FOR AMERICA':'PETE FOR AMERICA, INC.', 'PETE FOR AMERICA EXPLORATORY':'PETE FOR AMERICA, INC.'})
snapsub2['PayingAdvertiserName'] = snapsub2['PayingAdvertiserName'].replace({'WARREN FOR PRESIDENT':'WARREN FOR PRESIDENT, INC.'})
snapsub2['PayingAdvertiserName'] = snapsub2['PayingAdvertiserName'].replace({'TULSI NOW':'TULSI NOW INC'})
snapsub2['PayingAdvertiserName'] = snapsub2['PayingAdvertiserName'].replace({'TRUMP MAKE AMERICA GREAT AGAIN COMMITTEE':'DONALD J. TRUMP FOR PRESIDENT, INC.'})



snapsub2.to_csv("snapchat_demographic.csv")
