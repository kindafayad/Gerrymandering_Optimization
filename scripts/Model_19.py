import pandas as pd
from gurobipy import Model, GRB, quicksum, min_, max_
from apportionment import estimated_districts_dict
from county_adjacency import check_county_adjacency, counties_geoId
from population import population_data

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

district_numb = 50

# Calculate Ideal popilation
ideal_pop = total_population / district_numb

# Create a MILP Gurobi model
model = Model("gerrymandering_model")


# Create variables    
# variables for counties and districts
x = model.addVars(len(counties_geoId), len(counties_geoId), district_numb, vtype=GRB.BINARY, name="x")
y = model.addVars(len(counties_geoId), district_numb, vtype=GRB.BINARY, name="y")

# District population per district
z = model.addVars(district_numb, vtype=GRB.INTEGER, name="z")
z_max = model.addVars(district_numb, vtype=GRB.INTEGER, name="z_max")
z_min = model.addVars(district_numb, vtype=GRB.INTEGER, name="z_min")

# Add constraints to ensure each district exists (one or more counties in the district)
for k in range(district_numb):
    model.addConstr(quicksum(y[i, k] for i in range(len(counties_geoId))) >= 1, f"district_existence_{k}")

# Add constraints to ensure each county is assigned to exactly one district
for i in range(len(counties_geoId)):
    model.addConstr(quicksum(y[i, k] for k in range(district_numb)) == 1, f"county_assignment_{i}")

# Add constraint to ensure that counties are adjacent and also ensure that the county is assigned to the district     
for i in range(len(counties_geoId)):
    for j in range(len(counties_geoId)):
        if i != j:
            for k in range(district_numb):
                model.addConstr(x[i, j, k] <= y[i, k], f"county_assignment_{i}_{j}_{k}")
                model.addConstr(x[i, j, k] <= y[j, k], f"county_assignment_{i}_{j}_{k}")
                model.addConstr(x[i, j, k] >= y[i, k] + y[j, k] - 1, f"county_assignment_{i}_{j}_{k}")
                model.addConstr(x[i, j, k] <= check_county_adjacency(counties_geoId[i], counties_geoId[j]), f"county_assignment_{i}_{j}_{k}")

# Big-M method setup
M = 10000000  # A large constant, adjust based on the maximum possible population

for a in range(district_numb):
    for b in range(len(counties_geoId)):
        pop = int(filtered_population_data.iloc[b]["Total"])  # Assuming this is how you access population

        # Constraints to ensure z_max[a] is at least the population of each county assigned to it
        model.addConstr(z_max[a] >= pop - M * (1 - y[b, a]))

        # Constraints to ensure z_min[a] is no more than the population of any county assigned to it
        model.addConstr(z_min[a] <= pop + M * (1 - y[b, a]))

objective = quicksum(z_max[a] - z_min[a] for a in range(district_numb))

model.setObjective(objective, GRB.MINIMIZE)

model.Params.TimeLimit = 60

# Optimize the model
model.optimize()

# Check if the model is feasible
#if model.status == GRB.OPTIMAL:
print("Optimal solution found.")

for k in range(district_numb):
    outputDf = pd.DataFrame(columns=["County_Name", "County_GEOID", "Population"])

    print(f"District {k} Population: {z[k].x}")
    for i in range(len(counties_geoId)):
        if y[i, k].x: 
            outputDf = outputDf._append({"County_Name": filtered_population_data[filtered_population_data['GEOID'] == counties_geoId[i]]["County"].iloc[0], "County_GEOID": counties_geoId[i], "Population": int(filtered_population_data[filtered_population_data['GEOID'] == counties_geoId[i]]["Total"].iloc[0])}, ignore_index=True)

    print(outputDf)
    print("--------------------------------------------------------------------\n")
        
      
try:
    model.computeIIS()
    model.write("model.ilp")
    print("IIS written to model.ilp")
except Exception as e:
    print(f"An error occurred: {e}")