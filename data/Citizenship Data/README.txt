Indiana 2021 Select Citizenship Data from the American Community Survey (2017-2021) at the County level

##Redistricting Data Hub (RDH) Retrieval Date
05/30/23

##Sources
ACS data retrieved using the Census API: https://api.census.gov/data/2021/acs/acs5

##Fields
Field Name Description                                                                                  
GEOID      Unique Geographic Identifier                                                                 
COUNTYFP   County Identifier                                                                                  
COUNTY     County Name                                                                                  
TOT_POP21  Total population (B05001_001E)                                                               
CIT_TOT21  Total U.S. citizen population (sum of B05001_002E, B05001_003E, B05001_004E, and B05001_005E)
C_US_BRN21 U.S. citizen population born in the United States (B05001_002E)                              
C_PR_BRN21 U.S. citizen population born in Puerto Rico or U.S. Island Areas (B05001_003E)               
C_AB_BRN21 U.S. citizen population born abroad of American parent(s) (B05001_004E)                      
C_NTRLZN21 U.S. citizen by naturalization population (B05001_005E)                                      
NOT_CIT21  Not a U.S. citizen (B05001_006E)                                                             

##Processing
ACS data for Indiana was retrieved with a Python script from the Census API.
The county data is available for all counties in Indiana. The script extracted the data for all counties in Indiana. 
Each field represents an estimate from the Census for a particular variable or sum of variables, as noted in the Fields section above.

##Additional Notes
For any questions about this dataset or if you would like additional related ACS data, please email info@redistrictingdatahub.org.