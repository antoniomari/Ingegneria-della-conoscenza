import pandas as pd

import pytholog

def create_kb():

    kb = pytholog.knowledge_base("crimes.pl")
    kb([
        "same_district(C1, C2) :- district(C1, D), district(C2, D)",
        # "has_arrest(C, A)", # fact for each copule (crime, arrest)
        "is_domestic(C) :- location_description(C, apartment); location_description(C, house); "
                                "local_description(C, residence); local_description(C, driveway)",
        # "criminal_arrested(C, P) :- has_arrest(C, A), arrested(A, P)",
        # "is_ratial(C) :- criminal_arrested(C, P), victim(C, V), neq(race(V), race(P))",
        # "victim(C, V)",
        "same_beat(C1, C2) :- beat(C1, B), beat(C2, B)",
        "same_ward(C1, C2) :- ward(C1, W), ward(C2, W)",
        "same_comm_area(C1, C2) :- comm_area(C1, COM), comm_area(C2, COM)",
        # "income_area(C, I) :- comm_area(C, COM), income(COM, I)",
        # "num_of_victims(C, N) :- findall(V, victim(V, C), L), length(L, N)",
        "num_of_crimes_in_district(C, N) :- findall(C1, same_district(C, C1), L), length(L, N)"
        ])
        # TODO: distanza coordinate

    crimes_df = pd.read_csv("crimes_selected.csv")
    for index, row in crimes_df.iterrows():
        case_num = row['CASE_NUMBER']
        facts = [f"location_description({case_num}, {row['Location Description']})",
                 f"beat({case_num},{row['Beat']})",
                 f"district({case_num},{row['District']})",
                 f"comm_area({case_num},{row['Community Area']})",
                 f"ward({case_num},{row['Ward']})"]
        kb(facts)

    print(kb.query(pytholog.Expr("same_district(C1, C2)")))

create_kb()

