import json
import subprocess

def stringHoursToMinute(str):
    return int(str.split('h')[0]) * 60 + int(str.split('h')[1])

# Load the JSON data from a file
with open('easy/easy_1.json', 'r') as input_json:
    data = json.load(input_json)

# Create a MiniZinc data file
with open('model_data.dzn', 'w') as dataFile:
    dataFile.write(f"numRequests = {len(data['patients'])};\n")
    # Write Same Vehicle Backward
    dataFile.write(f"sameVehicleBackward = {'true' if data['sameVehicleBackward'] else 'false'};\n")
    # Write Max Wait Time
    dataFile.write(f"maxWaitTime = {stringHoursToMinute(data['maxWaitTime'])};\n")

  
    # Write starting points
    dataFile.write(f"start = {list(map(lambda x: x['start'], data['patients']))};\n")
    # Write care center points
    dataFile.write(f"dest = {list(map(lambda x: x['destination'], data['patients']))};\n")
    # Write return points
    dataFile.write(f"ret = {list(map(lambda x: x['end'], data['patients']))};\n")
    # Write sests ocuppied by patient
    dataFile.write(f"l = {list(map(lambda x: x['load'], data['patients']))};\n")
    # Write sests ocuppied by patient
    dataFile.write(f"u = {list(map(lambda x: stringHoursToMinute(x['rdvTime']), data['patients']))};\n")
    # Write sests ocuppied by patient
    dataFile.write(f"d = {list(map(lambda x: stringHoursToMinute(x['rdvDuration']), data['patients']))};\n")
    # Write sests ocuppied by patient
    dataFile.write(f"p = {list(map(lambda x: stringHoursToMinute(data['maxWaitTime']), data['patients']))};\n")
    # Write sests ocuppied by patient
    dataFile.write(f"c = {list(map(lambda x: x['category'], data['patients']))};\n")
    


subprocess.run(["minizinc", "model.mzn", "model_data.dzn"])
