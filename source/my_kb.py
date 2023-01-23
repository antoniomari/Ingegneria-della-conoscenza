import pytholog

def create_kb():
    
    kb = pytholog.knowledge_base("crimes.pl")
    kb([
        "same_district(C1, C2) :- district(C1, D), district(C2, D)",
        "has_arrest(C, A)", # fact for each copule (crime, arrest)
        "is_domestic(C) :- location_description(C, apartment); location_description(C, house); local_description(C, residence); local_description(C, driveway);",
        ])
    pass