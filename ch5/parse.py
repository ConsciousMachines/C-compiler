

from typing import List, Tuple, Optional
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

class assignment_operator(AstNode):
    pass

class declaration(AstNode):
    pass

class block_item(AstNode):
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
    def __init__(self, name:identifier, body:List[block_item]):
        self.name:identifier = name 
        self.body:List[block_item] = body

# statement

class Return(statement):
    def __init__(self, exp_:exp):
        self.exp_:exp = exp_

class Expression(statement):
    def __init__(self, exp_:exp):
        self.exp_:exp = exp_

class Null(statement):
    def __init__(self):
        pass

# declaration

class Declaration(declaration):
    def __init__(self, name:identifier, init:Optional[exp] = None):
        self.name:identifier = name
        self.init:exp = init

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

class Var(exp):
    def __init__(self, ident:identifier):
        self.ident:identifier = ident

class Assignment(exp):
    def __init__(self, kind:Optional[assignment_operator], exp1:exp, exp2:exp):
        self.kind:assignment_operator = kind
        self.exp1:exp = exp1
        self.exp2:exp = exp2

# unary_operator

class Complement(unary_operator):
    def __init__(self):
        pass

class Negate(unary_operator):
    def __init__(self):
        pass

class Not(unary_operator):
    def __init__(self):
        pass

class Increment(unary_operator):
    def __init__(self):
        pass

class Decrement(unary_operator):
    def __init__(self):
        pass

class IncrementPost(unary_operator):
    def __init__(self):
        pass

class DecrementPost(unary_operator):
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

class And(binary_operator):
    def __init__(self):
        pass

class Or(binary_operator):
    def __init__(self):
        pass

class Equal(binary_operator):
    def __init__(self):
        pass

class NotEqual(binary_operator):
    def __init__(self):
        pass

class LessThan(binary_operator):
    def __init__(self):
        pass

class LessOrEqual(binary_operator):
    def __init__(self):
        pass

class GreaterThan(binary_operator):
    def __init__(self):
        pass

class GreaterOrEqual(binary_operator):
    def __init__(self):
        pass

# assignment_operator

class RegularAssignment(assignment_operator):
    def __init__(self):
        pass

class CompoundAssPlusEq(assignment_operator):
    def __init__(self):
        pass

class CompoundAssMinusEq(assignment_operator):
    def __init__(self):
        pass

class CompoundAssMultEq(assignment_operator):
    def __init__(self):
        pass

class CompoundAssDivEq(assignment_operator):
    def __init__(self):
        pass

class CompoundAssModEq(assignment_operator):
    def __init__(self):
        pass

class CompoundAssAndEq(assignment_operator):
    def __init__(self):
        pass

class CompoundAssOrEq(assignment_operator):
    def __init__(self):
        pass

class CompoundAssXorEq(assignment_operator):
    def __init__(self):
        pass

class CompoundAssShlEq(assignment_operator):
    def __init__(self):
        pass

class CompoundAssShrEq(assignment_operator):
    def __init__(self):
        pass


# block_item

class S(block_item):
    def __init__(self, stmnt:statement):
        self.stmnt:statement = stmnt

class D(block_item):
    def __init__(self, decl:declaration):
        self.decl:declaration = decl

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
    fd:function_definition = parse_function_definition(tokens)
    if len(tokens) > 0:
        msg = 'parse_program: tokens remaining after parsing finished'
        error(msg)
    return Program(fd)

def parse_function_definition(tokens) -> function_definition:
    expect(Lexer_Token.RESERVED_INT, tokens)   # int
    name:identifier = parse_identifier(tokens) # <identifier>
    expect(Lexer_Token.BRACKET_OPEN, tokens)   # (
    expect(Lexer_Token.RESERVED_VOID, tokens)  # void
    expect(Lexer_Token.BRACKET_CLOSE, tokens)  # )
    expect(Lexer_Token.BRACE_OPEN, tokens)     # {

    function_body:List[block_item] = []
    while True:
        type_, str_ = peek_token(tokens, delete_it=False)
        if type_ != Lexer_Token.BRACE_CLOSE: # }
            next_block_item:block_item = parse_block_item(tokens)
            function_body.append(next_block_item)
        else:
            expect(Lexer_Token.BRACE_CLOSE, tokens)    # }
            break
    return Function(name, function_body)

