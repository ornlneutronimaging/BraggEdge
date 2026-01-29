"""Pydantic models for neutronbraggedge.

This module defines data models using Pydantic for type validation and
serialization of Bragg edge calculations and experimental data.
"""

from typing import Literal

import numpy as np
from pydantic import BaseModel, ConfigDict, Field, field_validator

# Type alias for supported crystal structures
CrystalStructure = Literal["BCC", "FCC"]


class MaterialConfig(BaseModel):
    """Configuration for a custom material.

    Parameters
    ----------
    name : str
        Material name/symbol (e.g., "Fe", "Ni").
    lattice : float
        Lattice constant in Angstroms. Must be positive.
    crystal_structure : CrystalStructure
        Crystal structure type ("BCC" or "FCC").

    Examples
    --------
    >>> config = MaterialConfig(name="Ta", lattice=3.31, crystal_structure="BCC")
    >>> config.model_dump()
    {'name': 'Ta', 'lattice': 3.31, 'crystal_structure': 'BCC'}
    """

    name: str = Field(..., min_length=1, description="Material name/symbol")
    lattice: float = Field(..., gt=0, description="Lattice constant in Angstroms")
    crystal_structure: CrystalStructure = Field(..., description="Crystal structure type")

    model_config = ConfigDict(frozen=True)


class MaterialMetadata(BaseModel):
    """Metadata retrieved for a material.

    Parameters
    ----------
    material : str
        Material name/symbol.
    lattice : float
        Lattice constant in Angstroms.
    crystal_structure : CrystalStructure
        Crystal structure type ("BCC" or "FCC").
    use_local_table : bool
        Whether local metadata table was used.

    Examples
    --------
    >>> metadata = MaterialMetadata(
    ...     material="Fe",
    ...     lattice=2.8664,
    ...     crystal_structure="BCC",
    ...     use_local_table=True
    ... )
    """

    material: str = Field(..., description="Material name/symbol")
    lattice: float = Field(..., gt=0, description="Lattice constant in Angstroms")
    crystal_structure: CrystalStructure = Field(..., description="Crystal structure type")
    use_local_table: bool = Field(default=True, description="Whether local metadata table was used")

    model_config = ConfigDict(frozen=True)


class BraggEdgeEntry(BaseModel):
    """A single Bragg edge entry with hkl indices and calculated values.

    Parameters
    ----------
    h : int
        Miller index h.
    k : int
        Miller index k.
    l : int
        Miller index l.
    d_spacing : float
        Interplanar spacing in Angstroms.
    bragg_edge : float
        Bragg edge wavelength in Angstroms.
    """

    h: int = Field(..., description="Miller index h")
    k: int = Field(..., description="Miller index k")
    l: int = Field(..., description="Miller index l")
    d_spacing: float = Field(..., description="Interplanar spacing in Angstroms")
    bragg_edge: float = Field(..., description="Bragg edge wavelength in Angstroms")

    model_config = ConfigDict(frozen=True)


class BraggEdgeResult(BaseModel):
    """Complete Bragg edge calculation results for a material.

    Parameters
    ----------
    material : str
        Material name/symbol.
    lattice : float
        Lattice constant in Angstroms.
    crystal_structure : CrystalStructure
        Crystal structure type.
    use_local_table : bool
        Whether local metadata table was used.
    entries : list[BraggEdgeEntry]
        List of Bragg edge entries with hkl and calculated values.

    Examples
    --------
    >>> result = BraggEdgeResult(
    ...     material="Fe",
    ...     lattice=2.8664,
    ...     crystal_structure="BCC",
    ...     use_local_table=True,
    ...     entries=[
    ...         BraggEdgeEntry(h=1, k=1, l=0, d_spacing=2.0269, bragg_edge=4.0537)
    ...     ]
    ... )
    >>> result.model_dump_json()  # Serialize to JSON
    """

    material: str = Field(..., description="Material name/symbol")
    lattice: float = Field(..., gt=0, description="Lattice constant in Angstroms")
    crystal_structure: CrystalStructure = Field(..., description="Crystal structure type")
    use_local_table: bool = Field(default=True, description="Whether local metadata table was used")
    entries: list[BraggEdgeEntry] = Field(default_factory=list, description="Bragg edge entries")

    model_config = ConfigDict(frozen=True)

    @property
    def hkl(self) -> list[tuple[int, int, int]]:
        """Get list of (h, k, l) tuples."""
        return [(e.h, e.k, e.l) for e in self.entries]

    @property
    def d_spacing(self) -> list[float]:
        """Get list of d-spacing values."""
        return [e.d_spacing for e in self.entries]

    @property
    def bragg_edges(self) -> list[float]:
        """Get list of Bragg edge values."""
        return [e.bragg_edge for e in self.entries]


