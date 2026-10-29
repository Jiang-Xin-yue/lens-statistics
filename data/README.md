# Observational lens catalogue

`lens_sample.csv` contains 200 systems, with one system per row and seven columns. UTF-8 text, comma-separated, with one header row. Numerical values retain the supplied precision.

| Column | Unit | Definition |
| --- | --- | --- |
| `lens_name` | — | System identifier as recorded in the compiled sample |
| `z_l` | — | Observed lens redshift |
| `z_s` | — | Observed background-source redshift |
| `theta_E_arcsec` | arcsec | Adopted Einstein radius |
| `sigma_obs_kms` | km/s | Adopted measured stellar velocity dispersion |
| `sigma_err_kms` | km/s | Quoted symmetric uncertainty: `sigma_obs_kms ± sigma_err_kms` |
| `survey` | — | Survey or source-sample label recorded in the compilation |

The velocity-dispersion uncertainties are reproduced as supplied, rather than recalculated or assigned a new confidence convention. Measurements retain their original aperture conventions; no common aperture correction has been applied for this catalogue export. The observational measurements and their literature context are described in the accompanying paper.

`survey` records sample provenance. It is not a spectroscopic targeting flag and does not uniquely determine the selection-window or foreground parameters. The reference function requires those parameters as explicit inputs and does not assign them from this table.

The measured `sigma_obs_kms` is distinct from the model-predicted `sigma_ref` passed to the reference function. The former is an observed catalogue quantity; the latter depends on the adopted lens model and trial lens redshift.

Source: the 200-system compilation accompanying Jiang et al.; see [../CITATION.bib](../CITATION.bib).
