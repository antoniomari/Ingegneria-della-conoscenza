import pandas as pd
from pyswip import Prolog
import pytholog

def create_kb():

    kb = pytholog.knowledge_base("facts.pl")

    """kb(["same_district(C1, C2) :- district(C1, D), district(C2, D)",
               "same_beat(C1, C2) :- beat(C1, B), beat(C2, B)",
               "same_ward(C1, C2) :- ward(C1, W), ward(C2, W)",
               "same_comm_area(C1, C2) :- comm_area(C1, COM), comm_area(C2, COM)"])"""
    """
    kb([
        "same_district(C1, C2) :- district(C1, D), district(C2, D)",
        # "has_arrest(C, A)", # fact for each copule (crime, arrest)
        #"is_domestic(C) :- location_description(C, apartment); location_description(C, house); "
        #                        "local_description(C, residence); local_description(C, driveway)",
        # "criminal_arrested(C, P) :- has_arrest(C, A), arrested(A, P)",
        # "is_ratial(C) :- criminal_arrested(C, P), victim(C, V), neq(race(V), race(P))",
        # "victim(C, V)",
        "same_beat(C1, C2) :- beat(C1, B), beat(C2, B)",
        "same_ward(C1, C2) :- ward(C1, W), ward(C2, W)",
        "same_comm_area(C1, C2) :- comm_area(C1, COM), comm_area(C2, COM)",
        # "income_area(C, I) :- comm_area(C, COM), income(COM, I)",
        # "num_of_victims(C, N) :- findall(V, victim(V, C), L), length(L, N)",
        # "num_of_crimes_in_district(C, N) :- findall(C1, same_district(C, C1), L), length(L, N)",
        # "is_homicide(C) :- victim(C, V), victimization(V, HOMICIDE)",
        # "num_of_dead(C, N) :- findall(V, (victim(V, C), victimization(V, HOMICIDE), L), count(L, N) "
        ])
        """
        # TODO: distanza coordinate
    print(kb.query(pytholog.Expr("district(C1, 1.0)")))

def use_pyswip():
    prolog = Prolog()
    prolog.consult("facts.pl")

    """clauses = ["same_district(C1, C2) :- district(C1, D), district(C2, D).",
               "same_beat(C1, C2) :- beat(C1, B), beat(C2, B).",
               "same_ward(C1, C2) :- ward(C1, W), ward(C2, W).",
               "same_comm_area(C1, C2) :- comm_area(C1, COM), comm_area(C2, COM)."]"""

    # "has_arrest(C, A)", # fact for each copule (crime, arrest)
    # "is_domestic(C) :- location_description(C, apartment); location_description(C, house); "
    #                        "local_description(C, residence); local_description(C, driveway)",
    # "criminal_arrested(C, P) :- has_arrest(C, A), arrested(A, P)",
    # "is_ratial(C) :- criminal_arrested(C, P), victim(C, V), neq(race(V), race(P))",
    # "victim(C, V)",
    # "income_area(C, I) :- comm_area(C, COM), income(COM, I)",
    # "num_of_victims(C, N) :- findall(V, victim(V, C), L), length(L, N)",
    # "num_of_crimes_in_district(C, N) :- findall(C1, same_district(C, C1), L), length(L, N)",
    # "is_homicide(C) :- victim(C, V), victimization(V, HOMICIDE)",
    # "num_of_dead(C, N) :- findall(V, (victim(V, C), victimization(V, HOMICIDE), L), count(L, N) "


    """for clause in clauses:
        prolog.assertz(clause)"""

    #print(list(prolog.query("district(C1, 1.0).")))

use_pyswip()
#create_kb()

