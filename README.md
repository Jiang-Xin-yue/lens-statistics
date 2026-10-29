# Lens selection function S_B

Companion tables, adopted parameters, and a reference implementation for Appendix A of:

**Jiang et al., _The mass density slope of early-type galaxies: newest results from the redshift distribution of strong gravitational lenses_.**

The selection function combines a spectroscopic magnitude-window factor with foreground-light suppression. The calculation starts from a reference velocity dispersion supplied by a lens model, predicts the total apparent magnitude through `m = M + mu + K + E`, and evaluates these two factors.

## Contents

| File or directory | Contents |
| --- | --- |
| [parameters.md](parameters.md) | Luminosity and size relations, magnitude limits, foreground parameters, and numerical conventions |
| [tables/](tables/) | Distance modulus, three K-corrections, three evolution corrections, and the DESI aperture correction |
| [sb_reference.py](sb_reference.py) | Standalone Python implementation of the magnitude prediction and selection factors |
| [data/lens_sample.csv](data/lens_sample.csv) | 200-system observational catalogue, including velocity-dispersion uncertainties |
| [data/README.md](data/README.md) | Catalogue column definitions and measurement conventions |

The reference function takes the window parameters and foreground transition magnitude explicitly. It does not infer selection parameters from the catalogue's `survey` field. The lens-model mapping to `sigma_ref`, the optical-depth calculation, and the MCMC analysis are outside the scope of this release.

## Quick start

Download this repository with **Code → Download ZIP**, extract it, and open a terminal in the extracted directory. Python 3.9 or later is sufficient; no additional packages are required.

```bash
python3 sb_reference.py
```

To use the function in another calculation:

```python
from sb_reference import SelectionTables, Window

tables = SelectionTables()

# Illustrative inputs, not an assignment for any catalogue object.
result = tables.components(
    z_l=0.3,
    sigma_ref=250.0,  # km/s, supplied by the caller's lens model
    windows=[Window("r", faint=19.26, bright=14.26)],
    m_sup=16.2,      # illustrative fixed i-band transition magnitude
    epsilon=0.2,
)
print(result)  # window, foreground, and S_B
```

For this example, the factors are approximately `window=0.8480518872`, `foreground=0.9999783243`, and `S_B=0.8480335051`.

`tables.evaluate(...)` accepts the same arguments and returns just `S_B`. Load the tables once and reuse the object.

Window specifications:

```python
sdss_windows = [Window("r", faint=19.26, bright=14.26)]
boss_windows = [Window("r", faint=19.6, bright=16.0),
                Window("i", faint=19.9, bright=17.5)]
desi_windows = [Window("z", faint=21.6, aperture=True)]
```

Multiple window probabilities are combined by their maximum. An empty `windows` sequence gives a window factor of one. `m_sup=None` disables foreground suppression; an empty window sequence with `m_sup=None` gives `S_B=1`. The adopted foreground values and their definitions are in [parameters.md](parameters.md).

## Numerical domain

The correction tables extend to redshift 3.5. The reference function accepts `0 < z_l <= 3.5` and positive `sigma_ref` in km/s. It rejects redshifts outside this interval rather than silently extrapolating. Some source redshifts in the observational catalogue exceed 3.5; this release does not supply corrections beyond the tabulated range.

The reference implementation interpolates directly on the released grids. It is intended to implement the equations and documented numerical conventions, rather than reproduce every lookup or floating-point detail of an analysis pipeline. See [parameters.md](parameters.md) for the aperture-table boundary convention and high-redshift spectral prescription.

## Citation

If you use these tables, parameters, catalogue, or reference implementation in a research publication, please cite the accompanying paper. Copy the entry in [CITATION.bib](CITATION.bib), or use GitHub's **Cite this repository** button. The citation currently identifies the manuscript; its publication identifier should be added when available.

The adopted empirical relations and model ingredients have their own sources, listed in [parameters.md](parameters.md). Please also cite the original work where appropriate.

## Licence

The original contributions in this repository are released under [CC BY 4.0](LICENSE). The licence applies to the released material, not to unpublished analysis files or third-party works cited as sources. Please retain source attribution and indicate modifications when redistributing the material under the licence.

Version: **1.0.0**.
