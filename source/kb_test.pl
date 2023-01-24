district(c1, d).
district(c2, d).
district(c3, d).
same_district(c1, c2).
same_district(c1, c3).
same_district(c2, c3).
same_beat(C1, C2) :- beat(C1, B), beat(C2, B).
same_ward(C1, C2) :- ward(C1, W), ward(C2, W).
same_comm_area(C1, C2) :- comm_area(C1, COM), comm_area(C2, COM).
location_description(hs227745, house).
location_description(hs335199, alley).
location_description(hs440368, house).