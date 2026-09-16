# Shared experiment package

The historical p19 path is kept for command compatibility; it is not a third manuscript. `paper/` is industrial TII; `paper_TPAMI/` owns the general policy/multi-domain study. See root PAPER_SCOPE.md.

`routing.py`/`toy_routing.py` compare fixed predictors. `policy_certificate.py` calibrates a frozen policy family on independent bounded group losses; `certified_selection_demo.py` supplies an explicit CPU statistical experiment. These do not train HSE, convert raw external data or implement a universal router.

`statistics.py` handles empirical additive recording/group means; `phm_metrics.py` recomputes nonlinear classification metrics; the certificate has stricter assumptions and is not interchangeable with either. Plotters read CSV only and preserve negative observations.

No module here imports PHMFactory internals. Only the revision-specific acceptance script runs inside the isolated upstream environment to restore its unchanged model and export its own dataset. No duplicate model factory, registry or paper-specific trainer is needed.
