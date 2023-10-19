include "cumulative.mzn";
include "globals.mzn";  % Include the globals module for array operations
int: numRequests;
set of int: R = 1..numRequests;
int: numVehicles;
int: distMatrixLen;

bool: sameVehicleBackward;
int: maxWaitTime;
int: H = 24 * 60;
array[R] of int: start;
array[R] of int: dest;
array[R] of int: ret;
array[R] of int: l;
array[R] of int: u;
array[R] of int: d;
array[R] of int: srv;
array[R] of int: p;
array[R] of int: c;


set of int: V = 1..numVehicles;

array[V] of set of int: C;
array[V] of int: k;
array[V] of int: vas;
array[V] of int: vae;
array[V] of int: vstart;
array[V] of int: vend;

array[0..<distMatrixLen, 0..<distMatrixLen] of int: T;

%2
array[R] of var 0..1: S;
%3
%FORWARD
array[R] of var 0..H: sf;
array[R] of var 0..H: ef;
array[R] of var 0..1: xf;
array[R] of var V: vf;
%BACKWARD
array[R] of var 0..H: sb;
array[R] of var 0..H: eb;
array[R] of var 0..1: xb;
array[R] of var V: vb;

constraint forall(i in R)(
    ef[i] - sf[i] >= 0
    /\ sf[i] >= 0 
    /\ sf[i] <= u[i] - maxWaitTime
    /\ ef[i] >= 0 
    /\ ef[i] <= u[i] - maxWaitTime
    /\ member([j | j in V where c[i] in C[j]], vf[i])
);

constraint forall(i in R)(
    eb[i] - sb[i] >= 0 
    /\ sb[i] >= u[i] + d[i] + maxWaitTime %14
    /\ sb[i] <= H 
    /\ eb[i] >= u[i] + d[i] + maxWaitTime %14
    /\ eb[i] <= H 
    /\ member([j | j in V where c[i] in C[j]], vb[i])
);

%4
constraint forall(i in R)(
    (S[i] = 1) -> (xf[i] = 1 \/ xb[i] = 1)
);

constraint forall(i in R)(
    (xf[i] = 1) -> (start[i] != -1)
);

constraint forall(i in R)(
    (xb[i] = 1) -> (ret[i] != -1)
);

/*
%6
%FORWARD - FORWARD
constraint forall(i, j in R)(
    if i != j /\ xf[i] = 1 /\ start[i] != -1 /\ xf[j] = 1 /\ start[j] != -1 then
        (vf[i] = vf[j]) -> 
                        (sf[j] - sf[i] >= T[start[i], start[j]] + srv[i]
                        \/ sf[i] - sf[j] >= T[start[j], start[i]] + srv[j])
    endif
);
constraint forall(i, j in R)(
    if i != j /\ xf[i] = 1 /\ start[i] != -1 /\ xf[j] = 1 /\ start[j] != -1 then
        (vf[i] = vf[j]) -> 
                        (sf[j] - ef[i] >= T[start[i], dest[j]]
                        \/ ef[i] - sf[j] >= T[dest[j], start[i]] + srv[j] + srv[i])
    endif
);
constraint forall(i, j in R)(
    if i != j /\ xf[i] = 1 /\ start[i] != -1 /\ xf[j] = 1 /\ start[j] != -1 then
        (vf[i] = vf[j]) -> 
                        (ef[j] - sf[i] >= T[dest[i], start[j]] + srv[i] + srv[j]
                        \/ sf[i] - ef[j] >= T[start[j], dest[i]])
    endif
);
constraint forall(i, j in R)(
    if i != j /\ xf[i] = 1 /\ start[i] != -1 /\ xf[j] = 1 /\ start[j] != -1 then
        (vf[i] = vf[j]) -> 
                        (ef[j] - ef[i] >= T[dest[i], dest[j]] + srv[j]
                        \/ ef[i] - ef[j] >= T[dest[j], dest[i]] + srv[i])
    endif
);

%BACKWARD - BACKWARD
constraint forall(i, j in R)(
    if i != j /\ xb[i] = 1 /\ start[i] != -1 /\ xb[j] = 1 /\ start[j] != -1 then
        (vb[i] = vb[j]) -> 
                        (sb[j] - sb[i] >= T[start[i], start[j]] + srv[i]
                        \/ sb[i] - sb[j] >= T[start[j], start[i]] + srv[j])
    endif
);
constraint forall(i, j in R)(
    if i != j /\ xb[i] = 1 /\ start[i] != -1 /\ xb[j] = 1 /\ start[j] != -1 then
        (vb[i] = vb[j]) -> 
                        (sb[j] - eb[i] >= T[start[i], dest[j]]
                        \/ eb[i] - sb[j] >= T[dest[j], start[i]] + srv[j] + srv[i])
    endif
);
constraint forall(i, j in R)(
    if i != j /\ xb[i] = 1 /\ start[i] != -1 /\ xb[j] = 1 /\ start[j] != -1 then
        (vb[i] = vb[j]) -> 
                        (eb[j] - sb[i] >= T[dest[i], start[j]] + srv[i] + srv[j]
                        \/ sb[i] - eb[j] >= T[start[j], dest[i]])
    endif
);
constraint forall(i, j in R)(
    if i != j /\ xb[i] = 1 /\ start[i] != -1 /\ xb[j] = 1 /\ start[j] != -1 then
        (vb[i] = vb[j]) -> 
                        (eb[j] - eb[i] >= T[dest[i], dest[j]] + srv[j]
                        \/ eb[i] - eb[j] >= T[dest[j], dest[i]] + srv[i])
    endif
);
*/
%7
constraint forall(i in R)(
    if (xf[i] = 1 /\ start[i] != -1) then 
        ((ef[i] - sf[i]) >= T[start[i], dest[i]]) 
    endif
);

constraint forall(i in R)(
    if (xb[i] = 1 /\ ret[i] != -1) then 
        ((eb[i] - sb[i]) >= T[dest[i], ret[i]]) 
    endif
);

%8
constraint forall(i in R)(
    ef[i] - sf[i] <= p[i]
);
constraint forall(i in R)(
    eb[i] - sb[i] <= p[i]
);


%9

constraint forall(j in V)(
    cumulative(
        [sf[i] * bool2int(vf[i] = j /\ xf[i] = 1 /\ start[i] != -1) | i in R],
        [max(ef[i] - sf[i], 0) * bool2int(vf[i] = j /\ xf[i] = 1 /\ start[i] != -1) | i in R],
        [l[i] * bool2int(vf[i] = j /\ xf[i] = 1 /\ start[i] != -1) | i in R],
        k[j]
    )
);

constraint forall(j in V)(
    cumulative(
        [sb[i] * bool2int(vb[i] = j /\ xb[i] = 1 /\ ret[i] != -1) | i in R],
        [max(eb[i] - sb[i], 0) * bool2int(vb[i] = j /\ xb[i] = 1 /\ ret[i] != -1) | i in R],
        [l[i] * bool2int(vb[i] = j /\ xb[i] = 1 /\ ret[i] != -1) | i in R],
        k[j]
    )
);


%15
/*constraint forall(i in R)(
    sf[i] >= 
);*/

solve maximize sum(S);
