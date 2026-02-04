"""Miscellaneous utilities used across the erado library."""

import numpy as np
import pydantic
import typing_extensions

from collections.abc import (
    Iterable,
    Generator,
    Sized,
)
from pathlib import Path
import multiprocessing
import multiprocessing.context
import contextlib
import os


type NPVector[T: np.generic] = np.ndarray[tuple[int], np.dtype[T]]
"""1-dimensional NumPy array of a given type."""

type NPMatrix[T: np.generic] = np.ndarray[tuple[int, int], np.dtype[T]]
"""2-dimensional NumPy array of a given type."""

type NPTensor[T: np.generic] = np.ndarray[tuple[int, ...], np.dtype[T]]
"""N-dimensional NumPy array of a given type.

This is functionally equivalent to `numpy.typing.NDArray` but is defined here for consistency
with our other aliases, `NPVector` and `NPMatrix`, which are both subtypes of `NPTensor`.
"""


type NestedList[T] = list[T | NestedList[T]]
"""Arbitrarily-nested `list` of a given value type.

This is effectively the built-in equivalent of `NPTensor`.
"""


def _nptensor_serialiser[T: np.generic](x: NPTensor[T]) -> NestedList[T]:
    return x.tolist()  # type: ignore # Incompatible with NumPy's type hint overloads

def _nptensor_validator(value: object) -> NPTensor:
    if isinstance(value, np.ndarray):
        return value

    if isinstance(value, list):
        return np.asarray(value)

    raise ValueError("Object is neither an NPTensor nor a built-in list.")

type NPPydantic[T: NPTensor] = typing_extensions.Annotated[
    T,
    pydantic.PlainSerializer(_nptensor_serialiser),
    pydantic.BeforeValidator(_nptensor_validator),
]
"""Pydantic field annotator that enables (de-)serialisation for NumPy arrays.

Don't forget that `arbitrary_types_allowed=True` is still required on models if using this
annotator.
"""


def get_series(
        models: Iterable[pydantic.BaseModel],
        field: str,
        subarray_size: int | None = None,
    ) -> NPVector | NPMatrix:
    """Make a data series from a collection of Pydantic models.

    The NumPy `dtype` is inferred from the type annotation in the model definition. A type
    annotation is therefore required on the field (dynamic inference is not possible due to the use
    of `numpy.fromiter` for performance).

    If the requested field is a scalar or other arbitrary object type, an `NPVector` is returned
    with length equal to the number of objects in `models`.

    If the requested field is a NumPy vector (annotated as `NPPydantic[NPVector[T]]`), an
    `NPMatrix[T]` is returned with each vector as a row. As the matrix must be square, `subarray_size`
    must be provided and all vectors in `models` must be of this length.

    Higher-dimensional subarrays are not currently supported (i.e. the field cannot be
    `NPMatrix`/`NPTensor`).

    Args:
        models: Collection of model instances.
        field: Model field to extract.
        subarray_size: Length of each subarray.

    Raises:
        TypeError: If field has no type annotation.
        NotImplementedError: If field is a `NPMatrix`/`NPTensor` (not currently supported).
        ValueError: If subarray_size is not provided despite the field being a subarray type.

    Returns:
        NumPy array with `dtype` corresponding to the field declaration.
    """
    field_type = type(next(iter(models))).model_fields[field].annotation
    if field_type is None:
        raise TypeError("Requested field has no declared type.")

    if field_type.__name__ == "NPPydantic":
        if field_type.__args__[0].__name__ != "NPVector":
            raise NotImplementedError("Only NPVector is currently supported as a subarray type.")

        if subarray_size is None:
            raise ValueError("subarray_size must be provided for subarray types.")

        dtype = np.dtype((field_type.__args__[0].__args__[0], subarray_size))
    else:
        dtype = field_type

    # -1 is the default value in np.fromiter which just sizes dynamically
    count = len(models) if isinstance(models, Sized) else -1

    return np.fromiter((getattr(model, field) for model in models), dtype=dtype, count=count)


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


@contextlib.contextmanager
def working_directory(path: Path, mkdir: bool = True) -> Generator[None]:
    """Context manager for safely and temporarily changing the current working directory.

    Examples:
        >>> with working_directory(Path("mysubdir")):
        ...     plt.savefig("figure.pdf")
        # Will save the figure as mysubdir/figure.pdf (creating mysubdir if it doesn't exist).

    Args:
        path: New working directory.
        mkdir: If true, make the directory if it doesn't exist.
    """
    if mkdir:
        path.mkdir(exist_ok=True, parents=True)

    cwd = Path.cwd()
    os.chdir(path)

    try:
        yield
    finally:
        os.chdir(cwd)


def get_mp_context() -> multiprocessing.context.DefaultContext | multiprocessing.context.ForkServerContext:
    """Obtain a suitable multiprocessing context for the current platform.

    This ensures that `fork` is not the start method, instead preferring `forkserver`.

    Returns:
        Multiprocessing context.
    """
    # The default start method on POSIX was changed in Python 3.14 from 'fork' to 'forkserver', for good reason.
    # So, if 'fork' is detected (e.g. on Python <3.14), change it to 'forkserver'.
    context = multiprocessing.get_context()
    if context.get_start_method() == "fork":
        return multiprocessing.get_context("forkserver")
    else:
        return context
