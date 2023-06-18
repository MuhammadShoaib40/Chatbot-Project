male(faisal).
male(shoaib).
male(shahood).
male(qasim).
male(saeed).
male(mustafa).
female(shazia).
female(amna).
female(fozia).
female(fatima).
female(summaiyah).
female(tasneem).
parent(faisal,shoaib).
parent(faisal,shahood).
parent(faisal,qasim).
parent(faisal,fatima).
parent(faisal,summaiyah).
parent(shazia,shoaib).
parent(shazia,shahood).
parent(shazia,qasim).
parent(shazia,fatima).
parent(shazia,summaiyah).
parent(saeed,amna).
parent(tasneem,amna).

% Rule: father(X, Y) - X is the father of Y
father(X, Y) :-
    parent(X, Y),
    male(X).

% Rule: mother(X, Y) - X is the mother of Y
mother(X, Y) :-
    parent(X, Y),
    female(X).


% Rule: brother(X, Y) - X is the brother of Y
brother(X, Y) :-
    male(X),
    sibling(X, Y).

% Rule: sister(X, Y) - X is the sister of Y
sister(X, Y) :-
    female(X),
    sibling(X, Y).

sibling(X, Y) :-
    parent(Z, X),
    parent(Z, Y).


% Rule: grandmother(X, Y) - X is the grandmother of Y
grandmother(X, Y) :-
    female(X),
    parent(X, Z),
    parent(Z, Y).

% Rule: grandfather(X, Y) - X is the grandfather of Y
grandfather(X, Y) :-
    male(X),
    parent(X, Z),
    parent(Z, Y).

% Rule: husband(X, Y) - X is the husband of Y
husband(X, Y) :-
    male(X),
    parent(X, Z),
    parent(Y, Z).

% Rule: wife(X, Y) - X is the wife of Y
wife(X, Y) :-
    female(X),
    parent(X, Z),
    parent(Y, Z).

% Rule: mother_sister(X, Y) - X is the sister of Y's mother
mother_sister(X, Y) :-
    mother(M, Y),
    sister(X, M).

% Rule: father_brother(X, Y) - X is the brother of Y's father
father_brother(X, Y) :-
    father(F, Y),
    brother(X, F).

% Rule: mother_brother(X, Y) - X is the brother of Y's mother
mother_brother(X, Y) :-
    mother(M, Y),
    brother(X, M).

% Rule: father_sister(X, Y) - X is the sister of Y's father
father_sister(X, Y) :-
    father(F, Y),
    sister(X, F).

