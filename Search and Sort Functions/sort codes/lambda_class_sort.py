class gfg:
    def __init__(self, a, b):
        self.a = a
        self.b = b

        def __repr__(self):
            return str((self.a, self.b))


a = [
    gfg("geeks", 1),
    gfg(" computer", 3),
    gfg("for", 2),
    gfg("geeks", 4),
    gfg("science", 3)
]

res = sorted(a, key=lambda x: x.b)
print(a)
print(res)
