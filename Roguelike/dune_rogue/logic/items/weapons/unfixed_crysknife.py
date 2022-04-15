from dune_rogue.logic.items.weapons.weapon import Weapon
from dune_rogue.logic.stats import Stats


class UnfixedCrysknife(Weapon):
    def __init__(self):
        super().__init__(weight=1, usable=False,
                         stats=Stats(0, 0, 1, 0), name='Unifxed crysknife',
                         description='This crysknife used to be a mighty weapon of a freeman but it has been away '
                                     'from the human body for too long so it lost most of its power',
                         )
