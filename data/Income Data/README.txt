Indiana 2021 Select Income Data from the American Community Survey (2017-2021) at the County level

##Redistricting Data Hub (RDH) Retrieval Date
05/30/23

##Sources
ACS data retrieved using the Census API: https://api.census.gov/data/2021/acs/acs5

##Fields
Field Name Description                                                                                                                               
GEOID      Unique Geographic Identifier                                                                                                              
COUNTYFP   County Identifier
COUNTY     County Name                                                                                                                               
MEDN_INC21 Median household income in past 12 months (in 2021 inflation-adjusted dollars) (B19013_001E)                                              
TOT_HOUS21 Total households (B19001_001E)                                                                                                            
LESS_10K21 Households with less than $10,000 in household income in the past 12 months (in 2021 inflation-adjusted dollars) (B19001_002E)            
10K_15K21  Households with between $10,000 and $14,999 in household income in the past 12 months (in 2021 inflation-adjusted dollars) (B19001_003E)  
15K_20K21  Households with between $15,000 and $19,999 in household income in the past 12 months (in 2021 inflation-adjusted dollars) (B19001_004E)  
20K_25K21  Households with between $20,000 and $24,999 in household income in the past 12 months (in 2021 inflation-adjusted dollars) (B19001_005E)  
25K_30K21  Households with between $25,000 and $29,999 in household income in the past 12 months (in 2021 inflation-adjusted dollars) (B19001_006E)  
30K_35K21  Households with between $30,000 and $34,999 in household income in the past 12 months (in 2021 inflation-adjusted dollars) (B19001_007E)  
35K_40K21  Households with between $35,000 and $39,999 in household income in the past 12 months (in 2021 inflation-adjusted dollars) (B19001_008E)  
40K_45K21  Households with between $40,000 and $44,999 in household income in the past 12 months (in 2021 inflation-adjusted dollars) (B19001_009E)  
45K_50K21  Households with between $45,000 and $49,999 in household income in the past 12 months (in 2021 inflation-adjusted dollars) (B19001_010E)  
50K_60K21  Households with between $50,000 and $59,999 in household income in the past 12 months (in 2021 inflation-adjusted dollars) (B19001_011E)  
60K_75K21  Households with between $60,000 and $74,999 in household income in the past 12 months (in 2021 inflation-adjusted dollars) (B19001_012E)  
75K_100K21 Households with between $75,000 and $99,999 in household income in the past 12 months (in 2021 inflation-adjusted dollars) (B19001_013E)  
100_125K21 Households with between $100,000 and $124,999 in household income in the past 12 months (in 2021 inflation-adjusted dollars) (B19001_014E)
125_150K21 Households with between $125,000 and $149,999 in household income in the past 12 months (in 2021 inflation-adjusted dollars) (B19001_015E)
150_200K21 Households with between $150,000 and $199,999 in household income in the past 12 months (in 2021 inflation-adjusted dollars) (B19001_016E)
200K_MOR21 Households with more than $200,000 in household income in the past 12 months (in 2021 inflation-adjusted dollars) (B19001_017E)           

##Processing
ACS data for Indiana was retrieved with a Python script from the Census API.
The county data is available for all counties in Indiana. The script extracted the data for all counties in Indiana. 
Each field represents an estimate from the Census for a particular variable, as noted in the Fields section above.
For MEDN_INC21, not all units have values and are recorded as -666666666 by the Census. These are stored as null values in this file, if applicable.

##Additional Notes
For any questions about this dataset or if you would like additional related ACS data, please email info@redistrictingdatahub.org.