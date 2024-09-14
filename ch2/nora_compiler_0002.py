#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# # my compiler driver must be command line with 1 argument, the C source
# # produce executable in same directory, same name 
# # terminate w exit code 0
# # if failure, return non-0 exit code

# # options:
# # --lex 
# # --parse: lexer and parser
# # --codegen: stop before code eimssion
# # ^ these dont produce files, but exit with 0 if success
# # -S emit assembly file



# # ---------- R E C U R S I V E   W A L K   G E N E R A T O R
# # exception: integer
# # exception: identifier
# # exception: Function body

# if False: 
        
#     text = '''

#     class cg_identifier(CgNode):
#         def __init__(self, str_:str):
#             self.str_:str = str_ 

#     class cg_integer(CgNode):
#         def __init__(self, int_:int):
#             self.int_:int = int_

#     # cg_program

#     class cg_Program(cg_program):
#         def __init__(self, fd:cg_function_definition):
#             self.fd:cg_function_definition = fd

#     # cg_function_definition

#     class cg_Function(cg_function_definition):
#         def __init__(self, name:cg_identifier, instructions:List[cg_instruction]):
#             self.name:cg_identifier = name 
#             self.instructions:List[cg_instruction] = instructions

#     # cg_instruction

#     class cg_Mov(cg_instruction):
#         def __init__(self, src:cg_operand, dst:cg_operand):
#             self.src:cg_operand = src 
#             self.dst:cg_operand = dst

#     class cg_Unary(cg_instruction):
#         def __init__(self, unop:cg_unary_operator, op:cg_operand):
#             self.unop:cg_unary_operator = unop 
#             self.op:cg_operand = op

#     class cg_AllocateStack(cg_instruction):
#         def __init__(self, integer_:cg_integer):
#             self.integer_:cg_integer = integer_

#     class cg_Ret(cg_instruction):
#         def __init__(self):
#             pass

#     # cg_unary_operator

#     class cg_Neg(cg_unary_operator):
#         def __init__(self):
#             pass

#     class cg_Not(cg_unary_operator):
#         def __init__(self):
#             pass

#     # cg_operand

#     class cg_Imm(cg_operand):
#         def __init__(self, integer_:cg_integer):
#             self.integer_:cg_integer = integer_

#     class cg_Reg(cg_operand):
#         def __init__(self, reg:cg_reg):
#             self.reg:cg_reg = reg

#     class cg_Pseudo(cg_operand):
#         def __init__(self, ident:cg_identifier):
#             self.ident:cg_identifier = ident 

#     class cg_Stack(cg_operand):
#         def __init__(self, integer_:cg_integer):
#             self.integer_:cg_integer = integer_

#     # cg_reg

#     class cg_AX(cg_reg):
#         def __init__(self):
#             pass

#     class cg_R10(cg_reg):
#         def __init__(self):
#             pass

#     '''

#     lines = text.split('\n')

#     i = 0 
#     results = []
#     while i < len(lines):
#         line = lines[i]
#         j = i # use j to check out the lines ahead
#         # state 0: we are in a class definition
#         if line[:5] == 'class':
#             members = []
#             class_name = line[6:].split(':')[0].split('(')[0]
#             # get next line
#             j += 1 
#             line = lines[j]
#             # state 1: we are in def __init__
#             if line.strip()[:12] == 'def __init__':
#                 # collect all the members that start with self.<member>
#                 while True:
#                     # get next line
#                     j += 1        
#                     line = lines[j]
#                     if line[:13] != '        self.':
#                         break
#                     else:
#                         member = line[13:].split('=')[0].split(':')[0]
#                         members.append(member)
#             results.append((class_name, members))
#         i += 1


#     _prologue = '''
#     def recurse(node):
#         match node:'''
#     _epilogue = '''        case _:
#                 global e 
#                 e = node
#                 _type = type(node)
#                 msg = f'Pretty print ASM: Unknown type: {_type}'
#                 raise Exception(msg)
#     '''
#     for i, result in enumerate(results):
#         if i == 0:
#             print(_prologue)
#         class_name = result[0]
#         if '_' in class_name: # remove cg_ prefix
#             _class_name = class_name.split('_')[1]
#         members = result[1]
#         # print(class_name)
#         # for member in members:
#         #     print(f'\t{member}')

#         # print the code
#         _counter.reset()
#         args = ''
#         arguments = []
#         for member in members:
#             args += f'{member}={member},'
#         line1 = f'        case {class_name}({args}):'
#         lines = [line1]
#         for member in members:
#             argument = f'x{make_temporary()}'
#             line = f'            {argument} = recurse({member})'
#             lines.append(line)
#             arguments.append(argument)
#         line_last = f'            return {class_name}({",".join(arguments)})'
#         lines.append(line_last)

#         # exception: identifier / integer types
#         if _class_name in ['identifier', 'integer']:
#             lines = [lines[0]] # keep only the 'case' line
#             line = f'            return {class_name}({members[0]})'
#             lines.append(line)

#         if _class_name in ['Function']:
#             line1 = f'            x1 = [recurse(i) for i in instructions]'
#             _ = lines.pop(-2)
#             lines.insert(-1, line1)

#         for line in lines:
#             print(line)
#         if i == len(results)-1:
#             print(_epilogue)




# # ---------- P R E T T Y   P R I N T E R   G E N E R A T O R
# # exception: integer
# # exception: identifier
# # exception: Function body
# if False:
        
#     text = '''

#     '''

#     lines = text.split('\n')

