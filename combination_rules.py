import regex as re

from regex_matches import ClsCombinationRegexes


class ClsTransitionCombinationChecker:

    def __init__(self, _str_combination, _obj_match_details):
        self.str_combination = _str_combination
        self.obj_match_details = _obj_match_details

        self._dct_halftime_check_mtd = {
            "1": self.obj_match_details.mtd_host_won_ht,
            "2": self.obj_match_details.mtd_guest_won_ht,
            "X": self.obj_match_details.mtd_tied_ht,
        }
        self._dct_endtime_check_mtd = {
            "1": self.obj_match_details.mtd_host_won,
            "2": self.obj_match_details.mtd_guest_won,
            "X": self.obj_match_details.mtd_tied,
        }

    def mtd_handle_transition_combination(self):
        obj_reg_match = \
            re.match(ClsCombinationRegexes.R_TRANSITION,
                     self.str_combination)

        lst_groups = obj_reg_match.groups()

        return self._dct_halftime_check_mtd[lst_groups[0]]() and \
            self._dct_endtime_check_mtd[lst_groups[1]]()


class ClsGoalCombinationChecker:

    def __init__(self, _str_combination, _obj_match_details):
        self.str_combination = _str_combination
        self.obj_match_details = _obj_match_details

    def _mtd_check_goal_range(self, int_goals, int_lower, int_upper):
        return int_lower <= int_goals <= int_upper \
            if int_upper is not None \
            else int_lower <= int_goals

    def _mtd_get_goal_number(self, str_half_modifier):
        if str_half_modifier == "":
            return (
                self.obj_match_details.obj_end_goals.mtd_get_total_goals(),
                self.obj_match_details.obj_end_goals.int_host_v,
                self.obj_match_details.obj_end_goals.int_guest_v
            )

        if str_half_modifier == "P1":
            return (
                self.obj_match_details.obj_first_half_goals
                .mtd_get_total_goals(),
                self.obj_match_details.obj_first_half_goals.int_host_v,
                self.obj_match_details.obj_first_half_goals.int_guest_v
            )

        if str_half_modifier == "P2":
            return (
                self.obj_match_details.obj_second_half_goals
                .mtd_get_total_goals(),
                self.obj_match_details.obj_second_half_goals.int_host_v,
                self.obj_match_details.obj_second_half_goals.int_guest_v
            )

    def _mtd_handle_goal_range(self, str_half_modifier, str_modifier,
                               int_lower, int_upper):

        if str_modifier == "":
            return self._mtd_check_goal_range(
                self.obj_match_details.obj_end_goals.mtd_get_total_goals(),
                int_lower, int_upper)
        if str_modifier == "D":
            return self._mtd_check_goal_range(
                self.obj_match_details.obj_end_goals.int_host_v,
                int_lower, int_upper)
        if str_modifier == "G":
            return self._mtd_check_goal_range(
                self.obj_match_details.obj_end_goals.int_guest_v,
                int_lower, int_upper)

        print(f"Modifier '{str_modifier}' not recognized!")
        return False

    def mtd_handle_goal_combination(self):
        obj_reg = re.match(ClsCombinationRegexes.R_GOALS, self.str_combination)
        lst_reg_groups = obj_reg.groups()
        if lst_reg_groups[2] is not None and lst_reg_groups[3] is not None:
            return self._mtd_handle_goal_range(
                lst_reg_groups[0],
                lst_reg_groups[1],
                int(lst_reg_groups[2]), int(lst_reg_groups[3]))
        if lst_reg_groups[4] is not None:
            return self._mtd_handle_goal_range(
                lst_reg_groups[0],
                lst_reg_groups[1],
                int(lst_reg_groups[4]), None)

        print(f"Combination '{self.str_combination}' is not valid!")
        return False


class ClsCombinationChecker:

    def __init__(self, _obj_match_details, _lst_combinations_to_check):
        self.lst_combinations_to_check = _lst_combinations_to_check
        self.obj_match_details = _obj_match_details

        self.dct_combinations = {
            "1": lambda: self.obj_match_details.mtd_host_won(),
            "2": lambda: self.obj_match_details.mtd_guest_won(),
            "X": lambda: self.obj_match_details.mtd_tied(),
            "P1": lambda: self.obj_match_details.mtd_host_won_ht(),
            "P2": lambda: self.obj_match_details.mtd_guest_won_ht(),
            "PX": lambda: self.obj_match_details.mtd_tied_ht(),
            "1X": lambda: (
                    self.obj_match_details.mtd_host_won()
                    or self.obj_match_details.mtd_tied()),
            "X2": lambda: (
                    self.obj_match_details.mtd_guest_won()
                    or self.obj_match_details.mtd_tied()),
            "12": lambda: (
                    self.obj_match_details.mtd_host_won()
                    or self.obj_match_details.mtd_guest_won())
        }

    def _mtd_handle_combination_mix(self, str_combination):
        if "|" in str_combination:
            return any(
                self._mtd_get_combination_result(str_split_cmb)
                for str_split_cmb in str_combination.split("|"))

        if "&" in str_combination:
            return all(
                self._mtd_get_combination_result(str_split_cmb)
                for str_split_cmb in str_combination.split("&"))

    def _mtd_get_combination_result(self, str_combination):
        if "|" in str_combination or "&" in str_combination:
            return self._mtd_handle_combination_mix(str_combination)

        if str_combination in self.dct_combinations:
            return self.dct_combinations[str_combination]()

        if re.match(ClsCombinationRegexes.R_TRANSITION,
                    str_combination) is not None:
            return ClsTransitionCombinationChecker(
                str_combination, self.obj_match_details
            ).mtd_handle_transition_combination()

        if re.match(ClsCombinationRegexes.R_GOALS,
                    str_combination) is not None:
            return ClsGoalCombinationChecker(
                str_combination,
                self.obj_match_details
            ).mtd_handle_goal_combination()

    def mtd_check_all_combinations(self):
        dct_result = {}
        for str_combination in self.lst_combinations_to_check:
            if str_combination in dct_result:
                continue

            dct_result[str_combination] = self._mtd_get_combination_result(
                str_combination)

        return dct_result
