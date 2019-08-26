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
import argparse
import logging
import os
from protobuf.parser import parse
import sys


def parse_file(file_path, go_verbose):
    if go_verbose:
        logging.basicConfig(level=logging.INFO)
    with open(file_path) as f:
        logging.info('## ' + file_path)
        logging.info(parse(f.read()))


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-v',
                        help='Go verbose',
                        action='store_true')
    parser.add_argument('--protobufs-root',
                        help='Path of the root directory where protobuf schemas are located',
                        required=True)
    args = parser.parse_args(argv)

    for dir_name, _, file_names in os.walk(args.protobufs_root):
        for file_name in file_names:
            parse_file('%s/%s' % (dir_name, file_name), args.v)


if __name__ == '__main__':
    main(sys.argv[1:])
