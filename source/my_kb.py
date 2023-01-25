import time

import pandas as pd
from pyswip import Prolog


def create_kb() -> Prolog:
    prolog = Prolog()

    prolog.consult("facts.pl")

    # CLAUSES ABOUT GEO-DATA
    prolog.assertz("same_district(C1, C2) :- district(C1, D), district(C2, D)")
    prolog.assertz("same_beat(C1, C2) :- beat(C1, B), beat(C2, B)")
    prolog.assertz("same_ward(C1, C2) :- ward(C1, W), ward(C2, W)")
    prolog.assertz("same_comm_area(C1, C2) :- comm_area(C1, COM), comm_area(C2, COM)")
    prolog.assertz("same_block(C1, C2) :- block(C1, B), block(C2, B)")
    prolog.assertz("num_of_crimes_in_district(C, N) :- findall(C1, same_district(C, C1), L), length(L, N)")
    prolog.assertz("num_of_crimes_in_beat(C, N) :- findall(C1, same_beat(C, C1), L), length(L, N)")
    prolog.assertz("num_of_crimes_community_area(C, N) :- findall(C1, same_comm_area(C, C1), L), length(L, N)")
    prolog.assertz("num_of_crimes_ward(C, N) :- findall(C1, same_ward(C, C1), L), length(L, N)")
    prolog.assertz("num_of_crimes_block(C, N) :- findall(C1, same_block(C, C1), L), length(L, N)")

    prolog.assertz("criminal_arrested(C, P) :- has_arrest(C, A), arrested(A, P)")
    prolog.assertz("is_ratial(C) :- criminal_arrested(C, P), victim(C, V), "
                   "neq(victim_race(V, VR), criminal_race(P, PR))")
    prolog.assertz("same_zipcode(V1, V2) :- zip_code(V1, Z), zip_code(V2, Z)")
    prolog.assertz("crime_zip_code(C, Z) :- victimization(C, V, T), zip_code(V, Z)")

    prolog.assertz("income_area(C, I) :- comm_area(C, COM), income(COM, I)")

    prolog.assertz("num_of_victims(C, N) :- findall(V, victimization(C, V, T), L), length(L, N)")

    prolog.assertz("num_of_dead(C, N) :- findall(V, victimization(C, V, homicide), L), length(L, N)")
    prolog.assertz("num_of_arrest(C, N) :- findall(S, has_arrest(C, S), L), length(L, N)")
    prolog.assertz("is_homicide(C) :- victimization(C, V, homicide)")
    prolog.assertz("is_killed(V) :- victimization(C, V, homicide)")
    prolog.assertz("is_domestic(C) :- location_description(C, apartment); location_description(C, house); "
                   "local_description(C, residence); local_description(C, driveway)")
    prolog.assertz("night_crime(C) :- crime_date(C, datime(date(Y, M, D, H, M, S))), ((H >= 20; H =< 6))")
    prolog.assertz("crime_data_arrest(C, D) :- has_arrest(C, A), arrest_data(A, D)")
    prolog.assertz("immediate_arrest(C) :- crime_data(C, D), crime_data_arrest(C, D)") # or choose an error of date
    # Add victime_age fact, i.e victim_age(crime, victim)
    prolog.assertz("is_there_a_child(C, T) :- victimization(C, V, T), victim_age(V, A), A =< 15")
    prolog.assertz("is_killed_a_child(C) :- is_there_a_child(C, homicide)")

    prolog.assertz("crime_by_group(C) :- num_of_arrest(C, N), N >= 2")
    prolog.assertz("poverty_of_zone(C, P) :- comm_area(C, COMM), comm_poverty_level(COMM, P)")
    prolog.assertz("instruction_of_zone(C, I) :- comm_area(C, COMM), comm_hs_diploma(COMM, I)")
    prolog.assertz("unemployment_of_zone(C, U) :- comm_area(C, COMM), comm_unemployment(COMM, U)")
    prolog.assertz("homicide_rate_of_zone(C, H) :- comm_area(C, COMM), comm_unemployment(COMM, U)")
    prolog.assertz("firearm_rate_of_zone(C, H) :- comm_area(C, COMM), comm_unemployment(COMM, U)")
    prolog.assertz("street_organization(C, O) :- victimization(C, V, T), street_org(V, O)")

    return prolog


# suppongo che ci sia già
def calculate_features(kb, crime_id) -> dict:
    features_dict = {}
    # num of crimes in district

    features_dict["NUM_CRIMES_DISTRICT"] = list(kb.query(f"num_of_crimes_in_district({crime_id}, N)"))[0]["N"]
    features_dict["NUM_CRIMES_BEAT"] = list(kb.query(f"num_of_crimes_in_beat({crime_id}, N)"))[0]["N"]
    features_dict["NUM_CRIMES_COMM_AREA"] = list(kb.query(f"num_of_crimes_community_area({crime_id}, N)"))[0]["N"]
    features_dict["NUM_CRIMES_WARD"] = list(kb.query(f"num_of_crimes_ward({crime_id}, N)"))[0]["N"]
    features_dict["NUM_CRIMES_BLOCK"] = list(kb.query(f"num_of_crimes_block({crime_id}, N)"))[0]["N"]
    return features_dict


start = time.time()

kb = create_kb()
for crime_id in pd.read_csv("crimes_selected.csv")["CASE_NUMBER"]:
    print(calculate_features(kb, crime_id))

print(pd.read_csv("crimes_selected.csv")["CASE_NUMBER"])

end = time.time()
print("Time: ", end-start)


