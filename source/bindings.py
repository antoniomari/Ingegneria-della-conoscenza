from datetime import datetime

import numpy as np
import pyswip
import rdflib
import pandas as pd
from rdflib.plugins.sparql import prepareQuery

# ds =
# ds1 =
# ds2 =
# ds3 =
# ds4 = crimes

"""
g = rdflib.Graph()
g.parse("dataset/complete.rdf")

query = prepareQuery("SELECT ?crime WHERE "
                     "{ ?crime ds4:case_number ?o. "
                     "  ?arrest ds3:case_number ?o. }",
                     initNs={"ds4": g.store.namespace("ds4"), "ds3": g.store.namespace("ds3")})
results = g.query(query)

for row in results:
    print(row)

print(f"Num: {len(results)}")

"""

"""
arrest_case_codes = pd.concat([arrest_1_df["CASE NUMBER"], arrest_2_df["CASE NUMBER"]])
print(f"Ci sono {len(arrest_case_codes)} casi di arresto")

shoot_case_codes = shoot_df["CASE_NUMBER"]
print(f"Ci sono {len(shoot_case_codes)} casi di spari")

result = arrest_case_codes[arrest_case_codes.isin(shoot_case_codes)]
print(f"Intersezione: {len(result)}")
"""

SHOOT_DATASET_PATH = "../old_dataset/shoot.csv"
CRIME_DATASET_PATHS = ["../old_dataset/" + str(i) + ".csv" for i in range(2010, 2023)]
ARRESTS_DATASET_PATHS = ["../old_dataset/arrests_1.csv", "../old_dataset/arrests_2.csv"]
HEALTH_DATASET_PATH = "../old_dataset/health.csv"

CLEAN_CRIME_PATH = "crimes_selected.csv"
CLEAN_SHOOT_PATH = "shoot_selected.csv"
CLEAN_ARREST_PATH = "arrest_selected.csv"

# Adjust features in complete_crimes.csv (renaming and deleting)
def adjust_features():
    col_ren = {'Date': 'Date_Crime', 'DATE': 'DATE_SHOOT',
               'RACE_x': 'victim_race', 'RACE_y': 'criminal_race', 'CB_NO': 'ARREST_NUMBER'}

    # VICTIMIZATION_IUCR_CD == IUCR
    # BLOCK_SHOOT == Block_crime ?
    # COMMUNITY_AREA -> area names are useless, we already have the community area ids
    # INCIDENT_FBI_DESCR and VICTIMIZATION_FBI_DESCR -> same information of INCIDENT/VICTIMIZATION_PRIMARY
    # VICTIMIZATION_FBI_CD and INCIDENT_FBI_CD -> useless FBI codes, we already have IUCR codes
    # VICTIMIZATION_IUCR_SECONDARY and INCIDENT_IUCR_SECONDARY -> we already have IUCR codes, redundant
    # UPDATED -> is the time of the last update, useless for our purposes
    # LATITUDE, LONGITUDE, LOCATION -> the position is altered for anonymization, as stated here
    # https://data.cityofchicago.org/Public-Safety/Violence-Reduction-Victims-of-Homicides-and-Non-Fa/gumc-mgzr
    #
    # ID -> crime record ID, useless
    # Block -> duplicate, the same information is in BLOCK (from shoot dataset)
    # IUCR -> duplicate, the same information is in VICTIMIZATION and INCIDENT IUCR codes
    # Primary Type, Description -> redundant, same information in IUCR codes
    # Arrest -> inconsistent data, not updated. We know that everyone has been arrested
    # FBI code -> duplicate
    # X Coordinate, Y coordinate -> redundandt, we already have Latitude and Longitude
    # Year -> redundant
    # Updated On -> useless
    # Location -> redundant
    # MONTH -> redundant
    # HOUR -> redundant
    col_del = ['VICTIMIZATION_IUCR_CD', 'UNIQUE_ID', 'COMMUNITY_AREA', 'VICTIMIZATION_FBI_DESCR',
               'INCIDENT_FBI_DESCR', 'VICTIMIZATION_FBI_CD', 'INCIDENT_FBI_CD', 'VICTIMIZATION_IUCR_SECONDARY',
               'INCIDENT_IUCR_SECONDARY', 'UPDATED', 'LATITUDE', 'LONGITUDE', 'LOCATION', 'ID', 'Block', 'IUCR',
               'Primary Type', 'Description', 'Arrest', 'FBI Code', 'X Coordinate', 'Y Coordinate', 'Year',
               'Updated On', 'Location', 'MONTH', 'HOUR']

    complete_crimes = pd.read_csv("../old source/complete_crimes.csv")

    complete_crimes.rename(columns=col_ren, inplace=True)
    complete_crimes = complete_crimes.drop(col_del, axis=1)

    complete_crimes.to_csv("complete_crimes_adjust.csv", index=False)

    # Remove duplicates, a small feature selection
    check_values_consistency()


