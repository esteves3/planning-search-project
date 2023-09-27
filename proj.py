import json
import subprocess

# Load the JSON data from a file
with open('easy/easy_1.json', 'r') as json_file:
    data = json.load(json_file)

# Create a MiniZinc data file
with open('model_data.dzn', 'w') as dzn_file:
    # Write Max Wait Time
    dzn_file.write(f"maxWaitTime = \"{data['maxWaitTime']}\";\n")

    # Write Places
    dzn_file.write("places = [|")
    for place in data['places']:
        dzn_file.write(f"{place['category']}, ")
    dzn_file.write("|];\n")

    # Write Vehicles
    dzn_file.write("vehicles = [|")
    for vehicle in data['vehicles']:
        dzn_file.write(f"{vehicle['canTake']}, {vehicle['start']}, {vehicle['end']}, {vehicle['capacity']}, \"")
        for window in vehicle['availability']:
            dzn_file.write(f"{window}, ")
        dzn_file.write("\" |];\n")

    # Write Patients
    dzn_file.write("patients = [|")
    for patient in data['patients']:
        dzn_file.write(f"{patient['category']}, {patient['load']}, {patient['start']}, {patient['destination']}, {patient['end']}, \"{patient['rdvTime']}\", \"{patient['rdvDuration']}\", \"{patient['srvDuration']}\", ")
    dzn_file.write("|];\n")

    # Write Distance Matrix
    dzn_file.write("distMatrix = [|")
    for row in data['distMatrix']:
        dzn_file.write("|")
        for distance in row:
            dzn_file.write(f"{distance}, ")
    dzn_file.write("|];\n")

    # Write Same Vehicle Backward
    dzn_file.write(f"sameVehicleBackward = {data['sameVehicleBackward']};\n")



# Run MiniZinc with the model file
subprocess.run(["minizinc", "proj.mzn"])
