
from tacky import *


pseud_2_stack = {}
stack_offset = 0

def get_stack_size(pseud_2_stack):
    offset = len(pseud_2_stack.items())
    if offset == 0:
        stack_size = 0
    else:
        stack_size     = min([v for k,v in pseud_2_stack.items()])
    return stack_size 

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

class cg_binary_operator(CgNode):
    pass 

class cg_reg(CgNode):
    pass 

# grammar RHS 
# -----------------------------------------------------------------------------
# --- BEGIN CLASS DEFINITION

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

class cg_Binary(cg_instruction):
    def __init__(self, binop:cg_binary_operator, op1:cg_operand, op2:cg_operand):
        self.binop:cg_binary_operator = binop 
        self.op1:cg_operand = op1 
        self.op2:cg_operand = op2

class cg_Idiv(cg_instruction):
    def __init__(self, op:cg_operand):
        self.op:cg_operand = op

class cg_Cdq(cg_instruction):
    def __init__(self):
        pass

# cg_unary_operator

class cg_Neg(cg_unary_operator):
    def __init__(self):
        pass

class cg_Not(cg_unary_operator):
    def __init__(self):
        pass

# cg_binary_operator

class cg_Add(cg_binary_operator):
    def __init__(self):
        pass

class cg_Sub(cg_binary_operator):
    def __init__(self):
        pass

class cg_Mult(cg_binary_operator):
    def __init__(self):
        pass

class cg_And(cg_binary_operator):
    def __init__(self):
        pass

class cg_Or(cg_binary_operator):
    def __init__(self):
        pass

class cg_Xor(cg_binary_operator):
    def __init__(self):
        pass

class cg_Shr(cg_binary_operator):
    def __init__(self):
        pass

class cg_Shl(cg_binary_operator):
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

class cg_CX(cg_reg):
    def __init__(self):
        pass

class cg_DX(cg_reg):
    def __init__(self):
        pass

class cg_R10(cg_reg):
    def __init__(self):
        pass

class cg_R11(cg_reg):
    def __init__(self):
        pass

# --- END CLASS DEFINITION

