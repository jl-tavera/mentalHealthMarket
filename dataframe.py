#%%
import pandas as pd
'''
LOADING DATAFRAMES
'''

totalPop = pd.read_excel('raw/Total_Population.xls')
healthPop = pd.read_csv('raw/Mental_Health.csv')
whoCodes = pd.read_csv('raw/WHO_codes.csv')

'''
WHO COUNTRY CODES FORMAT
'''

Afg = {'COUNTRY': 'COUNTRY', 'AFG': 'AFG', 'Afghanistan': 'Afghanistan'}
whoCodes = whoCodes.append(Afg, ignore_index=True)
whoCodes = whoCodes.rename(columns = {'AFG':'CODE', 'Afghanistan': 'Country'})
whoCodes = whoCodes.loc[:, ['CODE','Country']]

'''
TOTAL POPULATION FORMAT
'''

totalPop = totalPop.loc[:, ['Country Code', '2019']]
totalPop = totalPop.dropna()
totalPop = totalPop.rename(columns = { '2019': 'Total Pop','Country Code': 'CODE'})

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
MERGE
'''

whoStats = pd.merge(healthPop, whoCodes)
data = pd.merge(whoStats, totalPop)


'''
TOTAL PSYCHOLOGISTS
'''

data['MH size'] = round((data['Total Pop']*data['Mental Health'])/100000)
total = data['MH size'].sum()

print(total)
