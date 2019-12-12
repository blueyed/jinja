import sys
import warnings
from importlib import import_module

warnings.warn(
    "'jinja2' has been renamed to 'jinja'. Install and import from the"
    " 'jinja' package instead.",
    DeprecationWarning,
    stacklevel=2,
)
sys.modules["jinja2"] = import_module("jinja")
