
from codegen import *



# --- E M I S S I O N 
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def emit(node:CgNode, lines:List[str]):
    match node:
        case cg_integer(int_=int_):
            return f'{int_}'
        case cg_identifier(str_=str_):
            return str_
        case cg_Program(fd=fd):
            emit(fd, lines)
            lines.append('    .section .note.GNU-stack,"",@progbits')
        case cg_Function(name=name,instructions=instructions):
            _name = emit(name, lines)
            lines.append(f'    .globl {_name}')
            lines.append(f'{_name}:')
            lines.append(f'    pushq   %rbp')
            lines.append(f'    movq    %rsp, %rbp')
            for i in instructions:
                emit(i, lines)
        # instructions
        case cg_Mov(src=src,dst=dst):
            _src = emit(src, lines)
            _dst = emit(dst, lines)
            lines.append(f'    movl    {_src}, {_dst}')
        case cg_Ret():
            lines.append(f'    movq    %rbp, %rsp')
            lines.append(f'    popq    %rbp')
            lines.append(f'    ret')
        case cg_AllocateStack(integer_=integer_,):
            int_ = emit(integer_, lines)
            lines.append(f'    subq    ${int_}, %rsp')
        case cg_Unary(unop=unop,op=op,):
            _unop = emit(unop, lines)
            _opnd = emit(op, lines)
            lines.append(f'    {_unop}    {_opnd}')
        case cg_Binary(binop=binop,op1=op1,op2=op2,):
            _binop = emit(binop, lines)
            _op1   = emit(op1, lines)
            _op2   = emit(op2, lines)
            lines.append(f'    {_binop}    {_op1}, {_op2}')
        case cg_Idiv(op=op,):
            _op    = emit(op, lines)
            lines.append(f'    idivl   {_op}')
        case cg_Cdq():
            lines.append(f'    cdq')
        # cg_unary_operator (cg_innstruction)
        case cg_Neg():
            return 'negl'
        case cg_Not():
            return 'notl'
        case cg_Add():
            return 'addl'
        case cg_Sub():
            return 'subl'
        case cg_Mult():
            return 'imull'
        case cg_Shl():
            return 'shll'
        case cg_Shr():
            return 'sarl' # only changed this from *shrl* to pass test 
        case cg_Xor():
            return 'xorl'
        case cg_And():
            return 'andl'
        case cg_Or():
            return 'orl'
        # --- operands
        case cg_Stack(integer_=integer_,):
            int_ = emit(integer_, lines)
            return f'{int_}(%rbp)'
        case cg_Imm(integer_=integer_,):
            int_ = emit(integer_, lines)
            return f'${int_}'
        # registers
        case cg_Reg(reg=reg,):
            return emit(reg,lines)
        case cg_AX():
            return '%eax'
        case cg_CX():
            return '%ecx'
        case cg_DX():
            return '%edx'
        case cg_R10():
            return '%r10d'
        case cg_R11():
            return '%r11d'
        case _:
            global e 
            e = node
            _type = type(node)
            msg = f'emit: Unknown type: {_type}'
            error(msg)




if __name__ == "__main__":

    l = lexer()
    my_exit_code = l.lex(source_)
    l.print()

    ast = parse_program(l.tokens)
    pretty_print(ast)

    tacky = convert_ast(ast)
    pretty_print_tacky(tacky)

    asm = convert_tacky(tacky)
    pretty_print_asm(asm)

    asm2 = replace_pseud(asm)
    pretty_print_asm(asm2)

    asm3 = fixup_instructions(asm2)
    pretty_print_asm(asm3)

    lines = []
    emit(asm3, lines)
    for l in lines:
        print(l)



