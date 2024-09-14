
#include <iostream>

int main()
{
    std::cout << "Hello World" << std::endl;
}




// # my compiler driver must be command line with 1 argument, the C source
// # produce executable in same directory, same name 
// # terminate w exit code 0
// # if failure, return non-0 exit code

// # options:
// # --lex 
// # --parse: lexer and parser
// # --codegen: stop before code eimssion
// # ^ these dont produce files, but exit with 0 if success
// # -S emit assembly file






// import subprocess 
// import argparse
// import sys
// import os
// from enum import Enum
// from typing import List


// global e  # error

// def preprocess_file(in_name):
//     out_name = in_name.replace('.c', '.i')
//     args = f'gcc -E -P {in_name} -o {out_name}'.split()
//     assert 0 == subprocess.call(args), 'FAILED: pre-process'

// def assemble_and_link(file_name):
//     args = f'gcc {file_name} -o {file_name[:-2]}'.split()
//     assert 0 == subprocess.call(args), 'FAILED: assemble & link'

// def read_file(full_path):
//     with open(full_path, 'r') as f:
//         return f.read()


// # --- L E X E R 
// # -----------------------------------------------------------------------------
// # -----------------------------------------------------------------------------

// # lexer single tokens 
// class Lexer_Token(Enum):
//     SEMICOLON = 1
//     BRACE_OPEN = 2 
//     BRACE_CLOSE = 3
//     BRACKET_OPEN = 4
//     BRACKET_CLOSE = 5

//     INTEGER = 6
//     IDENTIFIER = 7

//     RESERVED_INT = 8
//     RESERVED_VOID = 9
//     RESERVED_RETURN = 10

// lexer_single_char_kw = ';{}()'
// lexer_single_char_kw_tok = [    Lexer_Token.SEMICOLON, 
//                                 Lexer_Token.BRACE_OPEN, 
//                                 Lexer_Token.BRACE_CLOSE, 
//                                 Lexer_Token.BRACKET_OPEN, 
//                                 Lexer_Token.BRACKET_CLOSE]

// # lexer number
// lexer_numeric_char = '0123456789'

// # lexer reserved words
// lexer_reserved_words = ['int', 'void', 'return']
// lexer_reserved_words_tok = [Lexer_Token.RESERVED_INT, 
//                             Lexer_Token.RESERVED_VOID, 
//                             Lexer_Token.RESERVED_RETURN,]
// lexer_non_numeric_char = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789'

// # create a word boundary class to check regex word boundary
// word_boundary = []
// for i in range(128):
//     c = chr(i)  # convert ASCII to char
//     if c.isalnum() or (c == '_'): # skip alphanumeric
//         continue
//     word_boundary.append(c)
// word_boundary = ''.join(word_boundary)

// # iterate over each character
// def lex(program, tokens):
        
//     i = 0 
//     while i < len(program):

//         # get corresponding char
//         c = program[i]

//         # if character is whitespace, skip it 
//         if c in [' ', '\t', '\n']:
//             i += 1
//             continue

//         # if character is single-char keyword, 
//         if c in lexer_single_char_kw:

//             # get index of the character (corresponding enum value)
//             idx = lexer_single_char_kw.find(c)

//             # return the corresponding token
//             tokens.append((lexer_single_char_kw_tok[idx], c))

//             # update current index
//             i += 1
//             continue       

//         # word boundary will be after identifier/keyword by definition
//         # only need to check it after number, in case 123abc

//         # if character is numeric, parse number
//         if c in lexer_numeric_char:
            
//             # start at next char
//             j = i + 1

//             # keep incrementing until we find non-number
//             while program[j] in lexer_numeric_char: 
//                 j += 1

//             # assert program[j] in word_boundary, 'numeric not followed by word boundary'
//             if program[j] not in word_boundary:
//                 print('Lexer Error: numeric not followed by word boundary')
//                 return 1


//             # now we know start and end of numeric sub-string
//             substr = program[i:j]

//             # add it to tokens & lexemes 
//             tokens.append((Lexer_Token.INTEGER, substr))

//             # update current index
//             i = j 
//             continue 

//         # otherwise, parse a word 
//         if c in lexer_non_numeric_char:

//             # start at next char
//             j = i + 1
            
//             # keep incrementing until we find something different
//             while program[j] in lexer_non_numeric_char: 
//                 j += 1

//             # now we know start and end of numeric sub-string
//             substr = program[i:j]

//             # is it a reserved word?
//             if substr in lexer_reserved_words:

//                 # get index of the character (corresponding enum value)
//                 idx = lexer_reserved_words.index(substr)

//                 # add it to tokens & lexemes 
//                 tokens.append((lexer_reserved_words_tok[idx], substr))

