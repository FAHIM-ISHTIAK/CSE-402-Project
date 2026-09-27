"""Course numerical methods implemented directly in Python/NumPy."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np


def trapezoidal(x: np.ndarray, y: np.ndarray) -> float:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if x.ndim != 1 or y.ndim != 1 or len(x) != len(y) or len(x) < 2:
        raise ValueError("x and y must be one-dimensional arrays of equal length >= 2")
    if np.any(np.diff(x) <= 0):
        raise ValueError("x must be strictly increasing")
    return float(np.sum(0.5 * np.diff(x) * (y[:-1] + y[1:])))


def simpson_uniform(x: np.ndarray, y: np.ndarray) -> float:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    if len(x) != len(y) or len(x) < 3 or (len(x) - 1) % 2:
        raise ValueError("Simpson's rule requires an even number of equal intervals")
    spacing = np.diff(x)
    if not np.allclose(spacing, spacing[0], rtol=1e-8, atol=1e-12):
        raise ValueError("Simpson's rule requires uniformly spaced x values")
    return float(
        spacing[0] / 3.0
        * (y[0] + y[-1] + 4.0 * np.sum(y[1:-1:2]) + 2.0 * np.sum(y[2:-1:2]))
    )
