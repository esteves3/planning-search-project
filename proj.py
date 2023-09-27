import json
import subprocess

# Load the JSON data from a file
with open('easy/easy_1.json', 'r') as input_json:
    data = json.load(input_json)

# Create a MiniZinc data file
with open('model_data.dzn', 'w') as data:
    # Write Max Wait Time
    data.write(f"maxWaitTime = \"{data['maxWaitTime']}\";\n")

    # Write Places
    data.write("places = [|")
    for place in data['places']:
        data.write(f"{place['category']}, ")
    data.write("|];\n")

    # Write Vehicles
    data.write("vehicles = [|")
    for vehicle in data['vehicles']:
        data.write(f"{vehicle['canTake']}, {vehicle['start']}, {vehicle['end']}, {vehicle['capacity']}, \"")
        for window in vehicle['availability']:
            data.write(f"{window}, ")
        data.write("\" |];\n")

    # Write Patients
    data.write("patients = [|")
    for patient in data['patients']:
        data.write(f"{patient['category']}, {patient['load']}, {patient['start']}, {patient['destination']}, {patient['end']}, \"{patient['rdvTime']}\", \"{patient['rdvDuration']}\", \"{patient['srvDuration']}\", ")
    data.write("|];\n")

    # Write Distance Matrix
    data.write("distMatrix = [|")
    for row in data['distMatrix']:
        data.write("|")
        for distance in row:
            data.write(f"{distance}, ")
    data.write("|];\n")

    # Write Same Vehicle Backward
    data.write(f"sameVehicleBackward = {data['sameVehicleBackward']};\n")


subprocess.run(["minizinc", "model.mzn"])
