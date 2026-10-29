# Adopted parameters and table conventions

These materials accompany Appendix A of Jiang et al. The equations below specify the released reference calculation. The caller supplies the lens redshift `z_l`, reference velocity dispersion `sigma_ref` in km/s, magnitude windows, and the fixed foreground transition `m_sup`.

## 1. Conditional luminosity relation

For each band b,

$$\overline M_b=M_{*,b}+A_b(\log_{10}\sigma_{\rm ref}-V_{*,b}),$$

$$A_b=\rho_{VM,b}\frac{\sigma_{M,b}}{\sigma_{V,b}},\qquad w_b=\sigma_{M,b}\sqrt{1-\rho_{VM,b}^2}.$$

Velocity dispersions inside the logarithm are expressed numerically in km/s. The conditional magnitude distribution is Gaussian with mean `M_bar` and standard deviation `w`.

| Band | M_star [mag] | V_star | sigma_M [mag] | sigma_V | rho_VM | A | w [mag] |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| r | -21.15 | 2.200 | 0.841 | 0.111 | -0.774 | -5.864 | 0.533 |
| i | -21.49 | 2.201 | 0.851 | 0.110 | -0.781 | -6.042 | 0.531 |
| z | -21.83 | 2.200 | 0.845 | 0.110 | -0.782 | -6.007 | 0.527 |

