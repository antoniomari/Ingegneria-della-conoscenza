import pandas as pd
from pyswip import Prolog
import pytholog

def kb_usage():

    kb = pytholog.KnowledgeBase("k.pl")
    kb.from_file("facts.pl")

    clauses = ["same_district(C1, C2) :- district(C1, D), district(C2, D).",
               "same_beat(C1, C2) :- beat(C1, B), beat(C2, B).",
               "same_ward(C1, C2) :- ward(C1, W), ward(C2, W).",
               "same_comm_area(C1, C2) :- comm_area(C1, COM), comm_area(C2, COM).",
               "num_of_same_district(X, Count) :- findall(Y, (between(1, 5, Y), Y mod 2 =:= 0), X), length(X, Count)"]

    kb(clauses)
    obj = kb.query(pytholog.Expr("findall(X, same_district(X, hs227745), L)."))

    if obj is None:
        pass # Do something
    else:
        print(obj)
    pass

kb_usage()