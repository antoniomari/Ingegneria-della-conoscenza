import owlready2
import rdflib
from rdflib import Namespace, URIRef, RDF
from rdflib import Literal
from rdflib.plugins.sparql import prepareQuery
import pandas as pd

"""
def main():
    g.parse("dataset/health.rdf", format="xml")
    g.parse("dataset/iucr.rdf", format="xml")
    g.parse("clean_dataset/shoot.rdf", format="xml")
    g.parse("clean_dataset/arrests.rdf", format="xml")
    g.parse("clean_dataset/crimes.rdf", format="xml")

    rdf_xml = g.serialize(format="xml")

    with open("../dataset/complete.rdf", "w") as f:
        f.write(rdf_xml)

    return

    # https://data.cityofchicago.org/resource/c7ck-438e
    # https://data.cityofchicago.org/resource/c7ck-438e/row-64j9.3jfn.um5m --> esempio categoria

    query = prepareQuery("SELECT ?s ?p ?o WHERE "
                         "{ ?s "
                         "?p <https://data.cityofchicago.org/resource/c7ck-438e>}")

    query = prepareQuery("SELECT ?s ?p ?o WHERE "
                         "{ ?s ?p ?o}")

    results = g.query(query)
    for row in results:
        print(row)

    print("Num risultati: " + str(len(results)))

    return


    crimes_list = []
    for sub, pred, obj in results:
        crimes_list.append(sub)

    # query_on_crime(crimes_list[0])
    search_inactive()


def query_on_crime(crime_uri: rdflib.term.URIRef):

    query = prepareQuery("SELECT ?s ?p ?o WHERE "
                         "{ ?s ?p ?o}")

    results = g.query(query, initBindings={"s": crime_uri})

    for row in results:
        print(row)


def search_inactive():
    query = prepareQuery("SELECT ?s WHERE "
                         "{ ?s <https://data.cityofchicago.org/resource/c7ck-438e/active> \"false\"}")

    results = g.query(query)
    for row in results:
        print(row)


g = rdflib.Graph()
main()

    columns = ["CASE_NUMBER", "DATE_SHOOT", "BLOCK", "VICTIMIZATION_PRIMARY", "INCIDENT_PRIMARY", "GUNSHOT_INJURY_I",
               "ZIP_CODE", "WARD", "STREET_OUTREACH_ORGANIZATION", "AREA", "DISTRICT", "BEAT", "AGE", "SEX",
               "victim_race", "INCIDENT_IUCR_CD", "HOMICIDE_VICTIM_FIRST_NAME", "HOMICIDE_VICTIM_MI",
               "HOMICIDE_VICTIM_LAST_NAME", "DAY_OF_WEEK", "STATE_HOUSE_DISTRICT", "STATE_SENATE_DISTRICT",
               "ARREST_NUMBER", "ARREST DATE", "criminal_race", "CHARGE 1 STATUTE", "CHARGE 1 DESCRIPTION",
               "CHARGE 1 TYPE", "CHARGE 1 CLASS", "CHARGE 2 STATUTE", "CHARGE 2 DESCRIPTION", "CHARGE 2 TYPE",
               "CHARGE 2 CLASS", "CHARGE 3 STATUTE", "CHARGE 3 DESCRIPTION", "CHARGE 3 TYPE", "CHARGE 3 CLASS",
               "CHARGE 4 STATUTE", "CHARGE 4 DESCRIPTION", "CHARGE 4 TYPE", "CHARGE 4 CLASS", "CHARGES STATUTE",
               "CHARGES DESCRIPTION", "CHARGES TYPE", "CHARGES CLASS", "Location Description", "Domestic",
               "Community Area", "Latitude", "Longitude"
               ]

    f = [, , "BLOCK", "VICTIMIZATION_PRIMARY", "INCIDENT_PRIMARY", "GUNSHOT_INJURY_I",
               "ZIP_CODE", "WARD", "STREET_OUTREACH_ORGANIZATION", "AREA", "DISTRICT", "BEAT", "AGE", "SEX",
               "victim_race", "INCIDENT_IUCR_CD", "HOMICIDE_VICTIM_FIRST_NAME", "HOMICIDE_VICTIM_MI",
               "HOMICIDE_VICTIM_LAST_NAME", "DAY_OF_WEEK", "STATE_HOUSE_DISTRICT", "STATE_SENATE_DISTRICT",
               "ARREST_NUMBER", "ARREST DATE", "criminal_race", "CHARGE 1 STATUTE", "CHARGE 1 DESCRIPTION",
               "CHARGE 1 TYPE", "CHARGE 1 CLASS", "CHARGE 2 STATUTE", "CHARGE 2 DESCRIPTION", "CHARGE 2 TYPE",
               "CHARGE 2 CLASS", "CHARGE 3 STATUTE", "CHARGE 3 DESCRIPTION", "CHARGE 3 TYPE", "CHARGE 3 CLASS",
               "CHARGE 4 STATUTE", "CHARGE 4 DESCRIPTION", "CHARGE 4 TYPE", "CHARGE 4 CLASS", "CHARGES STATUTE",
               "CHARGES DESCRIPTION", "CHARGES TYPE", "CHARGES CLASS", "Location Description", "Domestic",
               "Community Area", "Latitude", "Longitude"
               ]
"""


def create_graph():
    crime_dataset: pd.DataFrame = pd.read_csv("../source/crimes_selected.csv")
    g = rdflib.Graph()

    crime_ns = Namespace("urn:crime/")
    crime_onto = owlready2.get_ontology("crimes.owl").load()
    crime_class = URIRef(crime_onto.Crime.iri)
    ds = Namespace("https://data.cityofchicago.org/resource/crimes/")

    for index, row in crime_dataset.iterrows():
        crime_uri = crime_ns[row["CASE_NUMBER"]]
        g.add((crime_uri, ds["case_number"], Literal(row["CASE_NUMBER"])))
        g.add((crime_uri, RDF.type, crime_class))
        g.add((crime_uri, ds["location_description"], Literal(row["Location Description"])))
        g.add((crime_uri, ds["domestic"], Literal(row["Domestic"])))
        g.add((crime_uri, ds["beat"], Literal(row["Beat"])))
        g.add((crime_uri, ds["district"], Literal(row["District"])))
        g.add((crime_uri, ds["ward"], Literal(row["Ward"])))
        g.add((crime_uri, ds["community_area"], Literal(row["Community Area"])))
        g.add((crime_uri, ds["latitude"], Literal(row["Latitude"])))
        g.add((crime_uri, ds["longitude"], Literal(row["Longitude"])))

    rdf_xml = g.serialize(format="xml")

    with open("../rdf_prova/crimes.rdf", "w") as f:
        f.write(rdf_xml)


create_graph()



