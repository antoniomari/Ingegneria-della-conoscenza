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

# BINDING SHOOT e ARREST
shoot_df: pd.DataFrame = pd.read_csv("../old_dataset/shoot.csv")
arrest_1_df: pd.DataFrame = pd.read_csv("../old_dataset/arrests_1.csv").rename({"CASE NUMBER": "CASE_NUMBER"}, axis=1)
arrest_2_df: pd.DataFrame = pd.read_csv("../old_dataset/arrests_2.csv").rename({"CASE NUMBER": "CASE_NUMBER"}, axis=1)
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

"""
arrest_case_codes = pd.concat([arrest_1_df["CASE NUMBER"], arrest_2_df["CASE NUMBER"]])
print(f"Ci sono {len(arrest_case_codes)} casi di arresto")

shoot_case_codes = shoot_df["CASE_NUMBER"]
print(f"Ci sono {len(shoot_case_codes)} casi di spari")

result = arrest_case_codes[arrest_case_codes.isin(shoot_case_codes)]
print(f"Intersezione: {len(result)}")
"""

#Adjust features in complete_crimes.csv (renaming and deleting)
def adjust_features():

    col_ren = {'Date' : 'Date_Crime', 'DATE' : 'DATE_SHOOT',
                'BLOCK' : 'BLOCK_SHOOT', 'Block' : 'Block_Crime'}
    #VICTIMIZATION_IUCR_CD == IUCR
    #BLOCK_SHOOT == Block_crime ?
    col_del = ['VICTIMIZATION_IUCR_CD']

    complete_crimes = pd.read_csv("complete_crimes.csv")
    
    complete_crimes.rename(columns = col_ren, inplace = True)
    complete_crimes = complete_crimes.drop(col_del, axis=1)

    complete_crimes.to_csv("complete_crimes_adjust.csv")
    pass