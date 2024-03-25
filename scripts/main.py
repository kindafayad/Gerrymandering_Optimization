import pandas as pd
from gurobipy import Model, GRB, quicksum, min_, max_
import time

from apportionment import estimated_districts_dict
from county_adjacency import check_county_adjacency, counties_geoId
from population import population_data


#Assumptions:
# Only two parties
offset = 0.5
percent_offset_lb = 1 - offset
percent_offset_ub = 1 + offset

# selected_year = int(input("Please select a year (2010, 2020, 2030, 2040): "))
# while selected_year not in [2010, 2020, 2030, 2040]:
    # selected_year = int(input("Invalid selection. Please choose a valid year: "))
selected_year = 2010

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
    # z = model.addVars(district_numb, vtype=GRB.INTEGER, name="z")
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
    # for k in range(district_numb):
    #     for i in range(len(counties_geoId)):
    #         for j in range(len(counties_geoId)):
    #             if check_county_adjacency(counties_geoId[i], counties_geoId[j]):
    #                 model.addConstr(x[k, i] + x[k, j] <= 2, f"Contiguity_{i}_{j}_{k}")


    for k in range(district_numb):
        for i in range(len(counties_geoId)):
            model.addConstr(quicksum(x[k, j] * check_county_adjacency(counties_geoId[i], counties_geoId[j]) for j in range(len(counties_geoId))) <= 1, f"Contiguity_{i}_{k}")

    # Add population constraints
    for i in range(district_numb):
        model.addConstr(quicksum(x[i, j] * int(filtered_population_data[filtered_population_data['GEOID'] == geoid]["Total"].iloc[0]) for j, geoid in enumerate(counties_geoId)) == z[i], f"district_{i}_pop_equals_aggregate_county_pop")

    # Set Auxiliary Variables
    model.addGenConstrMin(z_min, z, name="set_z_min")
    model.addGenConstrMax(z_max, z, name="set_z_max")

    # Optimize the model
    model.optimize()

    # Check if the model is feasible
    if model.status == GRB.OPTIMAL:
        print("Optimal solution found.")

        for i in range(district_numb):
            outputDf = pd.DataFrame(columns=["County_Name", "County_GEOID", "Population"])

            print(f"District {i} Population: {z[i].x}")
            for j in range(len(counties_geoId)):
                if x[i, j].x: 
                    outputDf = outputDf._append({"County_Name": filtered_population_data[filtered_population_data['GEOID'] == counties_geoId[j]]["County"].iloc[0], "County_GEOID": counties_geoId[j], "Population": int(filtered_population_data[filtered_population_data['GEOID'] == counties_geoId[j]]["Total"].iloc[0])}, ignore_index=True)

            print(outputDf)
            print("-------------------")
    

        print(z_min.x)
        print(z_max.x)
    else:
        print("No feasible solution found.")

for i in range (8, 10, 1):
    print(f"Running model for iteration {i}")
    run_model(i)
    # time.sleep(3)