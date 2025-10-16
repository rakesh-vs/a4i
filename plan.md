- Rearchitecture this project. 

first responder
- find user location (from user input, gemini live chat)
- disaster_discovery_agent
    - big_query_data_agent, uses:
        - International Disaster Database
        - Storm Events Database
        - Disaster Declarations Summaries
    - fema_live_agent
        - uses FEMA API
    - noaa_live_agent
        - uses NOAA API

-relief_finder_agent
    - shelter_finder_agent
        - find nearby shelters using map_tool
        - check shelter capacity using big_query_data_agent
    - hospital_finder_agent
        - find nearby hospitals using map tool
        - check hospital capacity using big_query_data_agent
    - supply_finder_agent
        - check supplies using big_query_data_agent


1. big_query_data_agent should be common and should have the capabilties for different use cases
2. map_tool should be common and should have capabilties like
    = find nearby shelters
    - find nearby hospitals
    - find nearby supplies
    - display_disaster_map
    - display_relief_resources_map
    - display_combined_map