import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats as st

games = pd.read_csv('games.csv')
games.info()
print()


# STEP 2. Data pre-processing
# column names to lowercase
games.columns = games.columns.str.lower()
# to int
games['year_of_release'] = games['year_of_release'].astype('Int64')

print('Games with "tbd" score')
print(games.query('user_score == "tbd"').count().max(), '\n')
print('Year of games with "tbd" score')
print(games.query('user_score == "tbd"')['year_of_release'].value_counts(), '\n')

# replacing tbd with -2
games.loc[games['user_score'] == 'tbd', 'user_score'] = -2
# replacing NaN with -1
games['user_score'].fillna(-1, inplace=True)
# to float
games['user_score'] = games['user_score'].astype('float64')

# replacing NaN with -1
games['critic_score'].fillna(-1, inplace=True)

# replacing NaN with 'undefined'
games['rating'].fillna('undefined', inplace=True)

games.dropna(inplace=True, subset=['name'], axis='index')

# counting total sales
def total(row):
    return row['na_sales'] + row['eu_sales'] + row['jp_sales'] + row['other_sales']


games['total_sales'] = games.apply(total, axis=1)
# print(games['total_sales'])
games.info()
print()


# Step 3. Analysis
# games per year
games_per_year = games.pivot_table(index='year_of_release', values='name', aggfunc='count')
games_per_year.columns = ['games_count']
print(games_per_year, '\n')

# platform information
# table shows total sales of each platform in each year.
platforms_year = games.pivot_table(index=['year_of_release', 'platform'], values='total_sales', aggfunc='sum')
platforms_year.columns = ['platform_per_year_sales']
print(platforms_year, '\n')

# table shows total sales from 1980-2016 for each platform
platforms_total = games.pivot_table(index='platform', values='total_sales', aggfunc='sum')
platforms_total.columns = ['platform_total_sales']
platforms_total = platforms_total.sort_values(by='platform_total_sales', ascending=False)
print(platforms_total, '\n')
top6_platforms = ['PS2', 'X360', 'PS3', 'Wii', 'DS', 'PS']

# Plotting bars to see the difference in sales between platforms for each year
years = [i for i in range(1980, 2017)]
for year in years:
    platforms_year.query('year_of_release == @year').plot.barh(y='platform_per_year_sales', grid=True)
    plt.show()

# Filtering out information
# have to fill NaN with smth to work with year_of_release
games['year_of_release'].fillna(0, inplace=True)
games_sort = games.query('year_of_release >= 2001').copy()
games_sort.info()
print()
print(games_sort, '\n')

# total sales for each platform
platforms_sort_total = games_sort.pivot_table(index='platform', values='total_sales', aggfunc='sum')
platforms_sort_total.columns = ['platform_total_sales']
platforms_sort_total = platforms_sort_total.sort_values(by='platform_total_sales', ascending=False)
print(platforms_total, '\n')

# PS4 sales
ps4_info = games_sort.query('platform == "PS4"')[['critic_score', 'user_score', 'total_sales']].copy()
ps4_info.query('user_score >= 0').plot(x='user_score', y='total_sales', kind='scatter', title='Users')
plt.show()
ps4_info.query('critic_score >= 0').plot(x='critic_score', y='total_sales', kind='scatter', title='Critics')
plt.show()
print(ps4_info[['user_score', 'total_sales']].corr(), '\n')
print(ps4_info[['critic_score', 'total_sales']].corr(), '\n')

# Call of Duty: Ghosts & Witcher info
# just 2 random games from data
CoD_info = games_sort.query('name == "Call of Duty: Ghosts"')[['platform', 'year_of_release', 'user_score', 'critic_score', 'total_sales']]
print(CoD_info, '\n')
witcher_info = games_sort.query('name == "The Witcher 3: Wild Hunt"')[['platform', 'year_of_release', 'user_score', 'critic_score', 'total_sales']]
print(witcher_info, '\n')

# Genres info
# creating pivot table with genres as index and total_sales count, sum, mean as values
genres = games_sort.pivot_table(index='genre', values=['total_sales'], aggfunc=['count', 'sum', 'mean'])
genres.columns = ['number_of_games', 'total_sales', 'sales_per_game']
# sorting data by values
print('---------Sorting data by values---------')
print('By number of games')
print(genres.sort_values(by='number_of_games', ascending=False), '\n')
print('By total sales')
print(genres.sort_values(by='total_sales', ascending=False), '\n')
print('By sales per game')
print(genres.sort_values(by='sales_per_game', ascending=False), '\n')