#     i = 0 
#     results = []
#     while i < len(lines):
#         line = lines[i]
#         j = i # use j to check out the lines ahead
#         # state 0: we are in a class definition
#         if line[:5] == 'class':
#             members = []
#             class_name = line[6:].split(':')[0].split('(')[0]
#             # get next line
#             j += 1 
#             line = lines[j]
#             # state 1: we are in def __init__
#             if line.strip()[:12] == 'def __init__':
#                 # collect all the members that start with self.<member>
#                 while True:
#                     # get next line
#                     j += 1        
#                     line = lines[j]
#                     if line[:13] != '        self.':
#                         break
#                     else:
#                         member = line[13:].split('=')[0].split(':')[0]
#                         members.append(member)
#             results.append((class_name, members))
#         i += 1

#     for result in results:
#         class_name = result[0]
#         if '_' in class_name: # remove cg_ prefix
#             _class_name = class_name.split('_')[1]
#         members = result[1]
#         # print(name)
#         # for member in members:
#         #     print(f'\t{member}')
#         args = ''
#         for member in members:
#             args += f'{member}={member},'
#         line1 = f'        case {class_name}({args}):'
#         line2 = f'            print(depth*" " + "{_class_name}")'
#         lines = [line1, line2]
#         for member in members:
#             line = f'            pretty_print_asm({member}, depth+4)'
#             lines.append(line)
#         for line in lines:
#             print(line)
#     '''

#     '''



# # converting nested expressions into TAC
# if False:

#     class UnaryExpType(Enum):
#         cmp = 1 # bitwise complement
#         neg = 2 # negation 

#     class BinaryExpType(Enum):
#         add = 1
#         xor = 2

#     class SoyExp:
#         pass 

#     class UnaryExp(SoyExp):
#         def __init__(self, type_:UnaryExpType, op:SoyExp):
#             self.type_ = type_ 
#             self.op = op # operand is a nested expression

#     class BinaryExp(SoyExp):
#         def __init__(self, type_:BinaryExpType, op1:SoyExp, op2:SoyExp):
#             self.type_ = type_ 
#             self.op1 = op1 
#             self.op2 = op2

#     class Constant(SoyExp):
#         def __init__(self, int_:int):
#             self.int_ = int_

#     def pretty_print(e:SoyExp, depth=0):
#         match e:
#             case Constant(int_=int_):
#                 print(depth*' ' + f'Const({int_})')
#             case UnaryExp(type_=type_,op=op):
#                 print(depth*' ' + f'Unary({type_})')
#                 pretty_print(op, depth+4)             
#             case BinaryExp(type_=type_,op1=op1,op2=op2):
#                 print(depth*' ' + f'Binary({type_})')
#                 pretty_print(op1, depth+4)             
#                 pretty_print(op2, depth+4)    
#             case _:
#                 raise Exception('unknown type')         

#     class TaExp:
#         pass 

#     class ta_UnaryExp(TaExp):
#         def __init__(self, type_:UnaryExpType, src1:ta_val, dst:ta_val):
#             self.type_ = type_ 
#             self.src1 = src1
#             self.dst = dst

#     class ta_BinaryExp(TaExp):
#         def __init__(self, type_:BinaryExpType, src1:ta_val, src2:ta_val, dst:ta_val):
#             self.type_ = type_ 
#             self.src1 = src1
#             self.src2 = src2
#             self.dst = dst

#     class ta_val:
#         pass 

#     class ta_Constant(ta_val):
#         def __init__(self, int_:int):
#             self.int_ = int_

#     class ta_Variable(ta_val):
#         def __init__(self, s):
#             self.s = s


#     def emit_sacky(e:SoyExp, instrs):
#         match e:

#             case Constant(int_=int_):
#                 return ta_Constant(int_)

#             case UnaryExp(type_=type_,op=op):
#                 src :ta_val  = emit_sacky(op, instrs)
#                 dst          = ta_Variable(f'tmp_{make_temporary()}')
#                 instrs.append(ta_UnaryExp(type_, src, dst))
#                 return dst

#             case BinaryExp(type_=type_,op1=op1,op2=op2):
#                 src1 :ta_val = emit_sacky(op1, instrs)
#                 src2 :ta_val = emit_sacky(op2, instrs)
#                 dst          = ta_Variable(f'tmp_{make_temporary()}')
#                 instrs.append(ta_BinaryExp(type_, src1, src2, dst))
#                 return dst 

#             case _:
#                 raise Exception('unknown type')         

#     def pretty_print_sacky(v, depth=0):
#         match v:
#             case ta_Constant(int_=int_):
#                 print(depth*' ' + f'Const({int_})')
#             case ta_Variable(s=s):
#                 print(depth*' ' + f'Var({s})')
#             case ta_UnaryExp(type_=type_,src1=src1,dst=dst):
#                 print(depth*' ' + f'Unary({type_})')
#                 pretty_print_sacky(src1, depth+4)            
#                 pretty_print_sacky(dst, depth+4)            

#             case ta_BinaryExp(type_=type_,src1=src1,src2=src2,dst=dst):
#                 print(depth*' ' + f'Binary({type_})')
#                 pretty_print_sacky(src1, depth+4)            
#                 pretty_print_sacky(src2, depth+4)            
#                 pretty_print_sacky(dst, depth+4)   
#             case _:
#                 global e 
#                 e = v
#                 raise Exception('unknown type')  

#     def pps2(v):
#         match v:
#             case ta_Constant(int_=int_):
#                 return int_
#             case ta_Variable(s=s):
#                 return s
#             case ta_UnaryExp(type_=type_,src1=src1,dst=dst):
#                 print(f'{type_}\t{pps2(dst)} <- {pps2(src1)}')
#             case ta_BinaryExp(type_=type_,src1=src1,src2=src2,dst=dst):
#                 print(f'{type_}\t{pps2(dst)} <- {pps2(src1)},{pps2(src2)}')
#             case _:
#                 global e 
#                 e = v
#                 raise Exception('unknown type')  

#     _counter.reset()


#     e1 = Constant(5)
#     e2 = UnaryExp(UnaryExpType.cmp, e1)
#     e3 = Constant(420)
#     e4 = BinaryExp(BinaryExpType.add, e2, e3)
#     e5 = Constant(69)
#     e6 = BinaryExp(BinaryExpType.xor, e4, e5)
#     pretty_print(e6)


