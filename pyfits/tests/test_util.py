from __future__ import with_statement


import os
import signal
import sys

import nose
from nose.tools import assert_raises
from warnings import catch_warnings

from ..util import ignore_sigint
from . import PyfitsTestCase


class TestUtils(PyfitsTestCase):
    def test_ignore_sigint(self):
        if sys.platform.startswith('win'):
            # Not available in some Python versions on Windows
            raise nose.SkipTest('os.kill() not available')

        @ignore_sigint
        def test():
            with catch_warnings(record=True) as w:
                pid = os.getpid()
                os.kill(pid, signal.SIGINT)
                # One more time, for good measure
                os.kill(pid, signal.SIGINT)
                assert len(w) == 2
                assert (str(w[0].message) ==
                        'KeyboardInterrupt ignored until test is '
                        'complete!')

        assert_raises(KeyboardInterrupt, test)
