import pandas as pd
from datetime import date
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats as st

games = pd.read_csv('games.csv')
# games.info()
# print()

# STEP 2
games.columns = games.columns.str.lower()
games['year_of_release'] = games['year_of_release'].astype('Int64')
games.loc[games['user_score'] == 'tbd', 'user_score'] = -2
games['user_score'].fillna(-1, inplace=True)
games['user_score'] = games['user_score'].astype('float64')
games['critic_score'].fillna(-1, inplace=True)
games['rating'].fillna('undefined', inplace=True)
games.dropna(inplace=True, subset=['name'], axis='index')
# games.info()
# print()


def total(row):
    return row['na_sales'] + row['eu_sales'] + row['jp_sales'] + row['other_sales']


games['total_sales'] = games.apply(total, axis=1)
# print(games['total_sales'])
#
# print()
# print('Games with "tbd" score')
# print(games.query('user_score == "tbd"').count().max())
# print('Year of games with "tbd" score')
# print(games.query('user_score == "tbd"')['year_of_release'].value_counts())
# print()
games['user_score'] = games['user_score'].replace('tbd', np.nan)

## empty = games[games['year_of_release'].isnull()]['name'].tolist()
## games['year_of_release'].fillna(0, inplace=True)
## print(empty)
## for names in empty:
##    print(games.query('name == @names and year_of_release != 0')[['name', 'year_of_release']])


# STEP 3
games_per_year = games.pivot_table(index='year_of_release', values='name', aggfunc='count')
games_per_year.columns = ['games_count']
# print(games_per_year)
# print()

platforms_year = games.pivot_table(index=['year_of_release', 'platform'], values='total_sales', aggfunc='sum')
platforms_year.columns = ['platform_per_year_sales']
# print(platforms_year)
# print()
platforms_total = games.pivot_table(index='platform', values='total_sales', aggfunc='sum')
platforms_total.columns = ['platform_total_sales']
platforms_total = platforms_total.sort_values(by='platform_total_sales', ascending=False)
# print(platforms_total)
# print()
top6_platforms = ['PS2', 'X360', 'PS3', 'Wii', 'DS', 'PS']
years = [i for i in range(1980, 2017)]
# for year in years:
#     platforms_year.query('year_of_release == @year').plot.bar(y='platform_per_year_sales')
#     plt.show()

games['year_of_release'].fillna(0, inplace=True)
games_sort = games.query('year_of_release >= 2001').copy()
# games_sort.info()
# print()
platforms_sort_total = games_sort.pivot_table(index='platform', values='total_sales', aggfunc='sum')
platforms_sort_total.columns = ['platform_total_sales']
platforms_sort_total = platforms_sort_total.sort_values(by='platform_total_sales', ascending=False)
# print(platforms_total)

# BOXPLOT
# game_platform = games_sort.pivot_table(index=['name', 'platform'], values='total_sales').boxplot()
# plt.show()
# print(game_platform)


ps4_info = games_sort.query('platform == "PS4"')[['critic_score', 'user_score', 'total_sales']].copy()
# ps4_info.plot(x='user_score', y='total_sales', kind='scatter', title='Users')
# plt.show()
# ps4_info.plot(x='critic_score', y='total_sales', kind='scatter', title='Critics')
# plt.show()
# print(ps4_info)
# print(ps4_info[['user_score', 'total_sales']].corr())
# print(ps4_info[['critic_score', 'total_sales']].corr())

CoD_info = games_sort.query('name == "Call of Duty: Ghosts"')[['platform', 'year_of_release', 'user_score', 'critic_score', 'total_sales']]
# print(CoD_info)
witcher_info = games_sort.query('name == "The Witcher 3: Wild Hunt"')[['platform', 'year_of_release', 'user_score', 'critic_score', 'total_sales']]
# print(witcher_info)

genres = games_sort.pivot_table(index='genre', values=['total_sales'], aggfunc=['count', 'sum', 'mean'])
genres.columns = ['number_of_games', 'total_sales', 'sales_per_game']
# print(genres.sort_values(by='number_of_games', ascending=False))
# print(genres.sort_values(by='total_sales', ascending=False))
# print(genres.sort_values(by='sales_per_game', ascending=False))

