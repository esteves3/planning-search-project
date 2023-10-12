include "cumulative.mzn";
include "globals.mzn";  % Include the globals module for array operations
int: numRequests;
set of int: R = 1..numRequests;
int: numVehicles;
int: distMatrixLen;

bool: sameVehicleBackward;
int: maxWaitTime;

array[R] of int: start;
array[R] of int: dest;
array[R] of int: ret;
array[R] of 1..: l;
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
%2

%3
array[R] of var 0..: sf;
array[R] of var 0..: ef;
array[R] of var 0..: df;
array[R] of var 0..1: xf;
array[R] of var int: vf;

array[R] of var 0..: sb;
array[R] of var 0..: eb;
array[R] of var 0..: db;
array[R] of var 0..1: xb;
array[R] of var int: vb;
int: H = 24 * 60;

constraint forall(i in R)(
    %3
    df[i] = ef[i] - sf[i] /\
    db[i] = eb[i] - sb[i] /\
    member([j | j in V where  c[i] in C[j]], vf[i])  /\
    %14
    sf[i] >= 0 /\ sf[i] <= u[i] - p[i] /\
    ef[i] >= 0 /\ ef[i] <= u[i] - p[i] /\
    sb[i] >= u[i] + d[i] + p[i] /\ sb[i] <= H  /\
    eb[i] >= u[i] + d[i] + p[i] /\ eb[i] <= H  /\
    %14 %3
    %4
    (S[i] = 1) <-> (xf[i] = 1 \/ xb[i] = 1) /* /\
   (xf[i] = 1) <-> start[i] != -1 /\
    (xb[i] = 1) <-> ret[i] != -1*/
    %4
    /\
    %7
    ((start[i] != -1 /\ df[i] >= T[start[i], dest[i]]) \/ start[i] = -1) /\
    ((ret[i] != -1 /\ db[i] >= T[dest[i], ret[i]]) \/ ret[i] = -1)
    %7
    /\
    %8
    df[i] <= p[i] /\ db[i] <= p[i]
    %8
    /\
    %16
    (not sameVehicleBackward \/ (vf[i] = vb[i]))
    %16
);



%6
constraint forall(i, j in R)(
    if i != j /\ vf[i] = vf[j] /\ start[i] != -1 /\ start[j] != -1 
    then
        (
            (sf[j] - sf[i] >= T[start[i], start[j]] + srv[i])
            \/ 
            (sf[i] - sf[j] >= T[start[j], start[i]] + srv[j])
        ) 
        /\
        (
            (sf[j] - ef[i] >= T[start[i], dest[j]])
            \/ 
            (ef[i] - sf[j] >= T[dest[j], start[i]] + srv[j] + srv[i])
        ) 
        /\
        (
            (ef[j] - sf[i] >= T[dest[i], start[j]] + srv[i] + srv[j])
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
    if i != j /\ vb[i] == vb[j] /\ ret[i] != -1 /\ ret[j] != -1 then
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
        [sf[i] * bool2int(vf[i] = j /\ xf[i] = 1) | i in R],
        [df[i] * bool2int(vf[i] = j /\ xf[i] = 1) | i in R],
        [l[i]  * bool2int(vf[i] = j /\ xf[i] = 1) | i in R],
        k[j]
    )
    /\
    cumulative(
        [sb[i] * bool2int(vb[i] = j /\ xb[i] = 1) | i in R],
        [db[i] * bool2int(vb[i] = j /\ xb[i] = 1) | i in R],
        [l[i]  * bool2int(vb[i] = j /\ xb[i] = 1) | i in R],
        k[j]
    )
);

%9

/*
constraint forall(i in R, j in V)(
    %15
    vf[i] = j /\ sf[i] >= vas[j] + T[vstart[j], start[i]]
    /\
    vf[i] = j /\ ef[i] <= vae[j] - T[dest[i], vend[j]]

    /\

    vb[i] = j /\ sb[i] >= vas[j] + T[vstart[j], dest[i]]
    /\
    vb[i] = j /\ eb[i] <= vae[j] - T[ret[i], vend[j]]
    %15
)

*/