//             # else, it is an identifier
//             else:

//                 # add it to tokens & lexemes 
//                 tokens.append((Lexer_Token.IDENTIFIER, substr))

//             # update current index
//             i = j 
//             continue 

//         print(f'Lexer Error: unexpected character: {c}')
//         return 1 # error
            
//     return 0



// # --- P A R S E R 
// # -----------------------------------------------------------------------------
// # -----------------------------------------------------------------------------

// # base class
// # -----------------------------------------------------------------------------

// class AstNode: 
//     pass

// # grammar LHS
// # -----------------------------------------------------------------------------

// class program(AstNode):
//     pass 

// class function_definition(AstNode):
//     pass 

// class statement(AstNode):
//     pass 

// class exp(AstNode):
//     pass 

// # grammar RHS 
// # -----------------------------------------------------------------------------

// class identifier(AstNode):
//     def __init__(self, str_:str):
//         self.str_:str = str_ 

// class integer(AstNode):
//     def __init__(self, int_:int):
//         self.int_:int = int_

// class Program(program):
//     def __init__(self, function_definition_:function_definition):
//         self.function_definition_:function_definition = function_definition_

// class Function(function_definition):
//     def __init__(self, name:identifier, body:statement):
//         self.name:identifier = name 
//         self.body:statement = body

// class Return(statement):
//     def __init__(self, exp_:exp):
//         self.exp_:exp = exp_

// class Constant(exp):
//     def __init__(self, integer_:integer):
//         self.integer_:integer = integer_

// def parse_int(tokens):
//     type_, int_ = tokens.pop(0) # (token_type, *literal*)
//     if type_ != Lexer_Token.INTEGER:
//         raise Exception(f'Parsing Error: expected integer, found {type_}')
//     return integer(int_)

// def parse_identifier(tokens):
//     type_, str_ = tokens.pop(0) # (token_type, *literal*)
//     if type_ != Lexer_Token.IDENTIFIER:
//         raise Exception(f'Parsing Error: expected identifier, found {type_}')
//     return identifier(str_)

// def parse_exp(tokens):
//     int_:integer = parse_int(tokens)
//     return Constant(int_)

// def parse_statement(tokens):
//     expect('return', tokens)
//     exp_:exp = parse_exp(tokens)
//     expect(';', tokens)
//     return Return(exp_)

// def parse_function(tokens):
//     expect('int', tokens)
//     name:identifier = parse_identifier(tokens)
//     expect('(', tokens)
//     expect('void', tokens)
//     expect(')', tokens)
//     expect('{', tokens)
//     body:statement = parse_statement(tokens)
//     expect('}', tokens)
//     return Function(name, body)

// def parse_program(tokens):
//     function_definition_:function_definition = parse_function(tokens)
//     if len(tokens) > 0:
//         raise Exception('Parsing Error: tokens remaining in program')
//     return Program(function_definition_)

// def expect(expected, tokens):
//     type_, actual_ = tokens.pop(0) # take out first element
//     if actual_ != expected:
//         msg = f'Syntax Error: Unexpected token. Expected: {expected}, Found: {actual_}'
//         raise Exception(msg)

// def pretty_print(node, depth=0):
//     match node:
//         case Program(function_definition_=function_definition_):
//             print(depth*' ' + 'Program')
//             pretty_print(function_definition_, depth+4)
//         case Function(name=name, body=body):
//             print(depth*' ' + 'Function')
//             pretty_print(name, depth+4)
//             pretty_print(body, depth+4)
//         case Return(exp_=exp_):
//             print(depth*' ' + 'Return')
//             pretty_print(exp_, depth+4)
//         case Constant(integer_=integer_):
//             print(depth*' ' + 'Constant')
//             pretty_print(integer_, depth+4)
//         case identifier(str_=str_):
//             print(depth*' ' + f'identifier({str_})')
//         case integer(int_=int_):
//             print(depth*' ' + f'integer({int_})')
//         case _:
//             _type = type(node)
//             msg = f'Pretty print: Unknown type: {_type}'
//             global e 
//             e = node
//             raise Exception(msg)




// # - - - A S S E M B L Y   G E N E R A T I O N 
// # -----------------------------------------------------------------------------
// # -----------------------------------------------------------------------------

// # base class
// # -----------------------------------------------------------------------------

// class CgNode: 
//     pass

// # grammar LHS
// # -----------------------------------------------------------------------------

// class cg_program(CgNode):
//     pass 

// class cg_function_definition(CgNode):
//     pass 

// class cg_instruction(CgNode):
//     pass 

// class cg_operand(CgNode):
//     pass 

