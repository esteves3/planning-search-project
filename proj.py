import json
import subprocess

# Load the JSON data from a file
with open('easy/easy_1.json', 'r') as input_json:
    data = json.load(input_json)

# Create a MiniZinc data file
with open('model_data.dzn', 'w') as dataFile:
    # Write Same Vehicle Backward
    dataFile.write(f"sameVehicleBackward = {'true' if data['sameVehicleBackward'] else 'false'};\n")
    # Write Max Wait Time
    maxWaitTime = data['maxWaitTime']
    dataFile.write(f"maxWaitTime = {int(maxWaitTime.split('h')[0]) * 60 + int(maxWaitTime.split('h')[1])};\n")

    # Write Places
    dataFile.write("places = [|")
    for place in data['places']:
        dataFile.write(f"{place['category']}, ")
    dataFile.write("|];\n")

    # Write Vehicles
    dataFile.write("vehicles = [|")
    for vehicle in data['vehicles']:
        dataFile.write(f"{vehicle['canTake']}, {vehicle['start']}, {vehicle['end']}, {vehicle['capacity']}, \"")
        for window in vehicle['availability']:
            dataFile.write(f"{window}, ")
        dataFile.write("\" |];\n")

    # Write Patients
    dataFile.write("patients = [|")
    for patient in data['patients']:
        dataFile.write(f"{patient['category']}, {patient['load']}, {patient['start']}, {patient['destination']}, {patient['end']}, \"{patient['rdvTime']}\", \"{patient['rdvDuration']}\", \"{patient['srvDuration']}\", ")
    dataFile.write("|];\n")

    # Write Distance Matrix
    dataFile.write("distMatrix = [|")
    for row in data['distMatrix']:
        dataFile.write("|")
        for distance in row:
            dataFile.write(f"{distance}, ")
    dataFile.write("|];\n")

    


subprocess.run(["minizinc", "model.mzn", "model_data.dzn"])
