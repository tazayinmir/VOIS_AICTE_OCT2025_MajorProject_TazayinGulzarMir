import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
# Suppress the SettingWithCopyWarning which often occurs in data manipulation
warnings.filterwarnings('ignore')

# --- 1. Load the Dataset (The "Link" to the File) ---

CSV_FILE = "Netflix Dataset.csv"
EXCEL_FILE = "Netflix Dataset.xlsx"

try:
    # 1. ATTEMPT TO READ AS CSV (The format of the file you uploaded)
    df = pd.read_csv(CSV_FILE, encoding='latin-1')
    print(f"Successfully linked to and loaded data from {CSV_FILE} (CSV format).")
except FileNotFoundError:
    # 2. FALLBACK: ATTEMPT TO READ AS EXCEL (.xlsx) 
    # NOTE: If this fails, you may need to install 'openpyxl': pip install openpyxl
    try:
        df = pd.read_excel(EXCEL_FILE)
        print(f"Successfully linked to and loaded data from {EXCEL_FILE} (Excel format).")
    except FileNotFoundError:
        print("\n--- FATAL ERROR: DATA FILE NOT FOUND ---")
        print("Please ensure the data file is in the same folder as this script.")
        print(f"It must be named EITHER '{CSV_FILE}' OR '{EXCEL_FILE}'.")
        exit()
except Exception as e:
    print(f"An error occurred during file loading: {e}")
    exit()

# --- 2. Data Cleaning and Preprocessing ---

# Convert 'Release_Date' to datetime and extract 'Year_Added'
df['Date_Added'] = pd.to_datetime(df['Release_Date'], errors='coerce')
df['Year_Added'] = df['Date_Added'].dt.year

# Fill missing 'Country' values with 'Missing'
df['Country'] = df['Country'].fillna('Missing')

# Drop rows with missing 'Category' (Movie/TV Show)
df.dropna(subset=['Category'], inplace=True)

# --- 3. Objective 1: Analyze Movies vs. TV Shows over the Years (Chart 1) ---
print("\n--- 1. Analyzing Content Distribution Over Time ---")

content_over_time = df.dropna(subset=['Year_Added'])
content_over_time['Year_Added'] = content_over_time['Year_Added'].astype(int)
content_yearly = content_over_time.groupby(['Year_Added', 'Category']).size().unstack(fill_value=0)
plot_df = content_yearly.loc[content_yearly.index >= 2008]

plt.figure(figsize=(12, 6))
plot_df.plot(kind='bar', stacked=True, ax=plt.gca())

plt.title('Distribution of Content (Movies vs. TV Shows) Added to Netflix Per Year')
plt.xlabel('Year Added')
plt.ylabel('Count')
plt.legend(title='Category')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('Chart_1_Content_Distribution_Over_Time.png')
plt.close()

# --- 4. Objective 2: Identify the Most Common Genres (Type) (Chart 2) ---
print("--- 2. Identifying Top 10 Genres ---")

# Function to split and count genres
def count_genres(data):
    all_genres = ', '.join(data.dropna()).split(', ')
    return Counter(all_genres)

genre_counts = count_genres(df['Type'])
top_10_genres = pd.DataFrame(genre_counts.most_common(10), columns=['Genre', 'Count'])

# Visualize Top 10 Genres
plt.figure(figsize=(10, 7))
sns.barplot(x='Count', y='Genre', data=top_10_genres, palette='viridis')
plt.title('Top 10 Most Popular Genres on Netflix')
plt.xlabel('Total Content Count')
plt.ylabel('Genre')
plt.tight_layout()
plt.savefig('Chart_2_Top_10_Genres.png')
plt.close()

# --- 5. Objective 3: Compare Country-wise Contributions (Chart 3) ---
print("--- 3. Comparing Country Contributions ---")

# Function to split and count countries
def count_countries(data):
    valid_countries = [country.strip() for countries in data if countries != 'Missing' for country in countries.split(',')]
    return Counter(valid_countries)

country_counts = count_countries(df['Country'])
top_10_countries = pd.DataFrame(country_counts.most_common(10), columns=['Country', 'Count'])

# Visualize Top 10 Countries
plt.figure(figsize=(10, 7))
sns.barplot(x='Count', y='Country', data=top_10_countries, palette='magma')
plt.title('Top 10 Content Contributing Countries on Netflix')
plt.xlabel('Total Content Count')
plt.ylabel('Country')
plt.tight_layout()
plt.savefig('Chart_3_Top_10_Countries.png')
plt.close()

# --- 6. Print Key Insights for PPT ---
total_movies = len(df[df['Category'] == 'Movie'])
total_tv_shows = len(df[df['Category'] == 'TV Show'])
ratio = total_movies / total_tv_shows if total_tv_shows else 0

print("\n--- Project Analysis Summary---")
print(f"Total Content Count: {len(df)}")
print(f"Total Movies: {total_movies}")
print(f"Total TV Shows: {total_tv_shows}")
print(f"Ratio of Movies to TV Shows: {ratio:.2f} to 1")