// # grammar RHS 
// # -----------------------------------------------------------------------------

// class cg_identifier(CgNode):
//     def __init__(self, str_:str):
//         self.str_:str = str_ 

// class cg_integer(CgNode):
//     def __init__(self, int_:int):
//         self.int_:int = int_

// class cg_Program(cg_program):
//     def __init__(self, function_definition_:cg_function_definition):
//         self.function_definition_:cg_function_definition = function_definition_

// class cg_Function(cg_function_definition):
//     def __init__(self, name:cg_identifier, instructions:List[cg_instruction]):
//         self.name:cg_identifier = name 
//         self.instructions:List[cg_instruction] = instructions

// class cg_Mov(cg_instruction):
//     def __init__(self, src:cg_operand, dst:cg_operand):
//         self.src:cg_operand = src 
//         self.dst:cg_operand = dst

// class cg_Ret(cg_instruction):
//     def __init__(self):
//         pass

// class cg_Imm(cg_operand):
//     def __init__(self, integer_:cg_integer):
//         self.integer_:cg_integer = integer_

// class cg_Register(cg_operand):
//     def __init__(self):
//         pass

// # convert AST nodes to Assembly
// def convert(node):
//     match node:
//         case Program(function_definition_=function_definition_):
//             cgfd    :cg_function_definition  = convert(function_definition_)
//             return cg_Program(cgfd)
//         case Function(name=name, body=body):
//             cgname  :cg_identifier           = convert(name)
//             cginstr :List[cg_instruction]    = convert(body)
//             return cg_Function(cgname, cginstr)
//         case Return(exp_=exp_):
//             cg_exp                           = convert(exp_)
//             return [cg_Mov(cg_exp, cg_Register()), cg_Ret()]
//         case Constant(integer_=integer_):
//             return cg_Imm(cg_integer(integer_.int_))
//         case identifier(str_=str_):
//             return cg_identifier(node.str_)
//         case integer(int_=int_):
//             return cg_integer(node.int_)
//         case _:
//             global e 
//             e = node
//             _type = type(node)
//             msg = f'convert: Unknown type: {_type}'
//             raise Exception(msg)

// def pretty_print_asm(node, depth=0):
//     match node:
//         case cg_integer(int_=int_):
//             print(depth*' ' + f'integer({int_})')
//         case cg_identifier(str_=str_):
//             print(depth*' ' + f'identifier({str_})')
//         case cg_Imm(integer_=integer_):
//             print(depth*' ' + 'Imm')
//             pretty_print_asm(integer_, depth+4)
//         case cg_Register():
//             print(depth*' ' + 'Register')
//         case cg_Mov(src=src,dst=dst):
//             print(depth*' ' + 'Mov')
//             pretty_print_asm(src, depth+4)
//             pretty_print_asm(dst, depth+4)
//         case cg_Ret():
//             print(depth*' ' + 'Ret')
//         case cg_Program(function_definition_=function_definition_):
//             print(depth*' ' + 'Program')
//             pretty_print_asm(function_definition_, depth+4) 
//         case cg_Function(name=name,instructions=instructions):
//             print(depth*' ' + 'Function')
//             pretty_print_asm(name, depth+4) 
//             pretty_print_asm(instructions, depth+4) 
//         case list():
//             print(depth*' ' + 'Instructions')
//             for i in node:
//                 pretty_print_asm(i, depth+4) 
//         case _:
//             _type = type(node)
//             msg = f'Pretty print ASM: Unknown type: {_type}'
//             global e 
//             e = node
//             raise Exception(msg)


// # --- E M I S S I O N 
// # -----------------------------------------------------------------------------
// # -----------------------------------------------------------------------------

// def emission(node, lines):
//     match node:

//         case cg_Program(function_definition_=function_definition_):
//             emission(function_definition_, lines)
//             lines.append('\t.section\t.note.GNU-stack,"",@progbits')
        
//         case cg_Function(name=name,instructions=instructions):
//             _name = emission(name, lines)
//             lines.append(f'\t.globl\t{_name}')
//             lines.append(f'{_name}:')
//             emission(instructions, lines)

//         case cg_Mov(src=src,dst=dst):
//             _src = emission(src, lines)
//             _dst = emission(dst, lines)
//             lines.append(f'\tmovl\t{_src}, {_dst}')
//         case cg_Ret():
//             lines.append(f'\tret')

//         case cg_Register():
//             return '%eax'

//         case cg_Imm(integer_=integer_):
//             return emission(integer_, lines)

//         case cg_integer(int_=int_):
//             return f'${int_}'

//         case cg_identifier(str_=str_):
//             return str_