## STEP 4
na_platform = (games_sort
               .pivot_table(index='platform', values='na_sales', aggfunc='sum')
               .sort_values(by='na_sales', ascending=False)
               )
na_total = na_platform['na_sales'].sum()
na_platform['market_share'] = na_platform['na_sales'] / na_total
# print(na_platform)
# print()
eu_platform = (games_sort
               .pivot_table(index='platform', values='eu_sales', aggfunc='sum')
               .sort_values(by='eu_sales', ascending=False)
               )
eu_total = eu_platform['eu_sales'].sum()
eu_platform['market_share'] = eu_platform['eu_sales'] / eu_total
# print(eu_platform)
# print()
jp_platform = (games_sort
               .pivot_table(index='platform', values='jp_sales', aggfunc='sum')
               .sort_values(by='jp_sales', ascending=False)
               )
jp_total = jp_platform['jp_sales'].sum()
jp_platform['market_share'] = jp_platform['jp_sales'] / jp_total
# print(jp_platform)

na_genre = (games_sort
            .pivot_table(index='genre', values='na_sales', aggfunc='sum')
            .sort_values(by='na_sales', ascending=False)
            )
na_genre['market_share'] = na_genre['na_sales'] / na_total
# print(na_genre)
# print()
eu_genre = (games_sort
            .pivot_table(index='genre', values='eu_sales', aggfunc='sum')
            .sort_values(by='eu_sales', ascending=False)
            )
eu_genre['market_share'] = eu_genre['eu_sales'] / eu_total
# print(eu_genre)
# print()
jp_genre = (games_sort
            .pivot_table(index='genre', values='jp_sales', aggfunc='sum')
            .sort_values(by='jp_sales', ascending=False)
            )
jp_genre['market_share'] = jp_genre['jp_sales'] / jp_total
# print(jp_genre)
# print()

na_rating = (games_sort
             .pivot_table(index='rating', values='na_sales', aggfunc='sum')
             .sort_values(by='na_sales', ascending=False)
             )
na_rating['market_share'] = na_rating['na_sales'] / na_total
# print(na_rating)
# print()
eu_rating = (games_sort
             .pivot_table(index='rating', values='eu_sales', aggfunc='sum')
             .sort_values(by='eu_sales', ascending=False)
             )
eu_rating['market_share'] = eu_rating['eu_sales'] / eu_total
# print(eu_rating)
# print()
jp_rating = (games_sort
             .pivot_table(index='rating', values='jp_sales', aggfunc='sum')
             .sort_values(by='jp_sales', ascending=False)
             )
jp_rating['market_share'] = jp_rating['jp_sales'] / jp_total
# print(jp_rating)
# print()

## STEP 5
xone_user_score = games_sort.query('platform == "XOne" and user_score > 0')[['name', 'user_score']].copy()
# print(xone_user_score.var())
# print()
pc_user_score = games_sort.query('platform == "PC" and user_score > 0')[['name', 'user_score']].copy()
# print(pc_user_score.var())

alpha = 0.05
results = st.ttest_ind(xone_user_score['user_score'], pc_user_score['user_score'], equal_var=False)
# print('p-value:', results.pvalue)

# if (results.pvalue < alpha):
#     print('We reject the null hypothesis')
# else:
#     print("We can't reject the null hypothesis")

action_user_score = games_sort.query('genre == "Action" and user_score > 0')[['name', 'user_score']].copy()
# print(action_user_score.var())
# print()
sports_user_score = games_sort.query('genre == "Sports" and user_score > 0')[['name', 'user_score']].copy()
# print(sports_user_score.var())
# print()

results2 = st.ttest_ind(action_user_score['user_score'], sports_user_score['user_score'], equal_var=False)
# print('p-value:', results.pvalue)

# if (results.pvalue > alpha):
#     print('We reject the null hypothesis')
# else:
#     print("We can't reject the null hypothesis")