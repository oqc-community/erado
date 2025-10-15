"""Miscellaneous utilities used across the erado library."""

import numpy as np

import multiprocessing


type NPVector[T: np.generic] = np.ndarray[tuple[int], np.dtype[T]]
"""1-dimensional NumPy array of a given type."""

type NPMatrix[T: np.generic] = np.ndarray[tuple[int, int], np.dtype[T]]
"""2-dimensional NumPy array of a given type."""

type NPTensor[T: np.generic] = np.ndarray[tuple[int, ...], np.dtype[T]]
"""N-dimensional NumPy array of a given type."""


class MultiprocessingRNG:
    """Mixin class providing a NumPy random number generator (RNG) suitable for multiprocessing.

    Via the `_reseed` protected method, this allows for child processes to each have seeds which
    are unique yet deterministic w.r.t. the primary seed (or fully random if the seed is `None`).
    """
    _seed: int | None = None
    _rng: np.random.Generator = np.random.default_rng()
    _reseed_counter = multiprocessing.Value("I", 0)

    @classmethod
    def seed(cls, seed: int | None = None) -> None:
        """Seed the RNG by reconstructing it with the given argument.

        Args:
            seed: Seed value to be passed to NumPy RNG.
        """
        cls._seed = seed
        cls._rng = np.random.default_rng(seed)

    @classmethod
    def _reseed(cls) -> None:
        """Reseed this RNG instance.

        This reconstructs the RNG with fresh entropy if the current seed is `None`, or with a
        deterministically-advanced seed if the seed is an integer, suitable for use in initialiser
        functions for child processes.
        """
        with cls._reseed_counter.get_lock():
            cls._reseed_counter.value += 1

        new_seed = cls._seed
        if new_seed is not None:
            new_seed += cls._reseed_counter.value

        cls.seed(new_seed)
