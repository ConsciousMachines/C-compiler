#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess 
import argparse
import sys
import os
from emit import *



def preprocess_file(in_name:str) -> None:
    out_name = in_name.replace('.c', '.i')
    args = f'gcc -E -P {in_name} -o {out_name}'.split()
    assert 0 == subprocess.call(args), 'FAILED: pre-process'

def assemble_and_link(file_name:str) -> None:
    args = f'gcc {file_name} -o {file_name[:-2]}'.split()
    assert 0 == subprocess.call(args), 'FAILED: assemble & link'

def read_file(full_path:str) -> str:
    with open(full_path, 'r') as f:
        return f.read()

def print_intro() -> None:
    msg = 'SEV COMPILER'
    print('+' + '-'*78 + '+')
    print(f'| {msg}{(80 - 4 - len(msg))* " "} |')
    print('+' + '-'*78 + '+')




if __name__ == "__main__":



    # file_path = '/home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/tests/chapter_3/valid/extra_credit/bitwise_precedence.c'
    file_path = '/home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/tests/chapter_3/valid/extra_credit/bitwise_shiftr_negative.c'
    # change directory to where the input file is located
    dir_name             = os.path.dirname(file_path)
    file_name_orig       = os.path.basename(file_path)
    file_name_preprocess = file_name_orig.replace('.c', '.i')
    file_name_asm        = file_name_orig.replace('.c', '.s')
    os.chdir(dir_name)
    # pre-process the file 
    preprocess_file(file_name_orig)
    # read the pre=processed file contents 
    source_ = read_file(file_name_preprocess)
    print(source_)



        
    l = lexer()
    my_exit_code = l.lex(source_)
    ast = parse_program(l.tokens)
    tacky = convert_ast(ast)
    asm = convert_tacky(tacky)
    asm2 = replace_pseud(asm)
    asm3 = fixup_instructions(asm2)
    lines = []
    emit(asm3, lines)

    l.print()
    pretty_print(ast)
    pretty_print_tacky(tacky)
    pretty_print_asm(asm)
    pretty_print_asm(asm2)
    pretty_print_asm(asm3)
    for l in lines:
        print(l)

    lines.append('') # so that end of file is newline, to satisfy assembler
    assembly     = '\n'.join(lines)
    with open(f"{file_name_asm}", "w") as file:
        file.write(assembly)
    assemble_and_link(file_name_asm)


    os.remove(file_name_asm)

    os.remove(file_name_preprocess)
    print(f'EXIT CODE: {my_exit_code}')
    sys.exit(my_exit_code)


'''
/home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/test_compiler /home/chad/Desktop/_backups/notes/projects/nora_compiler/ch3/driver.py --chapter 3 --stage lex
/home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/test_compiler /home/chad/Desktop/_backups/notes/projects/nora_compiler/ch3/driver.py --chapter 3 --stage parse
/home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/test_compiler /home/chad/Desktop/_backups/notes/projects/nora_compiler/ch3/driver.py --chapter 3 --stage tacky
/home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/test_compiler /home/chad/Desktop/_backups/notes/projects/nora_compiler/ch3/driver.py --chapter 3 --stage codegen
/home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/test_compiler /home/chad/Desktop/_backups/notes/projects/nora_compiler/ch3/driver.py --chapter 3
/home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/test_compiler /home/chad/Desktop/_backups/notes/projects/nora_compiler/ch3/driver.py --chapter 3 --bitwise

/home/chad/Desktop/_backups/notes/projects/nora_compiler/ch3/driver.py /home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/tests/chapter_1/invalid_lex/invalid_identifier_2.c --lex
/home/chad/Desktop/_backups/notes/projects/nora_compiler/ch3/driver.py /home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/tests/chapter_3/valid/unop_parens.c
/home/chad/Desktop/_backups/notes/projects/nora_compiler/ch3/driver.py /home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/tests/chapter_3/valid/extra_credit/bitwise_precedence.c
/home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/tests/chapter_3/valid/unop_parens.c



'''

# test_dir = '/home/chad/Desktop/test'
# test_dir = '/home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/tests/chapter_1/valid'
# files = [i for i in os.listdir(test_dir) if i[-2:] == '.c']
# for file in files:
#     file_path = os.path.join(test_dir, file)
#     print()
#     print(file_path)