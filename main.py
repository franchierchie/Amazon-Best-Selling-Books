import pandas as pd

df = pd.read_csv('bestsellers.csv')
# print(df.head())
# print(df.shape)
# print(df.columns)
# print(df.info())
# print(df.describe())

# Cleaning/Formatting Data
df.rename(columns={'Name': 'Title', 'Year': 'Publication Year', 'User Rating': 'Rating'}, inplace=True)
df['Price'] = df['Price'].astype(float)

# Analising Data
author_counts = df['Author'].value_counts()
avg_rating_by_genre = df.groupby('Genre')['Rating'].mean()

df = df.drop_duplicates(inplace=True)

# Export Results
author_counts.head(10).to_csv('top_authors.csv')
avg_rating_by_genre.to_csv('avg_rating_by_genre.csv')