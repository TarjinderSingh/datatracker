from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from .tracker import Tracker
from .entry import Entry
from .file import InputFile, OutputFile
from .dictlist import DictList
from .schema import category_template