#     instrs = []
#     emit_sacky(e6, instrs)
#     for i in instrs:
#         pps2(i) # pretty_print_sacky(i)






import subprocess 
import argparse
import sys
import os
from enum import Enum
from typing import List


def preprocess_file(in_name):
    out_name = in_name.replace('.c', '.i')
    args = f'gcc -E -P {in_name} -o {out_name}'.split()
    assert 0 == subprocess.call(args), 'FAILED: pre-process'

def assemble_and_link(file_name):
    args = f'gcc {file_name} -o {file_name[:-2]}'.split()
    assert 0 == subprocess.call(args), 'FAILED: assemble & link'

def read_file(full_path):
    with open(full_path, 'r') as f:
        return f.read()

class counter:
    def __init__(self):
        self.v = 0
    def increment(self):
        ret = self.v
        self.v += 1
        return ret
    def reset(self):
        self.v = 0

def error(msg:str):
    print(msg)
    global my_exit_code
    my_exit_code = 1 
    raise Exception(msg)

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

    # multi-char lexemes
    INTEGER = 6
    IDENTIFIER = 7

    # reserved words 
    RESERVED_INT = 8
    RESERVED_VOID = 9
    RESERVED_RETURN = 10

class lexer:
    def __init__(self):

        self.lexer_single_char_kw = ';{}()-~'
        self.lexer_single_char_kw_tok = [    Lexer_Token.SEMICOLON, 
                                        Lexer_Token.BRACE_OPEN, 
                                        Lexer_Token.BRACE_CLOSE, 
                                        Lexer_Token.BRACKET_OPEN, 
                                        Lexer_Token.BRACKET_CLOSE,
                                        Lexer_Token.HYPHEN,
                                        Lexer_Token.TILDE,]

        # lexer number
        self.lexer_numeric_char = '0123456789'
        # lexer non-number
        self.lexer_non_numeric_char = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789'

        # lexer reserved words
        self.lexer_reserved_words = ['int', 'void', 'return']
        self.lexer_reserved_words_tok = [Lexer_Token.RESERVED_INT, 
                                    Lexer_Token.RESERVED_VOID, 
                                    Lexer_Token.RESERVED_RETURN,]

        # create a word boundary class to check regex word boundary
        word_boundary = []
        for i in range(128):
            c = chr(i)  # convert ASCII to char
            if c.isalnum() or (c == '_'): # skip alpha-numeric
                continue
            word_boundary.append(c)
        self.word_boundary = ''.join(word_boundary)

    # iterate over each character
    def lex(self, program, tokens):
            
        i = 0 
        while i < len(program):

            # get corresponding char
            c = program[i]

            # if character is whitespace, skip it 
            if c in [' ', '\t', '\n']:
                i += 1
                continue

            # if character is single-char keyword, 
            if c in self.lexer_single_char_kw:

                # # EXCEPTION: --, ++
                # if (c == '-') and (program[i+1] == '-'):
                #     # raise NotImplementedError
                #     tokens.append((Lexer_Token.DECREMENT, '--'))
                #     i += 2
                #     continue           

                # get index of the character (corresponding enum value)
                idx = self.lexer_single_char_kw.find(c)

                # return the corresponding token
                tokens.append((self.lexer_single_char_kw_tok[idx], c))

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
                tokens.append((Lexer_Token.INTEGER, substr))

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
                if substr in self.lexer_reserved_words:

                    # get index of the character (corresponding enum value)
                    idx = self.lexer_reserved_words.index(substr)

                    # add it to tokens & lexemes 
                    tokens.append((self.lexer_reserved_words_tok[idx], substr))

                # else, it is an identifier
                else:

                    # add it to tokens & lexemes 
                    tokens.append((Lexer_Token.IDENTIFIER, substr))

                # update current index
                i = j 
                continue 

            print(f'Lexer Error: unexpected character: {c}')
            return 1 # error
                
        return 0

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

# grammar RHS 
# -----------------------------------------------------------------------------

class identifier(AstNode):
    def __init__(self, str_:str):
        self.str_:str = str_ 

class integer(AstNode):
    def __init__(self, int_:int):
        self.int_:int = int_

class Program(program):
    def __init__(self, fd:function_definition):
        self.fd:function_definition = fd

class Function(function_definition):
    def __init__(self, name:identifier, body:statement):
        self.name:identifier = name 
        self.body:statement = body

class Return(statement):
    def __init__(self, exp_:exp):
        self.exp_:exp = exp_

class Constant(exp):
    def __init__(self, integer_:integer):
        self.integer_:integer = integer_

class Unary(exp):
    def __init__(self, unary_operator_:unary_operator, exp_:exp):
        self.unary_operator_:unary_operator = unary_operator_
        self.exp_:exp = exp_

class Complement(unary_operator):
    def __init__(self):
        pass

class Negate(unary_operator):
    def __init__(self):
        pass

def peek_token(tokens):
    if len(tokens) == 0:
        msg = 'peek_token: tokens list is empty'
        error(msg)
    return tokens[0]

def parse_int(tokens):
    type_, int_ = tokens.pop(0) # (token_type, *literal*)
    if type_ != Lexer_Token.INTEGER:
        msg = f'parse_int: expected integer, found {type_}'
        error(msg)
    return integer(int_)

def parse_identifier(tokens):
    type_, str_ = tokens.pop(0) # (token_type, *literal*)
    if type_ != Lexer_Token.IDENTIFIER:
        msg = f'parse_identifier: expected identifier, found {type_}'
        error(msg)
    return identifier(str_)

