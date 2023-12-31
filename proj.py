import sys
import json
import math
from minizinc import Instance, Model, Solver

print("STARTING...")
def stringHoursToMinute(str):
    return int(str.split('h')[0]) * 60 + int(str.split('h')[1])

def minuteToStringHours(minutes):
    hours, remainder_minutes = divmod(minutes, 60)
    return f"{hours:02d}h{remainder_minutes:02d}"

model = Model("./model.mzn")
gecode = Solver.lookup("gecode")
instance = Instance(gecode, model)

inputfile = sys.argv[1]
outputfile = sys.argv[2]

print("Reading from file: " + inputfile)
# Load the JSON data from a file
with open(inputfile, 'r') as input_json:
    data = json.load(input_json)

idsA = []
org = []
dst = []
srv = []
l = []
rdv = []
drdv = []
maxw = []
c = []
isForward = []

for patient in data['patients']:
    if patient["start"] != -1:
        idsA.append(int(patient["id"]))
        org.append(int(patient["start"]))
        dst.append(int(patient["destination"]))
        srv.append(stringHoursToMinute(patient["srvDuration"]))
        l.append(int(patient["load"]))
        rdv.append(stringHoursToMinute(patient["rdvTime"]))
        drdv.append(stringHoursToMinute(patient["rdvDuration"]))
        maxw.append(stringHoursToMinute(data['maxWaitTime']))
        c.append(patient["category"])
        isForward.append(1)

    if patient["end"] != -1:
        idsA.append(int(patient["id"]))
        org.append(int(patient["destination"]))
        dst.append(int(patient["end"]))
        srv.append(stringHoursToMinute(patient["srvDuration"]))
        l.append(int(patient["load"]))
        rdv.append(stringHoursToMinute(patient["rdvTime"]))
        drdv.append(stringHoursToMinute(patient["rdvDuration"]))
        maxw.append(stringHoursToMinute(data['maxWaitTime']))
        c.append(patient["category"])
        isForward.append(0)


instance['numActivities'] = len(idsA)
instance['numVehicles'] = sum(list(map(lambda x: len(x['availability']), data['vehicles'])))
instance['distMatrixLen'] = len(data['distMatrix'])
instance['sameVehicleBackward'] = data['sameVehicleBackward']
instance['maxWaitTime'] = stringHoursToMinute(data['maxWaitTime'])
instance['idsA'] = idsA
instance['org'] = org
instance['dst'] = dst
instance['srv'] = srv
instance['l'] = l
instance['rdv'] = rdv
instance['drdv'] = drdv
instance['maxw'] = maxw
instance['c'] = c
instance['isForward'] = isForward

idsV = []
k = []
C = []
sd = []
ed = []
savail = []
eavail = []
for v in data['vehicles']:
    for a in v['availability']:
        idsV.append(int(v['id']))
        k.append(int(v['capacity']))
        savail.append(stringHoursToMinute(a.split(':')[0]))
        eavail.append(stringHoursToMinute(a.split(':')[1]))
        sd.append(int(v['start']))
        ed.append(int(v['end']))
        C.append(set(list(map(lambda x: int(x), v['canTake']))))


instance['idsV'] = idsV
instance['k'] = k
instance['C'] = C
instance['sd'] = sd
instance['ed'] = ed
instance['savail'] = savail
instance['eavail'] = eavail


instance['T'] = data['distMatrix']


print("Variables defined, starting model...")
result = instance.solve()
print("Model solved")


print("Defining output...")
outputData = {}
outputList = []
vehicles = []

for i in range(len(idsA)):
    if result['S'][i] == 1:
        outputList.append({
            'id': idsA[i],
            'isForward': isForward[i],
            'startHour': result['sA'][i],
            'startHourS': minuteToStringHours(result['sA'][i]),
            'duration': result['dA'][i],
            'endHour': result['eA'][i],
            'endHourS': minuteToStringHours(result['eA'][i]),
            'vehicle': result['vA'][i],
            'startLoc': org[i],
            'endLoc': dst[i],
            'srv': srv[i]
        })
 
outputList.sort(key=lambda x: (x["startHour"]))



def createTripObject(origin, dest, arrival, patients):
    return {
        "origin": origin,
        "destination": dest,
        "arrival": minuteToStringHours(arrival),
        "patients": list(set(map(lambda x: x["id"], patients)))
    }

