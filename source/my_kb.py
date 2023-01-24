from pyswip import Prolog

def create_kb():
    prolog = Prolog()

    prolog.consult("facts.pl")

    prolog.assertz("same_district(C1, C2) :- district(C1, D), district(C2, D)")
    prolog.assertz("same_beat(C1, C2) :- beat(C1, B), beat(C2, B)")
    prolog.assertz("same_ward(C1, C2) :- ward(C1, W), ward(C2, W)")
    prolog.assertz("same_comm_area(C1, C2) :- comm_area(C1, COM), comm_area(C2, COM)")
    prolog.assertz("is_domestic(C) :- location_description(C, apartment); location_description(C, house); local_description(C, residence); local_description(C, driveway)")
    prolog.assertz("criminal_arrested(C, P) :- has_arrest(C, A), arrested(A, P)")
    prolog.assertz("is_ratial(C) :- criminal_arrested(C, P), victim(C, V), neq(race(V), race(P))")
    prolog.assertz("victim(C, V)")
    prolog.assertz("income_area(C, I) :- comm_area(C, COM), income(COM, I)")
    prolog.assertz("num_of_victims(C, N) :- findall(V, victim(V, C), L), length(L, N)")
    prolog.assertz("num_of_crimes_in_district(C, N) :- findall(C1, same_district(C, C1), L), length(L, N)")
    prolog.assertz("num_of_crimes_in_beat(C, N) :- findall(C1, same_beat(C, C1), L), length(L, N)")
    prolog.assertz("num_of_crimes_community_area(C, N) :- findall(C1, same_comm_area(C, C1), L), length(L, N)")
    prolog.assertz("num_of_crimes_ward(C, N) :- findall(C1, same_ward(C, C1), L), length(L, N)")
    prolog.assertz("num_of_dead(C, N) :- findall(V, (victim(V, C), victimization(V, homicide)), L), length(L, N)")
    prolog.assertz("is_homicide(C) :- victim(C, V), victimization(V, homicide)")
    prolog.assertz("is_killed(V) :- victim(C, V), is_homicide(C)")
    prolog.assertz("num_of_arrest(C, N) :- findall(S, has_arrest(C, S), L), length(L, N)")
    prolog.assertz("night_crime(C) :- crime_date(C, DT), hour_of_day(DT, H), ((H >= 20); (H =< 6))")

    obj = prolog.query("night_crime(X)")

    for x in obj:
        print(x)

create_kb()