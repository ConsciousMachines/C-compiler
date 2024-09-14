


from common import *
from parse import *

from typing import List





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

class ta_binary_operator(TaNode):
    pass 

# grammar RHS 
# -----------------------------------------------------------------------------
# --- BEGIN CLASS DEFINITION

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

class ta_Binary(ta_instruction):
    def __init__(self, binop:ta_binary_operator, src1:ta_val, src2:ta_val, dst:ta_val):
        self.binop : ta_binary_operator = binop
        self.src1  : ta_val             = src1
        self.src2  : ta_val             = src2
        self.dst   : ta_val             = dst

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

# ta_binary_operator

class ta_Add(ta_binary_operator):
    def __init__(self):
        pass

class ta_Subtract(ta_binary_operator):
    def __init__(self):
        pass

class ta_Multiply(ta_binary_operator):
    def __init__(self):
        pass

class ta_Divide(ta_binary_operator):
    def __init__(self):
        pass

class ta_Remainder(ta_binary_operator):
    def __init__(self):
        pass

class ta_BitwiseAnd(ta_binary_operator):
    def __init__(self):
        pass

class ta_BitwiseOr(ta_binary_operator):
    def __init__(self):
        pass

class ta_BitwiseXor(ta_binary_operator):
    def __init__(self):
        pass

class ta_LeftShift(ta_binary_operator):
    def __init__(self):
        pass

class ta_RightShift(ta_binary_operator):
    def __init__(self):
        pass

# --- END CLASS DEFINITION

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
        case Binary(binary_operator_=binary_operator_,exp1=exp1,exp2=exp2):
            src1     :ta_val                  = emit_tacky(exp1, instructions)
            src2     :ta_val                  = emit_tacky(exp2, instructions)
            dst      :ta_val                  = ta_Var(ta_identifier(f'tmp.{make_temporary()}'))
            tacky_op :ta_binary_operator      = convert_ast(binary_operator_)
            instructions.append(ta_Binary(tacky_op, src1, src2, dst))
            return dst


# convert AST nodes (except epr, which have separate function) to Tacky
def convert_ast(node:AstNode):
    match node:
        # same structure
        case identifier(str_=str_):
            return ta_identifier(str_)
        case integer(int_=int_):
            return ta_integer(int_)
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
        case Negate():
            return ta_Negate()
        case Complement():
            return ta_Complement()

        case Add():
            return ta_Add()
        case Subtract():
            return ta_Subtract()
        case Multiply():
            return ta_Multiply()
        case Divide():
            return ta_Divide()
        case Remainder():
            return ta_Remainder()

        case BitwiseAnd():
            return ta_BitwiseAnd()
        case BitwiseOr():
            return ta_BitwiseOr()
        case BitwiseXor():
            return ta_BitwiseXor()
        case LeftShift():
            return ta_LeftShift()
        case RightShift():
            return ta_RightShift()

        case _:
            global e 
            e = node
            _type = type(node)
            msg = f'convert_ast: Unknown type: {_type}'
            error(msg)



def pretty_print_tacky(node:TaNode, depth=0) -> None:
    match node:
        case ta_identifier(str_=str_,):
            print(depth*" " + f"identifier({str_})")
        case ta_integer(int_=int_,):
            print(depth*" " + f"integer({int_})")
        case ta_Program(fd=fd,):
            print(depth*" " + "Program")
            pretty_print_tacky(fd, depth+4)
        case ta_Function(name=name,body=body,):
            print(depth*" " + "Function")
            pretty_print_tacky(name, depth+4)
            for i in body: # body:List[]
                pretty_print_tacky(i, depth+4)
        case ta_Return(v=v,):
            print(depth*" " + "Return")
            pretty_print_tacky(v, depth+4)
        case ta_Unary(op=op,src=src,dst=dst,):
            print(depth*" " + "Unary")
            pretty_print_tacky(op, depth+4)
            pretty_print_tacky(src, depth+4)
            pretty_print_tacky(dst, depth+4)
        case ta_Binary(binop =binop ,src1  =src1  ,src2  =src2  ,dst   =dst   ,):
            print(depth*" " + "Binary")
            pretty_print_tacky(binop , depth+4)
            pretty_print_tacky(src1  , depth+4)
            pretty_print_tacky(src2  , depth+4)
            pretty_print_tacky(dst   , depth+4)
        case ta_Constant(integer=integer,):
            print(depth*" " + "Constant")
            pretty_print_tacky(integer, depth+4)
        case ta_Var(ident=ident,):
            print(depth*" " + "Var")
            pretty_print_tacky(ident, depth+4)
        case ta_Complement():
            print(depth*" " + "Complement")
        case ta_Negate():
            print(depth*" " + "Negate")
        case ta_Add():
            print(depth*" " + "Add")
        case ta_Subtract():
            print(depth*" " + "Subtract")
        case ta_Multiply():
            print(depth*" " + "Multiply")
        case ta_Divide():
            print(depth*" " + "Divide")
        case ta_Remainder():
            print(depth*" " + "Remainder")
        case ta_BitwiseAnd():
            print(depth*" " + "BitwiseAnd")
        case ta_BitwiseOr():
            print(depth*" " + "BitwiseOr")
        case ta_BitwiseXor():
            print(depth*" " + "BitwiseXor")
        case ta_LeftShift():
            print(depth*" " + "LeftShift")
        case ta_RightShift():
            print(depth*" " + "RightShift")
        case _:
            global e 
            e = node
            _type = type(node)
            msg = f'pretty_print_tacky: Unknown type: {_type}'
            error(msg)



# # automatically generate pretty print function
# # -----------------------------------------------------------------------------
# from zzz_pretty_printer_generator import file_2_pp
# pp = file_2_pp(__file__)
# pp = pp.replace('pretty_print', 'pretty_print_tacky')
# pp = pp.replace('_IN_TYPE_', 'TaNode')
# print(pp)


if __name__ == "__main__":
    l = lexer()
    my_exit_code = l.lex(source_)
    l.print()

    ast = parse_program(l.tokens)
    pretty_print(ast)

    tacky = convert_ast(ast)
    pretty_print_tacky(tacky)