def parse_unary_operator(tokens):
    curr_type, curr_lexe = tokens.pop(0)
    # hyphen / negate: "-"
    if curr_type == Lexer_Token.HYPHEN:
        return Negate()
    # tilde / complement: "~"
    elif curr_type == Lexer_Token.TILDE:
        return Complement()
    else:
        msg = f'parse_unary_operator: unknown type "{curr_type}" in "parse_unary_operator"'
        error(msg)

def parse_exp(tokens):
    curr_type, curr_lexe = peek_token(tokens) # peek, don't remove yet as we are choosing 
    # integer
    if curr_type == Lexer_Token.INTEGER:
        int_:integer = parse_int(tokens)
        return Constant(int_)
    # unary operator 
    elif curr_type in [Lexer_Token.HYPHEN, Lexer_Token.TILDE]: # unary op lexemes
        un_op:unary_operator = parse_unary_operator(tokens)
        exp_:exp = parse_exp(tokens)
        return Unary(un_op, exp_)
    # brackets 
    elif curr_type == Lexer_Token.BRACKET_OPEN:
        expect('(', tokens)
        exp_:exp = parse_exp(tokens)
        expect(')', tokens)
        return exp_ # book says compiler should not care whether exp is in brackets
    else:
        msg = f'parse_exp: unknown type "{curr_type}" in "parse_exp"'
        error(msg)

def parse_statement(tokens):
    expect('return', tokens)
    exp_:exp = parse_exp(tokens)
    expect(';', tokens)
    return Return(exp_)

def parse_function(tokens):
    expect('int', tokens)
    name:identifier = parse_identifier(tokens)
    expect('(', tokens)
    expect('void', tokens)
    expect(')', tokens)
    expect('{', tokens)
    body:statement = parse_statement(tokens)
    expect('}', tokens)
    return Function(name, body)

def parse_program(tokens):
    fd:function_definition = parse_function(tokens)
    if len(tokens) > 0:
        msg = 'parse_program: tokens remaining in program'
        error(msg)
    return Program(fd)

def expect(expected, tokens):
    type_, actual_ = tokens.pop(0) # take out first element
    if actual_ != expected:
        msg = f'expect: Unexpected token. Expected: {expected}, Found: {actual_}'
        error(msg)

def pretty_print(node, depth=0):
    match node:
        case Unary(unary_operator_=unary_operator_,exp_=exp_):
            print(depth*' ' + 'Unary')
            pretty_print(unary_operator_, depth+4)
            pretty_print(exp_, depth+4)
        case Negate():
            print(depth*' ' + 'Negate')
        case Complement():
            print(depth*' ' + 'Complement')
        case Program(fd=fd):
            print(depth*' ' + 'Program')
            pretty_print(fd, depth+4)
        case Function(name=name, body=body):
            print(depth*' ' + 'Function')
            pretty_print(name, depth+4)
            pretty_print(body, depth+4)
        case Return(exp_=exp_):
            print(depth*' ' + 'Return')
            pretty_print(exp_, depth+4)
        case Constant(integer_=integer_):
            print(depth*' ' + 'Constant')
            pretty_print(integer_, depth+4)
        case identifier(str_=str_):
            print(depth*' ' + f'identifier({str_})')
        case integer(int_=int_):
            print(depth*' ' + f'integer({int_})')
        case _:
            global e 
            e = node
            _type = type(node)
            msg = f'pretty_print: Unknown type: {_type}'
            error(msg)



# - - - T A C K Y   G E N E R A T I O N 
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

# base class
# -----------------------------------------------------------------------------

class TaNode: 
    pass

# grammar LHS
# -----------------------------------------------------------------------------

class ta_program(TaNode):
    pass 

class ta_function_definition(TaNode):
    pass 

class ta_instruction(TaNode):
    pass 

class ta_val(TaNode):
    pass

class ta_unary_operator(TaNode):
    pass 

# grammar RHS 
# -----------------------------------------------------------------------------

class ta_identifier(TaNode):
    def __init__(self, str_:str):
        self.str_:str = str_ 

class ta_integer(TaNode):
    def __init__(self, int_:int):
        self.int_:int = int_

# ta_program

class ta_Program(ta_program):
    def __init__(self, fd:ta_function_definition):
        self.fd:ta_function_definition = fd

# ta_function_definition

class ta_Function(ta_function_definition):
    def __init__(self, name:ta_identifier, body:List[ta_instruction]):
        self.name:ta_identifier        = name 
        self.body:List[ta_instruction] = body

# ta_instruction

class ta_Return(ta_instruction):
    def __init__(self, v:ta_val):
        self.v:ta_val = v

class ta_Unary(ta_instruction):
    def __init__(self, op:ta_unary_operator, src:ta_val, dst:ta_val):
        self.op:ta_unary_operator = op
        self.src:ta_val = src
        self.dst:ta_val = dst

# ta_val

class ta_Constant(ta_val):
    def __init__(self, integer:ta_integer):
        self.integer:ta_integer = integer 

class ta_Var(ta_val):
    def __init__(self, ident:ta_identifier):
        self.ident:ta_identifier = ident 

# ta_unary_operator

class ta_Complement(ta_unary_operator):
    def __init__(self):
        pass

class ta_Negate(ta_unary_operator):
    def __init__(self):
        pass

# NOTE: nested expressions only contain a source. 
#   translating them to TACKY, for each nested expression we generate a new tmp variable. 
#   this is the dst of that expression, becomes the src of the next expression. 

# this takes care of all exp sub-trees
def emit_tacky(e:exp, instructions:List[ta_instruction]) -> ta_val:
    match e:
        case Constant(integer_=integer_):
            ta_int   :ta_integer              = convert_ast(integer_)
            return ta_Constant(ta_int)
        case Unary(unary_operator_=unary_operator_, exp_=exp_):
            src      :ta_val                  = emit_tacky(exp_, instructions)
            dst      :ta_val                  = ta_Var(ta_identifier(f'tmp.{make_temporary()}'))
            tacky_op :ta_unary_operator       = convert_ast(unary_operator_)
            instructions.append(ta_Unary(tacky_op, src, dst))
            return dst

