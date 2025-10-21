import pandas as pd

def load_data():
  df = pd.read_csv('data/bestsellers.csv')
  return df

def clean_data(df):
  df.rename(columns={'Name': 'Title', 'Year': 'Publication Year', 'User Rating': 'Rating'}, inplace=True)
  df['Price'] = df['Price'].astype(float)

def handle_results(author_counts, avg_rating_by_genre):
  author_counts.head(10).to_csv('reports/top_authors.csv')
  avg_rating_by_genre.to_csv('reports/avg_rating_by_genre.csv')

def main():
  df = load_data()
  # print(df.head())
  # print(df.shape)
  # print(df.columns)
  # print(df.info())
  # print(df.describe())

  # Cleaning/Formatting Data
  clean_data(df)

  # Analize Data
  author_counts = df['Author'].value_counts()
  avg_rating_by_genre = df.groupby('Genre')['Rating'].mean()

  df = df.drop_duplicates(inplace=True)

  # Export Results
  handle_results(author_counts, avg_rating_by_genre)

if __name__ == '__main__':
  main()