from pyswip import Prolog

def kb_usage():

    kb = Prolog()
    kb.consult("facts.pl")
    obj = kb.query("night_crime(X)")

    for x in obj:
        print(x)