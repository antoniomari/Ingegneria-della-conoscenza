from pyswip import Prolog

def kb_usage():

    kb = Prolog()
    kb.consult("facts.pl")
    obj = kb.query("num_of_arrest(A, N)")

    for x in obj:
        print(x)