def check_values_consistency():
    complete_crimes = pd.read_csv("../old source/complete_crimes_adjust.csv")
    # check WARD
    diff_ward = complete_crimes[complete_crimes["WARD"] != complete_crimes["Ward"]]
    complete_crimes = complete_crimes.drop(["Ward"], axis=1)
    # after checking, the conclusion is to delete Ward, inconsistent with other data (Community Area)

    # check DISTRICT
    wrong_discrict_indices = complete_crimes["DISTRICT"] != complete_crimes["District"]
    diff_district = complete_crimes[wrong_discrict_indices]
    # there are 5 district mismatchings, so we delete the corresponding rows
    complete_crimes = complete_crimes.drop(complete_crimes.index[wrong_discrict_indices], axis=0)
    complete_crimes = complete_crimes.drop(["District"], axis=1)

    # check BEAT -> map type
    wrong_beat_indices = complete_crimes["BEAT"] != complete_crimes["Beat"]
    diff_beat = complete_crimes[wrong_beat_indices]
    complete_crimes = complete_crimes.drop(complete_crimes.index[wrong_beat_indices], axis=0)
    complete_crimes = complete_crimes.drop(["Beat"], axis=1)
    # there are 5 district mismatchings, so we delete the corresponding rows

    # mapping race
    victim_race_mapping = {"WHI": "WHITE", "BLK": "BLACK", "WWH": "WHITE HISPANIC",
                           "WBH": "BLACK HISPANIC", "API": "ASIAN / PACIFIC ISLANDER",
                           "I": "AMER INDIAN / ALASKAN NATIVE", "UNKNOWN": "UNKNOWN"}
    complete_crimes["victim_race"] = complete_crimes["victim_race"].map(victim_race_mapping)

    # mapping age we use a median value in the range as a representative one (only for value ordering purposes)
    # [0-19] -> 10
    # [20-29] -> 25
    # [30-39] -> 35
    # [40-49] -> 45
    # [50-59] -> 55
    # [60-69] -> 65
    # [70-79] -> 75
    # 80+     -> 80
    age_mapping = {"0-19": 10, "20-29": 25, "30-39": 35, "40-49": 45, "50-59": 55,
                   "60-69": 65, "70-79": 75, "80+": 80, "Unknown": None}
    # age to middle age
    complete_crimes["AGE"] = complete_crimes["AGE"].map(age_mapping)

    # check location description
    wrong_loc_desc_indices = complete_crimes["LOCATION_DESCRIPTION"] != complete_crimes["Location Description"]
    # we note that the only cases that are inconsistent make the distinction between street and (sidewalk or
    # porch). This information is rather similar than incoherent so we keep the column "Location Description",
    # because probably saying "sidewalk" or "porch" would be more precise than saying "street".
    complete_crimes = complete_crimes.drop(["LOCATION_DESCRIPTION"], axis=1)

    # check date
    wrong_date_indices = complete_crimes["DATE_SHOOT"] != complete_crimes["Date_Crime"]
    print(complete_crimes[wrong_date_indices][["DATE_SHOOT", "Date_Crime"]])
    # we note that DATE_SHOOT is never later than Date_Crime, so it surely will give a better approximation
    # Date_crime may be in fact delayed.
    complete_crimes = complete_crimes.drop(["Date_Crime"], axis=1)

    # mapping gunshot injury to boolean values
    gunshot_injury_mapping = {"NO": 0, "YES": 1}
    complete_crimes["GUNSHOT_INJURY_I"] = complete_crimes["GUNSHOT_INJURY_I"].map(gunshot_injury_mapping)

    complete_crimes.to_csv("complete_crimes_adjust.csv", index=False)