# convert AST nodes (except epr, which have separate function) to Tacky
def convert_ast(node:AstNode):
    match node:
        # same structure
        case identifier(str_=str_):
            return ta_identifier(str_)
        case integer(int_=int_):
            return ta_integer(int_)
        case Negate():
            return ta_Negate()
        case Complement():
            return ta_Complement()
        case Program(fd=fd):
            ta_fd    :ta_function_definition  = convert_ast(fd)
            return ta_Program(ta_fd)
        # for the function, the body *statement* needs to be converted to List[ta_instr]
        case Function(name=name, body=body):
            ta_name  :ta_identifier           = convert_ast(name)
            ta_body  :List[ta_instruction]    = convert_ast(body) # stmt -> list[instr] 
            return ta_Function(ta_name, ta_body)

        # return is the only statement, so needs to yield list of instr
        case Return(exp_=exp_):
            instrs = []
            src      :ta_val                  = emit_tacky(exp_, instrs)
            instrs.append(ta_Return(src))
            return instrs

        case _:
            global e 
            e = node
            _type = type(node)
            msg = f'convert_ast: Unknown type: {_type}'
            error(msg)

def pretty_print_tacky(node:TaNode, depth=0):
    match node:
        case ta_Unary(op=op,src=src,dst=dst):
            print(depth*' ' + 'Unary')
            pretty_print_tacky(op, depth+4)             
            pretty_print_tacky(src, depth+4)             
            pretty_print_tacky(dst, depth+4)             
        case ta_Return(v=v):
            print(depth*' ' + 'Return')
            pretty_print_tacky(v, depth+4)             
        case ta_Constant(integer=integer):
            print(depth*' ' + 'Constant')
            pretty_print_tacky(integer, depth+4) 
        case ta_Var(ident=ident):
            print(depth*' ' + 'Var')
            pretty_print_tacky(ident, depth+4) 
        case ta_Program(fd=fd):
            print(depth*' ' + 'Program')
            pretty_print_tacky(fd, depth+4) 
        case ta_Function(name=name,body=body):
            print(depth*' ' + 'Function')
            pretty_print_tacky(name, depth+4) 
            for i in body: # body:List[ta_instr]
                pretty_print_tacky(i, depth+4)
        case ta_integer(int_=int_):
            print(depth*' ' + f'integer({int_})')
        case ta_identifier(str_=str_):
            print(depth*' ' + f'identifier({str_})')
        case ta_Negate():
            print(depth*' ' + 'Negate')
        case ta_Complement():
            print(depth*' ' + 'Complement')
        case _:
            global e 
            e = node
            _type = type(node)
            msg = f'pretty_print_tacky: Unknown type: {_type}'
            error(msg)


# - - - A S S E M B L Y   G E N E R A T I O N 
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

# base class
# -----------------------------------------------------------------------------

class CgNode: 
    pass

# grammar LHS
# -----------------------------------------------------------------------------

class cg_program(CgNode):
    pass 

class cg_function_definition(CgNode):
    pass 

class cg_instruction(CgNode):
    pass 

class cg_operand(CgNode):
    pass 

class cg_unary_operator(CgNode):
    pass 

class cg_reg(CgNode):
    pass 

# grammar RHS 
# -----------------------------------------------------------------------------

class cg_identifier(CgNode):
    def __init__(self, str_:str):
        self.str_:str = str_ 

class cg_integer(CgNode):
    def __init__(self, int_:int):
        self.int_:int = int_

# cg_program

class cg_Program(cg_program):
    def __init__(self, fd:cg_function_definition):
        self.fd:cg_function_definition = fd

# cg_function_definition

class cg_Function(cg_function_definition):
    def __init__(self, name:cg_identifier, instructions:List[cg_instruction]):
        self.name:cg_identifier = name 
        self.instructions:List[cg_instruction] = instructions

# cg_instruction

class cg_Mov(cg_instruction):
    def __init__(self, src:cg_operand, dst:cg_operand):
        self.src:cg_operand = src 
        self.dst:cg_operand = dst

class cg_Unary(cg_instruction):
    def __init__(self, unop:cg_unary_operator, op:cg_operand):
        self.unop:cg_unary_operator = unop 
        self.op:cg_operand = op

class cg_AllocateStack(cg_instruction):
    def __init__(self, integer_:cg_integer):
        self.integer_:cg_integer = integer_

class cg_Ret(cg_instruction):
    def __init__(self):
        pass

# cg_unary_operator

class cg_Neg(cg_unary_operator):
    def __init__(self):
        pass

class cg_Not(cg_unary_operator):
    def __init__(self):
        pass

# cg_operand

class cg_Imm(cg_operand):
    def __init__(self, integer_:cg_integer):
        self.integer_:cg_integer = integer_

class cg_Reg(cg_operand):
    def __init__(self, reg:cg_reg):
        self.reg:cg_reg = reg

class cg_Pseudo(cg_operand):
    def __init__(self, ident:cg_identifier):
        self.ident:cg_identifier = ident 

class cg_Stack(cg_operand):
    def __init__(self, integer_:cg_integer):
        self.integer_:cg_integer = integer_

# cg_reg

class cg_AX(cg_reg):
    def __init__(self):
        pass

class cg_R10(cg_reg):
    def __init__(self):
        pass