def parse_block_item(tokens) -> block_item:
    type_, str_ = peek_token(tokens, delete_it=False)
    # if INT, it's a declaration
    if type_ == Lexer_Token.RESERVED_INT:
        decl:declaration = parse_declaration(tokens)
        return D(decl)
    # otherwise, it's a statement
    else:
        stmnt:statement = parse_statement(tokens)
        return S(stmnt)

def parse_declaration(tokens) -> declaration:
    expect(Lexer_Token.RESERVED_INT, tokens) # int
    ident:identifier = parse_identifier(tokens)
    # if next token is "=", there is initializer, if ";", then no
    type_, str_ = peek_token(tokens, delete_it=False)
    if type_ == Lexer_Token.EQUALS_SIGN:
        expect(Lexer_Token.EQUALS_SIGN, tokens) # = 
        exp_:exp = parse_exp(tokens)            # <exp> 
        expect(Lexer_Token.SEMICOLON, tokens)   # ;
        return Declaration(ident, exp_)
    else:
        expect(Lexer_Token.SEMICOLON, tokens)   # ;
        return Declaration(ident, None)

def parse_statement(tokens) -> statement:
    type_, str_ = peek_token(tokens, delete_it=False)
    # if ";" -> NULL
    if type_ == Lexer_Token.SEMICOLON:
        expect(Lexer_Token.SEMICOLON, tokens)       # ;
        return Null()
    # if "return" -> return
    if type_ == Lexer_Token.RESERVED_RETURN:
        expect(Lexer_Token.RESERVED_RETURN, tokens) # return
        exp_:exp = parse_exp(tokens)                # <exp>
        expect(Lexer_Token.SEMICOLON, tokens)       # ;
        return Return(exp_)
    # else, expression-statement
    else:
        exp_:exp = parse_exp(tokens)                # <exp>
        expect(Lexer_Token.SEMICOLON, tokens)       # ;
        return Expression(exp_)

def parse_unary_operator(tokens) -> unary_operator:
    type_, str_ = peek_token(tokens, delete_it=True)
    return _UnaryLexerToken_to_AstNode[type_]()

def parse_binary_operator(tokens) -> binary_operator:
    type_, str_ = peek_token(tokens, delete_it=True)
    return _BinaryLexerToken_to_AstNode[type_]()

def parse_unary_operator_POSTFIX(tokens) -> unary_operator:
    type_, str_ = peek_token(tokens, delete_it=True)
    return _PostfixUnaryLexerToken_to_AstNode[type_]()


def try_parse_postfix(left:exp, tokens) -> exp:
    # all RHS unary ops have highest prec, all LHS have second highest
    #   LHS ops are collected in a right-assoc way using recursion in parse_factor
    #   RHS ops are collected in a left-assoc way using a loop (same prec-climb algo)
    type_, str_ = peek_token(tokens, delete_it=False) 
    while (type_ in _postfix_unary_operators):
        operator : unary_operator  = parse_unary_operator_POSTFIX(tokens)
        left     : exp             = Unary(operator, left)
        type_, str_ = peek_token(tokens, delete_it=False) 
    return left 

def parse_factor(tokens) -> exp:
    type_, str_ = peek_token(tokens, delete_it=False) # peek, don't remove yet as we are choosing 
    # integer
    if type_ == Lexer_Token.INTEGER:
        int_:integer = parse_int(tokens)
        ret_ = Constant(int_)
    # variable / identifier
    elif type_ == Lexer_Token.IDENTIFIER:
        ident:identifier = parse_identifier(tokens)
        ret_ = Var(ident)
    # unary operator 
    elif type_ in _unary_operators: # unary op lexemes
        un_op:unary_operator = parse_unary_operator(tokens)
        exp_ :exp            = parse_factor(tokens)
        ret_ = Unary(un_op, exp_)
    # brackets 
    elif type_ == Lexer_Token.BRACKET_OPEN:
        expect(Lexer_Token.BRACKET_OPEN, tokens)  # (
        exp_:exp = parse_exp(tokens)              # <exp>
        expect(Lexer_Token.BRACKET_CLOSE, tokens) # )
        ret_ = exp_ # book says compiler should not care whether exp is inside brackets
    else:
        msg = f'parse_factor: unknown type "{type_}"'
        error(msg)
    # check for any postfix operators 
    return try_parse_postfix(ret_, tokens)



