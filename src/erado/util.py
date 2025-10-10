import numpy as np

import multiprocessing


def split_in_half(s: str) -> tuple[str, str]:
    """Given a string, return a tuple of the first and second halves of the string."""
    n = len(s)
    return (s[0:n//2], s[n//2:])


class MultiprocessingRNG:
    """
    Mixin class providing a NumPy random number generator (RNG) suitable for multiprocessing.

    The `seed` public method seeds the RNG by reconstructing it with the given argument.
    The `_reseed` private method reconstructs the RNG with fresh entropy if the current seed
    is `None`, or with a deterministically-advanced seed if the seed is an integer, suitable for
    use in initialiser functions for child processes.
    """
    _seed: int | None = None
    _rng: np.random.Generator = np.random.default_rng()
    _reseed_counter = multiprocessing.Value("I", 0)

    @classmethod
    def seed(cls, seed: int | None = None) -> None:
        cls._seed = seed
        cls._rng = np.random.default_rng(seed)

    @classmethod
    def _reseed(cls) -> None:
        with cls._reseed_counter.get_lock():
            cls._reseed_counter.value += 1

        new_seed = cls._seed
        if new_seed is not None:
            new_seed += cls._reseed_counter.value

        cls.seed(new_seed)
