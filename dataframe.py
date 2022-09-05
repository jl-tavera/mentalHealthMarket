#%%
import pandas as pd
import numpy as np
'''
LOADING DATAFRAMES
'''

#World Health Organization - WHO
healthPop = pd.read_csv('raw/Mental_Health.csv')
whoCodes = pd.read_csv('raw/WHO_codes.csv')

#World Bank
totalPop = pd.read_excel('raw/Total_Population.xls')
business = pd.read_csv('raw/New_Business_Registered.csv')
primarySE = pd.read_csv('raw/Primary_SE.csv')
secondarySE = pd.read_csv('raw/Secondary_SE.csv')
young = pd.read_csv('raw/Young.csv')

'''
WHO COUNTRY CODES FORMAT
'''

Afg = {'COUNTRY': 'COUNTRY', 'AFG': 'AFG', 'Afghanistan': 'Afghanistan'}
whoCodes = whoCodes.append(Afg, ignore_index=True)
whoCodes = whoCodes.rename(columns = {'AFG':'Country Code', 'Afghanistan': 'Country'})
whoCodes = whoCodes.loc[:, ['Country Code','Country']]

'''
MENTAL HEALTH SECTOR FORMAT
'''

healthPop = healthPop.rename(columns = {'Psychiatrists working in mental health sector (per 100 000 population)': 'Psychiatrists'})
healthPop = healthPop.rename(columns = {'Nurses working in mental health sector (per 100 000 population)': 'Nurses'})
healthPop = healthPop.rename(columns = {'Social workers working in mental health sector (per 100 000 population)': 'Social workers'})
healthPop = healthPop.rename(columns = {'Psychologists working in mental health sector (per 100 000 population)': 'Psychologists'})
healthPop = healthPop.loc[:, ['Country', 'Psychiatrists', 'Nurses', 'Social workers', 'Psychologists']]
healthPop =  healthPop.fillna(0)

healthPop['Mental Health'] = (healthPop['Psychiatrists'] +healthPop['Nurses'] +healthPop['Social workers'] +healthPop['Psychologists'] )
healthPop = healthPop.loc[:, ['Country', 'Mental Health']]

'''
WORLD BANK FORMAT
'''
#Total Population

totalPop = totalPop.loc[:, ['Country Code', '2019']]
totalPop = totalPop.dropna()
totalPop = totalPop.rename(columns = { '2019': 'Total Pop'})

#Business

business = business.replace('..',0.0)
business = business.drop(['Series Name', 'Series Code', 'Country Name'], axis=1)
business_cols=[i for i in business.columns if i not in ["Country Code"]]
for col in business_cols:
    business[col]=pd.to_numeric(business[col])
business['Companies'] = business.sum(axis=1, numeric_only= True)
business = business.loc[:, ['Country Code', 'Companies']]

#School Enrollment

primarySE = primarySE.drop(['Country Name', 'Indicator Name', 'Indicator Code'], axis=1)
primarySE = primarySE.fillna(0)
primarySE['primarySE'] = primarySE.max(axis=1)
primarySE = primarySE.loc[:, ['Country Code', 'primarySE']]

secondarySE = secondarySE.drop(['Country Name', 'Indicator Name', 'Indicator Code'], axis=1)
secondarySE = secondarySE.fillna(0)
secondarySE['secondarySE'] = secondarySE.max(axis=1)
secondarySE = secondarySE.loc[:, ['Country Code', 'secondarySE']]

#Age 0-14

young = young.loc[:, ['Country Code', '2019']]
young = young.dropna()
young = young.rename(columns = { '2019': 'Young'})

'''
MERGE
'''

whoStats = pd.merge(healthPop, whoCodes)
whoData = pd.merge(whoStats, totalPop)
wbdata1 = pd.merge(whoData, business)
wbdata2 = pd.merge(wbdata1, primarySE)
wbdata3 = pd.merge(wbdata2, secondarySE)
data = pd.merge(wbdata3, young)

'''
TOTAL PSYCHOLOGISTS
'''

data['MH size'] = round((data['Total Pop']*data['Mental Health'])/100000)
data['School Enrollment'] = ((data['primarySE'] + data['secondarySE'])/2)/100
data['Young'] = data['Young']/100
data['Schools'] = round((data['Young']*data['School Enrollment']*data['Total Pop'])/600)
total = data['Companies'].sum()

print(data)
