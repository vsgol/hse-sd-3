class Color:
    """Color representation"""
    def __init__(self, R, G, B):
        """
        :param R: red component
        :param G: green component
        :param B: blue component
        """
        self.R = R
        self.G = G
        self.B = B


WHITE_COLOR = Color(255, 255, 255)
GREY_COLOR = Color(50, 50, 50)
TITLE_COLOR = Color(249, 213, 162)
