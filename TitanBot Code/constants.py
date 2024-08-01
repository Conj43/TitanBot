# main file is main.py

# example user input to give to llm
EXAMPLES = [
    {   
        "input": "Can you provide me with the number of accidents that occurred during peak hours?", 
        "query": "SELECT COUNT(*) FROM accidents WHERE strftime('%H', time) BETWEEN '07' AND '09' OR strftime('%H', time) BETWEEN '16' AND '18';"
    },
    {
        "input": "Give me the number of accidents that happened during inclement weather.",
        "query": "SELECT COUNT(*) FROM accidents WHERE WTHR_COND IN ('SNOW', 'FREEZING', 'RAIN') OR RD_SURF_CO IN ('ICE', 'WET', 'SNOW');",
    },
    {
        "input": "Give me the list of counties where accidents occur, sorted by most often to least often.",
        "query": " SELECT COUNTY_NAME,COUNT(COUNTY_NAME) AS count FROM accidents GROUP BY COUNTY_NAME ORDER BY count DESC;",
    },
    {
        "input": "Provide me with the number of accidents that occurred in each season.",
        "query": "SELECT CASE WHEN strftime('%m', time) IN ('06', '07', '08') THEN 'summer' WHEN strftime('%m', time) IN ('12', '01', '02') THEN 'winter' WHEN strftime('%m', time) IN ('03', '04', '05') THEN 'spring' WHEN strftime('%m', time) IN ('09', '10', '11') THEN 'fall' END AS season, COUNT(*) AS number_of_accidents FROM accidents WHERE season IS NOT NULL GROUP BY season;",
    },
    {
        "input": "Return to me the number of rural accidents vs the number of urban accidents that occurred during inclement weather. ",
        "query": "SELECT AREA as area, COUNT(AREA) AS count FROM accidents WHERE (WTHR_COND IN ('SNOW', 'FREEZING', 'RAIN') OR RD_SURF_CO IN ('ICE', 'WET', 'SNOW')) GROUP BY AREA ORDER BY count DESC;",
    },
    {
        "input": "What specific roads have the highest rates of accidents?",
        "query": "SELECT ROUTE, accidents FROM (SELECT ROUTE, COUNT(ROUTE) AS accidents FROM accidents as A GROUP BY ROUTE) AS RouteCounts ORDER BY accidents DESC;",
    },
    {
        "input": "Show me the accidents that occurred in Jackson County during the winter months.",
        "query": "WITH WinterAccidents AS (SELECT * FROM accidents WHERE COUNTY_NAME = 'JACKSON' AND strftime('%m', time) IN ('12', '01', '02')) SELECT LATITUDE, LONGITUDE FROM WinterAccidents;",
    },
    {
        "input": "Tell me how many crashes occurred on a straight portion of road opposed to a curved portion of road. ",
        "query": "SELECT MSHP_ROAD as road, accidents FROM (SELECT MSHP_ROAD, COUNT(MSHP_ROAD) AS accidents FROM accidents AS A GROUP BY MSHP_ROAD) AS RoadCounts ORDER BY accidents DESC;",
    },
    {
        "input": "Provide the population of the city or town where accidents occurred in which the driver ran off the road. ",
        "query": "SELECT POPUL as population FROM accidents WHERE MHTD_ACC_T LIKE '%RAN OFF ROAD%';",
    },
    {
        "input": "Return the injury severity and road surface condition of accidents where a car ran off the road or flipped.",
        "query": "SELECT ACC_SVRTY as injury_severity, RD_SURF_CO as road_surface_condition FROM accidents WHERE MHTD_ACC_T LIKE '%RAN OFF%' OR MHTD_ACC_T LIKE '%OVERTURN%';",
    },
    {
        "input": "Provide me with the top 20 counties with the highest proportion of fatal accidents.",
        "query": "SELECT COUNTY_NAME as county, CAST(SUM(CASE WHEN ACC_SVRTY = 'FATAL' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) AS fatality_rate FROM accidents GROUP BY COUNTY_NAME ORDER BY fatality_rate DESC LIMIT 20;",
    },
    {
        "input": "How many accidents occurred in St Louis County?",
        "query": "SELECT COUNT(*) AS accident_count FROM accidents WHERE COUNTY_NAME = 'ST. LOUIS'",
    },
    {
        "input": "Map all of the accidents that happened in Boone County.",
        "query": "SELECT LATITUDE as latitude, LONGITUDE as longitude FROM accidents WHERE COUNTY_NAME = 'BOONE';",
    },
    {
        "input": "Map all of the accidents that took place while it was dark out.",
        "query": "SELECT LATITUDE as latitude, LONGITUDE as longitude FROM accidents WHERE LIGHT_COND LIKE '%DARK%';",
    },
    {
        "input": "Could you plot the accidents that involved a fatality.",
        "query": "SELECT LATITUDE as latitude, LONGITUDE as longitude FROM accidents WHERE ACC_SVRTY LIKE '%FATAL%';",
    },
    {
        "input": "Plot the crashes that involved a death during daylight.",
        "query": "SELECT LATITUDE as latitude, LONGITUDE as longitude FROM accidents WHERE LIGHT_COND = 'DAYLIGHT' AND ACC_SVRTY = 'FATAL';",
    },
    {
        "input": "What is the average speed on Highway 99?",
        "query": "SELECT AVG(speed) AS average_speed FROM sample WHERE tmc_code IN (SELECT tmc FROM tmc WHERE road = 'HI-99');"
    },
    {
        "input": "Calculate the speed index of area in 2022",
        "query": "SELECT * FROM traffic_data WHERE dt LIKE '2022%'"
    },
    {
        "input": "Find the speed index of area in 2023",
        "query": "SELECT * FROM traffic_data WHERE dt LIKE '2023%'"
    },
    {
        "input": "Make a congestion map of all roads in 2022",
        "query": "SELECT * FROM traffic_data WHERE dt LIKE '2022%'"
    },
    {
        "input": "Calculate the congestion level for link 4610 in 2023",
        "query": "SELECT * FROM traffic_data WHERE link = '4610' AND dt LIKE '2023%'"
    },

      {
        "input": "Are there any roadworks that attest to the change in congestion level in 2022 on link 4610?",
        "query": "SELECT * FROM accident_data WHERE pub_millis LIKE '2022%' AND event_class = 'ROADWORK'; SELECT * FROM traffic_data WHERE link = '4610' AND dt LIKE '2022%';"
    },
    


]



