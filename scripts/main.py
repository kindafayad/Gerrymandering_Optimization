import pandas as pd
from gurobipy import Model, GRB, quicksum, min_, max_

from apportionment import estimated_districts_dict
from county_adjacency import check_county_adjacency, counties_geoId
from population import population_data


#Assumptions:
# Only two parties
percent_offset_lb = 0.95
percent_offset_ub = 1.05

selected_year = int(input("Please select a year (2010, 2020, 2030, 2040): "))
while selected_year not in [2010, 2020, 2030, 2040]:
    selected_year = int(input("Invalid selection. Please choose a valid year: "))

# Filter data for the selected year
# Filter the population data for the selected year
filtered_population_data = population_data[population_data['Year'] == selected_year]

# Calculate the total population for the selected year
total_population = filtered_population_data['Total'].sum()

# Display the total state population for the selected year
print(f"\nTotal State Population in {selected_year}: {total_population}\n")

# Get the maximum number of districts for the selected year from the projected population and apportionment data
# max_districts = estimated_districts_dict[selected_year]
max_districts = 2

# Calculate Ideal popilation
ideal_pop = total_population / max_districts

# Create a MILP Gurobi model
model = Model("gerrymandering_model")

# Create variables
x = model.addVars(max_districts, len(counties_geoId), vtype=GRB.BINARY, name="x")

# District population per district
z = model.addVars(max_districts, vtype=GRB.INTEGER, ub=(ideal_pop * percent_offset_ub), lb=(ideal_pop * percent_offset_lb), name="z")
z_min = model.addVar(vtype=GRB.INTEGER, name="z_min")
z_max = model.addVar(vtype=GRB.INTEGER, name="z_max")

# Set objective function
model.setObjective(z_max - z_min, GRB.MINIMIZE)

# Add constraints
for j in range(len(counties_geoId)):
    model.addConstr((quicksum(x[i, j] for i in range(max_districts)) == 1), f"one_district_per_county_{j}")

for i in range(max_districts):
    model.addConstr(quicksum(x[i, j] for j in range(len(counties_geoId))) >= 2, name=f"more_than_one_district{i}")


# # Add adjacency constraints
for i in range(len(counties_geoId)):
    for j in range(len(counties_geoId)):
        if check_county_adjacency(counties_geoId[i], counties_geoId[j]):
            for k in range(max_districts):
                model.addConstr(x[k, i] - x[k, j] == 0 , f"Contiguity_{i}_{j}_{k}")

# for county1 in counties_geoId:
#     for county2 in counties_geoId:
#         if county1 != county2:
#             model.addConstr(districts[county1] + districts[county2] <= 1, f"adjacency_{county1}_{county2}")

# Add population constraints
for i in range(max_districts):
    model.addConstrs((quicksum(x[i, j] * (filtered_population_data[filtered_population_data['GEOID'] == geoid]["Total"].iloc[0])) for j, geoid in enumerate(counties_geoId)) == z[i], "population_districts_must_equal_sum_county_populations")

# Set Auxiliary Variables
model.addConstr(z_min == min_(z[i] for i in range(max_districts)), "set_z_min")
model.addConstr(z_max == max_(z[i] for i in range(max_districts)), "set_z_max")

# Optimize the model
model.optimize()

# Check if the model is feasible
if model.status == GRB.OPTIMAL:
    for var in x:
        print(f"District: {var[0]}, GEOID: {counties_geoId[var[1]]}, In district?:  {x[var].x}")
    
    for v in model.getVars():
        print(f"{v.varName}: {v.x}")
else:
    print("No feasible solution found.")