# convert Tacky to Assembly
def convert_tacky(node:TaNode):
    match node:
        # built-in
        case ta_identifier(str_=str_):
            return cg_identifier(str_)
        case ta_integer(int_=int_):
            return cg_integer(int_)
        # program
        case ta_Program(fd=fd):
            cgfd    :cg_function_definition  = convert_tacky(fd)
            return cg_Program(cgfd)
        case ta_Function(name=name, body=body):
            cgname  :cg_identifier           = convert_tacky(name)
            cginstr :List[cg_instruction]    = []
            for i in body:
                cginstr += convert_tacky(i)
            return cg_Function(cgname, cginstr)
        # ta_val
        case ta_Var(ident=ident):
            cg_ident :cg_identifier   = convert_tacky(ident)
            return cg_Pseudo(cg_ident)
        case ta_Constant(integer=integer):
            cg_int :cg_integer        = convert_tacky(integer)
            return cg_Imm(cg_int)
        # ta_instruction
        case ta_Return(v=v):
            op     :cg_operand        = convert_tacky(v) # ta_val -> cg_operand
            inst1  :cg_instruction    = cg_Mov(op, cg_Reg(cg_AX()))
            inst2  :cg_instruction    = cg_Ret()
            return [inst1, inst2]
        # ta_unary_operator
        case ta_Unary(op=op,src=src,dst=dst):
            src_   :cg_operand        = convert_tacky(src) # ta_val -> cg_operand
            dst_   :cg_operand        = convert_tacky(dst) # ta_val -> cg_operand
            inst1  :cg_instruction    = cg_Mov(src_,dst_)
            op_    :cg_unary_operator = convert_tacky(op)
            inst2  :cg_instruction    = cg_Unary(op_, dst_)
            return [inst1, inst2]
        case ta_Negate():
            return cg_Neg()
        case ta_Complement():
            return cg_Not()
        # ta_binary_operator
        case ta_Binary(binop =binop ,src1  =src1  ,src2  =src2  ,dst   =dst   ,):
            src1_  :cg_operand         = convert_tacky(src1  ) # ta_val -> cg_operand
            src2_  :cg_operand         = convert_tacky(src2  ) # ta_val -> cg_operand
            dst_   :cg_operand         = convert_tacky(dst   ) # ta_val -> cg_operand      
            _type = type(binop)
            # for Add / Sub / Mul / AND / OR / XOR:
            # https://www.felixcloutier.com/x86/and
            if _type in [ta_Add,ta_Subtract,ta_Multiply,ta_BitwiseAnd,ta_BitwiseOr,ta_BitwiseXor,ta_LeftShift,ta_RightShift]:
                op_    :cg_binary_operator = convert_tacky(binop)
                inst1  :cg_instruction     = cg_Mov(src1_, dst_)
                inst2  :cg_instruction     = cg_Binary(op_, src2_, dst_)
                return [inst1, inst2]
            # for idiv:
            # NOTE: assembly programs usually store important things on the stack,
            #   not in registers. so its ok to overwrite whatever is in EAX 
            elif _type in [ta_Divide, ta_Remainder]:
                inst1  :cg_instruction     = cg_Mov(src1_, cg_Reg(cg_AX()))
                inst2  :cg_instruction     = cg_Cdq()
                inst3  :cg_instruction     = cg_Idiv(src2_)
                if _type == ta_Divide:
                    inst4  :cg_instruction     = cg_Mov(cg_Reg(cg_AX()), dst_)
                elif _type == ta_Remainder:
                    inst4  :cg_instruction     = cg_Mov(cg_Reg(cg_DX()), dst_)
                return [inst1, inst2, inst3, inst4]
            else:
                msg = f'convert_tacky: ta_Binary: Unknown type: {_type}'
                error(msg)
        case ta_Add():
            return cg_Add()
        case ta_Subtract():
            return cg_Sub()
        case ta_Multiply():
            return cg_Mult()
        case ta_LeftShift():
            return cg_Shl()
        case ta_RightShift():
            return cg_Shr()
        case ta_BitwiseXor():
            return cg_Xor()
        case ta_BitwiseOr():
            return cg_Or()
        case ta_BitwiseAnd():
            return cg_And()
        case _:
            global e 
            e = node
            _type = type(node)
            msg = f'convert_tacky: Unknown type: {_type}'
            error(msg)




def pretty_print_asm(node:CgNode, depth=0) -> None:
    match node:
        case cg_identifier(str_=str_,):
            print(depth*" " + f"identifier({str_})")
        case cg_integer(int_=int_,):
            print(depth*" " + f"integer({int_})")
        case cg_Program(fd=fd,):
            print(depth*" " + "Program")
            pretty_print_asm(fd, depth+4)
        case cg_Function(name=name,instructions=instructions,):
            print(depth*" " + "Function")
            pretty_print_asm(name, depth+4)
            for i in instructions: # body:List[]
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
        case cg_Binary(binop=binop,op1=op1,op2=op2,):
            print(depth*" " + "Binary")
            pretty_print_asm(binop, depth+4)
            pretty_print_asm(op1, depth+4)
            pretty_print_asm(op2, depth+4)
        case cg_Idiv(op=op,):
            print(depth*" " + "Idiv")
            pretty_print_asm(op, depth+4)
        case cg_Cdq():
            print(depth*" " + "Cdq")
        case cg_Neg():
            print(depth*" " + "Neg")
        case cg_Not():
            print(depth*" " + "Not")
        case cg_Add():
            print(depth*" " + "Add")
        case cg_Sub():
            print(depth*" " + "Sub")
        case cg_Mult():
            print(depth*" " + "Mult")
        case cg_And():
            print(depth*" " + "And")
        case cg_Or():
            print(depth*" " + "Or")
        case cg_Xor():
            print(depth*" " + "Xor")
        case cg_Shr():
            print(depth*" " + "Shr")
        case cg_Shl():
            print(depth*" " + "Shl")
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
        case cg_CX():
            print(depth*" " + "CX")
        case cg_DX():
            print(depth*" " + "DX")
        case cg_R10():
            print(depth*" " + "R10")
        case cg_R11():
            print(depth*" " + "R11")
        case _:
            global e 
            e = node
            _type = type(node)
            msg = f'pretty_print_asm: Unknown type: {_type}'
            error(msg)



