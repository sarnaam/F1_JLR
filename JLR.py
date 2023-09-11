# Importing necessary libraries
import json
import requests

# Base URL for Ergast API
ERGAST_BASE_URL = "https://ergast.com/api/f1"

# Function to fetch constructors in the 2023 F1 season
def fetch_constructors_in_2023():
    # Constructing the URL for fetching constructors in 2023
    url = f"{ERGAST_BASE_URL}/2023/constructors.json"
    
    # Sending a GET request to the URL
    response = requests.get(url)
    
    # Checking if the response status code is 200 (Success)
    if response.status_code == 200:
        # Parsing the JSON data from the response
        data = response.json()
        # Extracting constructor data from the JSON
        constructor_data = data.get("MRData", {}).get("ConstructorTable", {}).get("Constructors", [])
        return constructor_data
    else:
        return []

# Function to fetch historical race results for a constructor
def fetch_historical_results_for_constructor(constructor_id):
    # Constructing the URL for fetching results for a specific constructor
    url = f"{ERGAST_BASE_URL}/constructors/{constructor_id}/results.json"
    
    # Sending a GET request to the URL
    response = requests.get(url)
    
    # Checking if the response status code is 200 (Success)
    if response.status_code == 200:
        # Parsing the JSON data from the response
        data = response.json()
        # Extracting race results from the JSON
        race_results = data.get("MRData", {}).get("RaceTable", {}).get("Races", [])
        return race_results
    else:
        return []

# Function to analyze historical performance for a constructor
def analyze_historical_performance(race_results):
    # Dictionary to store points for each circuit
    circuit_points = {}

    # Iterating through each race result
    for race in race_results:
        # Extracting circuit name
        circuit = race.get("Circuit", {}).get("circuitName")
        # Extracting position of the constructor in the race
        position = race.get("Results", [])[0].get("position")

        # Assigning points based on position
        points = 0
        if position == '1':
            points = 25
        elif position == '2':
            points = 18
        elif position == '3':
            points = 15
        elif position == '4':
            points = 12
        elif position == '5':
            points = 10
        elif position == '6':
            points = 8
        elif position == '7':
            points = 6
        elif position == '8':
            points = 4
        elif position == '9':
            points = 2
        elif position == '10':
            points = 1

        # Adding points to the respective circuit
        if circuit not in circuit_points:
            circuit_points[circuit] = 0
        circuit_points[circuit] += points

    # Finding the circuit with the highest points (best performance)
    best_circuit = max(circuit_points, key=circuit_points.get) if circuit_points else None

    return best_circuit

# Function to get the best circuit performances for all constructors in 2023
def get_best_circuit_performances():
    # Fetching constructors in the 2023 F1 season
    constructors_in_2023 = fetch_constructors_in_2023()
    constructor_performance = {}

    # Iterating through each constructor
    for constructor in constructors_in_2023:
        constructor_id = constructor.get("constructorId")
        # Fetching historical race results for the constructor
        race_results = fetch_historical_results_for_constructor(constructor_id)
        # Analyzing the historical performance to get the best circuit
        best_circuit = analyze_historical_performance(race_results)
        # Storing the result in a dictionary
        constructor_performance[constructor["name"]] = best_circuit

    # Returning the result in a dictionary format
    return {"constructor_performance": constructor_performance}

# Main block of code
if __name__ == "__main__":
    # Calling the function to get the best circuit performances
    result = get_best_circuit_performances()
    # Printing the result in a pretty JSON format
    print(json.dumps(result, indent=4))



# OUTPUT JSON    
# {
#     "constructor_performance": {
#         "Alfa Romeo": "Circuit Bremgarten",
#         "AlphaTauri": "Autodromo Nazionale di Monza",
#         "Alpine F1 Team": "Hungaroring",
#         "Aston Martin": "Baku City Circuit",
#         "Ferrari": "Reims-Gueux",
#         "Haas F1 Team": "Bahrain International Circuit",
#         "McLaren": "Aut\u00f3dromo Juan y Oscar G\u00e1lvez",
#         "Mercedes": "Reims-Gueux",
#         "Red Bull": "Albert Park Grand Prix Circuit",
#         "Williams": "N\u00fcrburgring"
#     }
# }