# returns all crime codes that are in common to ARREST_DATASET and SHOOT_DATASET
def extract_crime_codes() -> pd.Series:
    shoot_df: pd.DataFrame = pd.read_csv(SHOOT_DATASET_PATH)
    shoot_case_number: pd.Series = shoot_df["CASE_NUMBER"].drop_duplicates()

    arrest_1_df: pd.DataFrame = pd.read_csv(ARRESTS_DATASET_PATHS[0]).rename({"CASE NUMBER": "CASE_NUMBER"},
                                                                             axis=1)
    arrest_2_df: pd.DataFrame = pd.read_csv(ARRESTS_DATASET_PATHS[1]).rename({"CASE NUMBER": "CASE_NUMBER"},
                                                                             axis=1)

    arrest_case_number: pd.Series = pd.concat(
        [arrest_1_df["CASE_NUMBER"], arrest_2_df["CASE_NUMBER"]]).drop_duplicates()

    total_case_number = shoot_case_number[shoot_case_number.isin(arrest_case_number)]

    return total_case_number


# extract the dataset containing only crimes for which we have data from ARREST_DATASET and
def extract_crime_dataset(crime_codes: pd.Series) -> pd.DataFrame:

    crime_selected_df = None

    for path in CRIME_DATASET_PATHS:
        print(f"Processing File: {path}")
        crime_df: pd.DataFrame = pd.read_csv(path).rename({"Case Number": "CASE_NUMBER"}, axis=1)

        if crime_selected_df is None:
            crime_selected_df = crime_df[crime_df["CASE_NUMBER"].isin(crime_codes)]
        else:
            crime_selected_df = pd.concat(
                [crime_selected_df, crime_df[crime_df["CASE_NUMBER"].isin(crime_codes)]])

    return crime_selected_df


def extract_arrest_dataset(crime_codes: pd.Series) -> pd.DataFrame:

    arrest_dataset: pd.DataFrame = pd.concat(
        [pd.read_csv(ARRESTS_DATASET_PATHS[i]).rename({"CASE NUMBER": "CASE_NUMBER"}, axis=1) for i in {0, 1}])
    arrest_dataset = arrest_dataset[arrest_dataset["CASE_NUMBER"].isin(crime_codes)]
    return arrest_dataset


def extract_shoot_dataset(crime_codes: pd.Series) -> pd.DataFrame:
    shoot_dataset: pd.DataFrame = pd.read_csv(SHOOT_DATASET_PATH)
    shoot_dataset = shoot_dataset[shoot_dataset["CASE_NUMBER"].isin(crime_codes)]
    return shoot_dataset

