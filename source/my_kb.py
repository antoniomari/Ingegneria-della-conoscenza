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
    prolog.assertz("victimization(C, V, T)")
    prolog.assertz("income_area(C, I) :- comm_area(C, COM), income(COM, I)")
    prolog.assertz("num_of_victims(C, N) :- findall(V, victimization(C, V, T), L), length(L, N)")
    prolog.assertz("num_of_crimes_in_district(C, N) :- findall(C1, same_district(C, C1), L), length(L, N)")
    prolog.assertz("num_of_crimes_in_beat(C, N) :- findall(C1, same_beat(C, C1), L), length(L, N)")
    prolog.assertz("num_of_crimes_community_area(C, N) :- findall(C1, same_comm_area(C, C1), L), length(L, N)")
    prolog.assertz("num_of_crimes_ward(C, N) :- findall(C1, same_ward(C, C1), L), length(L, N)")
    prolog.assertz("num_of_dead(C, N) :- findall(V, victimization(C, V, homicide), L), length(L, N)")
    prolog.assertz("is_homicide(C) :- victimization(C, V, homicide)")
    prolog.assertz("is_killed(V) :- victimization(C, V, homicide)")
    prolog.assertz("num_of_arrest(C, N) :- findall(S, has_arrest(C, S), L), length(L, N)")
    prolog.assertz("night_crime(C) :- crime_date(C, datime(date(Y, M, D, H, M, S))), ((H >= 20; H =< 6))")

    prolog.assertz("immediately_arrest(C) :- crime_data(C, D1), arrest_date(C, D1)") # or choose an error of date
    # Add victime_age fact, i.e victim_age(crime, victim)
    prolog.assertz("is_there_a_child(C, T) :- victimization(C, V, T), victim_age(V, A), A <= 15")
    prolog.assertz("is_killed_a_child(C) :- is_there_a_child(C, homicide)")

    prolog.assertz("crime_by_group(C) :- num_of_arrest(C, N), N >= 2")
    obj = prolog.query("night_crime(X)")

    for x in obj:
        print(x)


# suppongo che ci sia già
def calculate_features(crime_id) -> dict:

    # num of crimes in district
    



create_kb()