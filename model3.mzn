

int: numActivities;
int: numVehicles;
int: distMatrixLen;
bool: sameVehicleBackward;
int: maxWaitTime;

set of int: R = 1..numActivities;
set of int: V = 1..numVehicles;
int: H = 24 * 60;

array[R] of int: idsA;
array[R] of int: org;
array[R] of int: dst;
array[R] of int: srv;
array[R] of int: l;
array[R] of int: rdv;
array[R] of int: drdv;
array[R] of int: maxw;
array[R] of int: c;


array[V] of int: idsV;
array[V] of int: k;
array[V] of set of int: C;
array[V] of int: sd;
array[V] of int: ed;
array[V] of int: savail;
array[V] of int: eavail;


array[0..<distMatrixLen, 0..<distMatrixLen] of int: T;