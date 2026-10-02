"""Flash-flood hazard plugin. Evidence: IMPLEMENTED baseline PHI."""

from hazards.flash_flood.phi import FORMULA_VERSION, MODEL_VERSION, compute_phi

__all__ = ["FORMULA_VERSION", "MODEL_VERSION", "compute_phi"]
