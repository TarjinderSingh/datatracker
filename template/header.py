# %%
#region
# Import necessary libraries
import os
from loguru import logger
import hail as hl
import {project_name} # Import your project

# Import classes from datatracker and findhere modules
from datatracker import Entry, InputFile, OutputFile, Tracker
from findhere import here, init_directories
#endregion

# Set environment variable
os.environ['VERSION'] = 'version' # Set the version of your project

# Initialize directories
# These directories are used to store your project files
cloudir, localdir, filedir = init_directories(__file__)

#%%
# Create tracker entry
# Tracker is used to keep track of your project's progress
tr = Tracker()
entry = Entry(tag='tag', # Tag to identify the entry
              description='desc', # Description of the entry
              category='category', # Category of the entry
              module='module') # Module of the entry

# %%
#---------------------------------------------------
# Define the name of the command
name = 'name'

# Add output file to the entry
outfile = entry.add(
    OutputFile(tag='tag', # Tag to identify the output file
               path=os.path.join(cloudir, 'path'), # Path of the output file
               description='desc')) # Description of the output file

# Add input file to the entry
infile = entry.add(
    InputFile(tag='tag', # Tag to identify the input file
              path=os.path.join(cloudir, 'path'), # Path of the input file
              description='desc')) # Description of the input file

# %%

# Add your code here

# %%
# Save the entry to the tracker
tr.save(entry)
# %%