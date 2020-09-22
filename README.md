# README

Datatracker is a basic logging Python package that keeps track of files and code within a Project. Each script is logged as an entry and input and output datafiles are recorded in order. Datatracker is able to manage versioning of both files and scripts, and is able to identify the most up-to-date version.

At the moment, this Python package is still in alpha, and I may include changes to both UI and file format that may be breaking.

## Installation

To install, run the following command:

```bash
pip install git+ssh://git@github.com/TarjinderSingh/datatracker
```

## Usage

### New entries

```python
from datatracker import *
tr = Tracker('db.json')

os.environ['VERSION'] = '0.1.0'

entry = Entry(tag='filter-common-variants',
              description='Filtering common variants in new GWAS data set.',
              category='Processing',
              module='Variant QC')

infile = entry.add(
    InputFile(tag='raw-plink-file',
              path='gs://bucket/raw-plink-file.bed',
              description='Raw PLINK file.'))


outfile = entry.add(
    OutputFile(tag='filt-plink-file',
               path='gs://bucket/raw-plink-file.bed',
               description='Filtered PLINK file.'))

tr.save(entry)
```

### View existing entries

```python
from datatracker import *
tr = Tracker('db.json')

tr.table
```

## License

MIT License (see repository)

## Maintainer

[TJ Singh @ tsingh@broadinstitute.org](tsingh@broadinstitute.org)
