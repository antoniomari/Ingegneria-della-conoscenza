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

    prolog.assertz("is_ratial(C) :- has_arrest(C, P), victimization(C, V, T), "
                   "victim_race(V, VR), criminal_race(P, PR), dif(VR, PR)")

    prolog.assertz("crime_victim_race(C, VR) :- victimization(C, V, T), victim_race(V, VR) ")
    # use this
    prolog.assertz("crimes_victim_same_race(C, VR) :- findall(VR, crime_victim_race(C, VR), L), length(L, 1)")
    prolog.assertz("crime_arrested_race(C, PR) :- has_arrest(C, P), criminal_race(P, PR) ")
    # use this
    prolog.assertz("crimes_arrested_same_race(C, PR) :- findall(PR, crime_arrested_race(C, PR), L), length(L, 1)")

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
    prolog.assertz("crime_date_arrest(C, D) :- has_arrest(C, A), arrest_date(A, D)")
    prolog.assertz("immediate_arrest(C) :- crime_date(C, D), crime_date_arrest(C, D)")  # or choose an error of date

    # Add victim_age fact, i.e victim_age(crime, victim)
    prolog.assertz("aver_age(C, Avg) :- findall(A, (victimization(C, V, T), victim_age(V, A)), L), "
                   "sumlist(L, Sum), length(L, Length), Length > 0, Avg is Sum / Length")

    # Add victim_sex
    prolog.assertz("is_there_a_child(C, T) :- victimization(C, V, T), victim_age(V, A), A =< 15")
    prolog.assertz("is_killed_a_child(C) :- is_there_a_child(C, homicide)")

    prolog.assertz("crime_by_group(C) :- num_of_arrest(C, N), N >= 2")
    prolog.assertz("street_organization(C, O) :- victimization(C, V, T), street_org(V, O)")
    prolog.assertz("has_street_organization(C) :- street_organization(C, O)")
    prolog.assertz("same_street_organization(C1, C2) :- street_organization(C1, O), street_organization(C2, O)")
    prolog.assertz("num_of_crimes_street_organization(C, N) :- "
                   "findall(C1, same_street_organization(C, C1), L), length(L, N)")

    prolog.assertz("avg_num_charge(C, Avg) :- "
                   "findall(NC, (has_arrest(C, A), num_of_charges(A, NC)), L), "
                   "sumlist(L, Sum), length(L, Length), Length > 0, Avg is Sum / Length")



    return prolog

# suppongo che ci sia già
def calculate_features(kb, crime_id) -> dict:
    features_dict = {}

    features_dict["CASE_NUMBER"] = crime_id

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
    features_dict["IS_RATIAL"] = len(list(kb.query(f"is_ratial({crime_id})")))

    arrested_race = list(kb.query(f"crimes_arrested_same_race({crime_id}, PR)"))
    features_dict["ARRESTED_RACE"] = arrested_race[0]['PR'] if len(arrested_race) == 1 else "mixed"

    victim_race = list(kb.query(f"crimes_victim_same_race({crime_id}, VR)"))
    features_dict["VICTIM_RACE"] = victim_race[0]['VR'] if len(victim_race) == 1 else "mixed"

    aver_age = list(kb.query(f"aver_age({crime_id}, Avg)"))
    features_dict["AVER_AGE"] = aver_age[0]['Avg'] if len(aver_age) == 1 else None

    features_dict["AVG_NUM_CHARGES"] = list(kb.query(f"avg_num_charge({crime_id}, Avg)"))[0]['Avg']

    features_dict["IMMEDIATE_ARREST"] = len(list(kb.query(f"immediate_arrest({crime_id})")))
    features_dict["IS_HOMICIDE"] = len(list(kb.query(f"is_homicide({crime_id})")))

    return features_dict

start = time.time()

kb = create_kb()

crimes_complete: pd.DataFrame = pd.read_csv("crimes_selected.csv")

extracted_values_df = None

first = True
for crime_id in crimes_complete["CASE_NUMBER"]:

    features_dict = calculate_features(kb, crime_id)
    if first:
        extracted_values_df = pd.DataFrame([features_dict])
        first = False
    else:
        extracted_values_df = pd.concat([extracted_values_df, pd.DataFrame([features_dict])], ignore_index=True)

extracted_values_df.to_csv("working_dataset.csv", index=False)
print(pd.read_csv("crimes_selected.csv")["CASE_NUMBER"])

end = time.time()
print("Time: ", end-start)

print(list(kb.query("crime_by_group(C)")))

