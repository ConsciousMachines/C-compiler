

from typing import List, Tuple
from common import *
from lex import *


# --- P A R S E R 
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

# base class
# -----------------------------------------------------------------------------

class AstNode: 
    pass

# grammar LHS
# -----------------------------------------------------------------------------

class program(AstNode):
    pass 

class function_definition(AstNode):
    pass 

class statement(AstNode):
    pass 

class exp(AstNode):
    pass 

class unary_operator(AstNode):
    pass

class binary_operator(AstNode):
    pass

# grammar RHS 
# -----------------------------------------------------------------------------
# --- BEGIN CLASS DEFINITION

class identifier(AstNode):
    def __init__(self, str_:str):
        self.str_:str = str_ 

class integer(AstNode):
    def __init__(self, int_:int):
        self.int_:int = int_

# program

class Program(program):
    def __init__(self, fd:function_definition):
        self.fd:function_definition = fd

# function_definition

class Function(function_definition):
    def __init__(self, name:identifier, body:statement):
        self.name:identifier = name 
        self.body:statement = body

# statement

class Return(statement):
    def __init__(self, exp_:exp):
        self.exp_:exp = exp_

# exp

class Constant(exp):
    def __init__(self, integer_:integer):
        self.integer_:integer = integer_

class Unary(exp):
    def __init__(self, unary_operator_:unary_operator, exp_:exp):
        self.unary_operator_:unary_operator = unary_operator_
        self.exp_:exp = exp_

class Binary(exp):
    def __init__(self, binary_operator_:binary_operator, exp1:exp, exp2:exp):
        self.binary_operator_:binary_operator = binary_operator_
        self.exp1:exp = exp1
        self.exp2:exp = exp2

# unary_operator

class Complement(unary_operator):
    def __init__(self):
        pass

class Negate(unary_operator):
    def __init__(self):
        pass

# binary_operator

class Add(binary_operator):
    def __init__(self):
        pass

class Subtract(binary_operator):
    def __init__(self):
        pass

class Multiply(binary_operator):
    def __init__(self):
        pass

class Divide(binary_operator):
    def __init__(self):
        pass

class Remainder(binary_operator):
    def __init__(self):
        pass

class BitwiseAnd(binary_operator):
    def __init__(self):
        pass

class BitwiseOr(binary_operator):
    def __init__(self):
        pass

class BitwiseXor(binary_operator):
    def __init__(self):
        pass

class LeftShift(binary_operator):
    def __init__(self):
        pass

class RightShift(binary_operator):
    def __init__(self):
        pass

# --- END CLASS DEFINITION

def peek_token(tokens, delete_it) -> Tuple[Lexer_Token, str]:
    if len(tokens) == 0:
        msg = 'peek_token: tokens list is empty'
        error(msg)
    ret = tokens[0]
    if delete_it: # the only place 'tokens' is modified
        tokens.pop(0) # remove first element. 
    return ret 

def expect(expected, tokens) -> None:
    type_, str_ = peek_token(tokens, delete_it=True) # check first element
    if type_ != expected:
        msg = f'expect: Unexpected token. Expected: {expected}, Found: {type_} :: {str_}'
        error(msg)

def parse_int(tokens) -> integer:
    type_, int_ = peek_token(tokens, delete_it=True) # (token_type, *literal*)
    if type_ != Lexer_Token.INTEGER:
        msg = f'parse_int: expected integer, found {type_}'
        error(msg)
    return integer(int_)

def parse_identifier(tokens) -> identifier:
    type_, str_ = peek_token(tokens, delete_it=True) # (token_type, *literal*)
    if type_ != Lexer_Token.IDENTIFIER:
        msg = f'parse_identifier: expected identifier, found {type_}'
        error(msg)
    return identifier(str_)

def parse_program(tokens) -> program:
    fd:function_definition = parse_function(tokens)
    if len(tokens) > 0:
        msg = 'parse_program: tokens remaining in program'
        error(msg)
    return Program(fd)

