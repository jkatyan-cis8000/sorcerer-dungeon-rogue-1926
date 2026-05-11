"""Random number provider for Tower of the Sorcerer."""

import random


class RandomProvider:
    """Provides seeded RNG for game operations."""

    def __init__(self, seed: int | None = None) -> None:
        """Initialize with optional seed."""
        self._seed = seed
        self._rng = random.Random(seed)

    def random_int(self, min_val: int, max_val: int) -> int:
        """Return a random integer between min_val and max_val (inclusive)."""
        return self._rng.randint(min_val, max_val)

    def random_float(self) -> float:
        """Return a random float between 0.0 and 1.0."""
        return self._rng.random()

    def shuffle(self, items: list) -> list:
        """Return a shuffled copy of the list."""
        shuffled = items.copy()
        self._rng.shuffle(shuffled)
        return shuffled

    def choice(self, items: list) -> any:
        """Return a random element from the list."""
        return self._rng.choice(items)
