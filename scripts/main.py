import pandas as pd
from gurobipy import Model, GRB, quicksum, min_, max_
import time

from apportionment import estimated_districts_dict
from county_adjacency import check_county_adjacency, counties_geoId
from population import population_data

#Assumptions:
# Only two parties
# offset = 1
# percent_offset_lb = 1 - offset
# percent_offset_ub = 1 + offset

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
# max_districts = estimated_districts_dict[selected_year]

# max_districts = 10


def run_model(max_districts: int = 100, min_districts:int = 1):
    # Calculate Ideal popilation
    # ideal_pop = total_population / max_districts

    # Create a MILP Gurobi model
    model = Model("gerrymandering_model")


# Create variables    
# variables for counties and districts
    x = model.addVars(len(counties_geoId), len(counties_geoId), max_districts, vtype=GRB.BINARY, name="x")
    y = model.addVars(len(counties_geoId), max_districts, vtype=GRB.BINARY, name="y")

    # Boolean if district exists
    e = model.addVars(max_districts, vtype=GRB.BINARY, name="e")

    A = model.addVars(len(counties_geoId), len(counties_geoId), vtype=GRB.BINARY, name="A")

    # District population per district
    z = model.addVars(max_districts, vtype=GRB.INTEGER, name="z")
    # z = model.addVars(max_districts, vtype=GRB.INTEGER, ub=(ideal_pop * percent_offset_ub), lb=(ideal_pop * percent_offset_lb), name="z")
    z_min = model.addVar(vtype=GRB.INTEGER, name="z_min")
    z_max = model.addVar(vtype=GRB.INTEGER, name="z_max")

    # Set objective function
    model.setObjective(z_max - z_min, GRB.MINIMIZE)

    # Add constraints
    # Constraints for districts existing based on variable e (e stands for district exist)
    model.addConstr(quicksum(e[k] for k in range(max_districts)) >= min_districts, "minimum district_constraint")
    for k in range(max_districts):
        for i in range(len(counties_geoId)):
            for j in range(len(counties_geoId)):
                model.addConstr(x[i, j, k] <= e[k], f"district_existence_{k}_{i}_{j}")

    for k in range(max_districts):
        for i in range(len(counties_geoId)):
            model.addConstr(y[i, k] <= e[k], f"district_existence_{k}_{i}")


    # Add constraints to ensure each county is assigned to exactly one district
    for i in range(len(counties_geoId)):
        model.addConstr(quicksum(y[i, k] for k in range(max_districts)) == 1, f"county_assignment_{i}")


    # Add adjacency matrix constraints
    # for i in range(len(counties_geoId)):
    #     for j in range(len(counties_geoId)):
    #         model.addConstr(A[i, j] == check_county_adjacency(counties_geoId[i], counties_geoId[j]))
                
    # Add constraint to ensure that counties are adjacent and also ensure that the county is assigned to the district
    # x(i,j,k) <= z(i,k)
    # x(i,j,k) <= z(j,k)
    # x(i,j,k) >= z(i,k) + z(j,k) - 1
    # x(i,j,k) <= A(i,j)     
    for i in range(len(counties_geoId)):
        for j in range(len(counties_geoId)):
            for k in range(max_districts):
                model.addConstr(x[i, j, k] <= y[i, k], f"county_assignment_{i}_{j}_{k}")
                model.addConstr(x[i, j, k] <= y[j, k], f"county_assignment_{i}_{j}_{k}")
                model.addConstr(x[i, j, k] >= y[i, k] + y[j, k] - 1, f"county_assignment_{i}_{j}_{k}")
                model.addConstr(x[i, j, k] <= A[i, j], f"county_assignment_{i}_{j}_{k}")

    # Add constraints to ensure that the total population of each district is within the specified bounds (z_min, z_max) 
    # This has already been set in ub and lb
                
    # Add constraint to ensure that population of each district is within the specified bounds (z_min, z_max)
    for k in range(max_districts):
        model.addConstr(z[k] == quicksum(y[i, k] * int(filtered_population_data[filtered_population_data['GEOID'] == counties_geoId[i]]["Total"].iloc[0]) for i in range(len(counties_geoId))), f"district_population_{k}")

    # Set Auxiliary Variables
    # will set to min and max of z
    model.addGenConstrMin(z_min, z, name="set_z_min")
    model.addGenConstrMax(z_max, z, name="set_z_max")

    # Optimize the model
    model.optimize()

    # Check if the model is feasible
    if model.status == GRB.OPTIMAL:
        print("Optimal solution found.")

        for k in range(max_districts):
            outputDf = pd.DataFrame(columns=["County_Name", "County_GEOID", "Population"])

            print(f"District {k} Population: {z[k].x}")
            for i in range(len(counties_geoId)):
                if y[i, k].x: 
                    outputDf = outputDf._append({"County_Name": filtered_population_data[filtered_population_data['GEOID'] == counties_geoId[i]]["County"].iloc[0], "County_GEOID": counties_geoId[i], "Population": int(filtered_population_data[filtered_population_data['GEOID'] == counties_geoId[i]]["Total"].iloc[0])}, ignore_index=True)

            print(outputDf)
            print("--------------------------------------------------------------------\n")
    

        print(z_min.x)
        print(z_max.x)
    else:
        print("No feasible solution found.")

# for i in range (49, 50, 1):
#     print(f"Running model for iteration {i}")
#     run_model()
#     # time.sleep(3)
        

run_model()