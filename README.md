# cdochain
This module helps create chains of cdo commands for easy manipulation of climate data.

## Installation

```
python3.5 -m pip install cdochain --pre
```
--- or ---
```
git clone https://github.com/OnionNinja/cdochain
cd cdochain
python3.5 setup.py install
```

## Usage

```python3
from cdochain import Chain as cch

ifile='./tests/testdata/sresa1b_ncar_ccsm3-example.nc'
ofile = '/tmp/tmp.nc'
data = cch.Chain(ifile=ifile, ofile=ofile)
routine = data.mermean().zonmean().sellevidx(53)
routine.execute()
```

... to be continued
