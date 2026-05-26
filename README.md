## Assignment 

## Approach :

This logistics simulator is built using a rule based greedy simulation approach to model one day of delivery operation for fiction company

## How It Works

1. Load test case JSON file
2. Normalize input data (agents, warehouses, packages)
3. Assign nearest agent to each package
4. Simulate delivery process
5. Track:
   - Distance traveled
   - Delivery count
   - Random delay
6. Compute efficiency
7. Identify best-performing agent
8. Export results



## Folder Structure :

Assignment
├── main.py
├── simulation.py
├── report.json
├── top_performers.csv
└── Test cases


## File contain functions and data:
1.main.py:

1. run_all_test_cases(folder_path)
2. save_report(report, output_file="report.json")
3. export_top_performers(final_report, output_file="top_performers.csv")
4. main()

2.simulation.py:
1. calculate_distance(point1, point2)
2. read_json_file(filename)
3. normalize_warehouses(warehouses)
4. normalize_agents(agents)
5. normalize_packages(packages)
6. find_nearest_agent(agents, warehouse_location)
7. calculate_efficiency(report)
8. run_simulation(filename)

3.report.json:
contain report of all the the executed test cases

4.top_performer.csv:
contain the best agent from all the test cases 

5.Test Cases:
contain all the testcase file in json format



##  Handling Undefined Scenarios:
###  Routing Order:
- Packages are processed **in the order they appear in the input list.
-If the package come at a same time with the same direction then we can assign one rider to that to make it fast and effective 
- No reordering or prioritization is applied during processing.

###  Tie-Breaking:
- If multiple agents are equally suitable (e.g., same distance,same efficiency),then the system selects the first encountered agent in iteration order. if not then it check other factors and decide which it assign to it.
- This ensures deterministic and consistent results.

### Delivery Delay due to Traffic and Other reason:
- for a agent face a this kind of situation for that we can use graph algorithm to show him a alternate fast route to reach the destination 


## Time Complexity Analysis:
- Overall simulation complexity: O(P × A)

### How to Optimize It:
1. Use Spatial Indexing
2. Grid-Based Bucketing