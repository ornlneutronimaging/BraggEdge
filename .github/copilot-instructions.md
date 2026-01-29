# BraggEdge AI Assistant Instructions

This document provides context for AI assistants (Claude Code, GitHub Copilot, etc.) working on this codebase.

## Project Overview

**neutronbraggedge** is a scientific Python library for neutron Bragg edge analysis used in neutron imaging research at Oak Ridge National Laboratory (ORNL).

### What are Bragg Edges?

Bragg edges occur at specific wavelengths in neutron transmission spectra due to crystallographic diffraction. When the neutron wavelength satisfies `λ = 2d`, where `d` is the crystal lattice spacing, neutrons are diffracted out of the beam, causing a sharp "edge" in the transmission spectrum.

Key concepts:
- **d-spacing**: Distance between crystal planes, calculated from Miller indices (h,k,l) and lattice parameter
- **Bragg edge wavelength**: `λ = 2d` (twice the d-spacing)
- **Crystal structures**: FCC (face-centered cubic), BCC (body-centered cubic)
- **Miller indices**: (h,k,l) notation for crystal planes - these are standard crystallography notation, not ambiguous variable names

## Technology Stack

- **Python**: 3.11+
- **Core dependencies**: numpy, pandas, lxml, beautifulsoup4
- **Environment management**: Pixi (conda-based)
- **Testing**: pytest with pytest-cov
- **Linting/Formatting**: Ruff
- **CI/CD**: GitHub Actions
- **Versioning**: versioningit (git tag-based)

## Project Structure

```
src/neutronbraggedge/
├── braggedge.py              # Main BraggEdge class (user entry point)
├── braggedges_handler/       # Bragg edge calculations
│   ├── braggedge_calculator.py
│   └── structure_handler.py  # FCC/BCC structure handling
├── experiment_handler/       # Experimental data handling
│   ├── experiment.py         # Main experiment class
│   ├── tof.py               # Time-of-flight handling
│   └── lambda_wavelength.py  # Wavelength calculations
├── lattice_handler/          # Lattice parameter calculations
│   └── lattice.py
├── material_handler/         # Material metadata
│   ├── retrieve_material_metadata.py
│   └── retrieve_metadata_table.py
├── data/                     # Static data files (material tables)
├── config.py                 # Configuration paths
└── utilities.py              # Shared utilities
```

## Code Style

### Formatting (enforced by Ruff)
- Line length: 120 characters
- Quote style: double quotes
- Indent style: spaces (4)
- Import sorting: isort-compatible

### Conventions
- Use `snake_case` for functions and variables
- Use `PascalCase` for classes
- Prefix private methods with `_`
- Miller indices variables (h, k, l) are intentionally single letters - this is standard crystallography notation

### Ruff Rules
```toml
select = ["E", "F", "I", "W", "UP"]
ignore = ["E741"]  # Allow h,k,l variable names (Miller indices)
```

## Testing

### Running Tests
```bash
pixi run test        # Full test suite with coverage
pixi run test-fast   # Quick test run (stop on first failure)
```

### Test Conventions
- Test files: `*_test.py` pattern
- Test data: `tests/data/` directory
- Use pytest fixtures from `tests/conftest.py`
- Aim for 80%+ coverage (currently ~95%)
- Use `pytest.approx()` for floating-point comparisons

### Example Test Pattern
```python
class TestClassName:
    def test_specific_behavior(self):
        """Docstring describing what is being tested."""
        handler = SomeClass(param=value)
        result = handler.method()
        assert result == expected
```

## Development Workflow

### Branch Structure
- `next`: Development branch (default, PRs target here)
- `qa`: Quality assurance (pre-release testing)
- `main`: Stable releases only

### Common Tasks
```bash
pixi run test          # Run tests
pixi run lint          # Check code style
pixi run format        # Auto-format code
pixi run pre-commit    # Run all pre-commit hooks
pixi run build         # Build package
```

## Domain-Specific Knowledge

### Key Classes

1. **BraggEdge**: Main entry point for users
   - Input: material name(s), number of Bragg edges
   - Output: hkl values, d-spacing, Bragg edge wavelengths

2. **Lattice**: Calculate lattice parameters from experimental data
   - Input: crystal structure, experimental Bragg edge array
   - Output: lattice parameter statistics

3. **TOF**: Time-of-flight data handling
   - Constructor param is `tof_array`, not `tof`
   - Supports unit conversion (s, ms, micros, ns)

4. **Experiment**: Calculate wavelength from TOF
   - Requires: distance_source_detector_m, detector_offset_micros

### Common Materials
- Fe (iron): BCC, lattice 2.8664 Å
- Ni (nickel): FCC, lattice 3.5238 Å
- Al (aluminum): FCC, lattice 4.0460 Å
- Cu (copper): FCC, lattice 3.6149 Å

### Physical Constants
- Neutron mass: defined in `constants.py`
- Planck constant: defined in `constants.py`

## Common Pitfalls to Avoid

1. **Parameter names**: `TOF` uses `tof_array`, not `tof`
2. **Constructor vs method params**: Some flags like `use_local_table` are constructor parameters, not method parameters
3. **Import paths**: Use `neutronbraggedge`, not `braggedge`
4. **Crystal structures**: Only "FCC" and "BCC" are currently supported
5. **Units**: Be explicit about units (seconds, microseconds, Angstroms)

## When Making Changes

1. Read the file before editing
2. Run `pixi run test` after changes
3. Run `pixi run pre-commit` before committing
4. Follow existing patterns in the codebase
5. Don't add features beyond what's requested
6. Keep changes minimal and focused