# OLD FUNCTION
def create_dataset() -> pd.DataFrame:
    # BINDING SHOOT e ARREST

    ## search case_number in shoot =
    shoot_df: pd.DataFrame = pd.read_csv(SHOOT_DATASET_PATH)
    shoot_case_number: pd.Series = shoot_df["CASE_NUMBER"].drop_duplicates()

    arrest_1_df: pd.DataFrame = pd.read_csv("../old_dataset/arrests_1.csv").rename({"CASE NUMBER": "CASE_NUMBER"},
                                                                                   axis=1)
    arrest_2_df: pd.DataFrame = pd.read_csv("../old_dataset/arrests_2.csv").rename({"CASE NUMBER": "CASE_NUMBER"},
                                                                                   axis=1)

    arrest_case_number: pd.Series = pd.concat(
        [arrest_1_df["CASE_NUMBER"], arrest_2_df["CASE_NUMBER"]]).drop_duplicates()

    total_case_number = shoot_case_number[shoot_case_number.isin(arrest_case_number)]

    print(f"Shoot df {len(shoot_df.index)}")
    print(f"Arrest 1 df {len(arrest_1_df.index)}")
    print(f"Arrest 2 df {len(arrest_2_df.index)}")
    print(f"Total case: {len(total_case_number)}")

    shoot_and_arrest_1_df: pd.DataFrame = shoot_df.merge(arrest_1_df, on="CASE_NUMBER")
    shoot_and_arrest_2_df: pd.DataFrame = shoot_df.merge(arrest_2_df, on="CASE_NUMBER")

    shoot_and_arrest: pd.DataFrame = pd.concat([shoot_and_arrest_1_df, shoot_and_arrest_2_df])

    print(len(shoot_and_arrest.index))

    # BINDING CON crimini
    crime_paths = ["../old_dataset/" + str(i) + ".csv" for i in range(2010, 2023)]
    complete_df = None

    crime_selected_df = None

    for path in crime_paths:
        print(f"File {path}")
        crime_df: pd.DataFrame = pd.read_csv(path).rename({"Case Number": "CASE_NUMBER"}, axis=1)
        print(f"\tLunghezza {len(crime_df.index)}")
        if complete_df is None:
            print("None")
            complete_df = shoot_and_arrest.merge(crime_df, on="CASE_NUMBER")
            crime_selected_df = crime_df[crime_df["CASE_NUMBER"].isin(total_case_number)]
        else:
            print("conc")
            complete_df = pd.concat([complete_df, shoot_and_arrest.merge(crime_df, on="CASE_NUMBER")])
            crime_selected_df = pd.concat(
                [crime_selected_df, crime_df[crime_df["CASE_NUMBER"].isin(total_case_number)]])

        print(f"Lunghezza completo: {len(complete_df.index)}")

    print(len(complete_df.index))
    complete_df.to_csv("complete_crimes.csv", index=False)
    complete_df.describe().to_csv("report1.csv", index=False)

    crime_selected_df.to_csv("crimes_selected.csv", index=False)

    return complete_df


def preprocess_crimes_dataset(extracted_crime_dataset: pd.DataFrame) -> pd.DataFrame:
    col_del = ['IUCR', 'Primary Type', 'Description', 'Arrest', 'FBI Code', 'X Coordinate',
               'Y Coordinate', 'Year', 'Updated On', 'Location', 'ID']

    col_ren = {'Date': 'Date_Crime'}

    extracted_crime_dataset = extracted_crime_dataset.drop(col_del, axis=1).drop_duplicates()

    # now the only wrong value is a duplicate with inconsistent Location
    # JA329470, there are two rows (one with value 'PORCH', one other with value 'STREET')
    # having checked in shoot dataset, the correct value is 'STREET'
    wrong_index = (extracted_crime_dataset["CASE_NUMBER"] == "JA329470") & (extracted_crime_dataset["Location Description"] == 'PORCH')
    extracted_crime_dataset = extracted_crime_dataset.drop(extracted_crime_dataset.index[wrong_index], axis=0)

    # important: string values to lowercase
    extracted_crime_dataset = adjust_string_columns(extracted_crime_dataset, except_columns=["Date"])

    return extracted_crime_dataset


def adjust_string_columns(df: pd.DataFrame, except_columns=None) -> pd.DataFrame:
    if except_columns is None:
        except_columns = []

    for col_name, col_data in df.iteritems():
        if pd.api.types.is_string_dtype(col_data) and (col_name not in except_columns):
            df[col_name] = df[col_name].apply(lambda x: str(x).lower())
            df[col_name] = df[col_name].apply(lambda x: ''.join(['_' if not c.isalnum() else c for c in x]))
    return df


def preprocess_arrest_dataset(extracted_arrest_dataset: pd.DataFrame) -> pd.DataFrame:
    col_ren = {'RACE': 'criminal_race', 'CB_NO': 'ARREST_NUMBER'}

    extracted_arrest_dataset.rename(columns=col_ren, inplace=True)

    # map races to match with victim races
    race_mapping = {"WHITE": "WHI", "BLACK": "BLK", "WHITE HISPANIC": "WWH",
                    "BLACK HISPANIC": "WBH", "ASIAN / PACIFIC ISLANDER": "API",
                    "AMER INDIAN / ALASKAN NATIVE": "I", "UNKNOWN": "UNKNOWN"}
    extracted_arrest_dataset["criminal_race"] = extracted_arrest_dataset["criminal_race"].map(race_mapping)

    # important: string values to lowercase
    extracted_arrest_dataset = adjust_string_columns(extracted_arrest_dataset, except_columns=["ARREST DATE"])

    return extracted_arrest_dataset


