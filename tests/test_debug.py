# -*- coding: utf-8 -*-
"""
    jinja2.testsuite.debug
    ~~~~~~~~~~~~~~~~~~~~~~

    Tests the debug system.

    :copyright: (c) 2017 by the Jinja Team.
    :license: BSD, see LICENSE for more details.
"""
import pytest

import re
import sys
from traceback import format_exception

from jinja2 import ChoiceLoader
from jinja2 import DictLoader
from jinja2 import Environment, TemplateSyntaxError


@pytest.fixture
def fs_env(filesystem_loader):
    '''returns a new environment.
    '''
    return Environment(loader=filesystem_loader)


@pytest.mark.debug
class TestDebug(object):

    def assert_traceback_matches(self, callback, expected_tb):
        try:
            callback()
        except Exception as e:
            tb = format_exception(*sys.exc_info())
            if re.search(expected_tb.strip(), ''.join(tb)) is None:
                assert False, ('Traceback did not match:\n\n%s\nexpected:\n%s' %
                               (''.join(tb), expected_tb))
        else:
            assert False, 'Expected exception'

    def test_runtime_error(self, fs_env):
        def test():
            tmpl.render(fail=lambda: 1 / 0)
        tmpl = fs_env.get_template('broken.html')
        self.assert_traceback_matches(test, r'''
  File ".*?broken.html", line 2, in (top-level template code|<module>)
    \{\{ fail\(\) \}\}
  File ".*debug?.pyc?", line \d+, in <lambda>
    tmpl\.render\(fail=lambda: 1 / 0\)
ZeroDivisionError: (int(eger)? )?division (or modulo )?by zero
''')

    def test_syntax_error(self, fs_env):
        # The trailing .*? is for PyPy 2 and 3, which don't seem to
        # clear the exception's original traceback, leaving the syntax
        # error in the middle of other compiler frames.
        self.assert_traceback_matches(lambda: fs_env.get_template('syntaxerror.html'), r'''(?sm)
  File ".*?syntaxerror.html", line 4, in (template|<module>)
    \{% endif %\}.*?
(jinja2\.exceptions\.)?TemplateSyntaxError: Encountered unknown tag 'endif'. Jinja was looking for the following tags: 'endfor' or 'else'. The innermost block that needs to be closed is 'for'.
    ''')

    def test_regular_syntax_error(self, fs_env):
        def test():
            raise TemplateSyntaxError('wtf', 42)
        self.assert_traceback_matches(test, r'''
  File ".*debug.pyc?", line \d+, in test
    raise TemplateSyntaxError\('wtf', 42\)
(jinja2\.exceptions\.)?TemplateSyntaxError: wtf
  line 42''')

    def test_include_syntax_error_source(self, filesystem_loader):
        e = Environment(loader=ChoiceLoader(
            [
                filesystem_loader,
                DictLoader({"inc": "a\n{% include 'syntaxerror.html' %}\nb"}),
            ]
        ))
        t = e.get_template("inc")

        with pytest.raises(TemplateSyntaxError) as exc_info:
            t.render()

        assert exc_info.value.source is not None

    def test_local_extraction(self):
        from jinja2.debug import get_template_locals
        from jinja2.runtime import missing
        locals = get_template_locals({
            'l_0_foo': 42,
            'l_1_foo': 23,
            'l_2_foo': 13,
            'l_0_bar': 99,
            'l_1_bar': missing,
            'l_0_baz': missing,
        })
        assert locals == {'foo': 13, 'bar': 99}

    def test_get_corresponding_lineno_traceback(self, fs_env):
        tmpl = fs_env.get_template('test.html')
        assert tmpl.get_corresponding_lineno(1) == 1