def parse_exp(tokens, min_prec=0) -> exp:
    left:exp = parse_factor(tokens)
    type_, str_ = peek_token(tokens, delete_it=False) 
    # greater than so that recursive call can create subexpressions
    #   with higher precedence operators
    # equal so that the loop can continue to gather expressions with 
    #   equal precedence like 1 + 2 + 3 ... into left-associative tree
    while (type_ in _binary_operators) and (_precedence_level[type_] >= min_prec):
        if type_ in _RightAssociativeBinaryOperators:
            expect(type_, tokens)
            right:exp = parse_exp(tokens, _precedence_level[type_])
            kind:assignment_operator = _BinaryLexerToken_to_AstNode[type_]()
            left:exp = Assignment(kind, left, right)
        else:
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

_RightAssociativeBinaryOperators = [
    Lexer_Token.EQUALS_SIGN,
    Lexer_Token.COMPOUND_ASSIGNMENT_PLUS_EQ,
    Lexer_Token.COMPOUND_ASSIGNMENT_MINUS_EQ,
    Lexer_Token.COMPOUND_ASSIGNMENT_MULT_EQ,
    Lexer_Token.COMPOUND_ASSIGNMENT_DIV_EQ,
    Lexer_Token.COMPOUND_ASSIGNMENT_MOD_EQ,
    Lexer_Token.COMPOUND_ASSIGNMENT_AND_EQ,
    Lexer_Token.COMPOUND_ASSIGNMENT_OR_EQ,
    Lexer_Token.COMPOUND_ASSIGNMENT_XOR_EQ,
    Lexer_Token.COMPOUND_ASSIGNMENT_SHL_EQ,
    Lexer_Token.COMPOUND_ASSIGNMENT_SHR_EQ,
]

_postfix_unary_operators = [
    Lexer_Token.INCREMENT,
    Lexer_Token.DECREMENT,   
]

_unary_operators = [
    Lexer_Token.HYPHEN, 
    Lexer_Token.TILDE,
    Lexer_Token.EXCLAMATION,
    Lexer_Token.INCREMENT,
    Lexer_Token.DECREMENT,
]

_binary_operators = [
    Lexer_Token.HYPHEN, 
    Lexer_Token.PLUS_SIGN, 
    Lexer_Token.ASTERISK, 
    Lexer_Token.FORWARD_SLASH, 
    Lexer_Token.PERCENT_SIGN,
    Lexer_Token.AMPERSAND,
    Lexer_Token.PIPE,
    Lexer_Token.CARET,
    Lexer_Token.LEFT_SHIFT,
    Lexer_Token.RIGHT_SHIFT,     
    Lexer_Token.LESS_THAN,
    Lexer_Token.GREATER_THAN,
    Lexer_Token.LOGICAL_AND,
    Lexer_Token.LOGICAL_OR,
    Lexer_Token.EQUAL_TO,
    Lexer_Token.NOT_EQUAL_TO,
    Lexer_Token.LESS_THAN_OR_EQUAL_TO,
    Lexer_Token.GREATER_THAN_OR_EQUAL_TO,
    Lexer_Token.EQUALS_SIGN,
    Lexer_Token.COMPOUND_ASSIGNMENT_PLUS_EQ,
    Lexer_Token.COMPOUND_ASSIGNMENT_MINUS_EQ,
    Lexer_Token.COMPOUND_ASSIGNMENT_MULT_EQ,
    Lexer_Token.COMPOUND_ASSIGNMENT_DIV_EQ,
    Lexer_Token.COMPOUND_ASSIGNMENT_MOD_EQ,
    Lexer_Token.COMPOUND_ASSIGNMENT_AND_EQ,
    Lexer_Token.COMPOUND_ASSIGNMENT_OR_EQ,
    Lexer_Token.COMPOUND_ASSIGNMENT_XOR_EQ,
    Lexer_Token.COMPOUND_ASSIGNMENT_SHL_EQ,
    Lexer_Token.COMPOUND_ASSIGNMENT_SHR_EQ,
]

