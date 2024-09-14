
from codegen import *


_UnaryOperator_to_Str = {
    cg_Neg    : 'negl',
    cg_Not    : 'notl',
}

_BinaryOperator_to_Str = {
    cg_Add    : 'addl',
    cg_Sub    : 'subl',
    cg_Mult   : 'imull',
    cg_Shl    : 'shll',
    cg_Shr    : 'sarl', # only changed this from *shrl* to pass test 
    cg_Xor    : 'xorl',
    cg_And    : 'andl',
    cg_Or     : 'orl',
}


_ConditionCode_to_Suffix = {
    cg_E   : 'e',
    cg_NE  : 'ne',
    cg_L   : 'l',
    cg_LE  : 'le',
    cg_G   : 'g',
    cg_GE  : 'ge',
}


# --- E M I S S I O N 
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def _register_to_str(reg:cg_Reg, byte_size:int):
    _reg_name = reg.reg
    if byte_size == 1:
        match _reg_name:
            case cg_AX():
                return '%al'
            case cg_CX():
                return '%cl'
            case cg_DX():
                return '%dl'
            case cg_R10():
                return '%r10b'
            case cg_R11():
                return '%r11b'   
            case _:
                msg = f'_register_to_str: unknown: {cg_Reg}'
                error(msg)
    if byte_size == 4:
        match _reg_name:
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
                msg = f'_register_to_str: unknown: {cg_Reg}'
                error(msg)
    else:
        msg = f'_register_to_str: unknown: {cg_Reg}'
        error(msg)



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
        case cg_Label(ident=ident):
            str_ = emit(ident, lines)
            lines.append(f'.L{str_}:')            
        case cg_SetCC(cc=cc,op=op):
            if type(op) == cg_Reg:
                op_ = _register_to_str(op, 1)
            else:
                op_ = emit(op, lines)
            suffix  = _ConditionCode_to_Suffix[type(cc)]
            lines.append(f'    set{suffix}   {op_}')            
        case cg_JmpCC(cc=cc,ident=ident):
            str_    = emit(ident, lines)
            suffix  = _ConditionCode_to_Suffix[type(cc)]
            lines.append(f'    j{suffix}     .L{str_}')            
        case cg_Jmp(ident=ident):
            str_ = emit(ident, lines)
            lines.append(f'    jmp     .L{str_}')            
        case cg_Cmp(op1=op1,op2=op2):
            _op1 = emit(op1, lines)
            _op2 = emit(op2, lines)
            lines.append(f'    cmpl    {_op1}, {_op2}')            
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
            _unop = _UnaryOperator_to_Str[type(unop)]
            _opnd = emit(op, lines)
            lines.append(f'    {_unop}    {_opnd}')
        case cg_Binary(binop=binop,op1=op1,op2=op2,):
            _binop = _BinaryOperator_to_Str[type(binop)]
            _op1   = emit(op1, lines)
            _op2   = emit(op2, lines)
            lines.append(f'    {_binop}    {_op1}, {_op2}')
        case cg_Idiv(op=op,):
            _op    = emit(op, lines)
            lines.append(f'    idivl   {_op}')
        case cg_Cdq():
            lines.append(f'    cdq')
        # cg_unary_operator (cg_innstruction)
        # --- operands
        case cg_Stack(integer_=integer_,):
            int_ = emit(integer_, lines)
            return f'{int_}(%rbp)'
        case cg_Imm(integer_=integer_,):
            int_ = emit(integer_, lines)
            return f'${int_}'
        # registers
        case cg_Reg(reg=reg,):
            return _register_to_str(node, 4)
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

    variable_map = {}
    ast2 = resolve(ast, variable_map)
    pretty_print(ast2)

    labels = {}
    resolve_labels(ast2, labels)

    tacky = convert_ast(ast2)
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



