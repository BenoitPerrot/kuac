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
max_line_len = 80


def generate_field_name_and_doc(f: Field):
    field_name = f.name + '_' if f.name in python_keywords + python_builtins else camel_case_to_snake_case(f.name)
    indent = 2 * 4 * ' '
    line = indent + ':param ' + field_name + ':'
    indent += 7 * ' '
    lines = []
    for w in ' '.join(x for x in f.desc if not x.startswith('+')).split():
        if len(line) + 1 + len(w) < max_line_len:
            line += ' '
        else:
            lines.append(line)
            line = indent
        line += w
    lines.append(line)
    return field_name, '\n'.join(lines)


def generate_field_type_name(f: Field):
    primitive_type_name_to_python = {
        'bool': ('bool', []),
        'int32': ('int', []),
        'int64': ('int', []),
        'bytes': ('bytes', []),
        'string': ('str', []),
        'map': ('dict', []),
        'IntOrString': ('Union[int, str]', ['from typing import Union'])
    }
    (field_type_name, import_statements) = \
        primitive_type_name_to_python.get(f.absolute_type_id.base) or \
        (f.absolute_type_id.base, [
          'from kuac.models.{namespace} import {classname}'.format(
              namespace=str(f.resolved_type.full_id),
              classname=f.resolved_type.full_id.base
          )
        ])
    return ('List[' + field_type_name + ']', import_statements + ['from typing import List']) if f.is_repeated else\
        (field_type_name, import_statements)


def generate_ctor(msg: Message):
    import_statements = set()
    ctor_args_doc = []
    ctor_args = ['self']
    ctor_opt_args = []
    ctor_attrs_init = []
    for f in msg.fields:
        field_name, field_doc = generate_field_name_and_doc(f)
        ctor_args_doc.append(field_doc)
        field_type_name, field_import_statements = generate_field_type_name(f)
        import_statements.update(field_import_statements)
        (ctor_opt_args if f.is_optional else ctor_args).append(field_name + ': ' + field_type_name)
        ctor_attrs_init.append('self.' + field_name + ' = ' + field_name)
    return import_statements, ctor_args_doc, ctor_args + [a + ' = None' for a in ctor_opt_args], ctor_attrs_init


def generate_class(msg: Message):
    import_statements, ctor_args_doc, ctor_args, ctor_attrs_init = generate_ctor(msg)
    return '''\
{imports}\
class {class_name}:
    def __init__({ctor_args}
                 ):
        """
        {ctor_doc}
        """
        {ctor_body}
'''.format(
        imports='\n'.join(sorted(import_statements)) + ('\n\n\n' if 0 < len(import_statements) else ''),
        class_name=msg.name,
        ctor_args=(',\n' + ' ' * 17).join(ctor_args),
        ctor_doc=''.join('\n' + a for a in ctor_args_doc),
        ctor_body=('\n' + ' ' * 8).join(ctor_attrs_init) if 0 < len(ctor_attrs_init) else 'pass'
    )