_precedence_level = { # https://en.cppreference.com/w/c/language/operator_precedence
    Lexer_Token.HYPHEN                      : 15 - 4,
    Lexer_Token.PLUS_SIGN                   : 15 - 4,
    Lexer_Token.ASTERISK                    : 15 - 3,
    Lexer_Token.FORWARD_SLASH               : 15 - 3,
    Lexer_Token.PERCENT_SIGN                : 15 - 3,
    Lexer_Token.AMPERSAND                   : 15 - 8,
    Lexer_Token.PIPE                        : 15 - 10,
    Lexer_Token.CARET                       : 15 - 9,
    Lexer_Token.LEFT_SHIFT                  : 15 - 5,
    Lexer_Token.RIGHT_SHIFT                 : 15 - 5,
    Lexer_Token.LESS_THAN                   : 15 - 6,
    Lexer_Token.GREATER_THAN                : 15 - 6,
    Lexer_Token.LOGICAL_AND                 : 15 - 11,
    Lexer_Token.LOGICAL_OR                  : 15 - 12,
    Lexer_Token.EQUAL_TO                    : 15 - 7,
    Lexer_Token.NOT_EQUAL_TO                : 15 - 7,
    Lexer_Token.LESS_THAN_OR_EQUAL_TO       : 15 - 6,
    Lexer_Token.GREATER_THAN_OR_EQUAL_TO    : 15 - 6,
    Lexer_Token.EQUALS_SIGN                 : 15 - 14,
    Lexer_Token.COMPOUND_ASSIGNMENT_PLUS_EQ : 15 - 14,
    Lexer_Token.COMPOUND_ASSIGNMENT_MINUS_EQ: 15 - 14,
    Lexer_Token.COMPOUND_ASSIGNMENT_MULT_EQ : 15 - 14,
    Lexer_Token.COMPOUND_ASSIGNMENT_DIV_EQ  : 15 - 14,
    Lexer_Token.COMPOUND_ASSIGNMENT_MOD_EQ  : 15 - 14,
    Lexer_Token.COMPOUND_ASSIGNMENT_AND_EQ  : 15 - 14,
    Lexer_Token.COMPOUND_ASSIGNMENT_OR_EQ   : 15 - 14,
    Lexer_Token.COMPOUND_ASSIGNMENT_XOR_EQ  : 15 - 14,
    Lexer_Token.COMPOUND_ASSIGNMENT_SHL_EQ  : 15 - 14,
    Lexer_Token.COMPOUND_ASSIGNMENT_SHR_EQ  : 15 - 14,
} 

_PostfixUnaryLexerToken_to_AstNode = {
    Lexer_Token.INCREMENT       : IncrementPost,   # ++
    Lexer_Token.DECREMENT       : DecrementPost,   # --
}

_UnaryLexerToken_to_AstNode = {
    Lexer_Token.HYPHEN          : Negate,      # - hyphen / negate
    Lexer_Token.TILDE           : Complement,  # ~ tilde / complement
    Lexer_Token.EXCLAMATION     : Not,         # ! logical not
    Lexer_Token.INCREMENT       : Increment,   # ++
    Lexer_Token.DECREMENT       : Decrement,   # --
}

