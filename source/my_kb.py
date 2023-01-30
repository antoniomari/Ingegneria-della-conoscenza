import time

import pandas as pd
from pyswip import Prolog


def assert_location_facts(kb):
    with open("locations.pl", "r") as loc_file:
        lines = loc_file.readlines()
        for line in lines:
            kb.assertz(line)


def create_kb() -> Prolog:
    prolog = Prolog()

    prolog.consult("facts.pl")
    assert_location_facts(kb=prolog)

    # CLAUSES ABOUT GEO-DATA
    prolog.assertz("same_district(crime(C1), crime(C2)) :- district(crime(C1), D), district(crime(C2), D)")
    prolog.assertz("same_beat(crime(C1), crime(C2)) :- beat(crime(C1), B), beat(crime(C2), B)")
    prolog.assertz("same_ward(crime(C1), crime(C2)) :- ward(crime(C1), W), ward(crime(C2), W)")
    prolog.assertz("same_comm_area(crime(C1), crime(C2)) :- comm_area(crime(C1), COM), comm_area(crime(C2), COM)")
    prolog.assertz("same_block(crime(C1), crime(C2)) :- block(crime(C1), B), block(crime(C2), B)")
    prolog.assertz("num_of_crimes_in_district(crime(C), N) :- "
                   "findall(C1, same_district(crime(C), crime(C1)), L), length(L, N)")
    prolog.assertz("num_of_crimes_in_beat(crime(C), N) :- findall(C1, same_beat(crime(C), crime(C1)), L), length(L, N)")
    prolog.assertz("num_of_crimes_community_area(crime(C), N) :- "
                   "findall(C1, same_comm_area(crime(C), crime(C1)), L), length(L, N)")
    prolog.assertz("num_of_crimes_ward(crime(C), N) :- findall(C1, same_ward(crime(C), crime(C1)), L), length(L, N)")
    prolog.assertz("num_of_crimes_block(crime(C), N) :- findall(C1, same_block(crime(C), crime(C1)), L), length(L, N)")

    # CLAUSES ABOUT GEO-DATA coming from VICTIMIZATION
    prolog.assertz("crime_zip_code(crime(C), Z) :- victimization(crime(C), victim(V), T), zip_code(victim(V), Z)")
    prolog.assertz("same_zip_code(crime(C1), crime(C2)) :- crime_zip_code(crime(C1), Z), crime_zip_code(crime(C2), Z)")
    prolog.assertz("num_of_crimes_in_zip_code(crime(C), N) :- "
                   "findall(C1, same_zip_code(crime(C), crime(C1)), L), length(L, N)")

    # CLAUSES ABOUT STREET ORGANIZATIONS from VICTIMIZATION
    prolog.assertz("street_organization(crime(C), O) :- "
                   "victimization(crime(C), victim(V), T), street_org(victim(V), O)")
    prolog.assertz("has_street_organization(crime(C)) :- street_organization(crime(C), O)")
    prolog.assertz("same_street_organization(crime(C1), crime(C2)) :- "
                   "street_organization(crime(C1), O), street_organization(crime(C2), O)")
    prolog.assertz("num_of_crimes_street_organization(crime(C), N) :- "
                   "findall(C1, same_street_organization(crime(C), crime(C1)), L), length(L, N)")

    # PROPERTIES OF COMMUNITY AREA
    prolog.assertz("crime_area_income(crime(C), I) :- comm_area(crime(C), COM), comm_income(COM, I)")
    prolog.assertz("crime_area_assault_homicide(crime(C), I) :- comm_area(crime(C), COM), comm_assault_homicide(COM, I)")
    prolog.assertz("crime_area_firearm(crime(C), I) :- comm_area(crime(C), COM), comm_firearm(COM, I)")
    prolog.assertz("crime_area_poverty_level(crime(C), I) :- comm_area(crime(C), COM), comm_poverty_level(COM, I)")
    prolog.assertz("crime_area_hs_diploma(crime(C), I) :- comm_area(crime(C), COM), comm_hs_diploma(COM, I)")
    prolog.assertz("crime_area_unemployment(crime(C), I) :- comm_area(crime(C), COM), comm_unemployment(COM, I)")
    prolog.assertz("crime_area_birth_rate(crime(C), I) :- comm_area(crime(C), COM), comm_birth_rate(COM, I)")

    # RACE AND SEX DATA
    prolog.assertz("crime_victim_sex(crime(C), S) :- "
                   "victimization(crime(C), victim(V), T), victim_sex(victim(V), S)")

    prolog.assertz("crime_victim_race(crime(C), VR) :- "
                   "victimization(crime(C), victim(V), T), victim_race(victim(V), VR)")
    prolog.assertz("crime_arrested_race(crime(C), PR) :- "
                   "has_arrest(crime(C), arrest(P)), criminal_race(arrest(P), PR) ")

    prolog.assertz("is_ratial(crime(C)) :- "
                   "crime_arrested_race(crime(C), PR), crime_victim_race(crime(C), VR), dif(VR, PR)")

    # Victim aver_age
    prolog.assertz("aver_age(crime(C), Avg) :- findall(A, (victimization(crime(C), victim(V), T), "
                   "victim_age(victim(V), A)), L), "
                   "sumlist(L, Sum), length(L, Length), Length > 0, Avg is Sum / Length")

    # features number of X
    prolog.assertz("num_of_victims(crime(C), N) :- findall(V, victimization(crime(C), victim(V), T), L), length(L, N)")
    prolog.assertz("num_of_dead(crime(C), N) :- "
                   "findall(V, victimization(crime(C), victim(V), homicide), L), length(L, N)")
    prolog.assertz("num_of_arrest(crime(C), N) :- findall(P, has_arrest(crime(C), arrest(P)), L), length(L, N)")
    prolog.assertz("is_homicide(crime(C)) :- victimization(crime(C), victim(V), homicide)")

    prolog.assertz("is_killed(victim(V)) :- victimization(crime(C), victim(V), homicide)")
    prolog.assertz("is_domestic(crime(C)) :- "
                   "location_description(crime(C), apartment); location_description(crime(C), house); "
                   "location_description(crime(C), residence); location_description(crime(C), driveway)")
    prolog.assertz("night_crime(crime(C)) :- crime_date(crime(C), datime(date(Y, M, D, H, M, S))), ((H >= 20; H =< 6))")
    prolog.assertz("crime_date_arrest(crime(C), D) :- has_arrest(crime(C), arrest(A)), arrest_date(arrest(A), D)")
    prolog.assertz("immediate_arrest(crime(C)) :- crime_date(crime(C), D), crime_date_arrest(crime(C), D)")
    prolog.assertz("same_month_arrest(crime(C)) :- crime_date(crime(C), datime(date(Y, M, D, H, M, S))), "
                   "crime_date_arrest(crime(C), datime(date(Y, M, D1, H1, M1, S1)))")

    prolog.assertz("is_there_a_child(crime(C), T) :- "
                   "victimization(crime(C), victim(V), T), victim_age(victim(V), A), A =< 15")
    prolog.assertz("is_killed_a_child(crime(C)) :- is_there_a_child(crime(C), homicide)")

    prolog.assertz("crime_by_group(crime(C)) :- num_of_arrest(crime(C), N), N >= 2")


    prolog.assertz("avg_num_charge(crime(C), Avg) :- "
                   "findall(NC, (has_arrest(crime(C), arrest(A)), num_of_charges(arrest(A), NC)), L), "
                   "sumlist(L, Sum), length(L, Length), Length > 0, Avg is Sum / Length")

    # added after Naive Bayes Categorical results

    # high abstracted categories
    prolog.assertz("is_vehicle(location(L)) :- is_private_vehicle(location(L)); is_public_vehicle(location(L))")
    prolog.assertz("is_public_place(location(L)) :- is_parking(location(L)); is_store_pub(location(L)); "
                   "is_gas_station(location(L)); is_park(location(L))")
    prolog.assertz("is_outside(location(L)) :- is_street(location(L)); is_sidewalk(location(L)); "
                   "is_alley(location(L))")
    prolog.assertz("is_residential(location(L)) :- is_apartment(location(L)); is_house(location(L)); "
                   "is_residence(location(L)); is_residential_outside(location(L))")

    for value in ["vehicle", "private_vehicle", "public_vehicle", "public_place", "parking", "store_pub", "gas_station",
                  "park", "outside", "street", "sidewalk", "alley", "residential", "apartment", "house", "residence",
                  "residential_outside"]:
        prolog.assertz(f"location_{value}(crime(C)) :- location_description(crime(C), location(L)), "
                       f"is_{value}(location(L))")

    return prolog


