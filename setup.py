#!/usr/bin/env python
import pytest
from setuptools import setup, Command

class TestCommand(Command):
    """Runs the test suite."""
    description = """Runs the test suite."""
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        import pytest
        pytest.main('./mediagoblin_3dbureau/tests')

__VERSION__="0.1.0"
setup(
    name='mediagoblin-3dbureau',
    version=__VERSION__,
    description='Purchase 3d designs',
    author='Rodrigo Rodrigues da Silva',
    author_email='rsilva@metamaquina.com.br',
    url='https://example.com/REPO',
    download_url='https://example.com/mediagoblin-3dbureau-v' + __VERSION__,
    packages=['mediagoblin_3dbureau'],
    include_package_data=True,
    license=(b'License :: OSI Approved :: GNU Affero General Public License '
             b'v3 or later (AGPLv3+)'),
    cmdclass={'test': TestCommand},
)