_BinaryLexerToken_to_AstNode = {
    Lexer_Token.PLUS_SIGN                   : Add,                # +
    Lexer_Token.ASTERISK                    : Multiply,           # *
    Lexer_Token.FORWARD_SLASH               : Divide,             # /
    Lexer_Token.HYPHEN                      : Subtract,           # -
    Lexer_Token.PERCENT_SIGN                : Remainder,          # %
    Lexer_Token.AMPERSAND                   : BitwiseAnd,         # &
    Lexer_Token.PIPE                        : BitwiseOr,          # |
    Lexer_Token.CARET                       : BitwiseXor,         # ^
    Lexer_Token.LEFT_SHIFT                  : LeftShift,          # <<
    Lexer_Token.RIGHT_SHIFT                 : RightShift,         # >>
    Lexer_Token.LOGICAL_AND                 : And,                # &&
    Lexer_Token.LOGICAL_OR                  : Or,                 # ||
    Lexer_Token.EQUAL_TO                    : Equal,              # ==
    Lexer_Token.NOT_EQUAL_TO                : NotEqual,           # !=
    Lexer_Token.LESS_THAN_OR_EQUAL_TO       : LessOrEqual,        # <=
    Lexer_Token.GREATER_THAN_OR_EQUAL_TO    : GreaterOrEqual,     # >=
    Lexer_Token.LESS_THAN                   : LessThan,           # <
    Lexer_Token.GREATER_THAN                : GreaterThan,        # >
    Lexer_Token.EQUALS_SIGN                 : RegularAssignment,  # =
    Lexer_Token.COMPOUND_ASSIGNMENT_PLUS_EQ : CompoundAssPlusEq,  # += 
    Lexer_Token.COMPOUND_ASSIGNMENT_MINUS_EQ: CompoundAssMinusEq, # -=
    Lexer_Token.COMPOUND_ASSIGNMENT_MULT_EQ : CompoundAssMultEq,  # *=
    Lexer_Token.COMPOUND_ASSIGNMENT_DIV_EQ  : CompoundAssDivEq,
    Lexer_Token.COMPOUND_ASSIGNMENT_MOD_EQ  : CompoundAssModEq,
    Lexer_Token.COMPOUND_ASSIGNMENT_AND_EQ  : CompoundAssAndEq,
    Lexer_Token.COMPOUND_ASSIGNMENT_OR_EQ   : CompoundAssOrEq,
    Lexer_Token.COMPOUND_ASSIGNMENT_XOR_EQ  : CompoundAssXorEq,
    Lexer_Token.COMPOUND_ASSIGNMENT_SHL_EQ  : CompoundAssShlEq,
    Lexer_Token.COMPOUND_ASSIGNMENT_SHR_EQ  : CompoundAssShrEq,
}



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
            for i in body: # body:List[]
                pretty_print(i, depth+4)
        case Return(exp_=exp_,):
            print(depth*" " + "Return")
            pretty_print(exp_, depth+4)
        case Expression(exp_=exp_,):
            print(depth*" " + "Expression")
            pretty_print(exp_, depth+4)
        case Null():
            print(depth*" " + "Null")
        case Declaration(name=name,init=init,):
            print(depth*" " + "Declaration")
            pretty_print(name, depth+4)
            pretty_print(init, depth+4)
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
        case Var(ident=ident,):
            print(depth*" " + "Var")
            pretty_print(ident, depth+4)
        case Assignment(kind=kind,exp1=exp1,exp2=exp2,):
            print(depth*" " + "Assignment")
            pretty_print(kind, depth+4)
            pretty_print(exp1, depth+4)
            pretty_print(exp2, depth+4)
        case Complement():
            print(depth*" " + "Complement")
        case Negate():
            print(depth*" " + "Negate")
        case Not():
            print(depth*" " + "Not")
        case Increment():
            print(depth*" " + "Increment")
        case Decrement():
            print(depth*" " + "Decrement")
        case IncrementPost():
            print(depth*" " + "IncrementPost")
        case DecrementPost():
            print(depth*" " + "DecrementPost")
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
        case And():
            print(depth*" " + "And")
        case Or():
            print(depth*" " + "Or")
        case Equal():
            print(depth*" " + "Equal")
        case NotEqual():
            print(depth*" " + "NotEqual")
        case LessThan():
            print(depth*" " + "LessThan")
        case LessOrEqual():
            print(depth*" " + "LessOrEqual")
        case GreaterThan():
            print(depth*" " + "GreaterThan")
        case GreaterOrEqual():
            print(depth*" " + "GreaterOrEqual")
        case RegularAssignment():
            print(depth*" " + "RegularAssignment")
        case CompoundAssPlusEq():
            print(depth*" " + "CompoundAssPlusEq")
        case CompoundAssMinusEq():
            print(depth*" " + "CompoundAssMinusEq")
        case CompoundAssMultEq():
            print(depth*" " + "CompoundAssMultEq")
        case CompoundAssDivEq():
            print(depth*" " + "CompoundAssDivEq")
        case CompoundAssModEq():
            print(depth*" " + "CompoundAssModEq")
        case CompoundAssAndEq():
            print(depth*" " + "CompoundAssAndEq")
        case CompoundAssOrEq():
            print(depth*" " + "CompoundAssOrEq")
        case CompoundAssXorEq():
            print(depth*" " + "CompoundAssXorEq")
        case CompoundAssShlEq():
            print(depth*" " + "CompoundAssShlEq")
        case CompoundAssShrEq():
            print(depth*" " + "CompoundAssShrEq")
        case S(stmnt=stmnt,):
            print(depth*" " + "S")
            pretty_print(stmnt, depth+4)
        case D(decl=decl,):
            print(depth*" " + "D")
            pretty_print(decl, depth+4)
        case _:
            global e 
            e = node
            _type = type(node)
            msg = f'pretty_print: Unknown type: {_type}'
            error(msg)



