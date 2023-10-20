include "globals.mzn";
include "cumulative.mzn";


int: numActivities;
int: numVehicles;
int: distMatrixLen;
bool: sameVehicleBackward;
int: maxWaitTime;

set of int: R = 1..numActivities;
set of int: V = 0..<numVehicles;
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
array[R] of int: isForward;


array[V] of int: idsV;
array[V] of int: k;
array[V] of set of int: C;
array[V] of int: sd;
array[V] of int: ed;
array[V] of int: savail;
array[V] of int: eavail;


array[0..<distMatrixLen, 0..<distMatrixLen] of int: T;


%DECISION VARIABLES

array[R] of var 0..1: S;
array[R] of var 0..H: sA;
array[R] of var 0..H: dA;
array[R] of var 0..H: eA;
%array[R] of var 0..1: xA;
array[R] of var V: vA;

constraint forall(r in R)(
    sA[r] >= savail[vA[r]] + T[sd[vA[r]], org[r]]
    /\
    eA[r] <= eavail[vA[r]] - T[dst[r], ed[vA[r]]]
);

constraint forall(r in R)(
    sameVehicleBackward /\ 
    r < numActivities /\ 
    isForward[r] = 1 /\ 
    isForward[min(r + 1, numActivities)] = 0 /\
    idsA[r] = idsA[min(r + 1, numActivities)] /\ (S[r] = 1 \/ S[min(r + 1, numActivities)] = 1)  -> vA[r] = vA[min(r + 1, numActivities)] /\ S[r] = 1 /\ S[min(r + 1, numActivities)] = 1
);

constraint forall(r in R)(
    (S[r] = 1) -> member([j | j in V where c[r] in C[j]], vA[r])
);


constraint forall(r in R)(
    (S[r] = 1) -> 
        (dA[r] = eA[r] - sA[r] /\
        dA[r] >= T[org[r], dst[r]] + 2 * srv[r] /\
        dA[r] >= 0)
);

constraint forall(r in R)(
    (S[r] = 1) ->
        if(isForward[r] = 1) then
            sA[r] >= rdv[r] - maxw[r] /\ sA[r] <= rdv[r]
            /\
            eA[r] >= rdv[r] - maxw[r] /\ eA[r] <= rdv[r]
        else
            sA[r] >= rdv[r] + drdv[r] /\ sA[r] <= rdv[r] + drdv[r] + maxw[r]
            /\
            eA[r] >= rdv[r] + drdv[r] /\ eA[r] <= rdv[r] + drdv[r] + maxw[r]
        endif
);


constraint forall(i, j in R)(
    if(i != j /\ vA[i] = vA[j]) then
        (S[j] = 1 /\ S[i] = 1)
        ->
        (
            sA[j] - sA[i] >= T[org[i], org[j]] + srv[i] \/ sA[i] - sA[j] >= T[org[j], org[i]] + srv[j]
        )
        /\
        (
            sA[j] - eA[i] >= T[dst[i], org[j]] \/ eA[i] - sA[j] >= T[org[j], dst[i]] + srv[j] + srv[i]
        )
        /\
        (
            eA[j] - sA[i] >= T[org[i], dst[j]] + srv[i] + srv[j] \/ sA[i] - eA[j] >= T[dst[j], org[i]]
        )
        /\
        (
            eA[j] - eA[i] >= T[dst[i], dst[j]] + srv[j] \/ eA[i] - eA[j] >= T[dst[j], dst[i]] + srv[i]
        )
    endif
);

constraint forall(v in V)(
    cumulative(
        sA,
        [if S[r] = 1 /\ vA[r] = v then dA[r] else 0 endif | r in R],
        l,
        k[v]
    )
);


solve maximize sum(S);