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

model = Model("./model3.mzn")
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

for i in range(len(idsA)):
    if result['S'][i] == 1:
        outputList.append({
            'id': idsA[i],
            'isForward': isForward[i],
            'startHour': minuteToStringHours(result['sA'][i]),
            'duration': minuteToStringHours(result['dA'][i]),
            'endHour': minuteToStringHours(result['eA'][i]),
            'vehicle': result['vA'][i]
        })

outputData['trips'] = outputList

print("Writing output to " + outputfile)
with open(outputfile, 'w') as output:
    output.write(json.dumps(outputData, indent=4))

print("Done")