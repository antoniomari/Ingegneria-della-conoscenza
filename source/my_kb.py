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

    # CLAUSES ABOUT GEO-DATA coming from
    prolog.assertz("crime_zip_code(C, Z) :- victimization(C, V, T), zip_code(V, Z)")
    prolog.assertz("same_zip_code(C1, C2) :- crime_zip_code(C1, Z), crime_zip_code(C2, Z)")
    prolog.assertz("num_of_crimes_in_zip_code(C, N) :- findall(C1, same_zip_code(C, C1), L), length(L, N)")

    prolog.assertz("criminal_arrested(C, P) :- has_arrest(C, A), arrested(A, P)")
    prolog.assertz("is_ratial(C) :- criminal_arrested(C, P), victim(C, V), "
                   "neq(victim_race(V, VR), criminal_race(P, PR))")

    prolog.assertz("crime_area_income(C, I) :- comm_area(C, COM), comm_income(COM, I)")
    prolog.assertz("crime_area_assault_homicide(C, I) :- comm_area(C, COM), comm_assault_homicide(COM, I)")
    prolog.assertz("crime_area_firearm(C, I) :- comm_area(C, COM), comm_firearm(COM, I)")
    prolog.assertz("crime_area_poverty_level(C, I) :- comm_area(C, COM), comm_poverty_level(COM, I)")
    prolog.assertz("crime_area_hs_diploma(C, I) :- comm_area(C, COM), comm_hs_diploma(COM, I)")
    prolog.assertz("crime_area_unemployment(C, I) :- comm_area(C, COM), comm_unemployment(COM, I)")
    prolog.assertz("crime_area_birth_rate(C, I) :- comm_area(C, COM), comm_birth_rate(COM, I)")

    prolog.assertz("num_of_victims(C, N) :- findall(V, victimization(C, V, T), L), length(L, N)")

    prolog.assertz("num_of_dead(C, N) :- findall(V, victimization(C, V, homicide), L), length(L, N)")
    prolog.assertz("num_of_arrest(C, N) :- findall(S, has_arrest(C, S), L), length(L, N)")
    prolog.assertz("is_homicide(C) :- victimization(C, V, homicide)")
    prolog.assertz("is_killed(V) :- victimization(C, V, homicide)")
    prolog.assertz("is_domestic(C) :- location_description(C, apartment); location_description(C, house); "
                   "location_description(C, residence); location_description(C, driveway)")
    prolog.assertz("night_crime(C) :- crime_date(C, datime(date(Y, M, D, H, M, S))), ((H >= 20; H =< 6))")
    prolog.assertz("crime_data_arrest(C, D) :- has_arrest(C, A), arrest_data(A, D)")
    prolog.assertz("immediate_arrest(C) :- crime_data(C, D), crime_data_arrest(C, D)") # or choose an error of date
    # Add victime_age fact, i.e victim_age(crime, victim)
    prolog.assertz("is_there_a_child(C, T) :- victimization(C, V, T), victim_age(V, A), A =< 15")
    prolog.assertz("is_killed_a_child(C) :- is_there_a_child(C, homicide)")

    prolog.assertz("crime_by_group(C) :- num_of_arrest(C, N), N >= 2")
    prolog.assertz("street_organization(C, O) :- victimization(C, V, T), street_org(V, O)")
    prolog.assertz("has_street_organization(C) :- street_organization(C, O)")
    prolog.assertz("same_street_organization(C1, C2) :- street_organization(C1, O), street_organization(C2, O)")
    # TODO: controllare il seguente
    prolog.assertz("num_of_crimes_street_organization(C, N) :- "
                   "findall(C1, same_street_organization(C, C1), L), length(L, N)")

    return prolog


# suppongo che ci sia già
def calculate_features(kb, crime_id) -> dict:
    features_dict = {}

    features_dict["NUM_CRIMES_DISTRICT"] = list(kb.query(f"num_of_crimes_in_district({crime_id}, N)"))[0]["N"]
    features_dict["NUM_CRIMES_BEAT"] = list(kb.query(f"num_of_crimes_in_beat({crime_id}, N)"))[0]["N"]
    features_dict["NUM_CRIMES_COMM_AREA"] = list(kb.query(f"num_of_crimes_community_area({crime_id}, N)"))[0]["N"]
    features_dict["NUM_CRIMES_WARD"] = list(kb.query(f"num_of_crimes_ward({crime_id}, N)"))[0]["N"]
    features_dict["NUM_CRIMES_BLOCK"] = list(kb.query(f"num_of_crimes_block({crime_id}, N)"))[0]["N"]
    features_dict["NUM_CRIMES_ZIP_CODE"] = list(kb.query(f"num_of_crimes_in_zip_code({crime_id}, N)"))[0]["N"]
    features_dict["NUM_CRIMES_STREET_ORG"] = list(kb.query(f"num_of_crimes_street_organization({crime_id}, N)"))[0]["N"]

    features_dict["AREA_INCOME"] = list(kb.query(f"crime_area_income({crime_id}, N)"))[0]["N"]
    features_dict["AREA_ASSAULT_HOMICIDE"] = list(kb.query(f"crime_area_assault_homicide({crime_id}, N)"))[0]["N"]
    features_dict["AREA_FIREARM"] = list(kb.query(f"crime_area_firearm({crime_id}, N)"))[0]["N"]
    features_dict["AREA_POVERTY_HEALTH"] = list(kb.query(f"crime_area_poverty_level({crime_id}, N)"))[0]["N"]
    features_dict["AREA_HIGH_SCHOOL_DIPLOMA"] = list(kb.query(f"crime_area_hs_diploma({crime_id}, N)"))[0]["N"]
    features_dict["AREA_UNEMPLOYMENT"] = list(kb.query(f"crime_area_unemployment({crime_id}, N)"))[0]["N"]
    features_dict["AREA_BIRTH_RATE"] = list(kb.query(f"crime_area_birth_rate({crime_id}, N)"))[0]["N"]

    features_dict["NUM_OF_DEAD"] = list(kb.query(f"num_of_dead({crime_id}, N)"))[0]["N"]
    features_dict["NUM_OF_ARREST"] = list(kb.query(f"num_of_arrest({crime_id}, N)"))[0]["N"]
    features_dict["NUM_OF_VICTIMS"] = list(kb.query(f"num_of_victims({crime_id}, N)"))[0]["N"]

    features_dict["IS_DOMESTIC"] = len(list(kb.query(f"is_domestic({crime_id})")))
    features_dict["NIGHT_CRIME"] = len(list(kb.query(f"night_crime({crime_id})")))
    features_dict["IS_KILLED_A_CHILD"] = len(list(kb.query(f"is_killed_a_child({crime_id})")))
    features_dict["MULTIPLE_ARRESTS"] = len(list(kb.query(f"crime_by_group({crime_id})")))
    features_dict["HAS_STREET_ORGANIZATION"] = len(list(kb.query(f"has_street_organization({crime_id})")))

    return features_dict


start = time.time()

kb = create_kb()
for crime_id in pd.read_csv("crimes_selected.csv")["CASE_NUMBER"]:
    print(calculate_features(kb, crime_id))

print(pd.read_csv("crimes_selected.csv")["CASE_NUMBER"])

end = time.time()
print("Time: ", end-start)