def resolve(node:AstNode, variable_map:dict) -> AstNode:
    match node:
        case Declaration(name=name,init=init,):
            if name.str_ in variable_map.keys():
                msg = f'resolve: Declaration: duplicate variable declaration: {name.str_}'
                error(msg)
            unique_name:str = f'{name.str_}.{make_temporary()}'
            variable_map[name.str_] = identifier(unique_name)
            if init is not None:
                init = resolve(init, variable_map) 
            return Declaration(variable_map[name.str_], init)
        case Var(ident=ident):
            if ident.str_ in variable_map.keys():
                return Var(variable_map[ident.str_])
            else:
                msg = f'resolve: Var: undeclared variable: {ident.str_}'
                error(msg)
        case Assignment(kind=kind, exp1=exp1, exp2=exp2):
            if type(exp1) != Var:
                msg = f'resolve: Assignment: invalid lvalue: {type(exp1)}'
                error(msg)
            return Assignment(kind, resolve(exp1, variable_map), resolve(exp2, variable_map))
        # everything else is just recursive
        case Return(exp_=exp_):
            return Return(resolve(exp_, variable_map))
        case Expression(exp_=exp_):
            return Expression(resolve(exp_, variable_map))
        case identifier(str_=str_,):
            return identifier(str_)
        case integer(int_=int_,):
            return integer(int_)
        case Program(fd=fd,):
            x0 = resolve(fd, variable_map)
            return Program(x0)
        case Function(name=name,body=body,):
            x0 = resolve(name, variable_map)
            x1 = [resolve(i, variable_map) for i in body]
            return Function(x0,x1)
        case Null():
            return Null()
        case Constant(integer_=integer_,):
            x0 = resolve(integer_, variable_map)
            return Constant(x0)
        case Unary(unary_operator_=unary_operator_,exp_=exp_,):
            if (type(unary_operator_) in [Increment,IncrementPost,Decrement,DecrementPost]):
                if (type(exp_) != Var):
                    msg = f'resolve: Unary: invalid lvalue: {type(exp_)}'
                    error(msg)
            x0 = resolve(unary_operator_, variable_map)
            x1 = resolve(exp_, variable_map)
            return Unary(x0,x1)
        case Binary(binary_operator_=binary_operator_,exp1=exp1,exp2=exp2,):
            x0 = resolve(binary_operator_, variable_map)
            x1 = resolve(exp1, variable_map)
            x2 = resolve(exp2, variable_map)
            return Binary(x0,x1,x2)
        case Complement():
            return Complement()
        case Negate():
            return Negate()
        case Not():
            return Not()
        case Add():
            return Add()
        case Subtract():
            return Subtract()
        case Multiply():
            return Multiply()
        case Divide():
            return Divide()
        case Remainder():
            return Remainder()
        case BitwiseAnd():
            return BitwiseAnd()
        case BitwiseOr():
            return BitwiseOr()
        case BitwiseXor():
            return BitwiseXor()
        case LeftShift():
            return LeftShift()
        case RightShift():
            return RightShift()
        case And():
            return And()
        case Or():
            return Or()
        case Equal():
            return Equal()
        case NotEqual():
            return NotEqual()
        case LessThan():
            return LessThan()
        case LessOrEqual():
            return LessOrEqual()
        case GreaterThan():
            return GreaterThan()
        case GreaterOrEqual():
            return GreaterOrEqual()
        case S(stmnt=stmnt,):
            x0 = resolve(stmnt, variable_map)
            return S(x0)
        case D(decl=decl,):
            x0 = resolve(decl, variable_map)
            return D(x0)
        case Increment():
            return Increment()
        case Decrement():
            return Decrement()
        case IncrementPost():
            return IncrementPost()
        case DecrementPost():
            return DecrementPost()
        case _:
            global e 
            e = node
            _type = type(node)
            msg = f'resolve: Unknown type: {_type}'
            error(msg)


    
# # automatically generate pretty print function
# # -----------------------------------------------------------------------------
# from zzz_pretty_printer_generator import file_2_pp
# pp = file_2_pp(__file__)
# pp = pp.replace('_IN_TYPE_', 'AstNode')
# print(pp)


# # automatically generate replace_pseud
# # -----------------------------------------------------------------------------
# from zzz_pretty_printer_generator import file_2_recurse
# recurse = file_2_recurse(__file__)
# recurse = recurse.replace('recurse', 'resolve')
# recurse = recurse.replace('_IN_TYPE_', 'exp')
# recurse = recurse.replace('_OUT_TYPE_', 'exp')
# print(recurse)


if __name__ == "__main__":
    l = lexer()
    my_exit_code = l.lex(source_)
    l.print()
    ast = parse_program(tokens = l.tokens)
    pretty_print(ast)

    variable_map = {}
    ast2 = resolve(ast, variable_map)
    pretty_print(ast2)



