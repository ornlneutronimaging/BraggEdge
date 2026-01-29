"""Neutron Bragg Edge calculations for crystalline materials."""

from loguru import logger

from .logging_config import configure_logging, disable_logging, enable_logging
from .models import (
    BraggEdgeEntry,
    BraggEdgeResult,
    CrystalStructure,
    ExperimentConfig,
    LatticeCalculationInput,
    LatticeResult,
    LatticeStatistics,
    MaterialConfig,
    MaterialMetadata,
    TOFData,
)

try:
    from ._version import __version__
except ImportError:
    # Package not installed, use fallback
    __version__ = "0.0.0.dev0"

# Disable logger by default (library best practice)
# Users can enable with: configure_logging() or enable_logging()
logger.disable("neutronbraggedge")

__all__ = [
    # Version
    "__version__",
    # Logging
    "logger",
    "configure_logging",
    "enable_logging",
    "disable_logging",
    # Models
    "CrystalStructure",
    "MaterialConfig",
    "MaterialMetadata",
    "BraggEdgeEntry",
    "BraggEdgeResult",
    "ExperimentConfig",
    "TOFData",
    "LatticeCalculationInput",
    "LatticeStatistics",
    "LatticeResult",
]
