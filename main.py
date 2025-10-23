import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def thousands_formatter(x, pos):
  """Formats large numbers into K (thousands)"""
  return f'{int(x/1000)}K'

def load_data():
  df = pd.read_csv('data/bestsellers.csv')
  return df

def clean_data(df):
  df.rename(columns={'Name': 'Title', 'Year': 'Publication Year', 'User Rating': 'Rating'}, inplace=True)
  df['Price'] = df['Price'].astype(float)

def handle_results(author_counts, avg_rating_by_genre):
  author_counts.head(10).to_csv('reports/top_authors.csv')
  avg_rating_by_genre.to_csv('reports/avg_rating_by_genre.csv')

def genre_performance_plot(df):
  # Genre Preformance
  yearly_genre_ratings = df.groupby(['Publication Year', 'Genre'])['Rating'].mean().reset_index()

  # Fiction
  fiction_ratings = yearly_genre_ratings[yearly_genre_ratings['Genre'] == 'Fiction']
  years_fiction = fiction_ratings['Publication Year']
  ratings_fiction = fiction_ratings['Rating']

  # Non Fiction
  non_fiction_ratings = yearly_genre_ratings[yearly_genre_ratings['Genre'] == 'Non Fiction']
  years_nonfiction = non_fiction_ratings['Publication Year']
  ratings_nonfiction = non_fiction_ratings['Rating']

  plt.figure(figsize=(10, 6))

  # Plot Fiction ratings over the years
  plt.plot(years_fiction, ratings_fiction, label='Fiction Average Rating', marker='o')

  # Plot Non-Fiction ratings over the years
  plt.plot(years_nonfiction, ratings_nonfiction, label='Non-Fiction Average Rating', marker='o')

  # Add titles and labels for clarity
  plt.title('Average User Rating Trend by Genre (2009-2019)')
  plt.xlabel('Year')
  plt.ylabel('Average User Rating')
  plt.legend()
  plt.grid(axis='y', linestyle='--')
  plt.xticks(years_fiction.unique()) # Ensure all years are clearly marked
  plt.savefig('plots/genre_performance_plot.png')
  plt.close()
  # plt.show()

def price_vs_rating_plot(df):
  # Price vs. User Rating
  plt.figure(figsize=(10, 6))
  # We use 'Genre' to color-code the points to see if genre plays a role.
  plt.scatter(df['Price'], df['Rating'], 
              c=df['Genre'].astype('category').cat.codes, 
              cmap='coolwarm', alpha=0.6)

  plt.title('Price vs. Rating of Best-Selling Books')
  plt.xlabel('Price ($)')
  plt.ylabel('User Rating (Out of 5)')
  plt.colorbar(label='Genre (0=Fiction, 1=Non Fiction)')
  plt.grid(True, linestyle='--', alpha=0.5)
  plt.savefig('plots/price_vs_rating_plot.png')
  plt.close()
  # plt.show()

def top_authors_plot(authors):
  top_ten_authors = authors.head(10).sort_values(ascending=True)

  plt.figure(figsize=(10, 6))

  # Plot the top 10 bestselling authors
  bars = plt.barh(top_ten_authors.index[::-1], top_ten_authors.values, color='skyblue', edgecolor='black')

  # Add Data Labels (Optional but highly recommended)
  for bar in bars:
    # bar.get_width() is the value (count)
    # bar.get_y() + bar.get_height()/2 is the center of the bar
    plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
            f'{int(bar.get_width())}', va='center')

  # Add titles and labels for clarity
  plt.title('Top 10 Bestselling Authors by Total Appearances')
  plt.xlabel('Total Bestseller Appearances')
  plt.ylabel('Author')
  # Set x-axis limit slightly higher to accommodate the data labels
  plt.xlim(0, top_ten_authors.max() + 2)
  plt.tight_layout()
  plt.savefig('plots/top_authors_plot.png')
  plt.close()
  # plt.show()

def rising_audience_plot(df):
  # Calculate the average yearly reviews
  yearly_average_reviews = df.groupby(['Publication Year'])['Reviews'].mean().reset_index()

  plt.figure(figsize=(10, 6))
  plt.plot(yearly_average_reviews['Publication Year'], yearly_average_reviews['Reviews'], marker='o')

  # Apply the custom formatter to the y-axis
  plt.gca().yaxis.set_major_formatter(FuncFormatter(thousands_formatter))

  # Add titles and labels for clarity
  plt.title('Rising Audience Engagement')
  plt.xlabel('Year')
  plt.ylabel('Average Reviews Count')
  plt.grid(axis='y', linestyle='--')
  plt.tight_layout()
  plt.savefig('plots/rising_audience_plot.png')
  plt.close()
  # plt.show()

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

  # Plotting
  genre_performance_plot(df)
  price_vs_rating_plot(df)
  top_authors_plot(author_counts)
  rising_audience_plot(df)

  df = df.drop_duplicates(inplace=True)

  # Export Results
  handle_results(author_counts, avg_rating_by_genre)

if __name__ == '__main__':
  main()