# Step 4. Regions info
# Top platforms
print('---------Top platforms---------')
na_platform = (games_sort
               .pivot_table(index='platform', values='na_sales', aggfunc='sum')
               .sort_values(by='na_sales', ascending=False)
               )
na_total = na_platform['na_sales'].sum()
print('Total sales in NA:', na_total)
na_platform['market_share'] = na_platform['na_sales'] / na_total
print(na_platform, '\n')

eu_platform = (games_sort
               .pivot_table(index='platform', values='eu_sales', aggfunc='sum')
               .sort_values(by='eu_sales', ascending=False)
               )
eu_total = eu_platform['eu_sales'].sum()
print('Total sales in EU:', eu_total)
eu_platform['market_share'] = eu_platform['eu_sales'] / eu_total
print(eu_platform, '\n')


jp_platform = (games_sort
              .pivot_table(index='platform', values='jp_sales', aggfunc='sum')
               .sort_values(by='jp_sales', ascending=False)
               )
jp_total = jp_platform['jp_sales'].sum()
print('Total sales in JP:', jp_total)
jp_platform['market_share'] = jp_platform['jp_sales'] / jp_total
print(jp_platform, '\n')

# Top genres
print('---------Top genres---------')
na_genre = (games_sort
            .pivot_table(index='genre', values='na_sales', aggfunc='sum')
            .sort_values(by='na_sales', ascending=False)
            )
na_genre['market_share'] = na_genre['na_sales'] / na_total
print(na_genre, '\n')

eu_genre = (games_sort
            .pivot_table(index='genre', values='eu_sales', aggfunc='sum')
            .sort_values(by='eu_sales', ascending=False)
            )
eu_genre['market_share'] = eu_genre['eu_sales'] / eu_total
print(eu_genre, '\n')

jp_genre = (games_sort
            .pivot_table(index='genre', values='jp_sales', aggfunc='sum')
            .sort_values(by='jp_sales', ascending=False)
            )
jp_genre['market_share'] = jp_genre['jp_sales'] / jp_total
print(jp_genre, '\n')

# ESRB Rating
print('---------ESRB Rating---------')
na_rating = (games_sort
             .pivot_table(index='rating', values='na_sales', aggfunc='sum')
             .sort_values(by='na_sales', ascending=False)
             )
na_rating['market_share'] = na_rating['na_sales'] / na_total
print(na_rating, '\n')

eu_rating = (games_sort
             .pivot_table(index='rating', values='eu_sales', aggfunc='sum')
             .sort_values(by='eu_sales', ascending=False)
             )
eu_rating['market_share'] = eu_rating['eu_sales'] / eu_total
print(eu_rating, '\n')

jp_rating = (games_sort
             .pivot_table(index='rating', values='jp_sales', aggfunc='sum')
             .sort_values(by='jp_sales', ascending=False)
             )
jp_rating['market_share'] = jp_rating['jp_sales'] / jp_total
print(jp_rating, '\n')


# Step 5. Hypotheses
# Average user ratings of the Xbox One and PC platforms.
print('---------Hypothesis №1---------')
xone_user_score = games_sort.query('platform == "XOne" and user_score > 0')[['name', 'user_score']].copy()
print(xone_user_score.var())
pc_user_score = games_sort.query('platform == "PC" and user_score > 0')[['name', 'user_score']].copy()
print(pc_user_score.var())

alpha = 0.05
# variances are not the same so equal_var=False
results = st.ttest_ind(xone_user_score['user_score'], pc_user_score['user_score'], equal_var=False)
print('p-value:', results.pvalue)

if (results.pvalue < alpha):
    print('We reject the null hypothesis', '\n')
else:
    print("We can't reject the null hypothesis", '\n')


# Average user ratings for the Action and Sports genres
print('---------Hypothesis №2---------')
action_user_score = games_sort.query('genre == "Action" and user_score > 0')[['name', 'user_score']].copy()
print(action_user_score.var())
sports_user_score = games_sort.query('genre == "Sports" and user_score > 0')[['name', 'user_score']].copy()
print(sports_user_score.var())

# variances are not the same so equal_var=False
results2 = st.ttest_ind(action_user_score['user_score'], sports_user_score['user_score'], equal_var=False)
print('p-value:', results.pvalue)

if (results.pvalue > alpha):
    print('We reject the null hypothesis', '\n')
else:
    print("We can't reject the null hypothesis", '\n')





