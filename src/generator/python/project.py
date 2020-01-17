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
from protobuf import ast
from protobuf.parser import parse
from typing import List, Dict


class Package:
    def __init__(self, full_id: ast.FullId):
        self.full_id = full_id
        # mutable:
        self.messages = []


class Field:
    def __init__(self,
                 is_repeated: bool,
                 absolute_type_id: ast.FullId,
                 name: str,
                 value: int,
                 desc: List[str]):
        self.is_repeated = is_repeated
        self.absolute_type_id = absolute_type_id
        self.name = name
        self.value = value
        self.desc = desc
        self.is_optional = '+optional' in desc
        # mutable:
        self.resolved_type = None


class Message:
    def __init__(self, package: Package, name: str, fields: List[Field]):
        self.package = package
        self.name = name
        self.fields = fields
        self.full_id = package.full_id.join(name)


primitive_types = ['bytes', 'string', 'int32', 'int64', 'bool', 'map']


class Project:
    def __init__(self, packages: Dict[str, Package]):
        self.packages = packages
        self.messages = {}
        for p in packages.values():
            for m in p.messages:
                self.messages[str(m.full_id)] = m
        for p in packages.values():
            for m in p.messages:
                for f in m.fields:
                    if str(f.absolute_type_id.base) not in primitive_types:
                        f.resolved_type = self.find_message(f.absolute_type_id)

    def find_message(self, type_id: ast.FullId):
        return self.messages[str(type_id)]


class ProjectBuilder:
    def __init__(self):
        self.__packages = {}

    def add(self, t):
        package = None
        for n in t:
            if isinstance(n, ast.PackageStatement):
                package = self.__packages.get(str(n.full_id), None)
                if package is None:
                    package = Package(n.full_id)
                    self.__packages[str(n.full_id)] = package
            elif isinstance(n, ast.MessageDeclaration):
                fields = [
                    Field(
                        f.is_repeated,
                        f.type_id if 0 < len(f.type_id.path) or f.type_id.base in primitive_types
                        else package.full_id.join(f.type_id.base),
                        f.name,
                        f.value,
                        f.desc
                    ) for f in n.fields]
                package.messages.append(Message(package, n.name, fields))

    def build(self):
        return Project(self.__packages)


def build_project(protobuf_schemas):
    b = ProjectBuilder()
    for p in protobuf_schemas:
        with open(p, 'r') as f:
            b.add(parse(f.read()))
    return b.build()
