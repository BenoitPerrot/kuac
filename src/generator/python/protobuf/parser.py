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
from .ast import *
import logging
from .scanner import Scanner, TokenKind


def parse(text):
    def parse_full_id(scanner):
        full = [scanner.expect(TokenKind.ID).lexeme]
        while scanner.skip(TokenKind.DOT):
            full.append(scanner.expect(TokenKind.ID).lexeme)
        return FullId(full[:-1], full[-1])

    def parse_after_syntax(scanner):
        scanner.expect(TokenKind.EQ)
        version = scanner.expect(TokenKind.STRING).lexeme
        scanner.expect(TokenKind.SEMI_COL)
        return SyntaxStatement(version)

    def parse_after_import(scanner):
        qualifier = scanner.peek().lexeme
        is_weak = qualifier == 'weak'
        is_public = qualifier == 'public'
        if is_weak or is_public:
            scanner.get(scanner)
        name = scanner.expect(TokenKind.STRING)
        scanner.expect(TokenKind.SEMI_COL)
        return ImportStatement(name)

    def parse_after_package(scanner):
        name = parse_full_id(scanner)
        scanner.expect(TokenKind.SEMI_COL)
        return PackageStatement(name)

    def parse_after_option(scanner):
        name = scanner.expect(TokenKind.ID).lexeme
        scanner.expect(TokenKind.EQ)
        constant = scanner.get()
        scanner.expect(TokenKind.SEMI_COL)
        return Option(name, constant)

    def parse_type_name(scanner):
        type_name = parse_full_id(scanner)  # TODO: support .ID
        if scanner.skip(TokenKind.LT):
            parameters = [parse_full_id(scanner)]
            while scanner.skip(TokenKind.COLON):
                parameters.append(parse_full_id(scanner))
            scanner.expect(TokenKind.GT)
            # TODO: store parameters
        return type_name

    def parse_after_message(scanner):
        def parse_message_field():
            desc = [s.lstrip() for s in scanner.preceding_comments]
            label = scanner.peek().lexeme
            is_optional = label == 'optional'
            is_repeated = label == 'repeated'
            is_required = label == 'required'
            if is_optional or is_repeated or is_required:
                scanner.get()
            type_name = parse_type_name(scanner)
            name = scanner.expect(TokenKind.ID).lexeme
            scanner.expect(TokenKind.EQ)
            number = scanner.get()
            if scanner.skip(TokenKind.LEFT_BRACKET):
                # TODO: parse field options
                scanner.expect(TokenKind.RIGHT_BRACKET)
            scanner.expect(TokenKind.SEMI_COL)
            return Field(is_optional, is_repeated, is_required, type_name, name, number, desc)

        message_desc = scanner.preceding_comments
        message_name = scanner.expect(TokenKind.ID).lexeme
        scanner.expect(TokenKind.LEFT_BRACE)
        fields = []
        while not scanner.skip(TokenKind.RIGHT_BRACE):
            fields.append(parse_message_field())
        return MessageDeclaration(message_name, fields, message_desc)

    def parse_root(scanner):
        ast = []
        while scanner.peek():
            t = scanner.get()
            parse_after = {
                'syntax': parse_after_syntax,
                'package': parse_after_package,
                'import': parse_after_import,
                'message': parse_after_message,
                'option': parse_after_option
            }.get(t.lexeme)
            if parse_after:
                ast.append(parse_after(scanner))
            else:
                logging.error(t)
        return ast

    return parse_root(Scanner(text))
