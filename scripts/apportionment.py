import pandas as pd

# Replace 'your_file_path.csv' with the path to your actual CSV file
file_path = 'data/National_Population_Projections.csv'

# Load the population data
population_data = pd.read_csv(file_path)

# Ensure the "Population" column is treated as integers
population_data['Population'] = population_data['Population'].str.replace(',', '').astype(int)

# Calculate the total U.S. population for each year
total_us_population_by_year = population_data.groupby('Year')['Population'].sum()

# Function to calculate and print the estimated number of districts for each state and each year
def calculate_districts(data):
    results = []
    indiana_districts = {}

    for year, group in data.groupby('Year'):
        total_population = total_us_population_by_year.loc[year]
        for _, row in group.iterrows():
            estimated_districts = round((row['Population'] / total_population) * 435)
            results.append({
                'State': row['State Names'],
                'Year': year,
                'Estimated Districts': estimated_districts
            })
            if row['State Names'] == 'Indiana':
                indiana_districts[year] = estimated_districts
    return indiana_districts

# Execute the function and get the estimated districts
estimated_districts_dict = calculate_districts(population_data)