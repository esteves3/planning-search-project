import json
import subprocess
from minizinc import Instance, Model, Solver

def stringHoursToMinute(str):
    return int(str.split('h')[0]) * 60 + int(str.split('h')[1])

model = Model("./model.mzn")
gecode = Solver.lookup("gecode")

instance = Instance(gecode, model)

# Load the JSON data from a file
with open('easy/easy_1.json', 'r') as input_json:
    data = json.load(input_json)

instance['numRequests'] = len(data['patients'])
instance['numVehicles'] = len(data['vehicles'])
instance['distMatrixLen'] = len(data['distMatrix'])
instance['sameVehicleBackward'] = data['sameVehicleBackward']
instance['maxWaitTime'] = stringHoursToMinute(data['maxWaitTime'])
instance['start'] = list(map(lambda x: int(x['start']), data['patients']))
instance['dest'] = list(map(lambda x: int(x['destination']), data['patients']))
instance['ret'] = list(map(lambda x: int(x['end']), data['patients']))
instance['l'] = list(map(lambda x: int(x['load']), data['patients']))
instance['u'] = list(map(lambda x: stringHoursToMinute(x['rdvTime']), data['patients']))
instance['d'] = list(map(lambda x: stringHoursToMinute(x['rdvDuration']), data['patients']))
instance['srv'] = list(map(lambda x: stringHoursToMinute(x['srvDuration']), data['patients']))
instance['p'] = list(map(lambda x: stringHoursToMinute(data['maxWaitTime']), data['patients']))
instance['c'] = list(map(lambda x: int(x['category']), data['patients']))

k = []
C = []
vas = []
vab = []
for v in data['vehicles']:
    for a in v['availability']:
        k.append(int(v['capacity']))
        vas.append(stringHoursToMinute(a.split(':')[0]))
        vab.append(stringHoursToMinute(a.split(':')[1]))
        C.append(set(list(map(lambda x: int(x), v['canTake']))))


instance['k'] = k
instance['C'] = C
instance['vas'] = vas
instance['vab'] = vab
instance['T'] = data['distMatrix']

instance.solve()