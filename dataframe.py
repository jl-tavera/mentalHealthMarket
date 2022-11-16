#%%
import requests
from bs4 import BeautifulSoup
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
tertiarySE = pd.read_csv('raw/Tertiary_SE.csv')
young = pd.read_csv('raw/Young.csv')
gdp = pd.read_csv('raw/GDP.csv')


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

tertiarySE = tertiarySE.drop(['Country Name', 'Indicator Name', 'Indicator Code'], axis=1)
tertiarySE = tertiarySE.fillna(0)
tertiarySE['tertiarySE'] = tertiarySE.max(axis=1)
tertiarySE = tertiarySE.loc[:, ['Country Code', 'tertiarySE']]

#Age 0-14

young = young.loc[:, ['Country Code', '2019']]
young = young.dropna()
young = young.rename(columns = { '2019': 'Young'})

#GDP

gdp = gdp.loc[:, ['Country Code', '2019']]
gdp = gdp.dropna()
gdp = gdp.rename(columns = { '2019': 'GDP'})

#World Regions

url = 'https://statisticstimes.com/geography/countries-by-continents.php'
region_table = pd.read_html(url, match='Country or Area')[0]
region_table = region_table.rename(columns = {'ISO-alpha3 Code':'Country Code'})


'''
MERGE
'''

whoStats = pd.merge(healthPop, whoCodes)
whoData = pd.merge(whoStats, totalPop)
wbdata1 = pd.merge(whoData, business)
wbdata2 = pd.merge(wbdata1, primarySE)
wbdata3 = pd.merge(wbdata2, secondarySE)
wbdata4 = pd.merge(wbdata3, tertiarySE)
wbdata5 = pd.merge(wbdata4, gdp)
data = pd.merge(wbdata5, young)
data = pd.merge(data, region_table)

'''
TOTAL PSYCHOLOGISTS AND SCHOOLS
'''

data['MH size'] = round((data['Total Pop']*data['Mental Health'])/100000)
data['School Enrollment'] = ((data['primarySE'] + data['secondarySE'])/2)/100
data['Young'] = data['Young']/100
data['Schools'] = round((data['Young']*data['School Enrollment']*data['Total Pop'])/600)
data['Universities'] = round((data['Young']*data['tertiarySE']*data['Total Pop']/100)/8000)

'''
TAM
'''

total_MHsize = data['MH size'].sum()
total_schools = data['Schools'].sum()
total_universities = data['Universities'].sum()


print('TOTAL ADRESSABLE MARKET')
print('Total Population Mental Health (Worldwide): ' + str(total_MHsize)) # 1510460.0
print('Total Universities (Worldwide): ' + str(total_universities)) # 80488.0
print('')

tam = (total_MHsize*30 + total_universities*250)*12
print('TAM = ' + str(tam)) # TAM = 785229600.0
print('')


'''
SAM
'''

data = data[data['GDP'] >= 6100]

total_MHsize = data['MH size'].sum()
total_schools = data['Schools'].sum()
total_universities = data['Universities'].sum()

print('SERVICEABLE AVAILABLE MARKET')
print('Total Population Mental Health (GDP per capita >= 6100): ' + str(total_MHsize)) # 1424099.0
print('Total Universities (GDP per capita >= 6100): ' + str(total_universities)) # 49811.0
print('')

sam = (total_MHsize*30 + total_universities*250)*12
print('SAM = ' + str(sam)) # SAM = 662108640.0
print('')

'''
SOM
'''

regions = [ 'South America', 'Caribbean', 'Central America']
regions_2 = ['Latin America and the Caribbean']

data = data[data['Region 2'].isin(regions_2)]

total_MHsize = data['MH size'].sum()
total_schools = data['Schools'].sum()
total_universities = data['Universities'].sum()

print('SERVICEABLE OBTAINABLE MARKET')
print('Total Population Mental Health (GDP per capita >= 6100 and Latin America and the Caribbean): ' + str(total_MHsize)) # 268761.0
print('Total Universities (GDP per capita >= 6100 and Latin America and the Caribbean): ' + str(total_universities)) # 9126.0
print('')

som = (total_MHsize*30 + total_universities*250)*12
print('SOM = ' + str(som)) # SOM = 124131960.0


