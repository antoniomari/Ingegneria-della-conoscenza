import rdflib
from rdflib.plugins.sparql import prepareQuery


def main():
    g.parse("dataset/cases_2022.rdf", format="xml")

    # https://data.cityofchicago.org/resource/c7ck-438e
    # https://data.cityofchicago.org/resource/c7ck-438e/row-64j9.3jfn.um5m --> esempio categoria
    query = prepareQuery("SELECT ?s ?p ?o WHERE "
                         "{ ?s "
                         "?p <https://data.cityofchicago.org/resource/c7ck-438e>}")
    results = g.query(query)

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