from pyswip import Prolog

def kb_usage():

    kb = Prolog()
    kb.consult("facts.pl")
    kb.asserta("num_of_arrest(C, N) :- findall(S, has_arrest(C, S), L), length(L, N)")
    obj = kb.query("num_of_arrest(A, N)")

    for x in obj:
        print(x)