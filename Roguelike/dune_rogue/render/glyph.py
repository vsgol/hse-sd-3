from dune_rogue.render.color import WHITE_COLOR


class Glyph:
    """Symbol and it's color to draw"""
    def __init__(self, symbol, color=WHITE_COLOR):
        """
        :param symbol: symbol for drawing
        :param color: color for drawing
        """
        assert len(symbol) == 1
        self.symbol = symbol
        self.color = color

    def __str__(self):
        return self.symbol
