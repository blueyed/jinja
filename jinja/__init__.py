# -*- coding: utf-8 -*-
"""
    jinja
    ~~~~~

    Jinja is a template engine written in pure Python.  It provides a
    Django inspired non-XML syntax but supports inline expressions and
    an optional sandboxed environment.

    Nutshell
    --------

    Here a small example of a Jinja template::

        {% extends 'base.html' %}
        {% block title %}Memberlist{% endblock %}
        {% block content %}
          <ul>
          {% for user in users %}
            <li><a href="{{ user.url }}">{{ user.username }}</a></li>
          {% endfor %}
          </ul>
        {% endblock %}


    :copyright: (c) 2017 by the Jinja Team.
    :license: BSD, see LICENSE for more details.
"""
__version__ = "2.11.0.dev0"

# high level interface
from jinja.environment import Environment, Template

# loaders
from jinja.loaders import BaseLoader, FileSystemLoader, PackageLoader, \
     DictLoader, FunctionLoader, PrefixLoader, ChoiceLoader, \
     ModuleLoader

# bytecode caches
from jinja.bccache import BytecodeCache, FileSystemBytecodeCache, \
     MemcachedBytecodeCache

# undefined types
from jinja.runtime import Undefined, ChainableUndefined, DebugUndefined, \
     StrictUndefined, make_logging_undefined

# exceptions
from jinja.exceptions import TemplateError, UndefinedError, \
     TemplateNotFound, TemplatesNotFound, TemplateSyntaxError, \
     TemplateAssertionError, TemplateRuntimeError

# decorators and public utilities
from jinja.filters import environmentfilter, contextfilter, \
     evalcontextfilter
from jinja.utils import Markup, escape, clear_caches, \
     environmentfunction, evalcontextfunction, contextfunction, \
     is_undefined, select_autoescape