The empirical inputs are from **Bernardi et al. (2003), Paper II, AJ 125, 1849, Table 1**, not the surface-brightness covariance table in Paper III. [Paper II](https://arxiv.org/abs/astro-ph/0301624). The rounded A and w values above are used directly in the reference function. M_star is the zero-redshift luminosity calibration. No additional linear `-Q*z` evolution term is applied.

## 2. Apparent magnitudes and correction tables

$$\overline m_b(z_l)=\overline M_b+\mu(z_l)+K_b(z_l)+E_b(z_l).$$

All magnitudes and corrections are in mag, with AB magnitudes used for the spectral corrections. The distance modulus uses a flat Lambda-CDM cosmology with Omega_m=0.3 and H_0=70 km/s/Mpc. The K- and E-corrections use the BC03 single-burst SSP, STELIB, a Chabrier IMF, solar metallicity, and formation redshift z_f=2.

| File | Columns | Grid and meaning |
| --- | --- | --- |
| `mu_z.csv` | `z,mu` | z=0–3.5, step 0.001; distance modulus |
| `K_SDSS_r__BC03_zf2_passive_evolution.csv` | `z,K_AB_mag` | z=0–3.5, step 0.005; SDSS r same-filter K |
| `K_SDSS_i__BC03_zf2_passive_evolution.csv` | `z,K_AB_mag` | Same grid; SDSS i same-filter K |
| `K_DECam_z__BC03_zf2_passive_evolution.csv` | `z,K_AB_mag` | Same grid; DECam z same-filter K |
| `E_z_SDSS_r_BC03_zf2.csv` | `z,E_AB_mag` | Same grid; SDSS r evolution |
| `E_z_SDSS_i_BC03_zf2.csv` | `z,E_AB_mag` | Same grid; SDSS i evolution |
| `E_z_DECam_z_BC03_zf2.csv` | `z,E_AB_mag` | Same grid; DECam z evolution |

The filter responses are SDSS r and i (Doi et al. 2010) and the DES Y3 DECam z response. The spectral model is Bruzual & Charlot (2003), with STELIB from Le Borgne et al. (2003) and the IMF of Chabrier (2003). Full references and the integral definitions are given in the paper. The K definition follows [Hogg et al. (2002)](https://arxiv.org/abs/astro-ph/0210394).

At z>1.05, the spectrum is held at the population age corresponding to z=1.05. E remains at E(1.05), while K continues to be evaluated at the actual redshift using that fixed-age spectrum. The distance modulus continues to vary with redshift.

The reference function linearly interpolates each one-dimensional table directly. It does not use an additional dense lookup grid. Redshift extrapolation is not supplied. The `z=0,mu=0` row is a numerical placeholder, not the physical distance modulus at zero distance. The function excludes z=0; interpolation between z=0 and 0.001 inherits this placeholder and should not be interpreted as an accurate local distance modulus. The observed lens sample starts at z_l=0.0625.

## 3. Magnitude windows

For a band with conditional mean m_bar and scatter w,

$$P_{\rm win}=\Phi[(m_{\rm faint}-\overline m)/w]-\Phi[(m_{\rm bright}-\overline m)/w].$$

With no bright-end cut the second term is zero. Phi is the standard normal CDF. The limits below are the adopted magnitude-only prescriptions, rather than a reconstruction of all targeting cuts such as colour or surface brightness.

| Prescription | Window used by the reference calculation |
| --- | --- |
| SDSS | Total SDSS r: 14.26 < r < 19.26 |
| BOSS | LOWZ: 16.0 < r < 19.6; CMASS: 17.5 < i < 19.9; use max(P_LOWZ, P_CMASS) |
| DESI | Total DECam z faint limit: 21.6 + delta_mag(z_l, sigma_ref); no bright-end cut |
| No parent-survey window | P_win=1 |

For SDSS, 0.24 mag is subtracted from each adopted Petrosian limit (14.5 and 19.5), corresponding to an enclosed fraction of about 0.8. The adopted Petrosian bright limit is an approximation to fibre-magnitude bright-target exclusions. BOSS cmodel magnitudes are treated as total magnitudes. The CMASS `i_fib2<21.5` condition is not imposed separately in this effective window prescription. SDSS targeting references include Strauss et al. (2002) and Eisenstein et al. (2001); BOSS targeting is described by Dawson et al. (2013) and Reid et al. (2016).

`max(P_LOWZ, P_CMASS)` is the adopted numerical combination. It is not an evaluation of a joint two-band union probability.

## 4. DESI aperture correction

The adopted z-band conditional size relation is

$$\log_{10}(R_e/{\rm kpc})=R_*+\rho_{RV}\frac{\sigma_R}{\sigma_V}(\log_{10}\sigma_{\rm ref}-V_*),$$

with R_star=0.450, sigma_R=0.241, sigma_V=0.110, rho_RV=0.543, and V_star=2.200 (Bernardi Paper II, Table 1; h_70=1). Convert R_e to angular size using D_A(z_l), convolve an n=4 de Vaucouleurs profile with a 1-arcsec-FWHM Gaussian PSF, and integrate within a radius of 0.75 arcsec. The resulting fraction of the total flux is eta. The aperture and smoothing follow the [Legacy Surveys DR9 predicted fibre-flux convention](https://www.legacysurvey.org/dr9/catalogs/). The adopted DESI LRG threshold is from Zhou et al. (2023).

$$\Delta m=2.5\log_{10}\eta<0,\qquad m_{{\rm faint},z}=21.6+\Delta m.$$

`aperture_corr_desi.csv` contains `z_l,sigma_kms,delta_mag`. Its complete grid has 101 redshifts from 0.05 to 1.05 (step 0.01) and 71 dispersions from 100 to 450 km/s (step 5). `delta_mag` is a negative additive correction to the faint limit, not the positive difference between fibre and total magnitude.

The reference function uses bilinear interpolation and clamps each aperture-grid coordinate to its actual nearest boundary outside the grid. The velocity dispersion used in the luminosity relation is not clamped. As a numerical check, delta_mag(0.7,250)=-1.0113608002 mag, giving an effective total limit of 20.5886391998 mag.

## 5. Foreground suppression

$$F_{\rm sup}=1-\varepsilon\Phi[(m_{\rm sup}-\overline m_i)/w_i],\qquad S_B=P_{\rm win}F_{\rm sup}.$$

Use SDSS i-band predictions for suppression, even when the magnitude window uses r or DECam z. The adopted w_i is 0.531 mag and the fiducial epsilon is 0.2. At m_i=m_sup, F_sup=0.9; for much brighter foregrounds it approaches 0.8, and for much fainter foregrounds it approaches one.

Each fixed m_sup is the 10th percentile of predicted i magnitudes within the corresponding selection subclass, calibrated from measured dispersions and observed lens redshifts in the full sample before inference.

| Selection subclass | Adopted m_sup(i) [mag] |
| --- | ---: |
| SDSS_MAIN_ONLY | 16.197 |
| SDSS_MAIN_LRG | 15.547 |
| SDSS_LRG_ONLY | 17.550 |
| SDSS_SPECIAL | 17.184 |
| BOSS_LOWZ | 18.697 |
| BOSS_CMASS | 18.998 |
| SUGOHI_CMASS | 19.268 |
| HSC_DESI | 18.495 |
| IMAGE_EMPIRICAL | 18.208 |

The reference function accepts m_sup explicitly and does not recalibrate it from the released catalogue. The table gives adopted values to three decimal places. `m_sup=None` disables suppression. With no magnitude window and no suppression, S_B=1.

The observational catalogue provides survey provenance, not per-object selection-subclass assignments. Those assignments are not inferred or supplied by this reference implementation.
