class ClsCombinationRegexes:

    R_OUTCOME = r"(2P|P)?(1|2|X)(1|2|X)?"
    R_GOALS = r"(P1|P2)?(D|G)?g(?:(\d+)-(\d+)|(\d+)\+)"
    R_TRANSITION = r"(NE)?(1|2|X)(1|2|X)?-(1|2|X)(1|2|X)?"
    R_GG_NG = r"(GG|NG)(1|2)?"
