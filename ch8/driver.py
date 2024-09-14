#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from test import *











def main():

    # get 1 input argument, the file path, and 3 optional arguments
    if True:
        parser      = argparse.ArgumentParser()
        parser.add_argument('file_path', type=str)
        parser.add_argument('--lex', action='store_true')
        parser.add_argument('--parse', action='store_true')
        parser.add_argument('--validate', action='store_true')
        parser.add_argument('--codegen', action='store_true')
        parser.add_argument('--tacky', action='store_true')
        args        = parser.parse_args()
        file_path   = args.file_path
        __lex       = args.lex 
        __parse     = args.parse 
        __validate  = args.validate
        __codegen   = args.codegen
        __tacky     = args.tacky

    # change directory to where the input file is located
    if True:
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


    if __lex:
        l = lexer()
        my_exit_code = l.lex(source_)
        # l.print()
    elif __parse:

        l = lexer()
        my_exit_code = l.lex(source_)
        # l.print()

        ast = parse_program(l.tokens)
        # pretty_print(ast)

    elif __validate:

        l = lexer()
        my_exit_code = l.lex(source_)
        # l.print()

        ast = parse_program(l.tokens)
        # pretty_print(ast)

        _variable_map = {}
        ast2 = resolve(ast, _variable_map)
        # pretty_print(ast2)

        resolve_labels(ast2, {})
        ast3 = loop_label(ast2, None)
        # pretty_print(ast3)


    elif __tacky:

        l = lexer()
        my_exit_code = l.lex(source_)
        # l.print()

        ast = parse_program(l.tokens)
        # pretty_print(ast)

        variable_map = {}
        ast2 = resolve(ast, variable_map)
        # pretty_print(ast2)

        labels = {}
        resolve_labels(ast2, labels)

        tacky = convert_ast(ast2)
        # pretty_print_tacky(tacky)

    elif __codegen: 

        l = lexer()
        my_exit_code = l.lex(source_)
        # l.print()

        ast = parse_program(l.tokens)
        # pretty_print(ast)

        variable_map = {}
        ast2 = resolve(ast, variable_map)
        # pretty_print(ast2)

        labels = {}
        resolve_labels(ast2, labels)

        tacky = convert_ast(ast2)
        # pretty_print_tacky(tacky)

        asm = convert_tacky(tacky)
        # pretty_print_asm(asm)

        asm2 = replace_pseud(asm)
        # pretty_print_asm(asm2)

        asm3 = fixup_instructions(asm2)
        # pretty_print_asm(asm3)

    else:

        l = lexer()
        my_exit_code = l.lex(source_)
        # l.print()

        ast = parse_program(l.tokens)
        # pretty_print(ast)

        variable_map = {}
        ast2 = resolve(ast, variable_map)
        # pretty_print(ast2)

        labels = {}
        resolve_labels(ast2, labels)

        tacky = convert_ast(ast2)
        # pretty_print_tacky(tacky)

        asm = convert_tacky(tacky)
        # pretty_print_asm(asm)

        asm2 = replace_pseud(asm)
        # pretty_print_asm(asm2)

        asm3 = fixup_instructions(asm2)
        # pretty_print_asm(asm3)

        lines = []
        emit(asm3, lines)
        # for l in lines:
            # print(l)


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
/home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/test_compiler /home/chad/Desktop/_backups/notes/projects/nora_compiler/ch8/driver.py --chapter 8 --stage lex
/home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/test_compiler /home/chad/Desktop/_backups/notes/projects/nora_compiler/ch8/driver.py --chapter 8 --stage parse
/home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/test_compiler /home/chad/Desktop/_backups/notes/projects/nora_compiler/ch8/driver.py --chapter 8 --stage validate
/home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/test_compiler /home/chad/Desktop/_backups/notes/projects/nora_compiler/ch8/driver.py --chapter 8 --stage tacky
/home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/test_compiler /home/chad/Desktop/_backups/notes/projects/nora_compiler/ch8/driver.py --chapter 8
/home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/test_compiler /home/chad/Desktop/_backups/notes/projects/nora_compiler/ch8/driver.py --chapter 8 --goto
/home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/test_compiler /home/chad/Desktop/_backups/notes/projects/nora_compiler/ch8/driver.py --chapter 8 --extra-credit



'''

# test_dir = '/home/chad/Desktop/test'
# test_dir = '/home/chad/Desktop/0__compiler/writing-a-c-compiler-tests-main/tests/chapter_1/valid'
# files = [i for i in os.listdir(test_dir) if i[-2:] == '.c']
# for file in files:
#     file_path = os.path.join(test_dir, file)
#     print()
#     print(file_path)


