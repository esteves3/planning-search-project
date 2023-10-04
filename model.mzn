int: numRequests;
int: numVehicles;
int: maxCategoryVehicle;
int: distMatrixLen;

bool: sameVehicleBackward;
int: maxWaitTime;

array[1..numRequests] of var int: start;
array[1..numRequests] of var int: dest;
array[1..numRequests] of var int: ret;
array[1..numRequests] of var int: l;
array[1..numRequests] of var int: u;
array[1..numRequests] of var int: d;
array[1..numRequests] of var int: srvDuration;
array[1..numRequests] of var int: p;
array[1..numRequests] of var int: c;

array[1..numVehicles] of var int: k;
array[1..numVehicles, 1..maxCategoryVehicle] of int: C;

array[1..distMatrixLen, 1..distMatrixLen] of int: T;


constraint numRequests != 0;

solve satisfy;
