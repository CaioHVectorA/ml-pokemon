import pandas as pd

# Read the dataset
df = pd.read_csv('./pokemon.csv')

# Print the first few rows of the dataset

features = df.columns[2:19]