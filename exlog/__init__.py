"""
exlog is a package for convenient experiment logging.

Generally, all you need are the functions in the `exlog.utils` subpackage. A general set of
functions is in `exlog.utils.general`, but there are other modules for more domain-specific
utilities (e.g. `exlog.utils.ml`).

If you want to extend `expath`, you'll want to use the functionalities provided by the
`expath.internals` module. For examples, take a look at some of the source code for the functions in
`exlog.utils`.
"""

from exlog import utils
from exlog import internals
