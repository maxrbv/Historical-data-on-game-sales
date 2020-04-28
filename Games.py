import pandas as pd
from datetime import date
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats as st

games = pd.read_csv('games.csv')
games.info()
print()

# STEP 2
games.columns = games.columns.str.lower()
games['year_of_release'] = games['year_of_release'].astype('Int64')
games['critic_score'] = games['critic_score'].astype('Int64')
games.info()
print()


def total(row):
    return row['na_sales'] + row['eu_sales'] + row['jp_sales'] + row['other_sales']


games['total_sales'] = games.apply(total, axis=1)
print(games['total_sales'])

print()
print('Games with "tbd" score')
print(games.query('user_score == "tbd"').count().max())
print('Year of games with "tbd" score')
print(games.query('user_score == "tbd"')['year_of_release'].value_counts())
print()

# empty = games[games['year_of_release'].isnull()]['name'].tolist()
# games['year_of_release'].fillna(0, inplace=True)
# print(empty)
# for names in empty:
   # print(games.query('name == @names and year_of_release != 0')[['name', 'year_of_release']])


# STEP 3
games_per_year = games.pivot_table(index='year_of_release', values='name', aggfunc='count')
games_per_year.columns = ['games_count']
print(games_per_year)
print()

platforms_year = games.pivot_table(index=['year_of_release', 'platform'], values='total_sales', aggfunc='sum')
platforms_year.columns = ['platform_per_year_sales']
print(platforms_year)
print()
platforms_total = games.pivot_table(index='platform', values='total_sales', aggfunc='sum')
platforms_total.columns = ['platform_total_sales']
platforms_total = platforms_total.sort_values(by='platform_total_sales', ascending=False)
print(platforms_total)
print()
top6_platforms = ['PS2', 'X360', 'PS3', 'Wii', 'DS', 'PS']
years = [i for i in range(1980, 2016)]
for year in years:
    platforms_year.query('year_of_release == @year').plot.bar(y='platform_per_year_sales')
    plt.show()




