# Copyright 2019 Benoit Perrot
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='kuac',
    version='0.1',
    description='Kubernetes configuration As Code',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='kubernetes',
    license='Apache-2.0',
    url='https://github.com/BenoitPerrot/kuac',
    author='Benoit Perrot',
    classifiers=[
        'License :: OSI Approved :: Apache License 2.0',
        'Programming Language :: Python :: 3',
    ],

    package_dir={
        '': 'src/main'
    },
    packages=[
        'kuac'
    ],
    python_requires='>=3.7',

    test_suite='src.test.kuac'
)
