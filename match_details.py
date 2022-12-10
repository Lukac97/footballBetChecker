class ClsResult:
    """
    Class used for storing the result of a portion of a match.

    Attributes
    ----------
        int_host_v: number of host goals.
        int_guest_v: number of guest goals.

    """

    def __init__(self, _host_v, _guest_v):
        """
        Construct instace of ClsResult.

        Parameters
        ----------
            _host_v: number of host goals.
            _guest_v: number of guest goals.

        """
        self.int_host_v = _host_v
        self.int_guest_v = _guest_v

    def mtd_get_total_goals(self):
        """
        Get total number of goals.

        Returns
        -------
            Guest and host goals.

        """
        return self.int_host_v + self.int_guest_v

    def mtd_host_won(self):
        """
        Check if host won.

        Returns
        -------
            True if host won, otherwise False.

        """
        return self.int_host_v > self.int_guest_v

    def mtd_guest_won(self):
        """
        Check if guest won.

        Returns
        -------
            True if guest won, otherwise False.

        """
        return self.int_host_v < self.int_guest_v

    def mtd_tied(self):
        """
        Check if tied.

        Returns
        -------
            True if tied, otherwise False.

        """
        return self.int_host_v == self.int_guest_v


class ClsMatchDetails:
    """
    Class used for storing match details.

    Attributes
    ----------
        obj_first_half_goals: object containing goals of the first half.
        obj_second_half_goals: object containing goals of the second half.
        obj_end_goals: object containing goals of the whole match.

    """

    def __init__(self):
        """Construct instance of ClsMatchDetails."""
        self.obj_first_half_goals = None
        self.obj_second_half_goals = None
        self.obj_end_goals = None
