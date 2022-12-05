import regex as re

from regex_matches import ClsCombinationRegexes


class ClsGGNGCombinationChecker:

    def __init__(self, _str_combination, _obj_match_details):
        self.str_combination = _str_combination
        self.obj_match_details = _obj_match_details

    def _mtd_get_goals(self, str_halftime_modifier):
        if str_halftime_modifier is None or str_halftime_modifier == "":
            return self.obj_match_details.obj_end_goals
        if str_halftime_modifier == "1":
            return self.obj_match_details.obj_first_half_goals
        if str_halftime_modifier == "2":
            return self.obj_match_details.obj_second_half_goals

        print("GG and NG must have either '', '1' or '2' "
              "as halftime modifiers!")

    @staticmethod
    def _mtd_check_gg_ng_goals(obj_goals, str_gg_modifier):
        if str_gg_modifier == "GG":
            return obj_goals.int_host_v >= 1 and obj_goals.int_guest_v >= 1
        if str_gg_modifier == "NG":
            return obj_goals.int_host_v < 1 or obj_goals.int_guest_v < 1

        print("GG and NG modifiers must be either 'GG' or 'NG' !")

    def mtd_handle_gg_ng_combination(self):
        obj_regex = re.match(ClsCombinationRegexes.R_GG_NG,
                             self.str_combination)
        str_gg_modifier, str_ht_modifier = obj_regex.groups()

        obj_goals = self._mtd_get_goals(str_ht_modifier)
        return self._mtd_check_gg_ng_goals(obj_goals, str_gg_modifier)


class ClsOutcomeCombinationChecker:

    def __init__(self, _str_combination, _obj_match_details):
        self.str_combination = _str_combination
        self.obj_match_details = _obj_match_details

    def _mtd_get_goals_to_check(self, str_halftime_modifier):
        if str_halftime_modifier is None or str_halftime_modifier == "":
            return self.obj_match_details.obj_end_goals
        if str_halftime_modifier == "P":
            return self.obj_match_details.obj_first_half_goals
        if str_halftime_modifier == "2P":
            return self.obj_match_details.obj_second_half_goals

        print("Wrong modifier given to outcome of the match, "
              "must be '', 'P' or '2P'!")

    @staticmethod
    def _mtd_get_single_outcome_result(obj_goals, str_res):
        if str_res is None:
            return False

        if str_res == "1":
            return obj_goals.int_host_v > obj_goals.int_guest_v
        if str_res == "2":
            return obj_goals.int_host_v < obj_goals.int_guest_v
        if str_res == "X":
            return obj_goals.int_host_v == obj_goals.int_guest_v

        return False

    def _mtd_handle_outcome_result(self, obj_goals, str_first_res,
                                   str_second_res):
        return \
            self._mtd_get_single_outcome_result(obj_goals, str_first_res) \
            or self._mtd_get_single_outcome_result(obj_goals, str_second_res)

    def mtd_handle_outcome_combination(self):
        obj_regex = re.match(
            ClsCombinationRegexes.R_OUTCOME, self.str_combination)
        str_ht_modifier, str_first_chance_res, str_second_chance_res = \
            obj_regex.groups()
        obj_goals_to_check = self._mtd_get_goals_to_check(str_ht_modifier)

        return self._mtd_handle_outcome_result(
            obj_goals_to_check, str_first_chance_res, str_second_chance_res)


class ClsTransitionCombinationChecker:

    def __init__(self, _str_combination, _obj_match_details):
        self.str_combination = _str_combination
        self.obj_match_details = _obj_match_details

        self._dct_halftime_check_mtd = {
            "1": self.obj_match_details.obj_first_half_goals.mtd_host_won,
            "2": self.obj_match_details.obj_first_half_goals.mtd_guest_won,
            "X": self.obj_match_details.obj_first_half_goals.mtd_tied,
        }
        self._dct_endtime_check_mtd = {
            "1": self.obj_match_details.obj_end_goals.mtd_host_won,
            "2": self.obj_match_details.obj_end_goals.mtd_guest_won,
            "X": self.obj_match_details.obj_end_goals.mtd_tied,
        }

    @staticmethod
    def _mtd_check_single_outcome(dct_check_mtd, str_outcome_1,
                                  str_outcome_2):
        if str_outcome_2 is None:
            return dct_check_mtd[str_outcome_1]()

        return dct_check_mtd[str_outcome_1]() \
            or dct_check_mtd[str_outcome_2]()

    def mtd_handle_transition_combination(self):
        obj_reg_match = \
            re.match(ClsCombinationRegexes.R_TRANSITION,
                     self.str_combination)

        str_logical_not, str_halftime_1, str_halftime_2, \
            str_end_1, str_end_2 = obj_reg_match.groups()

        bol_result = (
            self._mtd_check_single_outcome(
                self._dct_halftime_check_mtd, str_halftime_1, str_halftime_2)
            and
            self._mtd_check_single_outcome(
                self._dct_endtime_check_mtd, str_end_1, str_end_2)
        )

        return (
            not bol_result
            if str_logical_not == "NE"
            else bol_result)


