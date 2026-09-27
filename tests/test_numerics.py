from __future__ import annotations

import unittest

import numpy as np

from vortexflow.numerics import (
    simpson_uniform,
    trapezoidal,
)
from vortexflow.postprocess import frequency_fft, frequency_peak_to_peak, vorticity


class NumericalMethodsTests(unittest.TestCase):
    def test_integration(self) -> None:
        x = np.linspace(0.0, 2.0, 101)
        y = x**2
        exact = 8.0 / 3.0
        self.assertAlmostEqual(simpson_uniform(x, y), exact, places=10)
        self.assertLess(abs(trapezoidal(x, y) - exact), 3e-4)

    def test_signal_frequency(self) -> None:
        time = np.linspace(0.0, 5.0, 1001)
        signal = np.sin(2.0 * np.pi * 7.0 * time)
        peak, _, count = frequency_peak_to_peak(time, signal)
        fft, _, _ = frequency_fft(time, signal)
        self.assertGreater(count, 20)
        self.assertAlmostEqual(peak, 7.0, places=2)
        self.assertLess(abs(fft - 7.0), 1.0 / (time[-1] - time[0]))

    def test_frequency_rejects_roundoff_noise(self) -> None:
        time = np.linspace(0.0, 1.0, 501)
        signal = 1e-18 * np.sin(2.0 * np.pi * 40.0 * time)
        with self.assertRaises(ValueError):
            frequency_peak_to_peak(time, signal)

    def test_vorticity(self) -> None:
        axis = np.linspace(-1.0, 1.0, 31)
        x, y = np.meshgrid(axis, axis)
        omega = vorticity(-y, x, axis[1] - axis[0], axis[1] - axis[0])
        np.testing.assert_allclose(omega[2:-2, 2:-2], 2.0, atol=1e-12)


if __name__ == "__main__":
    unittest.main()
