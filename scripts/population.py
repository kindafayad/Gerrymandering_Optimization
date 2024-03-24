import pandas as pd

# Adjust the path to your population projection data file
population_data_path = 'data/downloaded_data/Population_Data.csv'
population_data = pd.read_csv(population_data_path)

# Ensure the 'Total' column is treated as numeric, removing any commas first
# This step is crucial if your data contains commas in the 'Total' population figures
population_data['Total'] = population_data['Total'].astype(str).str.replace(',', '')
population_data['Total'] = pd.to_numeric(population_data['Total'], errors='coerce')