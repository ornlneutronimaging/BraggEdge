# neutronbraggedge

[![CI](https://github.com/ornlneutronimaging/BraggEdge/actions/workflows/ci.yml/badge.svg?branch=next)](https://github.com/ornlneutronimaging/BraggEdge/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/ornlneutronimaging/BraggEdge/branch/next/graph/badge.svg)](https://codecov.io/gh/ornlneutronimaging/BraggEdge)
[![Documentation Status](https://readthedocs.org/projects/braggedge/badge/?version=latest)](https://braggedge.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/neutronbraggedge.svg)](https://badge.fury.io/py/neutronbraggedge)

A Python library for neutron Bragg edge analysis used in neutron imaging research at Oak Ridge National Laboratory.

## Overview

Bragg edges occur at specific wavelengths in neutron transmission spectra due to crystallographic diffraction. This library calculates:

- Bragg edge positions for various materials
- d-spacings from crystal structure
- Lattice parameters from experimental data
- Wavelength/TOF conversions

## Installation

```bash
pip install neutronbraggedge
```

## Quick Start

```python
from neutronbraggedge.braggedge import BraggEdge

# Get Bragg edges for Iron
handler = BraggEdge(material='Fe', number_of_bragg_edges=4)
print(handler.bragg_edges['Fe'])
# [4.0537, 2.8664, 2.3404, 2.0269]

print(handler.metadata['crystal_structure']['Fe'])
# 'BCC'
```

## Documentation

Full documentation is available at [braggedge.readthedocs.io](https://braggedge.readthedocs.io/).

## Development

We use [Pixi](https://pixi.sh/) for environment management:

```bash
git clone https://github.com/ornlneutronimaging/BraggEdge.git
cd BraggEdge
pixi install
pixi run test
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## License

BSD-3-Clause. See [LICENSE](LICENSE) for details.
