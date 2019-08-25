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
import re


class TokenKind:
    NEWLINES = 0
    H_SPACES = 1
    COMMENT = 2

    LEFT_PAR = 10
    RIGHT_PAR = 11
    LEFT_BRACE = 12
    RIGHT_BRACE = 13
    LEFT_BRACKET = 14
    RIGHT_BRACKET = 15

    EQ = 20
    LT = 21
    GT = 22

    SEMI_COL = 30
    DOT = 31
    COLON = 32

    ID = 50
    STRING = 51
    INT = 52

    def __init__(self, kind, lexeme):
        self.kind = kind
        self.lexeme = lexeme

    def __str__(self):
        return self.lexeme


class Scanner:
    def __init__(self, text):
        self.lookahead = None
        # noinspection PyUnresolvedReferences
        s = re.Scanner([
            (r'[\n\r]+', lambda _, w: TokenKind(TokenKind.NEWLINES, w)),
            (r'\s+', lambda _, w: TokenKind(TokenKind.H_SPACES, w)),
            (r'//[^\n\r]*[\n\r]|/\*([^*]|\*[^/])*\*/', lambda _, w: TokenKind(TokenKind.COMMENT, w)),

            (r'\(', lambda _, w: TokenKind(TokenKind.LEFT_PAR, w)),
            (r'\)', lambda _, w: TokenKind(TokenKind.RIGHT_PAR, w)),
            (r'\{', lambda _, w: TokenKind(TokenKind.LEFT_BRACE, w)),
            (r'\}', lambda _, w: TokenKind(TokenKind.RIGHT_BRACE, w)),
            (r'\[', lambda _, w: TokenKind(TokenKind.LEFT_BRACKET, w)),
            (r'\]', lambda _, w: TokenKind(TokenKind.RIGHT_BRACKET, w)),

            (r'=', lambda _, w: TokenKind(TokenKind.EQ, w)),
            (r'<', lambda _, w: TokenKind(TokenKind.LT, w)),
            (r'>', lambda _, w: TokenKind(TokenKind.GT, w)),

            (r';', lambda _, w: TokenKind(TokenKind.SEMI_COL, w)),
            (r'\.', lambda _, w: TokenKind(TokenKind.DOT, w)),
            (r',', lambda _, w: TokenKind(TokenKind.COLON, w)),

            (r'[a-zA-Z_][a-zA-Z_0-9]*', lambda _, w: TokenKind(TokenKind.ID, w)),
            (r'''('[^']*'|"[^"]*")''', lambda _, w: TokenKind(TokenKind.STRING, w)),
            (r'[0-9]+', lambda _, w: TokenKind(TokenKind.INT, w))
        ])
        self.__tokens, r = s.scan(text)
        self.__pos = 0
        self.preceding_comments = []

    def __get_next_significant_token(self):
        while self.__pos < len(self.__tokens):
            t = self.__tokens[self.__pos]
            self.__pos += 1
            if t.kind == TokenKind.COMMENT:
                self.preceding_comments.append(t.lexeme[2:][:-1])
            elif t.kind == TokenKind.NEWLINES:
                self.preceding_comments = []
            elif t.kind != TokenKind.H_SPACES:
                return t
        return None

    def get(self):
        if self.lookahead is None:
            return self.__get_next_significant_token()
        x = self.lookahead
        self.lookahead = None
        return x

    def peek(self):
        self.lookahead = self.get()
        return self.lookahead
