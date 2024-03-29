import pandas as pd
from gurobipy import Model, GRB, quicksum

# Prompt user for the year and number of districts
years = [2010, 2015, 2025, 2030, 2035, 2040, 2050]
year = int(input(f"Enter the year {years}: "))
while year not in years:
    year = int(input(f"Invalid year. Please enter a year from {years}: "))
d = int(input("Enter the number of districts: "))

# Load the population data
population_data_path = "data/downloaded_data/Population_Data.csv"
population_data = pd.read_csv(population_data_path)

# Load the adjacency matrix
adjacency_matrix_path = "data/County_Adjacency_Matrix.csv"
adjacency_matrix = pd.read_csv(adjacency_matrix_path)

# Preprocessing the population data for the selected year
selected_year_population_data = population_data[population_data['Year'] == year]
simplified_population_data = selected_year_population_data[['GEOID', 'Total']].copy()
simplified_population_data['Total'] = simplified_population_data['Total'].str.replace(',', '').astype(int)

# Adjusting and aligning the adjacency matrix with the population data's GEOIDs
adjacency_matrix_cleaned = adjacency_matrix.set_index('Unnamed: 0')
adjacency_matrix_cleaned.index = adjacency_matrix_cleaned.index.astype(int)
adjacency_matrix_cleaned.columns = adjacency_matrix_cleaned.columns.astype(int)

common_geoids = list(set(simplified_population_data['GEOID']).intersection(set(adjacency_matrix_cleaned.index)))
simplified_population_data = simplified_population_data[simplified_population_data['GEOID'].isin(common_geoids)]
simplified_population_data.reset_index(drop=True, inplace=True)
adjacency_matrix_aligned = adjacency_matrix_cleaned.loc[common_geoids, common_geoids]

# Convert the aligned adjacency matrix to a numpy array for the Gurobi model
A = adjacency_matrix_aligned.to_numpy()

# Initialize the Gurobi model
model = Model("Redistricting")
n = len(simplified_population_data)  # Number of counties

# Decision variables: x[i, j] = 1 if county i is assigned to district j
x = model.addVars(n, d, vtype=GRB.BINARY, name="assignment")

# Variable for each district's population
district_pops = model.addVars(d, vtype=GRB.INTEGER, name="district_pop")

# Calculate the total population and average district population
total_population = sum(simplified_population_data['Total'])
average_population = total_population / d

# Assignment constraint for each county to be assigned to one district
for i in range(n):
    model.addConstr(quicksum(x[i, j] for j in range(d)) == 1, name=f"county_assignment_{i}")

# Constraints to calculate the population of each district
for j in range(d):
    model.addConstr(district_pops[j] == quicksum(x[i, j] * simplified_population_data.loc[i, 'Total'] for i in range(n)), name=f"pop_district_{j}")

# Auxiliary variables and constraints for absolute deviations
abs_devs = model.addVars(d, vtype=GRB.INTEGER, name="abs_devs")
for j in range(d):
    model.addConstr(abs_devs[j] >= district_pops[j] - average_population, name=f"dev_pos_{j}")
    model.addConstr(abs_devs[j] >= -(district_pops[j] - average_population), name=f"dev_neg_{j}")

# Objective: Minimize the sum of absolute deviations from the average population
model.setObjective(quicksum(abs_devs[j] for j in range(d)), GRB.MINIMIZE)

# Contiguity constraints to ensure districts are connected
for k in range(d):
    for i in range(n):
        neighbors = [j for j in range(n) if A[i, j] == 1]
        if neighbors:  # If county i has neighbors
            model.addConstr(x[i, k] <= quicksum(x[j, k] for j in neighbors), name=f"contiguity_{i}_{k}")

# Adjacency constraint: Ensure counties in the same district are adjacent
for k in range(d):
    for i in range(n):
        for j in range(n):
            if i != j and A[i, j] == 0:  # Non-adjacent counties
                model.addConstr(x[i, k] + x[j, k] <= 1, name=f"non_adj_{i}_{j}_{k}")

# Setting a time limit for the optimization
model.Params.TimeLimit = 60

# Solve the optimization model
model.optimize()

# Assuming the optimization model has been solved

if model.status == GRB.OPTIMAL or model.status == GRB.TIME_LIMIT:
    print("Optimal solution found.\n")
    district_info = {j: {'details': [], 'population': 0} for j in range(d)}
    
    for i in range(n):
        for j in range(d):
            if x[i, j].X > 0.5:  # If county i is assigned to district j
                geo_id = simplified_population_data.iloc[i]['GEOID']
                county_name = selected_year_population_data[selected_year_population_data['GEOID'] == geo_id]['County'].values[0]
                county_population = simplified_population_data.iloc[i]['Total']
                district_info[j]['details'].append((geo_id, county_name, county_population))
                district_info[j]['population'] += county_population

    print("\n")  # Skip a line before printing variance information

    # Calculating and printing the variance of district populations
    district_populations = [district_info[j]['population'] for j in range(d)]
    mean_population = round(sum(district_populations) / d, 2)  # Rounded
    variance_population = round(sum((x - mean_population) ** 2 for x in district_populations) / d, 2)  # Rounded
    
    # Calculating variance percentage
    variance_percentage = round((variance_population / mean_population) * 100, 2)
    
    print(f"Mean District Population: {mean_population}")
    print(f"Variance of District Populations: {variance_population}")
    print(f"Variance Percentage: {variance_percentage}%\n")  # Printing variance percentage

    # Print the output for each district
    for j in district_info:
        print(f"District Number: {j + 1}, Total Population: {district_info[j]['population']}")
        for detail in district_info[j]['details']:
            print(f"GEOID {detail[0]}, County {detail[1]}, Population {detail[2]}")
        print()  # New line for better readability
else:
    print("No optimal solution found within the time limit.")
