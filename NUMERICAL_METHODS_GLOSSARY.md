# Numerical Methods Glossary and Complete Workflow

This document explains the symbols, equations, numerical methods, and optimization steps used in the vortex-flowmeter project.

## 5. Time-series measurements

Two wake sensors measure pressure above and below the body. The vortex signal is:

$$
s(t;R)=p_{\text{upper}}(t;R)-p_{\text{lower}}(t;R)
$$

The pressure-loss signal is:

$$
\Delta p(t;R)=p_{\text{upstream}}(t;R)-p_{\text{downstream}}(t;R)
$$

The program stores these values in `time_series.csv`.

## 6. Frequency and FFT

Vortex shedding produces an oscillating signal. The FFT converts the signal from time domain to frequency domain:

```text
pressure versus time  →  amplitude versus frequency
```

The largest non-zero FFT peak gives the dominant frequency:

$$
f(R)=\text{dominant vortex-shedding frequency}
$$

The Strouhal number is:

$$
St(R)=\frac{f(R)\,D}{U}
$$

FFT is used because it identifies the dominant periodic frequency objectively, even when the time signal contains small fluctuations.

## 7. Numerical integration

The average pressure drop is calculated using the trapezoidal rule:

$$
I_{\text{trap}}\approx\sum_{j=0}^{n-2}\frac{\Delta p_j+\Delta p_{j+1}}{2}\,(t_{j+1}-t_j)
$$

Simpson's rule provides an independent estimate:

$$
I_{\text{Simp}}=\frac{h}{3}\left[y_0+y_n+4\sum y_{\text{odd}}+2\sum y_{\text{even}}\right]
$$

The integration difference is:

$$
E_I=\left|I_{\text{trap}}-I_{\text{Simp}}\right|
$$

This is an estimate of numerical integration error.

## 15. Exact single-case numerical sequence

For the course configuration (`steps=36000`, `sample_start=18000`, `sample_interval=5`), the solver performs the following:

1. The LBM loop advances from step 0 through step 36,000, giving 36,001 solver states.
2. Only steps 18,000 through 36,000 are sampled for the steady wake.
3. The sampled step sequence is 18,000, 18,005, ..., 36,000.
4. Therefore the number of recorded time samples is:

$$
N=\frac{36000-18000}{5}+1=3601
$$

5. The time-series file contains 3,600 equal time intervals between those 3,601 samples.
6. Trapezoidal integration uses all 3,601 points and all 3,600 intervals:

$$
I_{\text{trap}}=\sum_{j=0}^{3599}\frac{y_j+y_{j+1}}{2}\,\Delta t
$$

7. Simpson's rule also uses all 3,601 points, grouped into 1,800 pairs of intervals. It is valid because 3,600 is even:

$$
I_{\text{Simp}}=\frac{\Delta t}{3}\left[y_0+y_{3600}+4\sum_{j\ \text{odd}}y_j+2\sum_{\substack{j\ \text{even}\\ j\ne 0,\,3600}}y_j\right]
$$

8. The pressure integral is divided by the observation duration $T=t_{3600}-t_0$ to obtain the mean pressure drop.

## 16. Exact frequency calculations

The 3,601 equally spaced vortex-signal samples are first linearly detrended using a two-column least-squares model:

$$
s(t)\approx a_0+a_1 t
$$

The fitted trend is subtracted before frequency analysis.

### FFT path

1. Apply a Hann window to the detrended 3,601-point signal.
2. Compute the real FFT (`rfft`), retaining the non-negative frequencies.
3. The frequency-bin spacing is:

$$
\Delta f=\frac{1}{T}
$$

4. Frequencies below $2/T$ are ignored because they cannot contain two complete cycles in the observation window.
5. The largest remaining FFT amplitude is the FFT frequency.

### Peak-to-peak path

1. Estimate a minimum peak separation from the FFT frequency.
2. A candidate peak must be greater than its two neighboring samples.
3. Its height must exceed 15% of the detrended signal RMS.
4. Peaks closer than the estimated minimum distance are merged, retaining the larger peak.
5. At least three peaks are required.
6. Consecutive peak periods are computed; periods farther than 25% from their median are rejected.
7. At least two accepted periods are required.
8. The peak frequency is $1/\overline{T}_{\text{peak}}$ (one over the mean accepted period), and its uncertainty is the sample standard deviation of the accepted individual frequencies.

The peak frequency is marked reliable only when it agrees with the FFT frequency within the larger of $2\Delta f$ or 20% of the FFT frequency.

## 17. Exact stationarity checks

The sampled series is split into two equal halves. For pressure:

$$
E_p=\frac{\left|\overline{p}_{\text{second}}-\overline{p}_{\text{first}}\right|}{\max\left(\left|\overline{\Delta p}_{\text{trap}}\right|,\ 10^{-14}\right)}
$$

For the detrended vortex signal, the RMS of each half is calculated:

$$
E_s=\frac{\left|\mathrm{RMS}_{\text{second}}-\mathrm{RMS}_{\text{first}}\right|}{\max\left(\mathrm{RMS}_{\text{first}},\ \mathrm{RMS}_{\text{second}},\ 10^{-14}\right)}
$$

The sampling window is accepted only when:

$$
E_p\le 0.15\quad\text{and}\quad E_s\le 0.25
$$

This is why a radius can finish its LBM run but still be rejected by the optimizer.