SYSTEM_PREFIX="""Your name is TitanBot. You are an agent designed to interact with a SQL Database.
Here are your steps of action:
1. Receive an input query from the user
2. Determine if the user's input is related to the database
3. If the question does not seem related to the database, you may use your knwowledge to chat with the user, and remind them to try and query the database.
4. Use the sql_db_schema tool to review the schema of all the tables in the database
5. After you have used sql_db_schema, create a syntactically correct {dialect} query to run. 
6. Determine if you need to use one of the tools you have access to
7. Use any tools you need to
8. Return your answer to the user

NOTES:
- DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.
- ALWAYS perform your steps of action in order.
- DO NOT assume example queries will have the same column names as the database you are interacting with
- DO NOT hallucinate, guess or make something up. If the questions is related to the database, you must use a query.
- You have access to these tools: [tti_tool, speed_index_tool, sql_db_query, sql_db_schema, sql_db_list_tables, sql_db_query_checker, map_tool, graph_tool, congestion_map_tool, congestion_level_tool,roadwork_search_tool].
- If you are asked to map something query for the latitudes and longitudes, then use the map tool.
- Provide the output in tabular whenever it is possible
- If you are asked to graph something, use the query results to input information into the graph tool.
- When you graph data, give a high level interpretation of the graph, as if you were a transportation engineer. Use your knowledge to explain why different trends occur.
- NEVER use the map tool and graph tool at the same time. Only use what is asked of you.
- When asked to calculate speed index, generate the query and input it into the speed_index_tool.
- When asked to calculate time travel index, generate the query and input it into the tti_tool.
- An increase in speed index means higher congestion. A decrease in speed index means lower congestion.
- When giving the user numbers, use 5 decimal places.
- Always check the chat history before querying to make sure you don't already have the information the user desires.
- When the user asks to generate a congestion map, input the query into the congestion_map_tool.
- When the user asks to calculate congestion level, input the query into the congestion_level_tool.
- When the user asks to calculate roadworks that attest to change in congestion level, input the query into the roadwork_search_tool.




Here are some examples of user inputs and their corresponding SQL queries:"""


