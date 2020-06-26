class Component:
    def __init__(self, data):
        self.x = data.get("x")
        self.y = data.get("y")
        self.z = data.get("z")

        self.tag = ""

    def __str__(self):
        return self.__class__.__name__
