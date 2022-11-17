'''
LIBRARIES
'''
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression

'''
POPULATION DATAFRAME
'''

colombian_pop = pd.read_excel('raw/Total_Population.xls')
colombian_pop = colombian_pop[colombian_pop['Country Name'] == 'Colombia']


'''
VARIABLES
'''
initial_year = 1960
fraction = 0.1

'''
DATAFRAME FUNCTIONS
'''

def psychologistPop(df, year, fraction): 
    x = []
    y = []

    while year < 2020:
        data = []
        colombian_pop = float((df[str(year)]).item())

        x.append([year])
        y.append([colombian_pop*(fraction/100)])  

             
        year += 1

    return x, y

psychologist_pop = psychologistPop(colombian_pop, initial_year, fraction)
print(psychologist_pop)
plot_values = []
model = LinearRegression().fit(psychologist_pop[0], psychologist_pop[1])

for k_year in range(2002, 2033):
    y_pred = model.predict([[k_year]])
    plot_values.append([k_year, y_pred.item()])

df_col = pd.DataFrame(plot_values)
df_col.columns = ['Year', 'Population']
df_col['Age 20-25'] = df_col['Population']*0.1357
df_col['Age 26-30'] = df_col['Population']*0.3581
df_col['Age 31-35'] = df_col['Population']*0.2412
df_col['Age 36-45'] = df_col['Population']*0.1781
df_col['Age 46 > '] = df_col['Population']*0.0867
df_col = df_col.set_index('Year')
print(df_col.head())


print(plot_values)
sns.set_theme(style='darkgrid', rc={'figure.dpi': 147}, font_scale=0.7)
sns_pp = sns.lineplot(data=df_col )
plt.savefig('figs/colombia.png')