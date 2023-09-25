import json

# Read the input data from a JSON file
with open('easy/easy_1.json', 'r') as file:
    data = json.load(file)

# Extract data from the JSON
maxWaitTime = data["maxWaitTime"]
places = data["places"]
vehicles = data["vehicles"]
patients = data["patients"]
distMatrix = data["distMatrix"]
sameVehicleBackWard = data["sameVehicleBackWard"]

# Now you can access the extracted data as needed.
# For example, to print the maxWaitTime:
print("Max Wait Time:", maxWaitTime)

# To iterate through the places:
for place in places:
    id = place["id"]
    category = place["category"]
    print(f"Place ID: {id}, Category: {category}")

# To iterate through the vehicles:
for vehicle in vehicles:
    id = vehicle["id"]
    canTake = vehicle["canTake"]
    start = vehicle["start"]
    end = vehicle["end"]
    capacity = vehicle["capacity"]
    availability = vehicle["availability"]
    print(f"Vehicle ID: {id}, Can Take: {canTake}, Start Depot: {start}, End Depot: {end}, Capacity: {capacity}, Availability: {availability}")

# To iterate through the patients:
for patient in patients:
    id = patient["id"]
    category = patient["category"]
    load = patient["load"]
    start = patient["start"]
    destination = patient["destination"]
    end = patient["end"]
    rdvTime = patient["rdvTime"]
    rdvDuration = patient["rdvDuration"]
    srvDuration = patient["srvDuration"]
    print(f"Patient ID: {id}, Category: {category}, Load: {load}, Start: {start}, Destination: {destination}, End: {end}, RDV Time: {rdvTime}, RDV Duration: {rdvDuration}, Service Duration: {srvDuration}")

# To access the distance matrix:
print("Distance Matrix:")
for row in distMatrix:
    print(row)

# To access the sameVehicleBackWard flag:
print("Same Vehicle Backward:", sameVehicleBackWard)
