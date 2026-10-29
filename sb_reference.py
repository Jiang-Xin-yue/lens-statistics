"""Reference evaluation of Appendix A. Python 3.9+; standard library only.

CC BY 4.0. Please cite Jiang et al.; see CITATION.bib.
The caller supplies sigma_ref and selection parameters explicitly.
"""

import csv
import math
from bisect import bisect_right
from dataclasses import dataclass
from pathlib import Path


# (M_star, V_star, conditional slope A, conditional scatter w [mag])
BERNARDI = {
    "r": (-21.15, 2.200, -5.864, 0.533),
    "i": (-21.49, 2.201, -6.042, 0.531),
    "z": (-21.83, 2.200, -6.007, 0.527),
}


@dataclass(frozen=True)
class Window:
    """Total-magnitude limits; DESI uses faint=21.6 and aperture=True."""

    band: str
    faint: float
    bright: float = None
    aperture: bool = False

    def __post_init__(self):
        if self.band not in BERNARDI:
            raise ValueError("band must be r, i, or z")
        if not math.isfinite(self.faint):
            raise ValueError("faint must be finite")
        if self.bright is not None:
            if not math.isfinite(self.bright) or self.bright >= self.faint:
                raise ValueError("bright must be finite and smaller than faint")
        if self.aperture and self.band != "z":
            raise ValueError("the supplied aperture correction is for DESI z only")


def _read_columns(path):
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        next(reader)
        return [tuple(map(float, row)) for row in reader if row]


def _linear(rows, x):
    """Linear interpolation; reject values beyond the tabulated domain."""
    if not rows[0][0] <= x <= rows[-1][0]:
        raise ValueError("redshift is outside the correction-table domain")
    i = min(max(bisect_right(rows, (x, math.inf)) - 1, 0), len(rows) - 2)
    x0, y0 = rows[i]
    x1, y1 = rows[i + 1]
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def _bracket(axis, value):
    """Clamp to the actual boundary, then find the interpolation cell."""
    value = min(max(value, axis[0]), axis[-1])
    i = min(max(bisect_right(axis, value) - 1, 0), len(axis) - 2)
    return i, (value - axis[i]) / (axis[i + 1] - axis[i])


def _cdf(x):
    return 0.5 * math.erfc(-x / math.sqrt(2.0))


def _window_probability(faint, bright, mean, width):
    # Use complementary tails when both limits lie above the mean.
    # This avoids subtracting two CDF values rounded to one.
    hi = (faint - mean) / width
    if bright is None:
        return _cdf(hi)
    lo = (bright - mean) / width
    p = _cdf(-lo) - _cdf(-hi) if lo > 0 else _cdf(hi) - _cdf(lo)
    return min(max(p, 0.0), 1.0)


class SelectionTables:
    """Load the eight released tables once, then evaluate S_B repeatedly."""

    def __init__(self, table_dir=None):
        root = Path(table_dir) if table_dir is not None else Path(__file__).parent / "tables"
        self.mu = _read_columns(root / "mu_z.csv")
        filters = {"r": "SDSS_r", "i": "SDSS_i", "z": "DECam_z"}
        self.k = {}
        self.e = {}
        for band, filt in filters.items():
            self.k[band] = _read_columns(root / f"K_{filt}__BC03_zf2_passive_evolution.csv")
            self.e[band] = _read_columns(root / f"E_z_{filt}_BC03_zf2.csv")
        aperture = _read_columns(root / "aperture_corr_desi.csv")
        self.ap_z = sorted({row[0] for row in aperture})
        self.ap_sigma = sorted({row[1] for row in aperture})
        self.ap_values = {(z, sigma): dm for z, sigma, dm in aperture}
        if len(self.ap_values) != len(self.ap_z) * len(self.ap_sigma):
            raise ValueError("incomplete aperture-correction grid")

    @staticmethod
    def _validate(z_l, sigma_ref):
        if not math.isfinite(z_l) or not 0 < z_l <= 3.5:
            raise ValueError("require 0 < z_l <= 3.5; no redshift extrapolation is provided")
        if not math.isfinite(sigma_ref) or sigma_ref <= 0:
            raise ValueError("sigma_ref must be positive and finite, in km/s")

    def apparent_magnitude(self, z_l, sigma_ref, band):
        """Conditional mean total apparent magnitude, including mu + K + E."""
        self._validate(z_l, sigma_ref)
        ms, vs, slope, _ = BERNARDI[band]
        return (ms + slope * (math.log10(sigma_ref) - vs)
                + _linear(self.mu, z_l)
                + _linear(self.k[band], z_l)
                + _linear(self.e[band], z_l))

    def aperture_correction(self, z_l, sigma_ref):
        """2.5 log10(fibre flux / total flux), in mag; bilinear interpolation."""
        self._validate(z_l, sigma_ref)
        i, u = _bracket(self.ap_z, z_l)
        j, v = _bracket(self.ap_sigma, sigma_ref)
        z0, z1 = self.ap_z[i:i + 2]
        s0, s1 = self.ap_sigma[j:j + 2]
        grid = self.ap_values
        return (grid[z0, s0] * (1 - u) * (1 - v)
                + grid[z1, s0] * u * (1 - v)
                + grid[z0, s1] * (1 - u) * v
                + grid[z1, s1] * u * v)

    def components(self, z_l, sigma_ref, windows=(), m_sup=None, epsilon=0.2):
        """Return magnitude-window factor, foreground factor, and their product.

        windows: sequence of Window objects; empty means no magnitude window.
        Multiple windows are combined by max, as in Appendix A.
        m_sup: fixed i-band transition magnitude; None disables suppression.
        No catalogue lookup or automatic selection assignment is performed.
        """
        self._validate(z_l, sigma_ref)
        if not math.isfinite(epsilon) or not 0 <= epsilon <= 1:
            raise ValueError("epsilon must lie between zero and one")
        if m_sup is not None and not math.isfinite(m_sup):
            raise ValueError("m_sup must be finite or None")
        probabilities = []
        for window in windows:
            faint = window.faint
            if window.aperture:
                faint += self.aperture_correction(z_l, sigma_ref)
            mean = self.apparent_magnitude(z_l, sigma_ref, window.band)
            probabilities.append(_window_probability(
                faint, window.bright, mean, BERNARDI[window.band][3]))
        p_window = max(probabilities) if probabilities else 1.0
        foreground = 1.0
        if m_sup is not None:
            mean_i = self.apparent_magnitude(z_l, sigma_ref, "i")
            foreground -= epsilon * _cdf((m_sup - mean_i) / BERNARDI["i"][3])
        return {"window": p_window, "foreground": foreground,
                "S_B": p_window * foreground}

    def evaluate(self, z_l, sigma_ref, windows=(), m_sup=None, epsilon=0.2):
        """Return S_B. See components() for arguments and intermediate factors."""
        return self.components(z_l, sigma_ref, windows, m_sup, epsilon)["S_B"]


if __name__ == "__main__":
    # Illustrative numerical inputs, not an assignment for a released object.
    tables = SelectionTables()
    print(tables.components(0.3, 250.0,
          windows=[Window("r", faint=19.26, bright=14.26)], m_sup=16.2))
