# Contributing to BraggEdge

Thank you for your interest in contributing to neutronbraggedge! This document provides guidelines for contributing to the project.

## Getting Started

### Prerequisites

- Python 3.11 or 3.12
- [Pixi](https://pixi.sh/) for environment management

### Setting Up the Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/ornlneutronimaging/BraggEdge.git
   cd BraggEdge
   ```

2. Install dependencies with Pixi:
   ```bash
   pixi install
   ```

3. Install pre-commit hooks:
   ```bash
   pixi run pre-commit-install
   ```

4. Verify your setup:
   ```bash
   pixi run test
   ```

## Development Workflow

### Branch Structure

We use a three-branch workflow:

- **`next`**: Development branch (default). All PRs should target this branch.
- **`qa`**: Quality assurance branch for pre-release testing.
- **`main`**: Stable release branch. Only receives merges from `qa`.

### Making Changes

1. Create a feature branch from `next`:
   ```bash
   git checkout next
   git pull origin next
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit:
   ```bash
   git add <files>
   git commit -m "Brief description of changes"
   ```

3. Push and create a pull request:
   ```bash
   git push -u origin feature/your-feature-name
   ```

4. Open a PR targeting the `next` branch.

## Code Style

We use [Ruff](https://github.com/astral-sh/ruff) for linting and formatting.

### Key Style Points

- **Line length**: 120 characters
- **Quotes**: Double quotes
- **Imports**: Sorted with isort-compatible ordering

### Running Linters

```bash
pixi run lint      # Check for issues
pixi run format    # Auto-format code
```

### Pre-commit Hooks

Pre-commit hooks run automatically on commit. To run manually:

```bash
pixi run pre-commit
```

## Testing

### Running Tests

```bash
pixi run test        # Full suite with coverage
pixi run test-fast   # Quick run (stops on first failure)
```

### Writing Tests

- Place tests in `tests/` mirroring the source structure
- Use `*_test.py` naming pattern
- Use pytest fixtures for common setup
- Use `pytest.approx()` for floating-point comparisons

Example:
```python
import pytest
from neutronbraggedge.braggedge import BraggEdge

class TestBraggEdge:
    def test_calculates_d_spacing_correctly(self):
        """d_spacing values should match expected crystallographic values."""
        handler = BraggEdge(material="Fe", number_of_bragg_edges=4)
        d_spacing = handler.d_spacing["Fe"]
        assert d_spacing[0] == pytest.approx(2.0269, abs=0.001)
```

### Test Data

Place test data files in `tests/data/`. Reference them using the `get_data_file` fixture from `conftest.py`.

## Pull Request Guidelines

### Before Submitting

- [ ] All tests pass (`pixi run test`)
- [ ] Pre-commit hooks pass (`pixi run pre-commit`)
- [ ] New code has appropriate test coverage
- [ ] Docstrings are updated for public APIs

### PR Description

Include:
- **Summary**: What the PR does
- **Motivation**: Why this change is needed
- **Test plan**: How to verify the changes work

### Review Process

1. Automated CI checks must pass
2. At least one maintainer approval required
3. Address review feedback promptly
4. Squash commits if requested

## Commit Messages

Write clear, concise commit messages:

```
Short summary (50 chars or less)

Optional longer description explaining the motivation
for the change. Wrap at 72 characters.

- Bullet points are fine
- Use present tense ("Add feature" not "Added feature")
```

## Reporting Issues

### Bug Reports

Include:
- Python version and OS
- Steps to reproduce
- Expected vs actual behavior
- Error messages and tracebacks

### Feature Requests

Include:
- Use case description
- Proposed solution (if any)
- Alternatives considered

## Questions?

- Open an issue for general questions
- Check existing issues and documentation first
- Tag maintainers if urgent

## License

By contributing, you agree that your contributions will be licensed under the BSD-3-Clause License.