# suppongo che ci sia già
def calculate_features(kb, crime_id, final=False) -> dict:
    features_dict = {}

    features_dict["CASE_NUMBER"] = crime_id

    crime_id = f"crime({crime_id})"

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

    features_dict["IS_DOMESTIC"] = query_boolean_result(kb, f"is_domestic({crime_id})")
    features_dict["NIGHT_CRIME"] = query_boolean_result(kb, f"night_crime({crime_id})")
    features_dict["IS_KILLED_A_CHILD"] = query_boolean_result(kb, f"is_killed_a_child({crime_id})")
    features_dict["MULTIPLE_ARRESTS"] = query_boolean_result(kb, f"crime_by_group({crime_id})")
    features_dict["HAS_STREET_ORGANIZATION"] = query_boolean_result(kb, f"has_street_organization({crime_id})")
    features_dict["IS_RATIAL"] = query_boolean_result(kb, f"is_ratial({crime_id})")

    arrested_race_list = list(kb.query(f"crime_arrested_race({crime_id}, PR)"))
    arrested_race_set = {arrested_race_list[0]['PR']}
    for i in range(1, len(arrested_race_list)):
        arrested_race_set.add(arrested_race_list[i]['PR'])
    features_dict["ARRESTED_RACE"] = next(iter(arrested_race_set)) if len(arrested_race_set) == 1 else "mixed"

    victim_race_list = list(kb.query(f"crime_victim_race({crime_id}, VR)"))
    victim_race_set = {victim_race_list[0]['VR']}
    for i in range(1, len(victim_race_list)):
        victim_race_set.add(victim_race_list[i]['VR'])
    features_dict["VICTIM_RACE"] = next(iter(victim_race_set)) if len(victim_race_set) == 1 else "mixed"

    victim_sex_list = list(kb.query(f"crime_victim_sex({crime_id}, S)"))
    victim_sex_set = {victim_sex_list[0]['S']}
    for i in range(1, len(victim_sex_list)):
        victim_sex_set.add(victim_sex_list[i]['S'])
    features_dict["VICTIM_SEX"] = next(iter(victim_sex_set)) if len(victim_sex_set) == 1 else "mixed"


    aver_age = list(kb.query(f"aver_age({crime_id}, Avg)"))
    features_dict["AVER_AGE"] = aver_age[0]['Avg'] if len(aver_age) == 1 else None

    features_dict["AVG_NUM_CHARGES"] = list(kb.query(f"avg_num_charge({crime_id}, Avg)"))[0]['Avg']

    features_dict["IMMEDIATE_ARREST"] = query_boolean_result(kb, f"immediate_arrest({crime_id})")
    features_dict["SAME_MONTH_ARREST"] = query_boolean_result(kb, f"same_month_arrest({crime_id})")
    features_dict["IS_HOMICIDE"] = query_boolean_result(kb, f"is_homicide({crime_id})")

    if final:
        # added after Naive Bayes Categorical results
        for value in ["vehicle", "private_vehicle", "public_vehicle", "public_place", "parking", "store_pub", "gas_station",
                      "park", "outside", "street", "sidewalk", "alley", "residential", "apartment", "house", "residence",
                      "residential_outside"]:
            features_dict[f"LOCATION_{value}"] = query_boolean_result(kb, f"location_{value}({crime_id})")

    return features_dict


def query_boolean_result(kb, query_str: str):
    return min(len(list(kb.query(query_str))), 1)


def produce_working_dataset(kb: Prolog, path: str, final=False):
    print(f"Producing dataset at {path}")
    start = time.time()
    crimes_complete: pd.DataFrame = pd.read_csv("crimes_selected.csv")

    extracted_values_df = None

    first = True
    for crime_id in crimes_complete["CASE_NUMBER"]:

        features_dict = calculate_features(kb, crime_id, final)
        if first:
            extracted_values_df = pd.DataFrame([features_dict])
            first = False
        else:
            extracted_values_df = pd.concat([extracted_values_df, pd.DataFrame([features_dict])], ignore_index=True)

    extracted_values_df.to_csv(path, index=False)
    end = time.time()
    print("Total time: ", end-start)


knowledge_base = create_kb()
produce_working_dataset(knowledge_base, "working_dataset.csv")
produce_working_dataset(knowledge_base, "working_dataset_final.csv", final=True)