def parse_function(tokens) -> function_definition:
    expect(Lexer_Token.RESERVED_INT, tokens)        # int
    name:identifier = parse_identifier(tokens) # <identifier>
    expect(Lexer_Token.BRACKET_OPEN, tokens)   # (
    expect(Lexer_Token.RESERVED_VOID, tokens)  # void
    expect(Lexer_Token.BRACKET_CLOSE, tokens)  # )
    expect(Lexer_Token.BRACE_OPEN, tokens)     # {
    body:statement = parse_statement(tokens)   # <statement>
    expect(Lexer_Token.BRACE_CLOSE, tokens)    # }
    return Function(name, body)

def parse_statement(tokens) -> statement:
    expect(Lexer_Token.RESERVED_RETURN, tokens) # return
    exp_:exp = parse_exp(tokens)                # <exp>
    expect(Lexer_Token.SEMICOLON, tokens)       # ;
    return Return(exp_)

def parse_unary_operator(tokens) -> unary_operator:
    type_, str_ = peek_token(tokens, delete_it=True)
    # hyphen / negate: "-"
    if type_ == Lexer_Token.HYPHEN:
        return Negate()
    # tilde / complement: "~"
    elif type_ == Lexer_Token.TILDE:
        return Complement()
    else:
        msg = f'parse_unary_operator: unknown type "{type_}"'
        error(msg)

def parse_binary_operator(tokens) -> binary_operator:
    type_, str_ = peek_token(tokens, delete_it=True)
    match type_:
        case Lexer_Token.PLUS_SIGN:
            return Add()
        case Lexer_Token.ASTERISK:
            return Multiply()
        case Lexer_Token.FORWARD_SLASH:
            return Divide()
        case Lexer_Token.HYPHEN:
            return Subtract()
        case Lexer_Token.PERCENT_SIGN:
            return Remainder()
        case Lexer_Token.AMPERSAND:
            return BitwiseAnd()
        case Lexer_Token.PIPE:
            return BitwiseOr() 
        case Lexer_Token.CARET:
            return BitwiseXor()
        case Lexer_Token.LEFT_SHIFT:
            return LeftShift()
        case Lexer_Token.RIGHT_SHIFT:
            return RightShift()
        case _:
            msg = f'parse_binary_operator: unknown type "{type_}"'
            error(msg)

def parse_factor(tokens) -> exp:
    type_, str_ = peek_token(tokens, delete_it=False) # peek, don't remove yet as we are choosing 
    # integer
    if type_ == Lexer_Token.INTEGER:
        int_:integer = parse_int(tokens)
        return Constant(int_)
    # unary operator 
    elif type_ in [Lexer_Token.HYPHEN, Lexer_Token.TILDE]: # unary op lexemes
        un_op:unary_operator = parse_unary_operator(tokens)
        exp_ :exp            = parse_factor(tokens)
        return Unary(un_op, exp_)
    # brackets 
    elif type_ == Lexer_Token.BRACKET_OPEN:
        expect(Lexer_Token.BRACKET_OPEN, tokens)  # (
        exp_:exp = parse_exp(tokens)              # <exp>
        expect(Lexer_Token.BRACKET_CLOSE, tokens) # )
        return exp_ # book says compiler should not care whether exp is in brackets
    else:
        msg = f'parse_factor: unknown type "{type_}"'
        error(msg)

def _is_binary_op(type_:Lexer_Token) -> bool:
    if type_ in [Lexer_Token.HYPHEN, 
                 Lexer_Token.PLUS_SIGN, 
                 Lexer_Token.ASTERISK, 
                 Lexer_Token.FORWARD_SLASH, 
                 Lexer_Token.PERCENT_SIGN,
                 Lexer_Token.AMPERSAND,
                 Lexer_Token.PIPE,
                 Lexer_Token.CARET,
                 Lexer_Token.LEFT_SHIFT,
                 Lexer_Token.RIGHT_SHIFT,     
                 ]:
        return True
    else:
        return False