# convert Tacky to Assembly
def convert_tacky(node:TaNode):
    match node:
        case ta_Var(ident=ident):
            cg_ident :cg_identifier   = convert_tacky(ident)
            return cg_Pseudo(cg_ident)
        case ta_Constant(integer=integer):
            cg_int :cg_integer        = convert_tacky(integer)
            return cg_Imm(cg_int)
        case ta_Negate():
            return cg_Neg()
        case ta_Complement():
            return cg_Not()

        case ta_Unary(op=op,src=src,dst=dst):
            src_   :cg_operand        = convert_tacky(src) # ta_val -> cg_operand
            dst_   :cg_operand        = convert_tacky(dst) # ta_val -> cg_operand
            inst1  :cg_instruction    = cg_Mov(src_,dst_)
            op_    :cg_unary_operator = convert_tacky(op)
            inst2  :cg_instruction    = cg_Unary(op_, dst_)
            return [inst1, inst2]
        case ta_Return(v=v):
            op     :cg_operand        = convert_tacky(v) # ta_val -> cg_operand
            inst1  :cg_instruction    = cg_Mov(op, cg_Reg(cg_AX()))
            inst2  :cg_instruction    = cg_Ret()
            return [inst1, inst2]
        case ta_Program(fd=fd):
            cgfd    :cg_function_definition  = convert_tacky(fd)
            return cg_Program(cgfd)
        case ta_Function(name=name, body=body):
            cgname  :cg_identifier           = convert_tacky(name)
            cginstr :List[cg_instruction]    = []
            for i in body:
                cginstr += convert_tacky(i)
            return cg_Function(cgname, cginstr)

        case ta_identifier(str_=str_):
            return cg_identifier(str_)
        case ta_integer(int_=int_):
            return cg_integer(int_)
        case _:
            global e 
            e = node
            _type = type(node)
            msg = f'convert_tacky: Unknown type: {_type}'
            error(msg)

def pretty_print_asm(node:CgNode, depth=0):
    match node:
        case cg_integer(int_=int_):
            print(depth*' ' + f'integer({int_})')
        case cg_identifier(str_=str_):
            print(depth*' ' + f'identifier({str_})')
        case cg_Program(fd=fd,):
            print(depth*" " + "Program")
            pretty_print_asm(fd, depth+4)
        case cg_Function(name=name,instructions=instructions,):
            print(depth*" " + "Function")
            pretty_print_asm(name, depth+4)
            for i in instructions:
                pretty_print_asm(i, depth+4) 
        case cg_Mov(src=src,dst=dst,):
            print(depth*" " + "Mov")
            pretty_print_asm(src, depth+4)
            pretty_print_asm(dst, depth+4)
        case cg_Unary(unop=unop,op=op,):
            print(depth*" " + "Unary")
            pretty_print_asm(unop, depth+4)
            pretty_print_asm(op, depth+4)
        case cg_AllocateStack(integer_=integer_,):
            print(depth*" " + "AllocateStack")
            pretty_print_asm(integer_, depth+4)
        case cg_Ret():
            print(depth*" " + "Ret")
        case cg_Neg():
            print(depth*" " + "Neg")
        case cg_Not():
            print(depth*" " + "Not")
        case cg_Imm(integer_=integer_,):
            print(depth*" " + "Imm")
            pretty_print_asm(integer_, depth+4)
        case cg_Reg(reg=reg,):
            print(depth*" " + "Reg")
            pretty_print_asm(reg, depth+4)
        case cg_Pseudo(ident=ident,):
            print(depth*" " + "Pseudo")
            pretty_print_asm(ident, depth+4)
        case cg_Stack(integer_=integer_,):
            print(depth*" " + "Stack")
            pretty_print_asm(integer_, depth+4)
        case cg_AX():
            print(depth*" " + "AX")
        case cg_R10():
            print(depth*" " + "R10")
        case _:
            global e 
            e = node
            _type = type(node)
            msg = f'pretty_print_asm: Unknown type: {_type}'
            error(msg)

# convert pseudo-registers to stack 
def replace_pseud(node:CgNode):
    match node:
        case cg_identifier(str_=str_,):
            return cg_identifier(str_)
        case cg_integer(int_=int_,):
            return cg_integer(int_)
        case cg_Program(fd=fd,):
            x0 = replace_pseud(fd)
            return cg_Program(x0)
        case cg_Function(name=name,instructions=instructions,):
            x0 = replace_pseud(name)
            x1 = []
            for i in instructions:
                x1.append(replace_pseud(i))
            return cg_Function(x0,x1)
        case cg_Mov(src=src,dst=dst,):
            x0 = replace_pseud(src)
            x1 = replace_pseud(dst)
            return cg_Mov(x0,x1)
        case cg_Unary(unop=unop,op=op,):
            x0 = replace_pseud(unop)
            x1 = replace_pseud(op)
            return cg_Unary(x0,x1)
        case cg_AllocateStack(integer_=integer_,):
            x0 = replace_pseud(integer_)
            return cg_AllocateStack(x0)
        case cg_Ret():
            return cg_Ret()
        case cg_Neg():
            return cg_Neg()
        case cg_Not():
            return cg_Not()
        case cg_Imm(integer_=integer_,):
            x0 = replace_pseud(integer_)
            return cg_Imm(x0)
        case cg_Reg(reg=reg,):
            x0 = replace_pseud(reg)
            return cg_Reg(x0)
        case cg_Pseudo(ident=ident):
            global pseud_2_stack
            id_ = ident.str_
            if id_ not in pseud_2_stack.keys():
                global stack_offset
                stack_offset -= 4
                pseud_2_stack[id_] = stack_offset
            this_offset = pseud_2_stack[id_]
            return cg_Stack(cg_integer(this_offset))
        case cg_Stack(integer_=integer_,):
            x0 = replace_pseud(integer_)
            return cg_Stack(x0)
        case cg_AX():
            return cg_AX()
        case cg_R10():
            return cg_R10()
        case _:
            global e 
            e = node
            _type = type(node)
            msg = f'replace_pseud: Unknown type: {_type}'
            error(msg)

 
# NOTE: the CgNode, Assembly AST is not very nested, 
#   the List[instr] has depth at most 3, no recursive nesting. 
#   so we can just loop over the instructions,
#   because the cases return a node rather than a list of nodes,
#   which is convoluted. 

