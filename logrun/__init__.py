"""
logrun is a package for convenient experiment logging.

Generally, all you need are the functions in the `logrun.utils` subpackage. A general set of
functions is in `logrun.utils.general`, but there are other modules for more domain-specific
utilities (e.g. `logrun.utils.ml`).

If you want to extend `logrun`, you'll want to use the functionalities provided by the
`logrun.internals` module. For examples, take a look at some of the source code for the functions in
`logrun.utils`.
"""

from logrun import utils
from logrun import internals


__version__ = '0.1.1'
