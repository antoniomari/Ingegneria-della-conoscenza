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
shoot_df: pd.DataFrame = pd.read_csv("../old_dataset/shoot.csv")
arrest_1_df: pd.DataFrame = pd.read_csv("../old_dataset/arrests_1.csv")
arrest_2_df: pd.DataFrame = pd.read_csv("../old_dataset/arrests_2.csv")

arrest_case_codes = pd.concat([arrest_1_df["CASE NUMBER"], arrest_2_df["CASE NUMBER"]])
print(f"Ci sono {len(arrest_case_codes)} casi di arresto")

shoot_case_codes = shoot_df["CASE_NUMBER"]
print(f"Ci sono {len(shoot_case_codes)} casi di spari")

result = arrest_case_codes[arrest_case_codes.isin(shoot_case_codes)]
print(f"Intersezione: {len(result)}")




