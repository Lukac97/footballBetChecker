import regex as re

from regex_matches import ClsCombinationRegexes


class ClsGGNGCombinationChecker:
    """
    Class used for checking goal-goal and no-goal combinations.

    Attributes
    ----------
        str_combination: combination to check.
        obj_match_details: match details upon which the check shall
                           be performed.

    """

    def __init__(self, _str_combination, _obj_match_details):
        """
        Construct instance of ClsGGNGCombinationChecker

        Parameters
        ----------
            _str_combination: combination to check.
            _obj_match_details: match details upon which the check shall
                                be performed.
        """
        self.str_combination = _str_combination
        self.obj_match_details = _obj_match_details

    def _mtd_get_goals(self, str_halftime_modifier):
        """
        Get goals from whole game or specific halftime.

        Parameters
        ----------
            str_halftime_modifier: specifies the halftime
                                   ('1', '2' or None/"").

        Returns
        -------
            Object containing information about goals of specific halftime
            or None if not found.

        """
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
        """
        Check if gg or ng is correct based on goals.

        Parameters
        ----------
            obj_goals: object containing goals.
            str_gg_modifier: combination, can be 'GG' or 'NG'

        Returns
        -------
            True or False, based on if combination is hit.

        """
        if str_gg_modifier == "GG":
            return obj_goals.int_host_v >= 1 and obj_goals.int_guest_v >= 1
        if str_gg_modifier == "NG":
            return obj_goals.int_host_v < 1 or obj_goals.int_guest_v < 1

        print("GG and NG modifiers must be either 'GG' or 'NG' !")

    def mtd_handle_gg_ng_combination(self):
        """
        Handle GG or NG combination.

        Returns
        -------
            True or False, based on if combination is hit.

        """
        obj_regex = re.match(ClsCombinationRegexes.R_GG_NG,
                             self.str_combination)
        str_gg_modifier, str_ht_modifier = obj_regex.groups()

        obj_goals = self._mtd_get_goals(str_ht_modifier)
        return self._mtd_check_gg_ng_goals(obj_goals, str_gg_modifier)


class ClsOutcomeCombinationChecker:
    """
    Class used for checking outcome combinations.

    Attributes
    ----------
        str_combination: combination to check.
        obj_match_details: match details upon which the check shall
                           be performed.

    """

    def __init__(self, _str_combination, _obj_match_details):
        """
        Construct instance of ClsOutcomeCombinationChecker.

        Parameters
        ----------
            _str_combination: combination to check.
            _obj_match_details: match details upon which the check shall
                                be performed.
        """
        self.str_combination = _str_combination
        self.obj_match_details = _obj_match_details

    def _mtd_get_goals_to_check(self, str_halftime_modifier):
        """
        Get object containing goals required for combination check.

        Parameters
        ----------
            str_halftime_modifier: specifies the halftime
                                   ('1', '2' or None/"").

        Returns
        -------
            Object containing goals.

        """
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
        """
        Get outcome of one result combination.

        Parameters
        ----------
            obj_goals: object containing goals.
            str_res: combination of one outcome.

        Returns
        -------
            True or false, based on correctness.

        """
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
        """
        Handle result of outcomes from combination.

        Parameters
        ----------
            obj_goals: object containing goals.
            str_first_res: first result combination.
            str_second_res: second result combination.

        Returns
        -------
            True if either of result combinations were hit, otherwise False.

        """
        return \
            self._mtd_get_single_outcome_result(obj_goals, str_first_res) \
            or self._mtd_get_single_outcome_result(obj_goals, str_second_res)

    def mtd_handle_outcome_combination(self):
        """
        Handle outcome combination check.

        Returns
        -------
            True if combination is hit, otherwise False.

        """
        obj_regex = re.match(
            ClsCombinationRegexes.R_OUTCOME, self.str_combination)
        str_ht_modifier, str_first_chance_res, str_second_chance_res = \
            obj_regex.groups()
        obj_goals_to_check = self._mtd_get_goals_to_check(str_ht_modifier)

        return self._mtd_handle_outcome_result(
            obj_goals_to_check, str_first_chance_res, str_second_chance_res)