def _insert_sublists_into_list(items, replace):

    # 'replace' is a list matching 'items', at each 
    # position has either None or a list of things 
    # to insert into 'items' at that position. 
    # we iterate backwards because the list grows 
    # as we insert items. 
        
    # items = list(range(11))

    # replace = []
    # for i, item in enumerate(items): 
    #     if i % 2 == 1:
    #         replace.append((item + 0.25, item + 0.5))
    #     else:
    #         replace.append(None) # dont replace anything

    # walk list backwards 
    for i in range(len(items)-1,-1,-1):
        item = items[i]
        # print(i, item, replace[i])
        to_insert = replace[i] # things to insert into list
        if to_insert is not None:
            _ = items.pop(i) # drop the element already there 
            for j in range(len(to_insert)-1,-1,-1): # iterate backwards
                items.insert(i, to_insert[j])

# add stack size, fix MOV(mem,mem)
def fixup_instructions(node):
    match node:
        case cg_identifier(str_=str_,):
            return cg_identifier(str_)
        case cg_integer(int_=int_,):
            return cg_integer(int_)
        case cg_Program(fd=fd,):
            x0 = fixup_instructions(fd)
            return cg_Program(x0)
        case cg_Function(name=name,instructions=instructions,):
            x0 = fixup_instructions(name)
            # fix MOV(mem, mem)
            replace = []
            for i, instr in enumerate(instructions):
                # if instr is MOV(mem,mem):
                if isinstance(instr,cg_Mov) and isinstance(instr.src,cg_Stack) and isinstance(instr.dst,cg_Stack):
                    # convert move{mem, mem} to put in R10D in between 
                    # emit_tacky returns a new ta_Var, destination register / address, 
                    #   for each expression. so a nested expression returns a ta_Var 
                    #   as the source. the dst is also a ta_Var because all dst become
                    #   variables. variables -> pseudo-registers -> stack locations.  

                    _src = instr.src 
                    _dst = instr.dst 
                    _tmp = cg_Reg(cg_R10())
                    instr1 = cg_Mov(_src, _tmp)
                    instr2 = cg_Mov(_tmp, _dst)
                    replace.append([instr1, instr2])
                else:
                    replace.append(None) 

            x1 = [fixup_instructions(i) for i in instructions]
            _insert_sublists_into_list(x1, replace)
            # insert stack size
            alloc_stack = cg_AllocateStack(cg_integer(-stack_size))
            x1.insert(0, alloc_stack)
            
            return cg_Function(x0,x1)
        case cg_Mov(src=src,dst=dst,):
            x0 = fixup_instructions(src)
            x1 = fixup_instructions(dst)
            return cg_Mov(x0,x1)
        case cg_Unary(unop=unop,op=op,):
            x0 = fixup_instructions(unop)
            x1 = fixup_instructions(op)
            return cg_Unary(x0,x1)
        case cg_AllocateStack(integer_=integer_,):
            x0 = fixup_instructions(integer_)
            return cg_AllocateStack(x0)
        case cg_Ret():
            return cg_Ret()
        case cg_Neg():
            return cg_Neg()
        case cg_Not():
            return cg_Not()
        case cg_Imm(integer_=integer_,):
            x0 = fixup_instructions(integer_)
            return cg_Imm(x0)
        case cg_Reg(reg=reg,):
            x0 = fixup_instructions(reg)
            return cg_Reg(x0)
        case cg_Pseudo(ident=ident,):
            x0 = fixup_instructions(ident)
            return cg_Pseudo(x0)
        case cg_Stack(integer_=integer_,):
            x0 = fixup_instructions(integer_)
            return cg_Stack(x0)
        case cg_AX():
            return cg_AX()
        case cg_R10():
            return cg_R10()
        case _:
            global e 
            e = node
            _type = type(node)
            msg = f'fixup_instructions: Unknown type: {_type}'
            error(msg)


# --- E M I S S I O N 
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def emission(node:CgNode, lines:List[str]):
    match node:
        case cg_integer(int_=int_):
            return f'{int_}'
        case cg_identifier(str_=str_):
            return str_
        case cg_Program(fd=fd):
            emission(fd, lines)
            lines.append('    .section .note.GNU-stack,"",@progbits')
        case cg_Function(name=name,instructions=instructions):
            _name = emission(name, lines)
            lines.append(f'    .globl {_name}')
            lines.append(f'{_name}:')
            lines.append(f'    pushq   %rbp')
            lines.append(f'    movq    %rsp, %rbp')
            for i in instructions:
                emission(i, lines)
        # instructions
        case cg_Mov(src=src,dst=dst):
            _src = emission(src, lines)
            _dst = emission(dst, lines)
            lines.append(f'    movl    {_src}, {_dst}')
        case cg_Ret():
            lines.append(f'    movq    %rbp, %rsp')
            lines.append(f'    popq    %rbp')
            lines.append(f'    ret')
        case cg_AllocateStack(integer_=integer_,):
            int_ = emission(integer_, lines)
            lines.append(f'    subq    ${int_}, %rsp')
        case cg_Unary(unop=unop,op=op,):
            _unop = emission(unop, lines)
            _opnd = emission(op, lines)
            lines.append(f'    {_unop}    {_opnd}')
        # cg_unary_operator (cg_innstruction)
        case cg_Neg():
            return 'negl'
        case cg_Not():
            return 'notl'
        # --- operands
        case cg_Stack(integer_=integer_,):
            int_ = emission(integer_, lines)
            return f'{int_}(%rbp)'
        case cg_Imm(integer_=integer_,):
            int_ = emission(integer_, lines)
            return f'${int_}'
        # registers
        case cg_Reg(reg=reg,):
            return emission(reg,lines)
        case cg_AX():
            return '%eax'
        case cg_R10():
            return '%r10d'
        case _:
            global e 
            e = node
            _type = type(node)
            msg = f'emission: Unknown type: {_type}'
            error(msg)




