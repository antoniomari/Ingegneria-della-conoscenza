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
               "num_of_same_district(C, N) :- findall(C1, same_district(C1, C), L), length(L, N)."]

    kb(clauses)
    obj = kb.query(pytholog.Expr("num_of_same_district(hs227745, N)"))

    if obj is None:
        pass # Do something
    else:
        print(obj)
    pass