//         case list():
//             for i in node:
//                 emission(i, lines)
//         case _:
//             global e 
//             e = node
//             _type = type(node)
//             msg = f'ERROR: Emission: Unknown type: {_type}'
//             raise Exception(msg)




// # _source = '''
// # int main(void) {
// #     return 2;
// # }
// # '''

// # tokens = []
// # my_exit_code = lex(_source, tokens)

// # for _tok, _lex in tokens:
// #     print(_lex, (20 - len(_lex)) * ' ', _tok)

// # ast = parse_program(tokens)
// # pretty_print(ast)

// # asm = convert(ast)
// # pretty_print_asm(asm)

// # lines = []
// # emission(asm, lines)
// # lines
// # for l in lines:
// #     print(l)





// # test_dir = '/home/chad/Desktop/test'
// # test_dir = '/home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/tests/chapter_1/valid'
// # files = [i for i in os.listdir(test_dir) if i[-2:] == '.c']
// # for file in files:
// #     file_path = os.path.join(test_dir, file)
// #     print()
// #     print(file_path)







// def main():

//     # intro message
//     if True:
//         msg = 'SEV COMPILER'
//         print('+' + '-'*78 + '+')
//         print(f'| {msg}{(80 - 4 - len(msg))* " "} |')
//         print('+' + '-'*78 + '+')

//     # get 1 input argument, the file path, and 3 optional arguments
//     if True:
//         parser      = argparse.ArgumentParser()
//         parser.add_argument('file_path', type=str)
//         parser.add_argument('--lex', action='store_true')
//         parser.add_argument('--parse', action='store_true')
//         parser.add_argument('--codegen', action='store_true')
//         args        = parser.parse_args()
//         file_path   = args.file_path
//         __lex       = args.lex 
//         __parse     = args.parse 
//         __codegen   = args.codegen

//     # change directory to where the input file is located
//     if True:
//         dir_name             = os.path.dirname(file_path)
//         file_name_orig       = os.path.basename(file_path)
//         file_name_preprocess = file_name_orig.replace('.c', '.i')
//         file_name_asm        = file_name_orig.replace('.c', '.s')
//         os.chdir(dir_name)
//         # print(f'Changed directory to: {dir_name}')
//         # print(file_name_orig)
//         # print(file_name_preprocess)
//         # print(file_name_asm)

//     # pre-process the file 
//     preprocess_file(file_name_orig)

//     # read the pre=processed file contents 
//     content = read_file(file_name_preprocess)
//     print(content)


//     my_exit_code = 0

//     if __lex:
//         tokens = []
//         my_exit_code = lex(content, tokens)
//         print(f'FINAL VERDICT: {my_exit_code}')
//         for _tok, _lex in tokens:
//             print(_lex, (20 - len(_lex)) * ' ', _tok)

//     elif __parse:
//         try:
//             tokens = []
//             my_exit_code = lex(content, tokens)
//             ast = parse_program(tokens)
//             # pretty_print(ast)
//         except:
//             my_exit_code = 1

//     elif __codegen: 
//         try:
//             tokens = []
//             my_exit_code = lex(content, tokens)
//             ast = parse_program(tokens)
//             pretty_print(ast)
//             asm = convert(ast)
//         except:
//             my_exit_code = 1

//     # do everything
//     else:
//         try:

//             tokens = []
//             my_exit_code = lex(content, tokens)

//             ast = parse_program(tokens)
//             asm = convert(ast)
//             # pretty_print(ast)
//             # pretty_print_asm(asm)
//             lines = []
//             emission(asm, lines)
//             lines.append('') # so that end of file is newline, to satisfy assembler
//             assembly = '\n'.join(lines)
//             print(assembly)
//             with open(f"{file_name_asm}", "w") as file:
//                 file.write(assembly)

//             assemble_and_link(file_name_asm)
//             os.remove(file_name_asm)

//         except:
//             my_exit_code = 1

//     os.remove(file_name_preprocess)
    
//     sys.exit(my_exit_code)

// if __name__ == "__main__":
//     main()









    




// '''
// /home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/test_compiler /home/chad/Desktop/_backups/notes/nora_compiler_0001.py --chapter 1 --stage lex
// /home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/test_compiler /home/chad/Desktop/_backups/notes/nora_compiler_0001.py --chapter 1 --stage parse
// /home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/test_compiler /home/chad/Desktop/_backups/notes/nora_compiler_0001.py --chapter 1 --stage codegen
// /home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/test_compiler /home/chad/Desktop/_backups/notes/nora_compiler_0001.py --chapter 1

// /home/chad/Desktop/_backups/notes/nora_compiler_0001.py /home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/tests/chapter_1/invalid_parse/end_before_expr.c --lex

// '''