# initialize compiler variables
# -----------------------------
global e              # error
global stack_offset
global stack_size
e            = None 
stack_offset = 0
stack_size   = 0
global _counter
_counter = counter()
_counter.reset()
global pseud_2_stack
pseud_2_stack = {}
make_temporary = lambda: str(_counter.increment())
# -----------------------------


def get_stack_size():
    offset = len(pseud_2_stack.items())
    if offset == 0:
        stack_size = 0
    else:
        stack_size     = min([v for k,v in pseud_2_stack.items()])
    return stack_size 


# _source = '''
# int main(void) {
#     return ~-~-~~~-2;
# }
# '''

# tokens = []
# l = lexer()
# my_exit_code = l.lex(_source, tokens)
# for _tok, _lex in tokens:
#     print(_lex, (20 - len(_lex)) * ' ', _tok)

# ast = parse_program(tokens)
# pretty_print(ast)

# tacky = convert_ast(ast)
# pretty_print_tacky(tacky)


# asm = convert_tacky(tacky)
# pretty_print_asm(asm)

# asm2 = replace_pseud(asm)
# pretty_print_asm(asm2)

# pseud_2_stack
# global stack_size
# stack_size = min([v for k,v in pseud_2_stack.items()])
# stack_size

# asm3 = fixup_instructions(asm2)
# pretty_print_asm(asm3)

# lines = []
# emission(asm3, lines)
# for l in lines:
#     print(l)



# test_dir = '/home/chad/Desktop/test'
# test_dir = '/home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/tests/chapter_1/valid'
# files = [i for i in os.listdir(test_dir) if i[-2:] == '.c']
# for file in files:
#     file_path = os.path.join(test_dir, file)
#     print()
#     print(file_path)






def main():

    # intro message
    if True:
        msg = 'SEV COMPILER'
        print('+' + '-'*78 + '+')
        print(f'| {msg}{(80 - 4 - len(msg))* " "} |')
        print('+' + '-'*78 + '+')

    # get 1 input argument, the file path, and 3 optional arguments
    if True:
        parser      = argparse.ArgumentParser()
        parser.add_argument('file_path', type=str)
        parser.add_argument('--lex', action='store_true')
        parser.add_argument('--parse', action='store_true')
        parser.add_argument('--codegen', action='store_true')
        parser.add_argument('--tacky', action='store_true')
        args        = parser.parse_args()
        file_path   = args.file_path
        __lex       = args.lex 
        __parse     = args.parse 
        __codegen   = args.codegen
        __tacky     = args.tacky

    # change directory to where the input file is located
    if True:
        dir_name             = os.path.dirname(file_path)
        file_name_orig       = os.path.basename(file_path)
        file_name_preprocess = file_name_orig.replace('.c', '.i')
        file_name_asm        = file_name_orig.replace('.c', '.s')
        os.chdir(dir_name)
        # print(f'Changed directory to: {dir_name}')
        # print(file_name_orig)
        # print(file_name_preprocess)
        # print(file_name_asm)

    # pre-process the file 
    preprocess_file(file_name_orig)

    # read the pre=processed file contents 
    content = read_file(file_name_preprocess)
    print(content)

    my_exit_code = 0

    if __lex:
        tokens         = []
        l              = lexer()
        my_exit_code   = l.lex(content, tokens)

    elif __parse:
        tokens         = []
        l              = lexer()
        my_exit_code   = l.lex(content, tokens)
        ast            = parse_program(tokens)

    elif __tacky:
        tokens         = []
        l              = lexer()
        my_exit_code   = l.lex(content, tokens)
        ast            = parse_program(tokens)
        tacky          = convert_ast(ast)


    elif __codegen: 
        tokens         = []
        l              = lexer()
        my_exit_code   = l.lex(content, tokens)
        ast            = parse_program(tokens)
        tacky          = convert_ast(ast)
        asm            = convert_tacky(tacky)
        asm2           = replace_pseud(asm)
        stack_size     = get_stack_size()
        asm3           = fixup_instructions(asm2)

    # do everything
    else:
        tokens         = []
        l              = lexer()
        my_exit_code   = l.lex(content, tokens)
        ast            = parse_program(tokens)
        tacky          = convert_ast(ast)
        asm            = convert_tacky(tacky)
        asm2           = replace_pseud(asm)
        stack_size     = get_stack_size()
        asm3           = fixup_instructions(asm2)
        lines          = []
        emission(asm3, lines)


        lines.append('') # so that end of file is newline, to satisfy assembler
        assembly     = '\n'.join(lines)
        with open(f"{file_name_asm}", "w") as file:
            file.write(assembly)
        assemble_and_link(file_name_asm)
        os.remove(file_name_asm)


    os.remove(file_name_preprocess)

    print(f'EXIT CODE: {my_exit_code}')
    
    sys.exit(my_exit_code)

if __name__ == "__main__":
    main()




'''
/home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/test_compiler /home/chad/Desktop/_backups/notes/nora_compiler_0002.py --chapter 2 --stage lex
/home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/test_compiler /home/chad/Desktop/_backups/notes/nora_compiler_0002.py --chapter 2 --stage parse
/home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/test_compiler /home/chad/Desktop/_backups/notes/nora_compiler_0002.py --chapter 2 --stage tacky
/home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/test_compiler /home/chad/Desktop/_backups/notes/nora_compiler_0002.py --chapter 2 --stage codegen
/home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/test_compiler /home/chad/Desktop/_backups/notes/nora_compiler_0002.py --chapter 2

/home/chad/Desktop/_backups/notes/nora_compiler_0002.py /home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/tests/chapter_1/invalid_parse/end_before_expr.c --lex
/home/chad/Desktop/_backups/notes/nora_compiler_0002.py /home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/tests/chapter_1/invalid_parse/end_before_expr.c --parse

'''