def preprocess_shoot_dataset(extracted_shoot_dataset: pd.DataFrame) -> pd.DataFrame:
    col_del = ['INCIDENT_IUCR_CD', 'VICTIMIZATION_IUCR_CD', 'UNIQUE_ID', 'COMMUNITY_AREA', 'VICTIMIZATION_FBI_DESCR',
               'INCIDENT_FBI_DESCR', 'VICTIMIZATION_FBI_CD', 'INCIDENT_FBI_CD', 'VICTIMIZATION_IUCR_SECONDARY',
               'INCIDENT_IUCR_SECONDARY', 'UPDATED', 'LATITUDE', 'LONGITUDE', 'LOCATION', 'WARD',
               'DISTRICT', 'BEAT', 'MONTH', 'HOUR', 'LOCATION_DESCRIPTION', 'BLOCK']

    col_ren = {'DATE': 'DATE_SHOOT', 'RACE': 'victim_race', 'VICTIMIZATION_PRIMARY': 'VICTIMIZATION',
               'INCIDENT_PRIMARY': 'INCIDENT', 'GUNSHOT_INJURY_I': 'GUNSHOT'}

    extracted_shoot_dataset.rename(columns=col_ren, inplace=True)
    extracted_shoot_dataset = extracted_shoot_dataset.drop(col_del, axis=1)

    age_mapping = {"0-19": 10, "20-29": 25, "30-39": 35, "40-49": 45, "50-59": 55,
                   "60-69": 65, "70-79": 75, "80+": 80, "Unknown": None}
    # age to middle age
    extracted_shoot_dataset["AGE"] = extracted_shoot_dataset["AGE"].map(age_mapping)

    # map gunshot to boolean
    # mapping gunshot injury to boolean values
    gunshot_injury_mapping = {"NO": 0, "YES": 1}
    extracted_shoot_dataset["GUNSHOT"] = extracted_shoot_dataset["GUNSHOT"].map(gunshot_injury_mapping)

    # important: string values to lowercase
    extracted_shoot_dataset = adjust_string_columns(extracted_shoot_dataset, except_columns=["DATE_SHOOT"])

    # since there is no id_column, we will add one
    extracted_shoot_dataset = extracted_shoot_dataset.assign(VICTIM_CODE=extracted_shoot_dataset.index)

    return extracted_shoot_dataset