# # automatically generate pretty_print
# # -----------------------------------------------------------------------------
# from zzz_pretty_printer_generator import file_2_pp
# pp = file_2_pp(__file__)
# pp = pp.replace('pretty_print', 'pretty_print_asm')
# pp = pp.replace('_IN_TYPE_', 'CgNode')
# print(pp)



# # automatically generate replace_pseud
# # -----------------------------------------------------------------------------
# from zzz_pretty_printer_generator import file_2_recurse
# recurse = file_2_recurse(__file__)
# recurse = recurse.replace('recurse', 'replace_pseud')
# recurse = recurse.replace('_IN_TYPE_', 'CgNode')
# recurse = recurse.replace('_OUT_TYPE_', 'CgNode')
# print(recurse)

'''
        # convert pseudo-registers to stack 
        case cg_Pseudo(ident=ident):
            global pseud_2_stack
            id_ = ident.str_
            if id_ not in pseud_2_stack.keys():
                global stack_offset
                stack_offset -= 4
                pseud_2_stack[id_] = stack_offset
            this_offset = pseud_2_stack[id_]
            return cg_Stack(cg_integer(this_offset))
'''



def replace_pseud(node:CgNode) -> CgNode:
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
            x1 = [replace_pseud(i) for i in instructions]
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
        case cg_Binary(binop=binop,op1=op1,op2=op2,):
            x0 = replace_pseud(binop)
            x1 = replace_pseud(op1)
            x2 = replace_pseud(op2)
            return cg_Binary(x0,x1,x2)
        case cg_Idiv(op=op,):
            x0 = replace_pseud(op)
            return cg_Idiv(x0)
        case cg_Cdq():
            return cg_Cdq()
        case cg_Neg():
            return cg_Neg()
        case cg_Not():
            return cg_Not()
        case cg_Add():
            return cg_Add()
        case cg_Sub():
            return cg_Sub()
        case cg_Mult():
            return cg_Mult()
        case cg_And():
            return cg_And()
        case cg_Or():
            return cg_Or()
        case cg_Xor():
            return cg_Xor()
        case cg_Shr():
            return cg_Shr()
        case cg_Shl():
            return cg_Shl()
        case cg_Imm(integer_=integer_,):
            x0 = replace_pseud(integer_)
            return cg_Imm(x0)
        case cg_Reg(reg=reg,):
            x0 = replace_pseud(reg)
            return cg_Reg(x0)
        # convert pseudo-registers to stack 
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
        case cg_DX():
            return cg_DX()
        case cg_R10():
            return cg_R10()
        case cg_R11():
            return cg_R11()
        case _:
            global e 
            e = node
            _type = type(node)
            msg = f'replace_pseud: Unknown type: {_type}'
            error(msg)






# # automatically generate fixup_instructions
# # -----------------------------------------------------------------------------
# from zzz_pretty_printer_generator import file_2_recurse
# recurse = file_2_recurse(__file__)
# recurse = recurse.replace('recurse', 'fixup_instructions')
# recurse = recurse.replace('_IN_TYPE_', 'CgNode')
# recurse = recurse.replace('_OUT_TYPE_', 'CgNode')
# print(recurse)

# NOTE: Tacky converts expression trees into List[instr], which is a 
#   list of instructions with NO NESTING!
#   so we can just loop over the instructions.