class ClsGoalCombinationChecker:

    def __init__(self, _str_combination, _obj_match_details):
        self.str_combination = _str_combination
        self.obj_match_details = _obj_match_details

    @staticmethod
    def _mtd_check_goal_range(int_goals, int_lower, int_upper):
        return int_lower <= int_goals <= int_upper \
            if int_upper is not None \
            else int_lower <= int_goals

    def _mtd_get_goal_number(self, str_half_modifier):
        if str_half_modifier is None or str_half_modifier == "":
            return self.obj_match_details.obj_end_goals

        if str_half_modifier == "P1":
            return self.obj_match_details.obj_first_half_goals

        if str_half_modifier == "P2":
            return self.obj_match_details.obj_second_half_goals

    def _mtd_handle_goal_range(self, obj_goals, str_modifier,
                               int_lower, int_upper):
        if str_modifier is None or str_modifier == "":
            return self._mtd_check_goal_range(
                obj_goals.mtd_get_total_goals(),
                int_lower, int_upper)
        if str_modifier == "D":
            return self._mtd_check_goal_range(
                obj_goals.int_host_v,
                int_lower, int_upper)
        if str_modifier == "G":
            return self._mtd_check_goal_range(
                obj_goals.int_guest_v,
                int_lower, int_upper)

        print(f"Modifier '{str_modifier}' not recognized!")
        return False

    def mtd_handle_goal_combination(self):
        obj_reg = re.match(ClsCombinationRegexes.R_GOALS, self.str_combination)
        str_ht_mod, str_guest_host_mod,\
            str_lower_limit, str_upper_limit, \
            str_single_goal_limit = obj_reg.groups()

        obj_goals = self._mtd_get_goal_number(str_ht_mod)

        if str_lower_limit is not None and str_upper_limit is not None:
            return self._mtd_handle_goal_range(
                obj_goals,
                str_guest_host_mod,
                int(str_lower_limit), int(str_upper_limit))
        if str_single_goal_limit is not None:
            return self._mtd_handle_goal_range(
                obj_goals,
                str_guest_host_mod,
                int(str_single_goal_limit), None)

        print(f"Combination '{self.str_combination}' is not valid!")
        return False


class ClsCombinationChecker:

    def __init__(self, _obj_match_details, _lst_combinations_to_check):
        self.lst_combinations_to_check = _lst_combinations_to_check
        self.obj_match_details = _obj_match_details

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

        dct_combination_regexes = {
            ClsCombinationRegexes.R_OUTCOME:
                ClsOutcomeCombinationChecker(
                    str_combination,
                    self.obj_match_details
                ).mtd_handle_outcome_combination,

            ClsCombinationRegexes.R_TRANSITION:
                ClsTransitionCombinationChecker(
                    str_combination, self.obj_match_details
                ).mtd_handle_transition_combination,

            ClsCombinationRegexes.R_GOALS:
                ClsGoalCombinationChecker(
                    str_combination,
                    self.obj_match_details
                ).mtd_handle_goal_combination,

            ClsCombinationRegexes.R_GG_NG:
                ClsGGNGCombinationChecker(
                    str_combination, self.obj_match_details
                ).mtd_handle_gg_ng_combination
        }

        for str_regex, mtd_checker in dct_combination_regexes.items():
            if re.fullmatch(str_regex, str_combination):
                return mtd_checker()

    def mtd_check_all_combinations(self):
        dct_result = {}
        for str_combination in self.lst_combinations_to_check:
            if str_combination in dct_result:
                continue

            dct_result[str_combination] = self._mtd_get_combination_result(
                str_combination)

        return dct_result
