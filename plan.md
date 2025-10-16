clean up big data query agent.

I just want the following funationalities:

get_available_shelter_info
required fields: lat, long
optional fields: min_beds, onsite_medical_clinic
eg query:
SELECT
 NAME, ADDRESS, CITY, STATE, ZIPCODE, WARD, PROVIDER, TYPE, SUBTYPE, STATUS, NUMBER_OF_BEDS, ON_SITE_MEDICAL_CLINIC, AGES_SERVED, HOW_TO_ACCESS, LGBTQ_FOCUSED, LATITUDE, LONGITUDE 
FROM
  qwiklabs-gcp-00-fb4bb5fddc00.c4datasetnew.Shelter where where LATITUDE = 37.7599 and LONGITUDE = -122.4449 and NUMBER_OF_BEDS > 0 and ON_SITE_MEDICAL_CLINIC = 'Yes'


get_ongoing_storms_info
required fields: lat, long
eg query:
SELECT YEARMONTH,EPISODE_ID, LOCATION_INDEX, RANGE, AZIMUTH, LOCATION, LATITUDE, LONGITUDE FROM qwiklabs-gcp-00-fb4bb5fddc00.c4datasetnew.StormLocations where LATITUDE = 37.7599 and LONGITUDE = -122.4449


check_hospital_capacity (placeholder)

check_supply_inventory (placeholder)
