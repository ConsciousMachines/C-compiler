


from typing import List, Tuple
from enum import Enum, auto
from common import *

# --- L E X E R 
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

# lexer single tokens 
class Lexer_Token(Enum):
    # 1 character lexemes
    SEMICOLON                    = auto() # ;
    BRACE_OPEN                   = auto() # {
    BRACE_CLOSE                  = auto() # }
    BRACKET_OPEN                 = auto() # (
    BRACKET_CLOSE                = auto() # )
    HYPHEN                       = auto() # -
    TILDE                        = auto() # ~
    PLUS_SIGN                    = auto() # +
    ASTERISK                     = auto() # *
    FORWARD_SLASH                = auto() # /
    PERCENT_SIGN                 = auto() # %
    EQUALS_SIGN                  = auto() # =
    AMPERSAND                    = auto() # &
    PIPE                         = auto() # |
    CARET                        = auto() # ^
    LESS_THAN                    = auto() # <
    GREATER_THAN                 = auto() # >
    EXCLAMATION                  = auto() # !
    QUESTION_MARK                = auto() # ?
    COLON                        = auto() # :

    # 2 character lexemes
    LEFT_SHIFT                   = auto() # <<
    RIGHT_SHIFT                  = auto() # >>
    LOGICAL_AND                  = auto() # &&
    LOGICAL_OR                   = auto() # ||
    EQUAL_TO                     = auto() # ==
    NOT_EQUAL_TO                 = auto() # != 
    LESS_THAN_OR_EQUAL_TO        = auto() # <= 
    GREATER_THAN_OR_EQUAL_TO     = auto() # >= 
    COMPOUND_ASSIGNMENT_PLUS_EQ  = auto() # += 
    COMPOUND_ASSIGNMENT_MINUS_EQ = auto() # -= 
    COMPOUND_ASSIGNMENT_MULT_EQ  = auto() # *= 
    COMPOUND_ASSIGNMENT_DIV_EQ   = auto() # /= 
    COMPOUND_ASSIGNMENT_MOD_EQ   = auto() # %= 
    COMPOUND_ASSIGNMENT_AND_EQ   = auto() # &= 
    COMPOUND_ASSIGNMENT_OR_EQ    = auto() # |= 
    COMPOUND_ASSIGNMENT_XOR_EQ   = auto() # ^= 
    INCREMENT                    = auto() # ++
    DECREMENT                    = auto() # --

    # 3 character lexemes
    COMPOUND_ASSIGNMENT_SHL_EQ   = auto() # <<= 
    COMPOUND_ASSIGNMENT_SHR_EQ   = auto() # >>= 

    # multi-char lexemes
    INTEGER                      = auto() # <integer>
    IDENTIFIER                   = auto() # <identifier>

    # reserved words 
    RESERVED_INT      = auto() # int
    RESERVED_VOID     = auto() # void
    RESERVED_RETURN   = auto() # return
    RESERVED_IF       = auto() # if
    RESERVED_ELSE     = auto() # else
    RESERVED_GOTO     = auto() # goto
    RESERVED_DO       = auto() # do
    RESERVED_WHILE    = auto() # while
    RESERVED_FOR      = auto() # for
    RESERVED_BREAK    = auto() # break
    RESERVED_CONTINUE = auto() # continue


                            

class lexer:
    def __init__(self) -> None:
        self.tokens : List[Tuple[Lexer_Token, str]] = []

        # lexer number
        self.lexer_numeric_char = '0123456789'
        # lexer non-number
        self.lexer_non_numeric_char = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789'

        # lexemes of length 1
        self._length1_lexeme_to_token = {
            ';' : Lexer_Token.SEMICOLON,
            '{' : Lexer_Token.BRACE_OPEN,
            '}' : Lexer_Token.BRACE_CLOSE,
            '(' : Lexer_Token.BRACKET_OPEN,
            ')' : Lexer_Token.BRACKET_CLOSE,
            '-' : Lexer_Token.HYPHEN,
            '~' : Lexer_Token.TILDE,
            '+' : Lexer_Token.PLUS_SIGN,
            '*' : Lexer_Token.ASTERISK,
            '/' : Lexer_Token.FORWARD_SLASH,
            '%' : Lexer_Token.PERCENT_SIGN,
            '=' : Lexer_Token.EQUALS_SIGN,
            '&' : Lexer_Token.AMPERSAND,
            '|' : Lexer_Token.PIPE,
            '^' : Lexer_Token.CARET,
            '<' : Lexer_Token.LESS_THAN,
            '>' : Lexer_Token.GREATER_THAN,
            '!' : Lexer_Token.EXCLAMATION,
            '?' : Lexer_Token.QUESTION_MARK,
            ':' : Lexer_Token.COLON,
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
            '+=' : Lexer_Token.COMPOUND_ASSIGNMENT_PLUS_EQ,
            '-=' : Lexer_Token.COMPOUND_ASSIGNMENT_MINUS_EQ,
            '*=' : Lexer_Token.COMPOUND_ASSIGNMENT_MULT_EQ,
            '/=' : Lexer_Token.COMPOUND_ASSIGNMENT_DIV_EQ,
            '%=' : Lexer_Token.COMPOUND_ASSIGNMENT_MOD_EQ,
            '&=' : Lexer_Token.COMPOUND_ASSIGNMENT_AND_EQ,
            '|=' : Lexer_Token.COMPOUND_ASSIGNMENT_OR_EQ,
            '^=' : Lexer_Token.COMPOUND_ASSIGNMENT_XOR_EQ,
            '++' : Lexer_Token.INCREMENT,
            '--' : Lexer_Token.DECREMENT,
        }
        self._length2_lexemes = self._length2_lexeme_to_token.keys()

        # lexemes of length 3
        self._length3_lexeme_to_token = {
            '<<=' : Lexer_Token.COMPOUND_ASSIGNMENT_SHL_EQ,
            '>>=' : Lexer_Token.COMPOUND_ASSIGNMENT_SHR_EQ,
        }
        self._length3_lexemes = self._length3_lexeme_to_token.keys()

        # reserved lexemes
        self._reserved_lexeme_to_token = {
            'int'     : Lexer_Token.RESERVED_INT,
            'void'    : Lexer_Token.RESERVED_VOID,
            'return'  : Lexer_Token.RESERVED_RETURN,
            'if'      : Lexer_Token.RESERVED_IF,
            'else'    : Lexer_Token.RESERVED_ELSE,
            'goto'    : Lexer_Token.RESERVED_GOTO,
            'do'      : Lexer_Token.RESERVED_DO,
            'while'   : Lexer_Token.RESERVED_WHILE,
            'for'     : Lexer_Token.RESERVED_FOR,
            'break'   : Lexer_Token.RESERVED_BREAK,
            'continue': Lexer_Token.RESERVED_CONTINUE,
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

        program = program + '  ' # add 2 padding, to preview size-3 lexemes

        i = 0 
        while i < len(program):

            # get corresponding char
            c = program[i]

            # if character is whitespace, skip it 
            if c in [' ', '\t', '\n']:
                i += 1
                continue

            # lexemes of length 3: <<= >>=
            ccc = program[i:i+3]
            if ccc in self._length3_lexemes:
                self.tokens.append((self._length3_lexeme_to_token[ccc], ccc))
                i += 3
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
