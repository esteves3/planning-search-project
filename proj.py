import json
from minizinc import Instance, Model, Solver

def stringHoursToMinute(str):
    return int(str.split('h')[0]) * 60 + int(str.split('h')[1])

model = Model("./model3.mzn")
gecode = Solver.lookup("gecode")

instance = Instance(gecode, model)

# Load the JSON data from a file
with open('easy/easy_1.json', 'r') as input_json:
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


result = instance.solve()

print( result['vf'])
print( result['vb'])
