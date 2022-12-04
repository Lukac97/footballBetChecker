class ClsResult:

    def __init__(self, _host_v, _guest_v):
        self.int_host_v = _host_v
        self.int_guest_v = _guest_v

    def mtd_get_total_goals(self):
        return self.int_host_v + self.int_guest_v


class ClsMatchDetails:

    def __init__(self):
        self.obj_first_half_goals = None
        self.obj_second_half_goals = None
        self.obj_end_goals = None

    def mtd_host_won(self):
        return self.obj_end_goals.int_host_v > \
               self.obj_end_goals.int_guest_v

    def mtd_guest_won(self):
        return self.obj_end_goals.int_host_v < \
               self.obj_end_goals.int_guest_v

    def mtd_tied(self):
        return self.obj_end_goals.int_host_v == \
               self.obj_end_goals.int_guest_v

    def mtd_host_won_ht(self):
        return self.obj_first_half_goals.int_host_v > \
               self.obj_first_half_goals.int_guest_v

    def mtd_guest_won_ht(self):
        return self.obj_first_half_goals.int_host_v < \
               self.obj_first_half_goals.int_guest_v

    def mtd_tied_ht(self):
        return self.obj_first_half_goals.int_host_v == \
               self.obj_first_half_goals.int_guest_v
