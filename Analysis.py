import pandas as pd
from Cleaning import df
import numpy as np

# Distribiution of the world's population based on country, year and sex

df_both = df.loc[df['Sex'] == 'Both Sexes'].groupby(
    ['Country or Area', 'Year', 'Sex'])['Value'].sum().reset_index()

df_male = df.loc[df['Sex'] == 'Male'].groupby(['Country or Area', 'Year', 'Sex'])[
    'Value'].sum().reset_index()

df_female = df.loc[df['Sex'] == 'Female'].groupby(
    ['Country or Area', 'Year', 'Sex'])['Value'].sum().reset_index()

df_merge = df_male.merge(
    df_female,
    how='inner',
    on=(['Country or Area', 'Year']),
    suffixes=['_m', '_f']
)

df_merge = df_merge.merge(
    df_both,
    how='inner',
    on=(['Country or Area', 'Year'])
)
df_merge = df_merge.rename(columns={'Sex': 'Sex_b', 'Value': 'Value_b'})

# Comparation of the amount of males and females in the world based on year

df_comparation = df_merge.groupby('Year')[['Value_m', 'Value_f']].sum()

# In which country, in which year there was the biggest difference in amount of males and females

df_diff = df_merge.copy()

df_diff = df_diff[['Country or Area', 'Year', 'Value_m', 'Value_f']]

df_diff['diff'] = np.where((df_diff['Value_f']-df_diff['Value_m']) > 0,
                           df_diff['Value_f']-df_diff['Value_m'], df_diff['Value_m']-df_diff['Value_f'])

df_diff['diff_sex'] = np.where(
    (df_diff['Value_f']-df_diff['Value_m']) > 0, 'f', 'm')

df_diff = df_diff.sort_values('diff', ascending=False).head(10)

# Top 10 cities with most residents

df_city = df.loc[df['Sex'] == 'Both Sexes']

df_city = df_city.groupby(
    ['City', 'Year'], as_index=False)['Value'].sum()

df_city = df_city.groupby('City', as_index=False)[
    'Value'].max().sort_values('Value', ascending=False).head(10)

# Top 10 countries with most residents

df_country = df.loc[df['Sex'] == 'Both Sexes']

df_country = df_country.groupby(
    ['Country or Area', 'Year'], as_index=False)['Value'].sum()

df_country = df_country.groupby('Country or Area', as_index=False)[
    'Value'].max().sort_values('Value', ascending=False).head(10)

# What is the name of the country where lives most amount of women and men in relation to total amount of people living in the country

df_percentage = df_merge.copy()

df_percentage = df_percentage[['Country or Area',
                               'Year', 'Value_m', 'Value_f', 'Value_b']]

df_percentage['percentage_f'] = round(
    df_percentage['Value_f']/df_percentage['Value_b']*100, 2)

df_percentage['percentage_m'] = round(
    df_percentage['Value_m']/df_percentage['Value_b']*100, 2)

# Let's give it a margin of error of a 1%

df_percentage = df_percentage.loc[(df_percentage['percentage_f']+df_percentage['percentage_m']
                                   ).between(99, 101, inclusive='both')]

df_percentage_f = df_percentage.groupby('Country or Area', as_index=False)[
    'percentage_f'].mean().sort_values('percentage_f', ascending=False)

df_percentage_m = df_percentage.groupby('Country or Area', as_index=False)[
    'percentage_m'].mean().sort_values('percentage_m', ascending=False)

df_percentage_result = df_percentage_f.merge(
    df_percentage_m,
    on='Country or Area',
    how='inner'
)
