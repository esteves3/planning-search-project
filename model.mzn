
include "cumulative.mzn";

int: numRequests;
set of int: R = 1..numRequests;
int: numVehicles;
int: maxCategoryVehicle;
int: distMatrixLen;

bool: sameVehicleBackward;
int: maxWaitTime;

array[R] of var int: start;
array[R] of var int: dest;
array[R] of var int: ret;
array[R] of var int: l;
array[R] of var int: u;
array[R] of var int: d;
array[R] of var int: srv;
array[R] of var int: p;
array[R] of var int: c;


set of int: V = 1..numVehicles;

array[V] of var int: k;
array[V] of set of int: C;

array[1..distMatrixLen, 1..distMatrixLen] of int: T;


%2
% Declare and initialize the array Si with false for all elements
array[R] of var 0..1: S = [0 | i in R];
%2

%3
array[R] of var int: sf = [0 | i in R];
array[R] of var int: ef = [0 | i in R];
array[R] of var int: df = [ef[i] - sf[i] | i in R];
array[R] of var 0..1: xf = [0 | i in R];
array[R] of var int: vf = [-1 | i in R];

array[R] of var int: sb = [u[i] + d[i] | i in R];
array[R] of var int: eb = [u[i] + d[i] | i in R];
array[R] of var int: db = [eb[i] - sb[i] | i in R];
array[R] of var 0..1: xb = [0 | i in R];
array[R] of var int: vb = [-1 | i in R];
var int: H = 99999;

constraint forall(i in R)(
    df[i] = ef[i] - sf[i] /\
    sf[i] >= 0 /\ sf[i] <= u[i] /\
    ef[i] >= 0 /\ ef[i] <= u[i] /\
    db[i] = eb[i] - sb[i] /\
    sb[i] >= u[i] + d[i] /\ sb[i] <= H /\
    eb[i] >= u[i] + d[i] /\ eb[i] <= H
);

constraint forall(i in R)(
    vf[i] in {j | j in V where c[i] in C[j]} /\
    vb[i] in {j | j in V where c[i] in C[j]} 
);
%3


constraint forall(i in R)(
    %4
    (S[i] = 1) = (xf[i] = 1 \/ xb[i] = 1)
    %4
    /\
    %7
    df[i] >= T[start[i], dest[i]] /\
    db[i] >= T[dest[i], ret[i]]
    %7
    /\
    %8
    df[i] <= p[i] /\
    db[i] <= p[i]
    %8
    /\
    %16
    (not sameVehicleBackward \/ (vf[i] == vb[i]))
    %16
);

%6
constraint forall(i, j in R)(
    if i != j /\ vf[i] == vf[j] then
        (
            sf[j] - sf[i] >= T[start[i], start[j]] + srv[i] 
            \/ 
            sf[i] - sf[j] >= T[start[j], start[i]] + srv[j]
        ) 
        /\
        (
            sf[j] - ef[i] >= T[start[i], dest[j]] 
            \/ 
            ef[i] - sf[j] >= T[dest[j], start[i]] + srv[j] + srv[i]
        ) 
        /\
        (
            ef[j] - sf[i] >= T[dest[i], start[j]] + srv[i] + srv[j]
            \/
            sf[i] - ef[j] >= T[start[j], dest[i]]
        )
        /\
        (
            ef[j] - ef[i] >= T[dest[i], dest[j]] + srv[j]
            \/
            ef[i] - ef[j] >= T[dest[j], dest[i]] + srv[i]
        )
    endif
);
constraint forall(i, j in R) (
    if i != j /\ vb[i] == vb[j] then
        (
            sb[j] - sb[i] >= T[dest[i], dest[j]] + srv[i] 
            \/ 
            sb[i] - sb[j] >= T[dest[j], dest[i]] + srv[j]
        ) 
        /\
        (
            sb[j] - eb[i] >= T[dest[i], ret[j]] 
            \/ 
            eb[i] - sb[j] >= T[ret[j], dest[i]] + srv[j] + srv[i]
        ) 
        /\
        (
            eb[j] - sb[i] >= T[ret[i], dest[j]] + srv[i] + srv[j]
            \/
            sb[i] - eb[j] >= T[dest[j], ret[i]]
        )
        /\
        (
            eb[j] - eb[i] >= T[ret[i], ret[j]] + srv[j]
            \/
            eb[i] - eb[j] >= T[ret[j], ret[i]] + srv[i]
        )
    endif
);
%6

%9

constraint forall(j in V)(
    cumulative(
        [sf[i] | i in R where vf[i] = j /\ xf[i] = 1],
        [df[i] | i in R where vf[i] = j /\ xf[i] = 1],
        [l[i] | i in R where vf[i] = j /\ xf[i] = 1],
        k[j]
    )
);
%9

solve satisfy;
