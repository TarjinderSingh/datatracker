# Datatracker

Datatracker is a Python package designed for logging and tracking files and code within a project. It logs each script as an entry and records input and output data files in sequence. Datatracker also manages versioning of files and scripts, identifying the most recent version.

## Installation

Install Datatracker using pip:

```bash
pip install -U datatracker
```

Or, install directly from Github:

```bash
pip install git+ssh://git@github.com/TarjinderSingh/datatracker
```

## Learning from Templates

To understand how to use Datatracker, refer to the template scripts in this repository. These scripts demonstrate the various features of Datatracker. For instance, view the header.py scriptt [here](https://github.com/TarjinderSingh/datatracker/blob/master/template/header.py).

## Syntax and explanation

### New entries

Each script you run is an "entry". An entry requires a tag, description, category, and module.

1. `tag` is a unique identifier to  the script in question and should be clear what the general purpose and output of the script is. (ie Merge is not what we want to see here)
2. `description` needs to be one or two sentences equivalent of the Git commit message that thoroughly describes the general purpose and output of the script.
3. `category` indicates the general step of analysis the script belongs to.
4. `module` is the sub-category for which the script belongs to. Type `category_template` in interactive Python for an idea of the appropriate categories and modules are.

Within an entry, you define InputFiles and OutputFiles:

1. `tag` is a unique identifier to the File in question and should be clear what the general purpose and output of the script is. (ie Merge is not what we want to see here).
2. `description` for a file is a one or two sentences equivalent of the Git commit message that thoroughly describe the general purposes of the File at hand.

```python
from datatracker import *
tr = Tracker()

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

### Viewing Existing Entries=

```python
from datatracker import *
tr = Tracker()

tr.table
```

### Using Existing Entries for Pipeline

```python
infile = entry.add(InputFile(entry_tag='filter-common-variants', tag='raw-plink-file', database=tr))
```

### Filtering and Removing Entries

```python
# filter to entry
tr.filter(tr.entry.tag_version == 'import-array_0.1.6')

# remove entry
tr.remove(tr.entry.tag_version == 'import-array_0.1.6')
```

### Exporting to Pandas and Excel

```python
df = tr.explode()
df = tr.explode('filt-plink-file')

df = tr.to_pandas()
df = tr.table

df.to_excel('spreadsheet.xlsx')
```

## Data artifacts

```python
infile = entry.add(InputFile(path='gs://checkpoint-cache/tmp/1.bed'))
```

## License

MIT License (see repository)

## Maintainer

[TJ Singh @ CUIMC](tsingh@nygenome.org)