class ExperimentConfig(BaseModel):
    """Configuration for an experiment calculation.

    Parameters
    ----------
    tof_array : list[float]
        Time-of-flight array in seconds.
    distance_source_detector_m : float, optional
        Distance from source to detector in meters.
    detector_offset_micros : float, optional
        Detector time offset in microseconds.
    lambda_array : list[float], optional
        Wavelength array in Angstroms.

    Notes
    -----
    Either lambda_array must be provided with one of distance/offset,
    or both distance and offset must be provided to calculate lambda.
    """

    tof_array: list[float] = Field(..., description="Time-of-flight array in seconds")
    distance_source_detector_m: float | None = Field(
        default=None, description="Distance from source to detector in meters"
    )
    detector_offset_micros: float | None = Field(default=None, description="Detector time offset in microseconds")
    lambda_array: list[float] | None = Field(default=None, description="Wavelength array in Angstroms")

    model_config = ConfigDict(frozen=True)


class TOFData(BaseModel):
    """Time-of-flight data container.

    Parameters
    ----------
    tof_array : list[float]
        Time-of-flight values in seconds.
    counts_array : list[float], optional
        Corresponding counts/intensity values.
    units : str
        Original units of the TOF data before conversion.

    Examples
    --------
    >>> tof = TOFData(tof_array=[1e-6, 2e-6, 3e-6], units="s")
    """

    tof_array: list[float] = Field(..., description="Time-of-flight values in seconds")
    counts_array: list[float] | None = Field(default=None, description="Counts/intensity values")
    units: str = Field(default="s", description="Original units of TOF data")

    model_config = ConfigDict(frozen=True)

    @field_validator("tof_array", "counts_array", mode="before")
    @classmethod
    def convert_numpy_array(cls, v):
        """Convert numpy arrays to lists for JSON serialization."""
        if isinstance(v, np.ndarray):
            return v.tolist()
        return v


class LatticeCalculationInput(BaseModel):
    """Input parameters for lattice calculation.

    Parameters
    ----------
    material : str, optional
        Material name/symbol.
    crystal_structure : CrystalStructure
        Crystal structure type.
    bragg_edge_array : list[float]
        Array of experimental Bragg edge values.
    bragg_edge_error_array : list[float], optional
        Array of errors for Bragg edge values.

    Examples
    --------
    >>> input_data = LatticeCalculationInput(
    ...     material="Fe",
    ...     crystal_structure="BCC",
    ...     bragg_edge_array=[4.05, 2.87, 2.34, 2.03]
    ... )
    """

    material: str | None = Field(default=None, description="Material name/symbol")
    crystal_structure: CrystalStructure = Field(..., description="Crystal structure type")
    bragg_edge_array: list[float] = Field(..., description="Experimental Bragg edge values")
    bragg_edge_error_array: list[float] | None = Field(default=None, description="Bragg edge error values")

    model_config = ConfigDict(frozen=True)


class LatticeStatistics(BaseModel):
    """Statistical results from lattice parameter calculations.

    Parameters
    ----------
    min : float
        Minimum lattice parameter value.
    max : float
        Maximum lattice parameter value.
    median : float
        Median lattice parameter value.
    mean : float
        Mean lattice parameter value.
    mean_error : float
        Error in mean lattice parameter.
    std : float
        Standard deviation of lattice parameters.

    Examples
    --------
    >>> stats = LatticeStatistics(
    ...     min=2.85, max=2.88, median=2.866,
    ...     mean=2.8664, mean_error=0.001, std=0.01
    ... )
    """

    min: float = Field(..., description="Minimum lattice parameter")
    max: float = Field(..., description="Maximum lattice parameter")
    median: float = Field(..., description="Median lattice parameter")
    mean: float = Field(..., description="Mean lattice parameter")
    mean_error: float = Field(..., description="Error in mean lattice parameter")
    std: float = Field(..., description="Standard deviation")

    model_config = ConfigDict(frozen=True)


class LatticeResult(BaseModel):
    """Complete lattice calculation results.

    Parameters
    ----------
    material : str, optional
        Material name/symbol.
    crystal_structure : CrystalStructure
        Crystal structure type.
    lattice_array : list[float]
        Calculated lattice parameters for each hkl.
    lattice_error_array : list[float]
        Errors in lattice parameters.
    statistics : LatticeStatistics
        Statistical summary of lattice parameters.
    hkl_bragg_edge : list[tuple]
        List of (hkl, bragg_edge, error) tuples.
    """

    material: str | None = Field(default=None, description="Material name/symbol")
    crystal_structure: CrystalStructure = Field(..., description="Crystal structure type")
    lattice_array: list[float] = Field(..., description="Calculated lattice parameters")
    lattice_error_array: list[float] = Field(..., description="Lattice parameter errors")
    statistics: LatticeStatistics = Field(..., description="Statistical summary")

    model_config = ConfigDict(frozen=True)
