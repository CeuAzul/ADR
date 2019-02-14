class CG:
    def __init__(self, data):
        self.x = data.get("x")
        self.y = data.get("y")

    def __str__(self):
        return self.__class__.__name__
