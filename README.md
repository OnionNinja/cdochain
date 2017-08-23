# [DEPRECATED] cdochain
> Please use [https://github.com/ucyo/xsuite](github.com/ucyo/xsuite)

This module helps create chains of cdo commands for easy manipulation of climate data.

#### Features
- Method execution is lazy and gets processed only on function call `Chain.execute()`.
- Input supports Unix style pathname pattern search.
   - The Input will be first run with [glob](https://docs.python.org/3/library/glob.html) and checked if several
    files match.  
    :exclamation: _If that is the case a temporary file will be created_.
- Output can be a file on disc, an [netCDF4.Dataset](http://unidata.github.io/netcdf4-python/#netCDF4.Dataset) or (not) masked
[numpy.ndarray](http://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html).

## Installation

```bash
python3.5 -m pip install cdochain --pre
```

--- or ---

```bash
git clone https://github.com/OnionNinja/cdochain.git
cd cdochain
python3.5 setup.py install
```

## TL;DR

```python
from cdochain import chaining as cch

input = './tests/testdata/sresa1b_ncar_ccsm3-example.nc'
output = './enso34-mm.nc'
data = cch.Chain(ifile=input, ofile=output)
enso34 = data.sellonlatbox(190,240,-5,5).monmean()
out = enso34.execute()
```

## Usage
This module implements [method chaining](https://en.wikipedia.org/wiki/Method_chaining) for
the [Climate Data Operators](https://code.zmaw.de/projects/cdo) (CDO) tool
from the Max Planck Institute for Meteorology. Let us start:

```python
from cdochain import chaining as cch
```

For initialisation one has to define **input**, **output**, and may define
several **options**.

### Input
Now we have to define the files we want to work on:

- To use one file

```python
input = './tests/testdata/sresa1b_ncar_ccsm3-example.nc'
```
- To use several files you can give a Unix style pattern

```python
input = './tests/testdata/*.nc'
```
 _This creates a temporary file_ :exclamation:

### Output
For defining the output we have several options.

- To output a **file on disc**:

```python
data = cch.Chain(ifile=input, ofile='/path/to/output.nc')
```
- To output an **netcdf4.Dataset** object:

```python
data = cch.Chain(ifile=input, ofile='netCDF4')
```
- To output an **numpy.ndarray** object:

```python
data = cch.Chain(ifile=input, ofile='array:<var>')  # numpy.ndarray
# or
data = cch.Chain(ifile=input, ofile='maarray:<var>')  # masked numpy.ndarray
```
`<var>` defines the variable to be extracted and saved to numpy.ndarray.

### Options
As for options one can use the same as described on the [CDO website](https://code.zmaw.de/projects/cdo/embedded/index.html#x1-70001.2.1). The
default is `options='-O -f nc'`.

### **Operations**
The operations defined in
[CDO](https://code.zmaw.de/projects/cdo/embedded/index.html) can now be used
on the data element.

```python
analysis = data.sellonlatbox(190,240,-5,5).sellevidx(1).mermean()
fn = analysis.execute()
```

Have fun :neckbeard:
