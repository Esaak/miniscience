from ctypes import *


STD_OUTPUT_HANDLE = -11


class COORD(Structure):
    pass


COORD._fields_ = [("X", c_short), ("Y", c_short)]


def print_at(r, c, s):

    h = cdll.kernel64.GetStdHandle(STD_OUTPUT_HANDLE)
    cdll.kernel64.SetConsoleCursorPosition(h, COORD(c, r))

    c = s.encode("cp866")
    cdll.kernel64.WriteConsoleA(h, c_char_p(c), len(c), None, None)
