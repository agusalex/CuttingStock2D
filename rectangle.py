class Rectangle:
    x = 0
    y = 0
    width = 0
    height = 0

    def __init__(self, x:int, y:int, width:int, height:int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def __str__(self):
        return "Rectangle(" + str(self.x) + "," + str(self.y) + "," + str(self.width) + "," + str(self.height) + ")"

    def __repr__(self):
        return "".join(["Rectangle(", str(self.x), ",", str(self.y), "," , str(self.width), "," , str(self.height) ,")"])