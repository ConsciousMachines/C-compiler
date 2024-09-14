


from typing import List, Tuple
from enum import Enum
from common import *

# --- L E X E R 
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

# lexer single tokens 
class Lexer_Token(Enum):
    # single character lexemes
    SEMICOLON = 1
    BRACE_OPEN = 2 
    BRACE_CLOSE = 3
    BRACKET_OPEN = 4
    BRACKET_CLOSE = 5
    HYPHEN = 11
    TILDE = 12
    DECREMENT = 13
    PLUS_SIGN = 14
    ASTERISK = 15
    FORWARD_SLASH = 16
    PERCENT_SIGN = 17

    AMPERSAND         = 18 
    PIPE              = 19 
    CARET             = 20
    LESS_THAN         = 21
    GREATER_THAN      = 22
    EXCLAMATION       = 25

    # multi-char lexemes
    INTEGER = 6
    IDENTIFIER = 7
    LEFT_SHIFT = 23
    RIGHT_SHIFT = 24
    LOGICAL_AND = 26
    LOGICAL_OR  = 27
    EQUAL_TO = 28
    NOT_EQUAL_TO = 29
    LESS_THAN_OR_EQUAL_TO = 30
    GREATER_THAN_OR_EQUAL_TO = 31

    # reserved words 
    RESERVED_INT = 8
    RESERVED_VOID = 9
    RESERVED_RETURN = 10


                            

class lexer:
    def __init__(self) -> None:
        self.tokens : List[Tuple[Lexer_Token, str]] = []

        # lexer number
        self.lexer_numeric_char = '0123456789'
        # lexer non-number
        self.lexer_non_numeric_char = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789'

        # lexemes of length 1
        self._length1_lexeme_to_token = {
            ';' : Lexer_Token.SEMICOLON ,
            '{' : Lexer_Token.BRACE_OPEN ,
            '}' : Lexer_Token.BRACE_CLOSE ,
            '(' : Lexer_Token.BRACKET_OPEN ,
            ')' : Lexer_Token.BRACKET_CLOSE ,
            '-' : Lexer_Token.HYPHEN ,
            '~' : Lexer_Token.TILDE ,
            '+' : Lexer_Token.PLUS_SIGN ,
            '*' : Lexer_Token.ASTERISK ,
            '/' : Lexer_Token.FORWARD_SLASH ,
            '%' : Lexer_Token.PERCENT_SIGN ,
            '&' : Lexer_Token.AMPERSAND ,
            '|' : Lexer_Token.PIPE ,
            '^' : Lexer_Token.CARET ,
            '<' : Lexer_Token.LESS_THAN ,
            '>' : Lexer_Token.GREATER_THAN ,
            '!' : Lexer_Token.EXCLAMATION,
        }
        self._length1_lexemes = self._length1_lexeme_to_token.keys()

        # lexemes of length 2
        self._length2_lexeme_to_token = {
            '<<' : Lexer_Token.LEFT_SHIFT,
            '>>' : Lexer_Token.RIGHT_SHIFT,
            '&&' : Lexer_Token.LOGICAL_AND,
            '||' : Lexer_Token.LOGICAL_OR,
            '==' : Lexer_Token.EQUAL_TO,
            '!=' : Lexer_Token.NOT_EQUAL_TO,
            '<=' : Lexer_Token.LESS_THAN_OR_EQUAL_TO,
            '>=' : Lexer_Token.GREATER_THAN_OR_EQUAL_TO,
        }
        self._length2_lexemes = self._length2_lexeme_to_token.keys()

        # reserved lexemes
        self._reserved_lexeme_to_token = {
            'int' : Lexer_Token.RESERVED_INT,
            'void' : Lexer_Token.RESERVED_VOID,
            'return' : Lexer_Token.RESERVED_RETURN,
        }
        self._reserved_lexemes = self._reserved_lexeme_to_token.keys()
        
        # create a word boundary class to check regex word boundary
        word_boundary = []
        for i in range(128):
            c = chr(i)  # convert ASCII to char
            if c.isalnum() or (c == '_'): # skip alpha-numeric
                continue
            word_boundary.append(c)
        self.word_boundary = ''.join(word_boundary)

    def print(self) -> None:
        for _tok, _lex in self.tokens:
            print(_lex, (20 - len(_lex)) * ' ', _tok)

    # iterate over each character
    def lex(self, program) -> int: 

        program = program + ' ' # add padding, to preview size-2 lexemes

        i = 0 
        while i < len(program):

            # get corresponding char
            c = program[i]

            # if character is whitespace, skip it 
            if c in [' ', '\t', '\n']:
                i += 1
                continue

            # lexemes of length 2: << >> && || != 
            cc = program[i:i+2]
            if cc in self._length2_lexemes:
                self.tokens.append((self._length2_lexeme_to_token[cc], cc))
                i += 2
                continue  

            # if character is single-char keyword, 
            if c in self._length1_lexemes:

                # return the corresponding token
                self.tokens.append((self._length1_lexeme_to_token[c], c))

                # update current index
                i += 1
                continue       

            # word boundary will be after identifier/keyword by definition
            # only need to check it after number, in case 123abc

            # if character is numeric, parse number
            if c in self.lexer_numeric_char:
                
                # start at next char
                j = i + 1

                # keep incrementing until we find non-number
                while program[j] in self.lexer_numeric_char: 
                    j += 1

                # assert program[j] in word_boundary, 'numeric not followed by word boundary'
                if program[j] not in self.word_boundary:
                    print('Lexer Error: numeric not followed by word boundary')
                    return 1


                # now we know start and end of numeric sub-string
                substr = program[i:j]

                # add it to tokens & lexemes 
                self.tokens.append((Lexer_Token.INTEGER, substr))

                # update current index
                i = j 
                continue 

            # otherwise, parse a word 
            if c in self.lexer_non_numeric_char:

                # start at next char
                j = i + 1
                
                # keep incrementing until we find something different
                while program[j] in self.lexer_non_numeric_char: 
                    j += 1

                # now we know start and end of numeric sub-string
                substr = program[i:j]

                # is it a reserved word?
                if substr in self._reserved_lexemes:

                    # add it to tokens & lexemes 
                    self.tokens.append((self._reserved_lexeme_to_token[substr], substr))

                # else, it is an identifier
                else:

                    # add it to tokens & lexemes 
                    self.tokens.append((Lexer_Token.IDENTIFIER, substr))

                # update current index
                i = j 
                continue 

            msg = f'Lexer Error: unexpected character: {c}'
            error(msg)
            return 1 # error, unreachable
                
        return 0


if __name__ == "__main__":
    l = lexer()
    my_exit_code = l.lex(source_)
    l.print()
