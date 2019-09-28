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
from project import Field, Message


def camel_case_to_snake_case(s):
    r = ''
    last_is_upper = False
    for c in s:
        if c.isupper():
            if not last_is_upper:
                r += '_'
            last_is_upper = True
        else:
            last_is_upper = False
        r += c.lower()
    return r


python_keywords = ['continue', 'except', 'from']
python_builtins = ['type', 'exec', 'range', 'object', 'min', 'max']


def generate_field_name(f: Field):
    return f.name + '_' if f.name in python_keywords + python_builtins else camel_case_to_snake_case(f.name)


def generate_ctor(msg: Message):
    ctor_args = ['self']
    ctor_opt_args = []
    ctor_attrs_init = []
    for f in msg.fields:
        field_name = generate_field_name(f)
        (ctor_opt_args if f.is_optional else ctor_args).append(field_name)
        ctor_attrs_init.append('self.' + field_name + ' = ' + field_name)
    return ctor_args + [a + '=None' for a in ctor_opt_args], ctor_attrs_init


def generate_class(msg: Message):
    ctor_args, ctor_attrs_init = generate_ctor(msg)
    return '''\
class {class_name}:
    def __init__({ctor_args}
                 ):
        {ctor_body}
'''.format(
        class_name=msg.name,
        ctor_args=(',\n' + ' ' * 17).join(ctor_args),
        ctor_body=('\n' + ' ' * 8).join(ctor_attrs_init) if 0 < len(ctor_attrs_init) else 'pass'
    )
