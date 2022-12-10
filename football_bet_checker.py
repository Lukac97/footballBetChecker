import sys

from combination_rules import ClsCombinationChecker
from match_parser import ClsMatchParser


def fct_take_user_input():
    """
    Take input from user, in case they are not given as arguments.

    Returns
    -------
        Link to match and combinations as string.

    """
    str_link = ""
    str_combinations = ""

    while "footystats.org" not in str_link:
        print("Please enter a footystats.org link to match: ")
        str_link = input()

    while str_combinations == "":
        print("Please enter combinations separated by a semicolon (;): ")
        str_combinations = input()

    return str_link, str_combinations


def fct_handle_inputs():
    """
    Handle user inputs, through arguments or through menu.

    Returns
    -------
        Match link and combinations.

    """
    if len(sys.argv) >= 3:
        return sys.argv[1], sys.argv[2]

    return fct_take_user_input()


def fct_football_bet_checker():
    """Check betting combinations on a football match."""
    str_match_link, str_combinations = fct_handle_inputs()

    obj_match_details = ClsMatchParser(
        str_match_link
    ).mtd_parse_match_details()

    dct_res = ClsCombinationChecker(
        obj_match_details, str_combinations.split(";")
    ).mtd_check_all_combinations()

    print("COMBINATION RESULTS: ")
    for str_comb, bol_res in dct_res.items():
        print(f"'{str_comb}': {bol_res}")


if __name__ == '__main__':
    fct_football_bet_checker()
