import pandas as pd
from pyswip import Prolog
import pytholog
import pyswip

def kb_usage():

    #kb = pytholog.KnowledgeBase("k.pl")
    #kb.from_file("my_findall.pl")
    kb = Prolog()
    kb.consult("my_findall.pl")
    obj = kb.query("num_of_c(a, N)")
    #obj = kb.query(pytholog.Expr("length([a, b], N)"))

    for x in obj:
        print(x)