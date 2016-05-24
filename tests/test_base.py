#!/usr/bin/python
# Copyright (c) 2015 SUSE Linux GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import imp
import os
import shutil
import subprocess
import sys
import tempfile
import unittest


# NOTE(toabctl): Hack to import non-module file for testing
sv = imp.load_source("renderspec", "renderspec")


RENDERSPEC_EXECUTABLE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../', 'renderspec')
)


class RenderspecBaseTest(unittest.TestCase):
    """Basic test class. Other tests should use this one"""

    def setUp(self):
        self._tmpdir = tempfile.mkdtemp(prefix='obs-service-renderspec-test-')
        os.chdir(self._tmpdir)

    def _run_renderspec(self, params=[]):
        self._tmpoutdir = tempfile.mkdtemp(
            prefix='obs-service-renderspec-test-outdir-')
        cmd = [sys.executable,
               RENDERSPEC_EXECUTABLE,
               '--outdir', self._tmpoutdir] + params
        try:
            subprocess.check_output(
                cmd, stderr=subprocess.STDOUT, env=os.environ.copy())
            for f in os.listdir(self._tmpoutdir):
                os.unlink(self._tmpdir+"/"+f)
                # FIXME: in most modes the files get not replaced,
                # but store in parallel with _service: prefix
                shutil.move(self._tmpoutdir+"/"+f, self._tmpdir)
            shutil.rmtree(self._tmpoutdir)
        except subprocess.CalledProcessError as e:
            raise Exception(
                "Can not call '%s' in dir '%s'. Error: %s" % (" ".join(cmd),
                                                              self._tmpdir,
                                                              e.output))

    def tearDown(self):
        shutil.rmtree(self._tmpdir)


class RenderspecBasics(RenderspecBaseTest):
    def _write_template(self, name):
        """write a template which can be rendered"""
        with open(os.path.join(self._tmpdir, name), 'w+') as f:
            f.write('{{ py2pkg("oslo.log") }}')

    def test_help(self):
        self._run_renderspec(['-h'])

    def test_render(self):
        self._write_template('template.spec.j2')
        self._run_renderspec(['--input-template', 'template.spec.j2'])


if __name__ == '__main__':
    unittest.main()
