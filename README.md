[![Project generated with PyScaffold](https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold)](https://pyscaffold.org/)
[![Coveralls](https://img.shields.io/coveralls/github/andrijdavid/python-debugtoolkit/main.svg)](https://coveralls.io/r/andrijdavid/python-debugtoolkit)
[![PyPI-Server](https://img.shields.io/pypi/v/python-debugtoolkit.svg)](https://pypi.org/project/python-debugtoolkit/)
[![Conda-Forge](https://img.shields.io/conda/vn/conda-forge/python-debugtoolkit.svg)](https://anaconda.org/conda-forge/python-debugtoolkit)
[![ReadTheDocs](https://readthedocs.org/projects/python-debugtoolkit/badge/?version=latest)](https://python-debugtoolkit.readthedocs.io/en/stable/)
[![Monthly Downloads](https://pepy.tech/badge/python-debugtoolkit/month)](https://pepy.tech/project/python-debugtoolkit)

# python-debugtoolkit

> DebugToolkit is a versatile Python package designed for debugging

This library provides decorators to log various aspects of function execution. It includes decorators to log input arguments, execution time, garbage collection counts, and resource usage.

## Installation

``` pip install debugtoolkit ```

## Usage
To use these decorators, simply import the decorators library and use the @ symbol followed by the decorator name before the function definition. For example:

```python
import debugtoolkit


@debugtoolkit.log_inputs
def my_function(a, b):
    return a + b
```
This will log the input arguments every time my_function is called.

### Contributing

Contributions are welcome. Please submit a pull request with any improvements.
