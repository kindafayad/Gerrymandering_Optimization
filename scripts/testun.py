import gurobipy as gp
from gurobipy import GRB
import pandas as pd
import numpy as np

# Load the data
population_data = pd.read_csv('data/downloaded_data/Population_Data.csv')
adjacency_matrix = pd.read_csv('data/County_Adjacency_Matrix.csv').set_index('Unnamed: 0')

# Prepare data
# Assume we're working with the most recent population estimates for simplicity
filtered_population_data = population_data[population_data['Year'] == 2050]
counties_geoId = filtered_population_data['GEOID'].tolist()
county_populations = filtered_population_data['Total'].str.replace(',', '').astype(int).tolist()

# Parameters
county_numb = len(counties_geoId)
district_numb = 40  # Number of districts

# Create a model
model = gp.Model('Redistricting')

# Decision variables
x = model.addVars(county_numb, county_numb, district_numb, vtype=GRB.BINARY, name="x")
y = model.addVars(county_numb, district_numb, vtype=GRB.BINARY, name="y")
z = model.addVars(district_numb, vtype=GRB.INTEGER, name="z")
z_min = model.addVar(vtype=GRB.INTEGER, name="z_min")
z_max = model.addVar(vtype=GRB.INTEGER, name="z_max")

# Objective: Minimize the difference between the most and least populated districts
model.setObjective(z_max - z_min, GRB.MINIMIZE)

# Constraints
# Population assignment to districts
for k in range(district_numb):
    model.addConstr(z[k] == gp.quicksum(y[i, k] * county_populations[i] for i in range(county_numb)))

model.addConstrs((z_min <= z[k] for k in range(district_numb)), name="MinPop")
model.addConstrs((z_max >= z[k] for k in range(district_numb)), name="MaxPop")

# Each county must be in exactly one district
model.addConstrs((gp.quicksum(y[i, k] for k in range(district_numb)) == 1 for i in range(county_numb)), name="OneDistrict")

# Adjacency constraints
for k in range(district_numb):
    for i in range(county_numb):
        model.addConstr(gp.quicksum(x[i, j, k] for j in range(county_numb) if adjacency_matrix.iloc[i, j] == 1) >= y[i, k])


# Optimize
model.optimize()

# Output
if model.status == GRB.OPTIMAL:
    print("Optimal solution found.")

    for k in range(district_numb):
        outputDf = pd.DataFrame(columns=["County_Name", "County_GEOID", "Population"])
        print(f"District {k} Population: {z[k].x}")
        for i in range(len(counties_geoId)):
            if y[i, k].x > 0.5:  # Using a small threshold to account for floating point arithmetic
                county_info = filtered_population_data[filtered_population_data['GEOID'] == counties_geoId[i]]
                outputDf = outputDf._append({"County_Name": county_info["County"].iloc[0], "County_GEOID": counties_geoId[i], "Population": int(county_info["Total"].iloc[0].replace(',', ''))}, ignore_index=True)
        print(outputDf)
        print("--------------------------------------------------------------------\n")
else:
    print("No feasible solution found.")
