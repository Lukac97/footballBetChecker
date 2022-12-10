from selenium import webdriver
from bs4 import BeautifulSoup

from match_details import ClsMatchDetails, ClsResult


class ClsMatchParser:
    """
    Class used for parsing match information from footystats.org.

    Attributes
    ----------
        str_match_link: link to match details on footystats.org

    """

    def __init__(self, _str_match_link):
        """
        Construct instance of ClsMatchParser.

        Parameters
        ----------
            _str_match_link: link to match details on footystats.org.

        """
        self.str_match_link = _str_match_link

    @staticmethod
    def _mtd_unpack_result_from_string(str_result):
        """
        Unpack resulst of a match from string.

        Parameters
        ----------
            str_result: result as string.

        Returns
        -------
            Object containing results.

        """
        lst_split_result = str_result.text.strip("()").split("-")
        int_host_v = int(lst_split_result[0])
        int_guest_v = int(lst_split_result[1])

        return ClsResult(int_host_v, int_guest_v)

    def _mtd_extract_main_stats(self, obj_main_stats):
        """
        Extract main information of match.

        Parameters
        ----------
            obj_main_stats: html node containing main match stats.

        Returns
        -------
            Object containing match details.

        """
        obj_match_details = ClsMatchDetails()

        lst_p = obj_main_stats.findChildren("p", recursive=False)

        obj_match_details.obj_end_goals = \
            self._mtd_unpack_result_from_string(lst_p[0])
        obj_match_details.obj_first_half_goals = \
            self._mtd_unpack_result_from_string(lst_p[2])

        obj_match_details.obj_second_half_goals = ClsResult(
            obj_match_details.obj_end_goals.int_host_v
            - obj_match_details.obj_first_half_goals.int_host_v,
            obj_match_details.obj_end_goals.int_guest_v
            - obj_match_details.obj_first_half_goals.int_guest_v
        )

        return obj_match_details

    def _mtd_get_stat_divs(self):
        """
        Parse html divs/nodes containing main and secondary stats of a match.

        Returns
        -------
            Html div containing main stats
            and html div containing secondary stats.

        """
        driver = webdriver.Firefox()

        driver.get(self.str_match_link)
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

    def mtd_parse_match_details(self):
        """
        Parse match details.

        Returns
        -------
            Object containing match details.

        """
        obj_main_stats, obj_secondary_stats = self._mtd_get_stat_divs()

        return self._mtd_extract_main_stats(obj_main_stats)