def load_data_in_kb(crimes_df: pd.DataFrame, arrest_df: pd.DataFrame,
                    shoot_df: pd.DataFrame, health_df: pd.DataFrame,
                    kb=None):

    prolog_file = None

    if kb is None:
        prolog_file = open("facts.pl", "w")
        action = lambda fact_list: assert_all_in_file(fact_list, prolog_file)
    else:
        action = lambda fact_list: assert_all(fact_list, kb)

    action([":-style_check(-discontiguous)"])

    # insert data for crimes
    for index, row in crimes_df.iterrows():
        case_num = row['CASE_NUMBER']
        facts = [f"location_description({case_num}, {row['Location Description']})",
                 f"beat({case_num},{row['Beat']})",
                 f"district({case_num},{row['District']})",
                 f"comm_area({case_num},{row['Community Area']})",
                 f"ward({case_num},{row['Ward']})",
                 f"crime_date({case_num}, {datetime_to_prolog_fact(row['Date'])})",
                 f"block({case_num}, {'block_' + row['Block']})"]  # due to initial number

        action(facts)

    # insert data for arrests
    for index, row in arrest_df.iterrows():
        arrest_num = row['ARREST_NUMBER']
        facts = [f"has_arrest({row['CASE_NUMBER']}, {arrest_num})",
                 f"arrest_date({arrest_num}, {datetime_to_prolog_fact(row['ARREST DATE'])})",
                 f"criminal_race({arrest_num},{row['criminal_race']})"]

        num_charges = 0
        for i in range(1, 5):
            if row[f"CHARGE {i} STATUTE"] != np.nan:
                print(row[f"CHARGE {i} STATUTE"])
                num_charges += 1
            else:
                break
        # note: num charges is always >= 1
        facts.append(f"num_of_charges({arrest_num}, {num_charges})")

        action(facts)

    # insert data for shoot
    # Add info about gunshot injury

    for index, row in shoot_df.iterrows():
        victim_code = row['VICTIM_CODE']
        facts = [f"victimization({row['CASE_NUMBER']}, {victim_code}, {row['VICTIMIZATION']})",
                 f"date_shoot({victim_code}, {datetime_to_prolog_fact(row['DATE_SHOOT'])})",
                 f"victim_race({victim_code},{row['victim_race']})",
                 f"incident({victim_code}, {row['INCIDENT']})",
                 f"zip_code({victim_code}, {row['ZIP_CODE']})",
                 f"victim_sex({victim_code}, {row['SEX']})",
                 f"victim_day_of_week({victim_code}, {row['DAY_OF_WEEK']})",
                 f"state_house_district({victim_code}, {row['STATE_HOUSE_DISTRICT']})",
                 f"state_house_district({victim_code}, {row['STATE_SENATE_DISTRICT']})"]

        # street outreach
        if row['STREET_OUTREACH_ORGANIZATION'] != 'none':
            facts.append(f"street_org({victim_code}, {row['STREET_OUTREACH_ORGANIZATION']})")

        if row['AGE'] is not None:
            facts.append(f"victim_age({victim_code}, {row['AGE']})")

        action(facts)

    # insert data for health

    for index, row in health_df.iterrows():
        comm_area_code = float(row["Community Area"])
        facts = [f"comm_birth_rate({comm_area_code}, {row['Birth Rate']})",
                 f"comm_assault_homicide({comm_area_code}, {row['Assault (Homicide)']})",
                 f"comm_firearm({comm_area_code}, {row['Firearm-related']})",
                 f"comm_poverty_level({comm_area_code}, {row['Below Poverty Level']})",
                 f"comm_hs_diploma({comm_area_code}, {row['No High School Diploma']})",
                 f"comm_income({comm_area_code}, {row['Per Capita Income']})",
                 f"comm_unemployment({comm_area_code}, {row['Unemployment']})"]

        action(facts)

    if kb is not None:
        prolog_file.close()


def assert_all(facts, kb):
    for fact in facts:
        kb.asserta(fact)


def assert_all_in_file(facts, kb_file):
    kb_file.writelines(".\n".join(facts) + ".\n")

def create_prolog_kb():
    crimes_df = pd.read_csv(CLEAN_CRIME_PATH)
    arrest_df = pd.read_csv(CLEAN_ARREST_PATH)
    shoot_df = pd.read_csv(CLEAN_SHOOT_PATH)
    health_df = pd.read_csv(HEALTH_DATASET_PATH)

    load_data_in_kb(crimes_df=crimes_df, arrest_df=arrest_df, shoot_df=shoot_df, health_df=health_df)



def datetime_to_prolog_fact(datetime_str: str) -> str:
    dt = datetime.strptime(datetime_str, '%m/%d/%Y %I:%M:%S %p')
    datetime_str = "date({}, {}, {}, {}, {}, {})".format(dt.year, dt.month, dt.day,
                                                         dt.hour, dt.minute, dt.second)
    return f"datime({datetime_str})"


def main():
    crime_codes = extract_crime_codes()
    clean_crime_dataset: pd.DataFrame = preprocess_crimes_dataset(extract_crime_dataset(crime_codes))
    clean_crime_dataset.to_csv(CLEAN_CRIME_PATH, index=False)

    clean_arrest_dataset: pd.DataFrame = preprocess_arrest_dataset(extract_arrest_dataset(crime_codes))
    clean_arrest_dataset.to_csv(CLEAN_ARREST_PATH, index=False)

    clean_shoot_dataset: pd.DataFrame = preprocess_shoot_dataset(extract_shoot_dataset(crime_codes))
    clean_shoot_dataset.to_csv(CLEAN_SHOOT_PATH, index=False)

    # create_dataset()
    # adjust_features()


#main()
create_prolog_kb()
