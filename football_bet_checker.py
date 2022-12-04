import sys

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

from combination_rules import ClsCombinationChecker
from match_details import ClsResult, ClsMatchDetails


def fct_unpack_result_from_string(str_result):
    lst_split_result = str_result.text.strip("()").split("-")
    int_host_v = int(lst_split_result[0])
    int_guest_v = int(lst_split_result[1])

    return ClsResult(int_host_v, int_guest_v)


def fct_extract_main_stats(obj_main_stats):
    obj_match_details = ClsMatchDetails()

    lst_p = obj_main_stats.findChildren("p", recursive=False)

    obj_match_details.obj_end_goals = \
        fct_unpack_result_from_string(lst_p[0])
    obj_match_details.obj_first_half_goals = \
        fct_unpack_result_from_string(lst_p[2])

    obj_match_details.obj_second_half_goals = ClsResult(
        obj_match_details.obj_end_goals.int_host_v
        - obj_match_details.obj_first_half_goals.int_host_v,
        obj_match_details.obj_end_goals.int_guest_v
        - obj_match_details.obj_first_half_goals.int_guest_v
    )

    return obj_match_details


def fct_get_stat_divs():
    driver = webdriver.Firefox()

    if len(sys.argv) <= 1:
        print("Please use link from footystats.org to a specific match "
              "as first argument!")
        sys.exit()

    driver.get(sys.argv[1])
    content = driver.page_source
    driver.close()

    soup = BeautifulSoup(content, features="html.parser")
    obj_main = soup.find_all("main")[0]
    obj_section = obj_main.findChildren(
        "section", class_="ft-data", recursive=False)[0]

    obj_div_row = obj_section.findChildren(
        "div", class_="row", recursive=False)[0]

    return obj_div_row.findChildren(
        "div", recursive=False)


if __name__ == '__main__':
    obj_main_stats, obj_secondary_stats = fct_get_stat_divs()

    obj_match_details = fct_extract_main_stats(obj_main_stats)

    if len(sys.argv) <= 2:
        print("No combinations were given.")
        sys.exit()

    dct_res = ClsCombinationChecker(
        obj_match_details, sys.argv[2].split(";")
    ).mtd_check_all_combinations()

    print("COMBINATION RESULTS: ")
    for str_comb, bol_res in dct_res.items():
        print(f"'{str_comb}': {bol_res}")
