import pandas as pd
from gurobipy import Model, GRB, quicksum, min_, max_
import time

from apportionment import estimated_districts_dict
from county_adjacency import check_county_adjacency, counties_geoId
from population import population_data


#Assumptions:
# Only two parties
percent_offset_lb = 0.50
percent_offset_ub = 1.50

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
# district_numb = estimated_districts_dict[selected_year]
# district_numb = 10


def run_model(district_numb):
    # Calculate Ideal popilation
    ideal_pop = total_population / district_numb

    # Create a MILP Gurobi model
    model = Model("gerrymandering_model")

    # Create variables
    x = model.addVars(district_numb, len(counties_geoId), vtype=GRB.BINARY, name="x")

    # District population per district
    z = model.addVars(district_numb, vtype=GRB.INTEGER, ub=(ideal_pop * percent_offset_ub), lb=(ideal_pop * percent_offset_lb), name="z")
    z_min = model.addVar(vtype=GRB.INTEGER, name="z_min")
    z_max = model.addVar(vtype=GRB.INTEGER, name="z_max")

    # Set objective function
    model.setObjective(z_max - z_min, GRB.MINIMIZE)

    # Add constraints
    for j in range(len(counties_geoId)):
        model.addConstr(quicksum(x[i, j] for i in range(district_numb)) == 1, f"one_district_per_county_{j}")

    for i in range(district_numb):
        model.addConstr(quicksum(x[i, j] for j in range(len(counties_geoId))) >= 1, f"more_than_one_district{i}")


    # Add adjacency constraints
    for i in range(len(counties_geoId)):
        for j in range(len(counties_geoId)):
            if check_county_adjacency(counties_geoId[i], counties_geoId[j]):
                # print(f"Adding adjacency constraint for {counties_geoId[i]} and {counties_geoId[j]}")
                for k in range(district_numb):
                    model.addConstr(quicksum((x[k, i], x[k, j])) == 2 , f"Contiguity_{i}_{j}_{k}")

    # Add population constraints
    for i in range(district_numb):
        model.addConstr(quicksum(x[i, j] * int(filtered_population_data[filtered_population_data['GEOID'] == geoid]["Total"].iloc[0]) for j, geoid in enumerate(counties_geoId)) == z[i], f"district_{i}_pop_equals_aggregate_county_pop")

    # Set Auxiliary Variables
    model.addConstr(z_min == min_(z[i] for i in range(district_numb)), "set_z_min")
    model.addConstr(z_max == max_(z[i] for i in range(district_numb)), "set_z_max")

    # Optimize the model
    model.optimize()

    # Check if the model is feasible
    if model.status == GRB.OPTIMAL:
        print("Optimal solution found.")
        for var in x:
            print(f"District: {var[0]}, GEOID: {counties_geoId[var[1]]}, In district?:  {x[var].x}")
        
        for v in model.getVars():
            print(f"{v.varName}: {v.x}")
    else:
        print("No feasible solution found.")

for i in range (7, 10, 1):
    print(f"Running model for iteration {i}")
    run_model(i)
    # time.sleep(3)
