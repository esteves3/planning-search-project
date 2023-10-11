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
    dataFile.write(f"numVehicles = {len(data['vehicles'])};\n")
    # dataFile.write(f"maxCategoryVehicle = {len(max(data['vehicles'], key= lambda x: len(x['canTake']))['canTake'])};\n")
    dataFile.write(f"distMatrixLen = {len(data['distMatrix'])};\n")
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
    # Write seats ocuppied by patient
    dataFile.write(f"l = {list(map(lambda x: x['load'], data['patients']))};\n")
    # Write appointment hour
    dataFile.write(f"u = {list(map(lambda x: stringHoursToMinute(x['rdvTime']), data['patients']))};\n")
    # Write appointment duration
    dataFile.write(f"d = {list(map(lambda x: stringHoursToMinute(x['rdvDuration']), data['patients']))};\n")
    # Write patient duration time to enter the vehicle
    dataFile.write(f"srv = {list(map(lambda x: stringHoursToMinute(x['srvDuration']), data['patients']))};\n")
    # Write wait time
    dataFile.write(f"p = {list(map(lambda x: stringHoursToMinute(data['maxWaitTime']), data['patients']))};\n")
    # Write patient category
    dataFile.write(f"c = {list(map(lambda x: x['category'], data['patients']))};\n")

    # Write vehicles capacity
    dataFile.write(f"k = {list(map(lambda x: x['capacity'], data['vehicles']))};\n")
    # Write patient category
    dataFile.write("C = [")
    for v in data['vehicles']:
        dataFile.write('{')
        for canTake in v['canTake']:
            dataFile.write(f"{canTake},")
        dataFile.write('},')
    dataFile.write("];\n")

    # Write travel times
    dataFile.write("T = [|")
    for row in data['distMatrix']:
        for col in row:
            dataFile.write(f"{col},")
        dataFile.write('|')
    dataFile.write("];\n")
    


subprocess.run(["minizinc", "model.mzn", "model_data.dzn"])
