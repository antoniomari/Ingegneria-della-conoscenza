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
    col_del = ['VICTIMIZATION_IUCR_CD', 'UNIQUE_ID', 'COMMUNITY_AREA', 'VICTIMIZATION_FBI_DESCR',
               'INCIDENT_FBI_DESCR', 'VICTIMIZATION_FBI_CD', 'INCIDENT_FBI_CD', 'VICTIMIZATION_IUCR_SECONDARY',
               'INCIDENT_IUCR_SECONDARY', 'UPDATED', 'LATITUDE', 'LONGITUDE', 'LOCATION', 'ID', 'Block', 'IUCR',
               'Primary Type', 'Description', 'Arrest', 'FBI Code', 'X Coordinate', 'Y Coordinate', 'Year',
               'Updated On', 'Location']

    complete_crimes = pd.read_csv("complete_crimes.csv")
    
    complete_crimes.rename(columns=col_ren, inplace=True)
    complete_crimes = complete_crimes.drop(col_del, axis=1)

    complete_crimes.to_csv("complete_crimes_adjust.csv")

    # ID
    # check WARD
    # check DISTRICT
    # check BEAT --> map types
    # mapping race
    # mapping age and sex
    # gunshot injury map to boolean
    # check location description
    # check date

def create_dataset() -> pd.DataFrame:
    # BINDING SHOOT e ARREST
    shoot_df: pd.DataFrame = pd.read_csv("../old_dataset/shoot.csv")
    arrest_1_df: pd.DataFrame = pd.read_csv("../old_dataset/arrests_1.csv").rename({"CASE NUMBER": "CASE_NUMBER"},
                                                                                   axis=1)
    arrest_2_df: pd.DataFrame = pd.read_csv("../old_dataset/arrests_2.csv").rename({"CASE NUMBER": "CASE_NUMBER"},
                                                                                   axis=1)
    print(f"Shoot df {len(shoot_df.index)}")
    print(f"Arrest 1 df {len(arrest_1_df.index)}")
    print(f"Arrest 2 df {len(arrest_2_df.index)}")

    shoot_and_arrest_1_df: pd.DataFrame = shoot_df.merge(arrest_1_df, on="CASE_NUMBER")
    shoot_and_arrest_2_df: pd.DataFrame = shoot_df.merge(arrest_2_df, on="CASE_NUMBER")

    shoot_and_arrest: pd.DataFrame = pd.concat([shoot_and_arrest_1_df, shoot_and_arrest_2_df])

    print(len(shoot_and_arrest.index))

    # BINDING CON crimini
    crime_paths = ["../old_dataset/" + str(i) + ".csv" for i in range(2010, 2023)]
    complete_df = None

    for path in crime_paths:
        print(f"File {path}")
        crime_df: pd.DataFrame = pd.read_csv(path).rename({"Case Number": "CASE_NUMBER"}, axis=1)
        print(f"\tLunghezza {len(crime_df.index)}")
        if complete_df is None:
            print("None")
            complete_df = shoot_and_arrest.merge(crime_df, on="CASE_NUMBER")
        else:
            print("conc")
            complete_df = pd.concat([complete_df, shoot_and_arrest.merge(crime_df, on="CASE_NUMBER")])

        print(f"Lunghezza completo: {len(complete_df.index)}")

    print(len(complete_df.index))
    complete_df.to_csv("complete_crimes.csv")
    complete_df.describe().to_csv("report1.csv")

    return complete_df


def main():
    create_dataset()
    adjust_features()

adjust_features()