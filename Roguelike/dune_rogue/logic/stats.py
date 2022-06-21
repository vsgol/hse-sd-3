class Stats:
    """Statistics class"""
    def __init__(self, hp=0, defence=0, attack=0, max_hp=0, regen=0):
        """
        :param hp: current health points
        :param defence: defence strength
        :param attack: attack strength
        :param max_hp: maximal health points number
        :param regen: regeneration rate
        """
        self.hp = hp
        self.defence = defence
        self.attack = attack
        self.max_hp = max_hp
        self.regen = regen

    def __add__(self, other):
        return Stats(self.hp + other.hp,
                     self.defence + other.defence,
                     self.attack + other.attack,
                     self.max_hp + other.max_hp,
                     self.regen + other.regen)

    def __neg__(self):
        return Stats(-self.hp, -self.defence, -self.attack, -self.max_hp, -self.regen)

    def __sub__(self, other):
        return self + (-other)

    def __repr__(self):
        return f'hp: {self.hp}, defence: {self.defence}, attack: {self.attack}, max hp: {self.max_hp}, regeneration: {self.regen}'

    def __eq__(self, other):
        return self.hp == other.hp and self.attack == other.attack \
               and self.defence == other.defence and self.max_hp == other.max_hp


class CharacterStats(Stats):
    """Character statistics"""
    def __init__(self, hp=0, defence=0, attack=0, max_hp=0, regen=0):
        """
        :param hp: current health points
        :param defence: defence strength
        :param attack: attack strength
        :param max_hp: maximal health points number
        """
        super().__init__(hp, defence, attack, max_hp, regen)

    def add_stats(self, bonus):
        """Add bonuses to statistics
        :param bonus: bonus statistics
        """
        s = self + bonus
        self.__dict__.update(s.__dict__)
        self.hp = min(self.max_hp, self.hp)

    def remove_stats(self, bonus):
        """Remove bonuses from statistics
        :param bonus: bonus statistics
        """
        s = self - bonus
        self.__dict__.update(s.__dict__)


_LVL_PROGRESSION = [8 * 2 ** i for i in range(30)]


class PlayerStats(CharacterStats):
    """Player statistics, contains level"""
    def __init__(self, hp=0, defence=0, attack=0, max_hp=0, level=0, exp=0):
        """
        :param hp: current health points
        :param defence: defence strength
        :param attack: attack strength
        :param max_hp: maximal health points number
        :param level: current level
        :param exp: current experience points
        """
        super().__init__(hp, defence, attack, max_hp)
        self.level = level
        self.exp = exp
        while self.check_level():
            self.level_up()

    def give_exp(self, exp):
        """Gives experience points
        :param exp: experience points to give
        """
        self.exp += exp
        if exp > 0:
            if self.check_level():
                self.level_up()

    def check_level(self):
        """Checks if experience points are enough to level up
        :return: True if enough. False otherwise
        """
        return self.exp >= _LVL_PROGRESSION[self.level]

    def level_up(self):
        """ Upgrades character statistics for new level grading
        :return:
        """
        self.exp -= _LVL_PROGRESSION[self.level]
        self.level += 1
        self.max_hp += 1
        self.attack += 1
        self.defence += 1

    def __str__(self):
        return f'HP: {self.hp}/{self.max_hp} ATK: {self.attack} DEF: {self.defence}' \
               f' LVL: {self.level} EXP: {self.exp}/{_LVL_PROGRESSION[self.level]}'
