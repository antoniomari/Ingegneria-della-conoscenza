from owlready2 import *


def define_onto():
    onto = get_ontology("urn:crimes")

    with onto:
        class Crime(Thing):
            pass

        class LocationDescription(Crime >> str):
            pass

        class BigCrime(Thing):
            pass

        class Arrest(Thing):
            pass

        class HasArrest(Crime >> Arrest):
            pass

        class Victim(Thing):
            pass

        class HasVictim(Crime >> Victim):
            pass

        class NumOfVictims(Crime >> int):
            pass



    onto.save("crimes.owl")


onto = get_ontology("https://data.cityofchicago.org/Public-Safety/Crimes-2019/w98m-zvie").load()
print(onto.to_string())
