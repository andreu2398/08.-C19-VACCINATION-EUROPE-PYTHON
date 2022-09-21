# -*- coding: utf-8 -*-
"""
Created on Thu Sep  9 17:35:28 2021

@author: Andreu
"""

"""
ANALYSIS OF COVID VACCINATION IN EUROPE
"""

#%% Packages, Downloading data & Importing it

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.impute import SimpleImputer
import urllib.request
import webbrowser
import datetime

"""urllib.request.urlretrieve(url = "https://opendata.ecdc.europa.eu/covid19/vaccine_tracker/csv/data.csv" , filename = "downloaded.csv")
urllib.request.urlretrieve(url = "https://www.ecdc.europa.eu/sites/default/files/documents/Variable_Dictionary_VaccineTracker-20-08-2021.pdf" , filename = "variable_dictionary.pdf")
"""
df = pd.read_csv("downloaded.csv")
"""webbrowser.open_new(r'variable_dictionary.pdf')
"""


#%% How many first jabs were supplied in Spain from th 2nd to the 15th of August 2021?

aa = df.filter(["YearWeekISO" , "FirstDose" , "Region" , "TargetGroup"])

aa = aa[(aa.Region == "ES")]
aa = aa.loc[(aa.TargetGroup == "ALL") | (aa.TargetGroup == "Age<18")]
aa = aa.loc[(aa.YearWeekISO == "2021-W32") | (aa.YearWeekISO == "2021-W33")]
aa = aa.FirstDose.sum()

print("Between the 2nd and the 15th of August (32nd and 33rd week of the year 2021), "
      , aa ,
      " doses were supplied in Spain.")

"""
Not necessary but useful:
aa = aa[(aa.ReportingCountry == "ES") & (aa.YearWeekISO == "2021-W02")]
aa[["Year" , "Week"]] = aa.YearWeekISO.str.split('-' , expand = True)
aa = aa[(aa.Year == "2021")]
aa["Week"] = aa.Week.str.replace("W" , "")
aa["Week"] = pd.to_numeric(aa["Week"])
aa["Year"] = pd.to_numeric(aa["Year"])
"""

#%% What has been being the population of Spain in the different weeks?

aa = df.filter(["YearWeekISO" , "Region" , "Population"])

aa = aa[(aa.Region == "ES")].reset_index()
aa = aa.filter(["Population"]).loc[1].sum()

print("The population in Spain considered for this period has been"
      , aa ,
      ".")

#%% How many second doses have been supplied in Italy?

aa = df.filter(["YearWeekISO" , "SecondDose" , "Region" , "TargetGroup"])

aa = aa[(aa.Region == "IT")]
aa = aa.loc[(aa.TargetGroup == "ALL") | (aa.TargetGroup == "Age<18")]
aa = aa.SecondDose.sum()

print("Since the beginning of the vacunation program, "
      , aa ,
      " second doses have been supplied in Italy")

#%% What are the percentages of population that don't want the first dose in France, Spain, Germany and Italy?

aa = df.filter(["Region" , "FirstDoseRefused" , "TargetGroup" , "Population"])

aa = aa.loc[(aa.Region == "FR") |
            (aa.Region == "ES") |
            (aa.Region == "DE") |
            (aa.Region == "IT")]
aa = aa.loc[(aa.TargetGroup == "ALL") | (aa.TargetGroup == "Age<18")]
aa = aa.groupby(["Region" ,"Population"])["FirstDoseRefused"].sum().reset_index()


aa['Percentage'] = aa.apply(lambda row: row.FirstDoseRefused*100 / row.Population, axis = 1)

for x in range(len(aa)):
    y = aa.Region[x]
    z = (aa.Percentage[x] == 0)
    if (aa.Percentage[x] == 0):
        print("The country "
              , y ,
              " has no valid observations for this phenomena.")
    else:
        print("In "
              , y ,
              ", the percentage of people who refused to the first dose was " ,
              round(aa.Percentage[x] , 2)
              , "% of people who refused to the first dose.")