_precedence_level = { # https://en.cppreference.com/w/c/language/operator_precedence
    Lexer_Token.HYPHEN        : 15 -  4,
    Lexer_Token.PLUS_SIGN     : 15 -  4,
    Lexer_Token.ASTERISK      : 15 -  3,
    Lexer_Token.FORWARD_SLASH : 15 -  3,
    Lexer_Token.PERCENT_SIGN  : 15 -  3,
    Lexer_Token.AMPERSAND     : 15 -  8,
    Lexer_Token.PIPE          : 15 - 10,
    Lexer_Token.CARET         : 15 -  9,
    Lexer_Token.LEFT_SHIFT    : 15 -  5,
    Lexer_Token.RIGHT_SHIFT   : 15 -  5,  
} 

def parse_exp(tokens, min_prec=0) -> exp:
    left:exp = parse_factor(tokens)
    type_, str_ = peek_token(tokens, delete_it=False) 
    # greater than so that recursive call can create subexpressions
    #   with higher precedence operators
    # equal so that the loop can continue to gather expressions with 
    #   equal precedence like 1 + 2 + 3 ... into left-associative tree
    while _is_binary_op(type_) and (_precedence_level[type_] >= min_prec):
        operator : binary_operator = parse_binary_operator(tokens)
        # is there a higher precedence sub expression? ex: 1 + 2*3
        right    : exp             = parse_exp(tokens, _precedence_level[type_] + 1) 
        left     : exp             = Binary(operator, left, right)
        # the token list is modified by the above parse calls
        type_, str_ = peek_token(tokens, delete_it=False) 
    # higher-precedence sub-expressions will be deeper in the tree
    #   tacky creates instructions depth-first, so hi-prec will be evaluated first
    # RHS wont include operatros with same precedence level 
    #   so each RHS is one factor -> tree is left-associative 
    return left 


def pretty_print(node:AstNode, depth=0) -> None:
    match node:
        case identifier(str_=str_,):
            print(depth*" " + f"identifier({str_})")
        case integer(int_=int_,):
            print(depth*" " + f"integer({int_})")
        case Program(fd=fd,):
            print(depth*" " + "Program")
            pretty_print(fd, depth+4)
        case Function(name=name,body=body,):
            print(depth*" " + "Function")
            pretty_print(name, depth+4)
            pretty_print(body, depth+4)
        case Return(exp_=exp_,):
            print(depth*" " + "Return")
            pretty_print(exp_, depth+4)
        case Constant(integer_=integer_,):
            print(depth*" " + "Constant")
            pretty_print(integer_, depth+4)
        case Unary(unary_operator_=unary_operator_,exp_=exp_,):
            print(depth*" " + "Unary")
            pretty_print(unary_operator_, depth+4)
            pretty_print(exp_, depth+4)
        case Binary(binary_operator_=binary_operator_,exp1=exp1,exp2=exp2,):
            print(depth*" " + "Binary")
            pretty_print(binary_operator_, depth+4)
            pretty_print(exp1, depth+4)
            pretty_print(exp2, depth+4)
        case Complement():
            print(depth*" " + "Complement")
        case Negate():
            print(depth*" " + "Negate")
        case Add():
            print(depth*" " + "Add")
        case Subtract():
            print(depth*" " + "Subtract")
        case Multiply():
            print(depth*" " + "Multiply")
        case Divide():
            print(depth*" " + "Divide")
        case Remainder():
            print(depth*" " + "Remainder")
        case BitwiseAnd():
            print(depth*" " + "BitwiseAnd")
        case BitwiseOr():
            print(depth*" " + "BitwiseOr")
        case BitwiseXor():
            print(depth*" " + "BitwiseXor")
        case LeftShift():
            print(depth*" " + "LeftShift")
        case RightShift():
            print(depth*" " + "RightShift")
        case _:
            global e 
            e = node
            _type = type(node)
            msg = f'pretty_print: Unknown type: {_type}'
            error(msg)



# # automatically generate pretty print function
# # -----------------------------------------------------------------------------
# from zzz_pretty_printer_generator import file_2_pp
# pp = file_2_pp(__file__)
# pp = pp.replace('_IN_TYPE_', 'AstNode')
# print(pp)




if __name__ == "__main__":

    l = lexer()
    my_exit_code = l.lex(source_)
    l.print()

    ast = parse_program(tokens = l.tokens)
    pretty_print(ast)


