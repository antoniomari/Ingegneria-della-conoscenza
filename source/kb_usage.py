from pyswip import Prolog

def kb_usage():

    kb = Prolog()
    kb.consult("facts.pl")
    obj = kb.query("arrest_date(30206087,01_04_2023_12_20_00_pm)")

    for x in obj:
        print(x)