class ClsTransitionCombinationChecker:
    """
    Class used for checking transition combinations.

    Attributes
    ----------
        str_combination: combination to check.
        obj_match_details: match details upon which the check shall
                           be performed.
        _dct_halftime_check_mtd: dictionary of methods used for checking who
                                 won at halftime.
        _dct_halftime_check_mtd: dictionary of methods used for checking who
                                 won at the end.

    """

    def __init__(self, _str_combination, _obj_match_details):
        """
        Construct instance of ClsTransitionCombinationChecker.

        Parameters
        ----------
            _str_combination: combination to check.
            _obj_match_details: match details upon which the check shall
                                be performed.
        """
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
        """
        Check one of the outcomes (halftime or at the end).

        Parameters
        ----------
            dct_check_mtd: dictionary with methods used for checking.
            str_outcome_1: first outcome attempt in combination.
            str_outcome_2: second outcome attempt in combination.

        Returns
        -------
            True if either outcome 1 or outcome 2 are hit, otherwise False.

        """
        if str_outcome_2 is None:
            return dct_check_mtd[str_outcome_1]()

        return dct_check_mtd[str_outcome_1]() \
            or dct_check_mtd[str_outcome_2]()

    def mtd_handle_transition_combination(self):
        """
        Handle checking of transition combination.

        Returns
        -------
            True if transition is hit, otherwise False.

        """
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
    """
    Class used for checking goals combinations.

    Attributes
    ----------
        str_combination: combination to check.
        obj_match_details: match details upon which the check shall
                           be performed.

    """

    def __init__(self, _str_combination, _obj_match_details):
        """
        Construct instance of ClsGoalCombinationChecker.

        Parameters
        ----------
            _str_combination: combination to check.
            _obj_match_details: match details upon which the check shall
                                be performed.

        """
        self.str_combination = _str_combination
        self.obj_match_details = _obj_match_details

    @staticmethod
    def _mtd_check_goal_range(int_goals, int_lower, int_upper):
        """
        Check if goals are in the goal range.

        Parameters
        ----------
            int_goals: goals to check.
            int_lower: lower limit.
            int_upper: upper limit.

        Returns
        -------
            True if goals are in range, otherwise False.

        """
        return int_lower <= int_goals <= int_upper \
            if int_upper is not None \
            else int_lower <= int_goals

    def _mtd_get_goal_number(self, str_half_modifier):
        """
        Get object containing goals.

        Parameters
        ----------
            str_half_modifier: specifies whether first half, second half or
                               whole match is taken.

        Returns
        -------
            Object containing goals.

        """
        if str_half_modifier is None or str_half_modifier == "":
            return self.obj_match_details.obj_end_goals

        if str_half_modifier == "P1":
            return self.obj_match_details.obj_first_half_goals

        if str_half_modifier == "P2":
            return self.obj_match_details.obj_second_half_goals

    def _mtd_handle_goal_range(self, obj_goals, str_modifier,
                               int_lower, int_upper):
        """
        Handle goal range for guest, host or both.

        Parameters
        ----------
            obj_goals: object containing goals.
            str_modifier: specifies whether host, guest or goals of both are
                          taken into account.
            int_lower: lower limit.
            int_upper: upper limit.

        Returns
        -------
            True if goals of host/guest/both are hit, otherwise False.

        """
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
        """
        Handle goal combination.

        Returns
        -------
            True if combination is hit, otherwise False.

        """
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
    """
    Class used for checking combinations.

    Attributes
    ----------
        lst_combinations_to_check: list of combinations to be checked.
        obj_match_details: match details upon which the check shall
                           be performed.

    """

    def __init__(self, _obj_match_details, _lst_combinations_to_check):
        """
        Construct instance of ClsCombinationChecker.

        Parameters
        ----------
            _obj_match_details: match details upon which the check shall
                                be performed.
            _lst_combinations_to_check: list of combinations to be checked.

        """
        self.lst_combinations_to_check = _lst_combinations_to_check
        self.obj_match_details = _obj_match_details

    def _mtd_handle_combination_mix(self, str_combination):
        """
        Handle mix of combinations.

        If combinations are separated by & or |, they are split and handled
        separately. The results of separated combinations are then merged using
        corresponding logical operations.

        Parameters
        ----------
            str_combination: combination to try to split.

        Returns
        -------
            True if combination is hit, otherwise False.

        """
        if "|" in str_combination:
            return any(
                self._mtd_get_combination_result(str_split_cmb)
                for str_split_cmb in str_combination.split("|"))

        if "&" in str_combination:
            return all(
                self._mtd_get_combination_result(str_split_cmb)
                for str_split_cmb in str_combination.split("&"))

    def _mtd_get_combination_result(self, str_combination):
        """
        Get result of combination.

        Parameters
        ----------
            str_combination: combination to check.

        Returns
        -------
            True if combination is hit, otherwise False.

        """
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
        """
        Check all combinations.

        Returns
        -------
            Dictionary of combinations and their results (True/False).

        """
        dct_result = {}
        for str_combination in self.lst_combinations_to_check:
            if str_combination in dct_result:
                continue

            dct_result[str_combination] = self._mtd_get_combination_result(
                str_combination)

        return dct_result
