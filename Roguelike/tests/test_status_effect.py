import unittest

from dune_rogue.logic.ai.status_effects.status_effect import StatusEffect


class StatusEffectTest(unittest.TestCase):
    DEPTH = 10
    store = []

    class Dummy(StatusEffect):
        def __init__(self, behavior, duration=3):
            super().__init__(behavior, duration)

        def move(self, entity, mediator):
            super().move(entity, mediator)
            StatusEffectTest.store.append(1)
            if self.behavior:
                self.behavior.move(None, None)

    def test_purification(self):
        self.store.clear()
        behavior = self.Dummy(None, 1)
        for i in range(2, self.DEPTH + 1):
            behavior = self.Dummy(behavior, i)
        target = 0
        for i in range(1, self.DEPTH + 1):
            target += i
            behavior.move(None, None)
            behavior.purify_others()
        self.assertEqual(sum(self.store), target)

    def test_purification_reversed(self):
        self.store.clear()
        behavior = None
        for i in range(self.DEPTH - 1, 0, -1):
            behavior = self.Dummy(behavior, i)
        behavior = self.Dummy(behavior, self.DEPTH)
        target = 0
        for i in range(1, self.DEPTH + 1):
            target += i
            behavior.move(None, None)
            behavior.purify_others()
        self.assertEqual(sum(self.store), target)


if __name__ == '__main__':
    unittest.main()
