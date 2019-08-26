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
from typing import List


class SyntaxStatement:
    def __init__(self, version):
        self.version = version


class FullId:
    def __init__(self, path: List[str], short_id: str):
        self.path = path
        self.base = short_id

    def __str__(self):
        return '.'.join(self.path + [self.base])

    def join(self, base: str):
        return FullId(self.path + [self.base], base)


class ImportStatement:
    def __init__(self, full_id: FullId):
        self.full_id = full_id


class PackageStatement:
    def __init__(self, full_id: FullId):
        self.full_id = full_id


class Option:
    def __init__(self, name, constant):
        self.name = name
        self.constant = constant


class Field:
    def __init__(self,
                 is_optional: bool,
                 is_repeated: bool,
                 is_required: bool,
                 type_id: FullId,
                 name: str,
                 value: int,
                 desc: List[str]):
        self.is_optional = is_optional
        self.is_repeated = is_repeated
        self.is_required = is_required
        self.type_id = type_id
        self.name = name
        self.value = value
        self.desc = desc


class MessageDeclaration:
    def __init__(self,
                 name: str,
                 fields: List[Field],
                 desc: List[str]):
        self.name = name
        self.fields = fields
        self.desc = desc
