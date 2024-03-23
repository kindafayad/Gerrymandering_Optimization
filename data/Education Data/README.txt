Indiana 2021 Select Educational Attainment Data from the American Community Survey (2017-2021) at the County level

##Redistricting Data Hub (RDH) Retrieval Date
06/02/23

##Sources
ACS data retrieved using the Census API: https://api.census.gov/data/2021/acs/acs5

##Fields
Field Name Description                                                                                                                                                                                                                                                      
GEOID      Unique Geographic Identifier                                                                                                                                                                                                                                                                                                                           
COUNTYFP   County Identifier FIPS                                                                                                                                                                                                                                                      
COUNTY     County Name                                                                                                                                                                                                                                                      
POP_25OV21 Total population 25 years and over (B15003_001E)                                                                                                                                                                                                                 
N_HSDIP21  Less than a high school diploma, GED or equivalent (sum of B15003_002E, B15003_003E, B15003_004E, B15003_005E, B15003_006E, B15003_007E, B15003_008E, B15003_009E, B15003_010E, B15003_011E, B15003_012E, B15003_013E, B15003_014E, B15003_015E, and B15003_016E)

HS_DIP21   High school diploma, GED or equivalent (sum of B15003_017E and B15003_018E)                                                                                                                                                                                      
SOM_COLL21 Some college, no degree (sum of B15003_019E and B15003_020E)                                                                                                                                                                                                     
ASSO_DEG21 Associates Degree (B15003_021E)                                                                                                                                                                                                                                  
BACH_DEG21 Bachelor's Degree (B15003_022E)                                                                                                                                                                                                                                  
MAST_DEG21 Master's Degree (B15003_023E)                                                                                                                                                                                                                                    
PROF_DEG21 Professional school degree (B15003_024E)                                                                                                                                                                                                                         
DOCT_DEG21 Doctorate degree (B15003_025E)                                                                                                                                                                                                                                   

##Processing
ACS data for Indiana was retrieved with a Python script from the Census API.
The county data is available for all counties in Indiana. The script extracted the data for all counties in Indiana. 
Each field represents an estimate from the Census for a particular variable or sum of variables, as noted in the Fields section above.

##Additional Notes
The counts of individuals by educational attainment are for the population of people 25 years and older.
For any questions about this dataset or if you would like additional related ACS data, please email info@redistrictingdatahub.org.