#ITERATE OVER THE LENGTH OF VEHICLES (AVAILABILITIES)
for v in range(len(idsV)):
    currentVehicleId = idsV[v]
    trips = []

    #ACTIVITIES MADE BY THIS VEHICLE IN HIS AVALABLE HOURS
    thisVehicleAvailAct = list(filter(lambda x: idsV[x['vehicle']] == currentVehicleId and x['startHour'] >= savail[v] and x['endHour'] <= eavail[v], outputList))
    
    #IF NONE EMPTY LIST
    if len(thisVehicleAvailAct) == 0:
        if len(list(filter(lambda x: x['id'] == currentVehicleId, vehicles))) != 0:
            list(filter(lambda x: x['id'] == currentVehicleId, vehicles))[0]['trips'] += trips
        else:
            vehicles.append({
                "id": currentVehicleId,
                "trips": trips
            })
        continue
    
    #FROM DEPOT TO REQUEST ORIGIN
    trips.append(createTripObject(sd[v], thisVehicleAvailAct[0]["startLoc"], thisVehicleAvailAct[0]["startHour"], []))
    
    patients = []
    lastArrival = thisVehicleAvailAct[0]["startHour"]
    for activityIndex in range(len(thisVehicleAvailAct)):
        currentActivity = thisVehicleAvailAct[activityIndex]

        #WHATS NEXT?!
        veryNextStartHour = next((trip for trip in thisVehicleAvailAct if trip["startHour"] > currentActivity["startHour"] and trip["startLoc"] != currentActivity["startLoc"]), None)
        veryNextEndHour = next((trip for trip in thisVehicleAvailAct if trip["endHour"] > currentActivity["startHour"] and trip["endLoc"] != currentActivity["endLoc"]), None)
        

        #THIS ORIGIN MUST BE LAST TRIP DESTINATION
        origin = trips[-1]["destination"]
        destination = -1
        arrival = "0"
        ifId = 0

        #IF LAST DESTINATION IS NOT THE NEXT ORIGIN: ADD THE TRIP BETWEEN THOSE PLACES
        if currentActivity["startLoc"] != origin and lastArrival < currentActivity["startHour"]:
            trips.append(createTripObject(origin, currentActivity["startLoc"], lastArrival + data["distMatrix"][origin][currentActivity["startLoc"]], patients))
            origin = currentActivity["startLoc"]

        #PATIENTS TRAVELING
        patients.append(currentActivity)
        

        #IF NOTHING START OR ENDS IN BETWEEN THIS ACTIVITY
        if (veryNextEndHour is None or veryNextStartHour is None) or currentActivity["endHour"] < veryNextStartHour["startHour"] and currentActivity["endHour"] < veryNextEndHour["endHour"]:
            lastArrival = currentActivity["endHour"]
            destination = currentActivity["endLoc"]
            arrival = currentActivity["endHour"]
            ifId = 1
        
        #IF SOMETHING STARTS IN BETWEEN
        elif currentActivity["endHour"] > veryNextStartHour["startHour"]:
            lastArrival = veryNextStartHour["startHour"]
            destination = veryNextStartHour["startLoc"]
            arrival = veryNextStartHour["startHour"]
            ifId = 2

        #IF SOMETHING ENDS IN BETWEEN
        elif currentActivity["endHour"] > veryNextEndHour["endHour"]:
            lastArrival = veryNextEndHour["endHour"]
            destination = veryNextEndHour["endLoc"]
            arrival = veryNextEndHour["endHour"]
            ifId = 3
        

        #PATIENTS THAT ARE IN THE VEHICLE AND HAVE THE CURRENT DESTINATION
        thisDestLst = list(filter(lambda x: x["endLoc"] == destination and x["id"] in list(map(lambda p: p["id"], patients)), thisVehicleAvailAct))
        if len(thisDestLst) != 0:
            #REMOVE THE MOST TIME TAKEN SRV
            arrival = arrival - max(map(lambda x: x["srv"], thisDestLst))

        #PUT PATIENTS THAT HAVE THE SAME ORIGIN AT ONCE
        patients = patients + list(filter(lambda x: x["startHour"] < lastArrival and x['endHour'] > lastArrival and x['startLoc'] == origin, thisVehicleAvailAct))


        trips.append(createTripObject(origin, destination, arrival, patients))


        #REMOVE PATIENTS FROM THE VEHICLE THAT WERE DROPPED HERE
        patients = list(filter(lambda x: x["endLoc"] != destination, patients))


    #ADD THE DEPOT RETURN
    trips.append(createTripObject(thisVehicleAvailAct[-1]["endLoc"], ed[v], thisVehicleAvailAct[-1]["endHour"] + data["distMatrix"][thisVehicleAvailAct[-1]["endLoc"]][ed[v]], []))

    if len(list(filter(lambda x: x['id'] == currentVehicleId, vehicles))) != 0:
        list(filter(lambda x: x['id'] == currentVehicleId, vehicles))[0]['trips'] += trips
    else:
        vehicles.append({
            "id": currentVehicleId,
            "trips": trips
        })

outputData['requests'] = len(set(list(map(lambda x: x['id'], outputList))))
outputData['test'] = outputList
outputData['vehicles'] = vehicles

print("Writing output to " + outputfile)
with open(outputfile, 'w') as output:
    output.write(json.dumps(outputData, indent=4))

print("Done")