#%%
import pandas as pd

'''
LOADING DATAFRAMES
'''

totalPop = pd.read_excel('raw/Total_Population.xls')
healthPop = pd.read_csv('raw/MentalHealthSector.csv')
whoCodes = pd.read_csv('raw/WHO_codes.csv')

'''
WHO COUNTRY CODES FORMAT
'''

Afg = {'COUNTRY': 'COUNTRY', 'AFG': 'AFG', 'Afghanistan': 'Afghanistan'}
whoCodes = whoCodes.append(Afg, ignore_index=True)
whoCodes = whoCodes.rename(columns = {'AFG':'CODE', 'Afghanistan': 'Location'})
whoCodes = whoCodes.loc[:, ['CODE','Location']]

'''
TOTAL POPULATION FORMAT
'''

totalPop = totalPop.loc[:, ['Country Code', '2019']]
totalPop = totalPop.dropna()
totalPop = totalPop.rename(columns = { '2019': 'Total Pop','Country Code': 'CODE'})

'''
MENTAL HEALTH SECTOR FORMAT
'''

healthPop = healthPop.loc[:, ['Location', 'First Tooltip']]
healthPop = healthPop.rename(columns = {'First Tooltip': 'Psychologists'})

'''
MERGE
'''

whoStats = pd.merge(healthPop, whoCodes)
data = pd.merge(whoStats, totalPop)

'''
TOTAL PSYCHOLOGISTS
'''

data['Total Psychologist'] = round((data['Total Pop']*data['Psychologists'])/100000)
total = data['Total Psychologist'].sum()


print(total)