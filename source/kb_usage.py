import pandas as pd
from pyswip import Prolog
import pytholog

def kb_usage():

    kb = pytholog.knowledge_base("facts.pl")

    kb(["same_district(C1, C2) :- district(C1, D), district(C2, D)",
                "district(c1, d)",
                "district(c2, d)",
               "same_beat(C1, C2) :- beat(C1, B), beat(C2, B)",
               "same_ward(C1, C2) :- ward(C1, W), ward(C2, W)",
               "same_comm_area(C1, C2) :- comm_area(C1, COM), comm_area(C2, COM)"])

    print(kb.query(pytholog.Expr("same_district(X,Y)")))
    pass


