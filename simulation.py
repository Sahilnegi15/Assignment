import json
import math
import random



# Calculate Distance
def calculate_distance(point1, point2):
    """
    Calculates Euclidean distance between two points.

    Parameters:
        point1 :
             (x1, y1)

        point2 :
             (x2, y2)

    Returns:
        float: Distance between two points
    """

    x1, y1 = point1
    x2, y2 = point2

    return math.sqrt( (x2 - x1) ** 2 +(y2 - y1) ** 2)



# Read JSON File
def read_json_file(filename):
    """
    Reads and loads JSON data from  file.

    Parameters:
        filename (str):
            Path to JSON file

    Returns:
        dict: Loaded JSON data
    """

    try:
        with open(filename, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        return None

    except json.JSONDecodeError:
        print(f"Error: The file '{filename}' does not contain valid JSON.")
        return None


# Normalize Warehouses
def normalize_warehouses(warehouses):
    """
    Convert warehouse data into a standard dictionary format.

    Parameters:
        warehouses (dict or list)

    Returns:
        dict:Normalized warehouse data
    """

    normalized = {}

    if isinstance(warehouses, dict):

        normalized = warehouses

    else:

        for warehouse in warehouses:

            normalized[ warehouse["id"] ] = warehouse["location"]

    return normalized



# Normalize Agents
def normalize_agents(agents):
    """
    Convert agent data into a standard dictionary format.

    Parameters:
        agents (dict or list)

    Returns:
        dict: Normalized agent data
    """

    normalized = {}

    if isinstance(agents, dict):

        normalized = agents

    else:

        for agent in agents:

            normalized[ agent["id"] ] = agent["location"]

    return normalized


# Normalize Packages

def normalize_packages(packages):
    """
    Correct The  package data structure.

    Parameters:
        packages (list)

    Returns:
        list: Normalized package list
    """

    normalized = []

    for package in packages:

        if "warehouse" in package:

            normalized.append(package)

        else:

            normalized.append({
                "id": package["id"],
                "warehouse": package[
                    "warehouse_id"
                ],
                "destination": package[
                    "destination"
                ]
            })

    return normalized


# Initialize Report

def initialize_report(agents):
    """
    Creates initial performance report structure for all agents.

    Parameters:
        agents (dict)

    Returns:
        dict:  Empty initialized report
    """

    report = {}

    for agent_id in agents:

        report[agent_id] = {
            "packages_delivered": 0,
            "total_distance": 0,
            "efficiency": 0,
            "total_delay": 0
        }

    return report


# Add New Agent Mid-Day
def add_new_agent(agents, report):
    """
    Adds a new delivery agent during midday.

    Parameters:
        agents (dict)
        report (dict)

    Returns:
        None
    """

    new_location = [
        random.randint(0, 100),
        random.randint(0, 100)
    ]

    agents["A_NEW"] = new_location

    report["A_NEW"] = {
        "packages_delivered": 0,
        "total_distance": 0,
        "efficiency": 0,
        "total_delay": 0
    }



# Find Nearest Agent
def find_nearest_agent(agents,warehouse_location ):
    """
    Finds the nearest delivery agent to the warehouse.

    Parameters:
        agents (dict)
        warehouse_location (list)

    Returns:
        str: Nearest agent ID
    """

    nearest_agent = None

    minimum_distance = float("inf")

    for agent_id, location in agents.items():

        distance = calculate_distance(location,warehouse_location)

        if distance < minimum_distance:

            minimum_distance = distance

            nearest_agent = agent_id

    return nearest_agent



# Process Deliveries
def process_deliveries( packages,warehouses,agents, report):
    """
    Simulates package deliveries.

    Parameters:
        packages (list)
        warehouses (dict)
        agents (dict)
        report (dict)

    Returns:
        None
    """
    midpoint = len(packages) // 2

    for index, package in enumerate(packages):

        # Add new agent mid-day
        if index == midpoint:

            add_new_agent( agents, report )

        warehouse_id = package["warehouse"]

        warehouse_location = warehouses[warehouse_id]

        destination = package["destination"]

        # Find nearest agent
        nearest_agent = find_nearest_agent(agents,warehouse_location)

        agent_location = agents[nearest_agent]

        # Distance calculations
        distance1 = calculate_distance(agent_location,warehouse_location)

        distance2 = calculate_distance(warehouse_location,destination)

        base_distance = (distance1 + distance2)

        # Random delay
        delay = random.randint(1, 10)

        total_distance = (base_distance + delay)

        # Update report
        report[nearest_agent]["packages_delivered"] += 1

        report[nearest_agent]["total_distance"] += total_distance

        report[nearest_agent]["total_delay"] += delay

        # Update location
        agents[nearest_agent] = destination


# Calculate Efficiency

def calculate_efficiency(report):
    """
    Calculates delivery efficiency for all agents and determines the best-performing agent.

    Efficiency Formula:
        total_distance / packages_delivered

    Lower value indicates better efficiency.

    Parameters:
        report (dict)

    Returns:
        None
    """

    best_agent = None

    best_efficiency = float("inf")

    for agent_id in report:

        delivered = report[agent_id]["packages_delivered" ]

        total_distance = report[agent_id]["total_distance"]

        if delivered > 0:

            efficiency = (total_distance / delivered )

        else:

            efficiency = 0

        report[agent_id]["total_distance"] = round(total_distance, 2)

        report[agent_id]["efficiency"] = round(efficiency, 2)

        if ( delivered > 0 and efficiency < best_efficiency):

            best_efficiency = efficiency

            best_agent = agent_id

    report["best_agent"] = best_agent


# Run Simulation
def run_simulation(filename):
    """
    Executes complete  simulation.

    Parameters:
        filename (str): Input JSON test case file

    Returns:
        dict: Final simulation report
    """

    data = read_json_file(filename)

    warehouses = normalize_warehouses(data["warehouses"] )

    agents = normalize_agents( data["agents"] )

    packages = normalize_packages(data["packages"])

    report = initialize_report(agents)

    process_deliveries(packages,warehouses,agents,report)

    calculate_efficiency(report)

    return report