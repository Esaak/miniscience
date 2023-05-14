

class Planet:
    def __init__(self, R, g, Po, T, coef_reflection):
        self.R = R
        self.g = g
        self.Po = Po
        self.T = T
        self.coef_reflection =  coef_reflection


class Atmosphere:
    def __init__(self, height, n, dh):
        self.height = height
        self.n = n
        self.dh = dh