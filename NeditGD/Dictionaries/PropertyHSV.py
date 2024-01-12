class HSV():
    h: 0
    s: 0
    v: 0

    s_checked: False
    v_checked: False

    def __init__(self, h: float, s: float, v: float,
                 s_checked: bool=False,
                 v_checked: bool=False) -> None:
        self.h = h
        self.s = s
        self.v = v
        self.s_checked = bool(s_checked)
        self.v_checked = bool(v_checked)

    def __str__(self):
        desc = 'HSV(h={0}, s={1}, v={2}'.format(
            *self.get_property_list())
        if self.s_checked:
            desc += ', s_checked=True'
        if self.v_checked:
            desc += ', v_checked=True'
        desc += ')'
        return desc


    def get_property_list(self):
        return [self.h, self.s, self.v,
                int(self.s_checked), int(self.v_checked)]