# this function gets called from Function, which has a List[cg_instr]
#   each instruction becomes 1 or more, so return a list 
def _fix_instruction(node:cg_instruction) -> List[cg_instruction]:
    match node:
        # MOV(mem, mem) -> put in R10D in between 
        case cg_Mov(src=src,dst=dst,):
            if isinstance(src,cg_Stack) and isinstance(dst,cg_Stack):
                _tmp   : cg_operand       = cg_Reg(cg_R10())
                instr1 : cg_instruction   = cg_Mov(src, _tmp)
                instr2 : cg_instruction   = cg_Mov(_tmp, dst)
                return [instr1, instr2]
            else:
                return [node]
        # idiv: input cannot be Immediate
        case cg_Idiv(op=op):
            if isinstance(op, cg_Imm):
                _dst   : cg_operand       = cg_Reg(cg_R10())
                instr1 : cg_instruction   = cg_Mov(op, _dst)
                instr2 : cg_instruction   = cg_Idiv(_dst)
                return [instr1, instr2]
            else:
                return [node]
        case cg_Binary(binop=binop,op1=op1,op2=op2):
            # ADD / SUB / AND / XOR / OR : cant have both operands be mem
            _type = type(binop)
            if (_type in [cg_Add,cg_Sub,cg_And,cg_Or,cg_Xor]) and isinstance(op1,cg_Stack) and isinstance(op2,cg_Stack):
                _tmp   : cg_operand       = cg_Reg(cg_R10())
                instr1 : cg_instruction   = cg_Mov(op1, _tmp)
                instr2 : cg_instruction   = cg_Binary(binop,_tmp, op2)
                return [instr1, instr2]
            # MULT cant have memory as destination
            elif (_type == cg_Mult) and isinstance(op2,cg_Stack):
                _tmp   : cg_operand       = cg_Reg(cg_R11()) # use R10 for src, R11 for dst
                instr1 : cg_instruction   = cg_Mov(op2, _tmp) # move destination into register
                instr2 : cg_instruction   = cg_Binary(binop, op1, _tmp) # perform mult 
                instr3 : cg_instruction   = cg_Mov(_tmp, op2) # move result to original destination
                return [instr1, instr2, instr3]
            # SHIFT
            # The destination operand can be a register or a memory location. 
            #   The count operand can be an immediate value or the CL register. 
            #   https://www.felixcloutier.com/x86/sal:sar:shl:shr
            elif _type in [cg_Shr,cg_Shl]:
                # just be lazy and mov whatever the count is, into the CL reg
                _tmp   : cg_operand       = cg_Reg(cg_CX())   # RCX, or CL (8 bit) 
                instr1 : cg_instruction   = cg_Mov(op1, _tmp) # move count to CL
                instr2 : cg_instruction   = cg_Binary(binop, _tmp, op2) # perform shift
                # instr3 : cg_instruction   = cg_Mov(_tmp, op2) # move result to original destination
                return [instr1, instr2]#, instr3]

            else:
                return [node]            

        case _:
            return [node]

# we only need to recurse deep enough to get the List[instr]
#   no instructions cases here, they are passed to _fix_instruction
def fixup_instructions(node:CgNode) -> CgNode:
    match node:
        case cg_Program(fd=fd,):
            x0 = fixup_instructions(fd)
            return cg_Program(x0)
        case cg_Function(name=name,instructions=instructions,):
            # convert each instr into list of fixed instructions
            x1 : List[cg_instruction] = []
            for instr in instructions:
                x1 += _fix_instruction(instr)
                    
            # add <allocate stack size> instr
            stack_size = get_stack_size(pseud_2_stack)
            alloc_stack = cg_AllocateStack(cg_integer(-stack_size))
            x1.insert(0, alloc_stack)
            
            return cg_Function(name,x1)
        case _:
            global e 
            e = node
            _type = type(node)
            msg = f'fixup_instructions: Unknown type: {_type}'
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


