import pandas as pd

# Step 1: Import the CSV file using pandas
population_data_path = '/Users/kindafayad/Documents/Year 3/OMIS4000/omis400/final project/Citizenship Data/citizenship.csv'  
population_data = pd.read_csv(population_data_path)

# Step 2: Calculate the population density for each county (people per square mile)
population_data['POP_PER_SQ_MILE'] = population_data['TOT_POP21'] / population_data['SQUARE_MILES']

# Output: Show population density for each county along with GEOID and COUNTY name
print(population_data[['GEOID', 'COUNTY', 'SQUARE_MILES']])  

# Step 3: Calculate overall population distribution statistics
overall_stats = {
    'Mean Population Density': population_data['POP_PER_SQ_MILE'].mean(),
    'Median Population Density': population_data['POP_PER_SQ_MILE'].median(),
    'Standard Deviation of Population Density': population_data['POP_PER_SQ_MILE'].std()
}

# Printing overall statistics
print("Overall Population Distribution Statistics:")
for stat, value in overall_stats.items():
    print(f"{stat}: {value:.2f}")

