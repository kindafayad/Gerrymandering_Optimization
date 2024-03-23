import pandas as pd
from gurobipy import Model, GRB, quicksum

# MAX_DISTRICTS = 15
# MIN_DISTRICTS = 0

# Adjust the path to where your adjacency matrix file is located
df = pd.read_csv('data/County_Adjacency_Matrix.csv', header=0, index_col=0)
counties_geoId = df.index # list of all counties geoid 

def check_county_adjacency(county1GeoId, county2GeoId) -> bool:
    return df.loc[county1GeoId, f"{county2GeoId}"]


# Adjust the path to your population projection data file
population_data_path = 'data/downloaded_data/Population_Data.csv'
population_data = pd.read_csv(population_data_path)

# Ensure the 'Total' column is treated as numeric, removing any commas first
# This step is crucial if your data contains commas in the 'Total' population figures
population_data['Total'] = population_data['Total'].astype(str).str.replace(',', '')
population_data['Total'] = pd.to_numeric(population_data['Total'], errors='coerce')

print("Please select a year (2010, 2015, 2020, 2025, 2030, 2035, 2040, 2045, 2050):")
# selected_year = int(input())
selected_year = 2020

while selected_year not in range(2010, 2051, 5):
    print("Invalid selection. Please choose a year in 5-year increments between 2010 and 2050.")
    selected_year = int(input())

# Filter data for the selected year
filtered_data = population_data[population_data['Year'] == selected_year]

# Calculate the total population for the selected year
total_population = filtered_data['Total'].sum()

# Display the total state population for the selected year
print(f"\nTotal State Population in {selected_year}: {total_population}\n")

# Display population data for each county in a table format
# Selecting relevant columns to display
display_columns = ['GEOID', 'County', 'Total', 'Square_Miles']
print(filtered_data[display_columns].to_string(index=False))

#User chooses number of districts
# print("Please enter the minimum number of districts:")
# min_districts = int(input())
# while min_districts < 0 or min_districts > 15:
#     print("Invalid input. The number of districts must be between 0 and 15.")
#     print("Please enter the minimum number of districts again:")
#     min_districts = int(input())

# print("Please enter the maximum number of districts:")
# max_districts = int(input())
# while max_districts < 0 or max_districts > 15 or max_districts < min_districts:
#     if max_districts < min_districts:
#         print("Invalid input. The maximum number of districts cannot be less than the minimum number of districts.")
#     else:
#         print("Invalid input. The number of districts must be between 0 and 15.")
#     print("Please enter the maximum number of districts again:")
#     max_districts = int(input())


max_districts = 10


ideal_pop = total_population / max_districts

# Create a MILP Gurobi model
model = Model("gerrymandering_model")

# Create variables
x = model.addVars(max_districts, len(counties_geoId), vtype=GRB.BINARY, name="x")
# y = model.addVars(max_districts, vtype=GRB.BINARY, name="y")

# District population per district
z = model.addVars(max_districts, vtype=GRB.INTEGER, name="z")
# pop_dev = model.addVars(max_districts, vtype=GRB.INTEGER, name="pop_dev")

# Set objective function
model.setObjective(z.sum(), GRB.MINIMIZE)

# print(x[0, 0])
# Add constraints
for j in range(len(counties_geoId)):
    model.addConstr((quicksum(x[i, j] for i in range(max_districts)) == 1), f"one_district_per_county_{j}")


# model.addConstrs((quicksum(x[i][j] for i in range(max_districts)) == 1 for j in rsange(len(counties_geoId))), "one_district_per_county")
# model.addConstr((y[i] for i in range(max_districts)) >= 0, "Districts_exist")


for i in range(len(counties_geoId)):
    for j in range(len(counties_geoId)):
        if check_county_adjacency(counties_geoId[i], counties_geoId[j]):
            for k in range(max_districts):
                model.addConstr(x[k, i] - x[k, j] == 0 , f"Contiguity_{i}_{j}_{k}")

# # Add adjacency constraints
# for county1 in counties_geoId:
#     for county2 in counties_geoId:
#         if county1 != county2:
#             model.addConstr(districts[county1] + districts[county2] <= 1, f"adjacency_{county1}_{county2}")

percent_offset_ub = 1.05
percent_offset_lb = 0.95

model.addConstrs((z[i] <=  ideal_pop * percent_offset_ub for i in range(max_districts)), "population_upper_bound")
model.addConstrs((z[i] >=  ideal_pop * percent_offset_lb for i in range(max_districts)), "population_lower_bound")

# Optimize the model
model.optimize()

# Check if the model is feasible
if model.status == GRB.OPTIMAL:
    print("Optimal solution found.")
    # Get the selected districts
    print(f"Selected districts: {x.X}")
    # print(f"Selected districts: {y.Y}")
    print(f"Selected districts: {z.Z}")
else:
    print("No feasible solution found.")