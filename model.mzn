int: numRequests;
bool: sameVehicleBackward;
int: maxWaitTime;

array[1..numRequests] of var int: start;
array[1..numRequests] of var int: dest;
array[1..numRequests] of var int: ret;
array[1..numRequests] of var int: l;
array[1..numRequests] of var int: u;
array[1..numRequests] of var int: d;
array[1..numRequests] of var int: p;
array[1..numRequests] of var int: c;


constraint numRequests != 0;

solve satisfy;
