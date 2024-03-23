Indiana 2021 Select Race Data from the American Community Survey (2017-2021) at the County level

##Redistricting Data Hub (RDH) Retrieval Date
06/01/23

##Sources
ACS data retrieved using the Census API: https://api.census.gov/data/2021/acs/acs5

##Fields
Field Name Description                                                                         
GEOID      Unique Geographic Identifier                                                                                                                          
COUNTYFP   County Identifier                                                                         
COUNTY     County Name                                                                         
TOT_POP21  Total Population (sum of B03002_002E and B03002_012E)                               
NHSP_POP21 Total Population (Not Hispanic/Latino) (B03002_002E)                                
HSP_POP21  Total Population (Hispanic/Latino) (B03002_012E)                                    
WHT_NHSP21 White Alone (Not Hispanic/Latino) (B03002_003E)                                     
BLK_NHSP21 Black or African-American Alone (Not Hispanic/Latino) (B03002_004E)                 
AIA_NHSP21 American Indian and Alaska Native Alone (Not Hispanic/Latino) (B03002_005E)         
ASN_NHSP21 Asian Alone (Not Hispanic/Latino) (B03002_006E)                                     
HPI_NHSP21 Native Hawaiian and Other Pacific Islander Alone (Not Hispanic/Latino) (B03002_007E)
OTH_NHSP21 Some Other Race Alone (Not Hispanic/Latino) (B03002_008E)                           
2OM_NHSP21 Two or More Races (Not Hispanic/Latino) (B03002_009E)                               
BLK_ALL21  Black or African-American Alone or In Combination (B02009_001E)                     
AIA_ALL21  American Indian and Alaska Native Alone or In Combination (B02010_001E)             
ASN_ALL21  Asian Alone or In Combination (B02011_001E)                                         
HPI_ALL21  Native Hawaiian and Other Pacific Islander Alone or In Combination (B02012_001E)    
OTH_ALL21  Some Other Race Alone or In Combination (B02013_001E)                               

##Processing
ACS data for Indiana was retrieved with a Python script from the Census API.
The county data is available for all counties in Indiana. The script extracted the data for all counties in Indiana. 
Each field represents an estimate from the Census for a particular variable or sum of variables, as noted in the Fields section above.

##Additional Notes
For any questions about this dataset or if you would like additional related ACS data, please email info@redistrictingdatahub.org.