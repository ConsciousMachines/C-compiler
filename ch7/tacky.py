


from validate import *
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

class ta_Copy(ta_instruction):
    def __init__(self, src:ta_val, dst:ta_val):
        self.src   : ta_val             = src
        self.dst   : ta_val             = dst

class ta_Jump(ta_instruction):
    def __init__(self, target:ta_identifier):
        self.target : ta_identifier     = target

class ta_JumpIfZero(ta_instruction):
    def __init__(self, condition:ta_val, target:ta_identifier):
        self.condition : ta_val         = condition
        self.target    : ta_identifier  = target

class ta_JumpIfNotZero(ta_instruction):
    def __init__(self, condition:ta_val, target:ta_identifier):
        self.condition:ta_val           = condition
        self.target : ta_identifier     = target

class ta_Label(ta_instruction):
    def __init__(self, ident:ta_identifier):
        self.ident      : ta_identifier     = ident

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

class ta_Not(ta_unary_operator):
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

class ta_Equal(ta_binary_operator):
    def __init__(self):
        pass

class ta_NotEqual(ta_binary_operator):
    def __init__(self):
        pass

class ta_LessThan(ta_binary_operator):
    def __init__(self):
        pass

class ta_LessOrEqual(ta_binary_operator):
    def __init__(self):
        pass

class ta_GreaterThan(ta_binary_operator):
    def __init__(self):
        pass

class ta_GreaterOrEqual(ta_binary_operator):
    def __init__(self):
        pass

# --- END CLASS DEFINITION

_UnaryOp_to_TaUnaryOp = { # unary_operator -> ta_unary_operator
    Complement : ta_Complement,
    Negate     : ta_Negate,
    Not        : ta_Not,
}

_BinaryOp_to_TaBinaryOp = { # binary_operator -> ta_binary_operator
    Add                     : ta_Add,
    Subtract                : ta_Subtract,
    Multiply                : ta_Multiply,
    Divide                  : ta_Divide,
    Remainder               : ta_Remainder,
    BitwiseAnd              : ta_BitwiseAnd,
    BitwiseOr               : ta_BitwiseOr,
    BitwiseXor              : ta_BitwiseXor,
    LeftShift               : ta_LeftShift,
    RightShift              : ta_RightShift,
    Equal                   : ta_Equal,
    NotEqual                : ta_NotEqual,
    LessThan                : ta_LessThan,
    LessOrEqual             : ta_LessOrEqual,
    GreaterThan             : ta_GreaterThan,
    GreaterOrEqual          : ta_GreaterOrEqual,
}

_CompoundAssignment_to_BinaryOperator = { # assignment_operator -> binary_operator
    CompoundAssPlusEq : Add,
    CompoundAssMinusEq: Subtract,
    CompoundAssMultEq : Multiply,
    CompoundAssDivEq  : Divide,
    CompoundAssModEq  : Remainder,
    CompoundAssAndEq  : BitwiseAnd,
    CompoundAssOrEq   : BitwiseOr,
    CompoundAssXorEq  : BitwiseXor,
    CompoundAssShlEq  : LeftShift,
    CompoundAssShrEq  : RightShift,
}

# this takes care of all exp sub-trees
def emit_tacky(node:exp, instructions:List[ta_instruction]) -> ta_val:
    match node:
        case Conditional(condition=condition, exp1=exp1, exp2=exp2):
            end_label :ta_identifier   = ta_identifier(f'END_{make_temporary()}')
            e2_label  :ta_identifier   = ta_identifier(f'e2_{make_temporary()}')
            result    :ta_val          = ta_Var(ta_identifier(f'tmp.{make_temporary()}'))

            c         :ta_val          = emit_tacky(condition, instructions)
            instructions.append(ta_JumpIfZero(c, e2_label)) 
            v1        :ta_val          = emit_tacky(exp1, instructions)
            instructions.append(ta_Copy(v1, result))
            instructions.append(ta_Jump(end_label))  
            instructions.append(ta_Label(e2_label)) 
            v2        :ta_val          = emit_tacky(exp2, instructions)
            instructions.append(ta_Copy(v2, result))
            instructions.append(ta_Label(end_label))  
            return result

        case Var(ident=ident):
            return ta_Var(ta_identifier(ident.str_))
        case Assignment(kind=kind, exp1=exp1,exp2=exp2):
            type_ : assignment_operator = type(kind)
            if type_ == RegularAssignment:
                dst_   : ta_val = emit_tacky(exp1, instructions) # Var -> ta_Var 
                result : ta_val = emit_tacky(exp2, instructions)
                instructions.append(ta_Copy(result, dst_))
                return dst_
            else:
                # [a += b] becomes [a = a + b]
                op     : binary_operator = _CompoundAssignment_to_BinaryOperator[type_]()
                rhs_   : exp             = Binary(op, exp1, exp2) # a + b
                ass_   : exp             = Assignment(RegularAssignment(), exp1, rhs_)
                dst_   : ta_val          = emit_tacky(ass_, instructions)
                return dst_
        case Constant(integer_=integer_):
            ta_int   :ta_integer              = convert_ast(integer_)
            return ta_Constant(ta_int)
        case Unary(unary_operator_=unary_operator_, exp_=exp_):
            type_ : unary_operator = type(unary_operator_)
            if type_ in [Increment, Decrement, IncrementPost, DecrementPost]:
                if type_ == Increment: # [++a] returns [a+1]
                    rhs_ : exp = Binary(Add(), exp_, Constant(integer(1)))
                    ass_ : exp = Assignment(RegularAssignment(), exp_, rhs_)
                    dst_ : ta_val = emit_tacky(ass_, instructions)
                    return dst_
                elif type_ == Decrement:
                    rhs_ : exp = Binary(Subtract(), exp_, Constant(integer(1)))
                    ass_ : exp = Assignment(RegularAssignment(), exp_, rhs_)
                    dst_ : ta_val = emit_tacky(ass_, instructions)
                    return dst_
                elif type_ == IncrementPost:
                    orig_valu :ta_val = emit_tacky(exp_, instructions) # original lvalue
                    save_orig :ta_val = ta_Var(ta_identifier(f'tmp.save_orig_IncrementPost.{make_temporary()}'))
                    instr1    :ta_instruction = ta_Copy(orig_valu, save_orig) 
                    instructions.append(instr1) # copy original value to a new variable, which we return

                    rhs_ : exp = Binary(Add(), exp_, Constant(integer(1)))
                    ass_ : exp = Assignment(RegularAssignment(), exp_, rhs_)
                    dst_ : ta_val = emit_tacky(ass_, instructions)
                    return save_orig
                elif type_ == DecrementPost:
                    orig_valu :ta_val = emit_tacky(exp_, instructions) # original lvalue
                    save_orig :ta_val = ta_Var(ta_identifier(f'tmp.save_orig_DecrementPost.{make_temporary()}'))
                    instr1    :ta_instruction = ta_Copy(orig_valu, save_orig) 
                    instructions.append(instr1) # copy original value to a new variable, which we return

                    rhs_ : exp = Binary(Subtract(), exp_, Constant(integer(1)))
                    ass_ : exp = Assignment(RegularAssignment(), exp_, rhs_)
                    dst_ : ta_val = emit_tacky(ass_, instructions)
                    return save_orig
            else:
                tacky_op :ta_unary_operator       = _UnaryOp_to_TaUnaryOp[type_]()
                src      :ta_val                  = emit_tacky(exp_, instructions)
                dst      :ta_val                  = ta_Var(ta_identifier(f'tmp.{make_temporary()}'))
                instructions.append(ta_Unary(tacky_op, src, dst))
                return dst
        case Binary(binary_operator_=binary_operator_,exp1=exp1,exp2=exp2):
            _type                             = type(binary_operator_)
            # logical AND (short-circuited)
            if _type == And:
                false_label  :ta_identifier   = ta_identifier(f'FALSE_LABEL_{make_temporary()}')
                end_label    :ta_identifier   = ta_identifier(f'END_{make_temporary()}')
                result_F     :ta_val          = ta_Constant(ta_integer(0)) # FALSE
                result_T     :ta_val          = ta_Constant(ta_integer(1)) # TRUE
                dst          :ta_val          = ta_Var(ta_identifier(f'tmp.{make_temporary()}'))

                # evaluate e1, if 0, jump to FALSE
                v1           :ta_val          = emit_tacky(exp1, instructions) # instructions for e1
                instr1       :ta_instruction  = ta_JumpIfZero(v1, false_label) # if e1 == 0, jump to FALSE
                instructions.append(instr1)

                # evaluate e2, if 0, jump to FALSE
                v2           :ta_val          = emit_tacky(exp2, instructions) # instructions for e2
                instr2       :ta_instruction  = ta_JumpIfZero(v2, false_label) # if e2 == 0, jump to FALSE
                instructions.append(instr2)

                # otherwise, both true, copy 1 to dst
                instr3       :ta_instruction  = ta_Copy(result_T, dst)
                instr4       :ta_instruction  = ta_Jump(end_label)
                instructions += [instr3, instr4]

                # FALSE_LABEL:
                instr5       :ta_instruction  = ta_Label(false_label)
                instr6       :ta_instruction  = ta_Copy(result_F, dst)
                instructions += [instr5, instr6]

                # END:
                instr7       :ta_instruction  = ta_Label(end_label)
                instructions.append(instr7)
                return dst

            # logical OR (short-circuited)
            if _type == Or:
                true_label   :ta_identifier   = ta_identifier(f'TRUE_LABEL_{make_temporary()}')
                end_label    :ta_identifier   = ta_identifier(f'END_{make_temporary()}')
                result_F     :ta_val          = ta_Constant(ta_integer(0)) # FALSE
                result_T     :ta_val          = ta_Constant(ta_integer(1)) # TRUE
                dst          :ta_val          = ta_Var(ta_identifier(f'tmp.{make_temporary()}'))

                # evaluate e1, if 1, jump to TRUE
                v1           :ta_val          = emit_tacky(exp1, instructions)   # instructions for e1
                instr1       :ta_instruction  = ta_JumpIfNotZero(v1, true_label) # if e1 == 1, jump to TRUE
                instructions.append(instr1)

                # evaluate e2, if 1, jump to TRUE
                v2           :ta_val          = emit_tacky(exp2, instructions)   # instructions for e2
                instr2       :ta_instruction  = ta_JumpIfNotZero(v2, true_label) # if e2 == 1, jump to TRUE
                instructions.append(instr2)

                # otherwise, both false, copy 0 to dst
                instr3       :ta_instruction  = ta_Copy(result_F, dst)
                instr4       :ta_instruction  = ta_Jump(end_label)
                instructions += [instr3, instr4]

                # TRUE_LABEL:
                instr5       :ta_instruction  = ta_Label(true_label)
                instr6       :ta_instruction  = ta_Copy(result_T, dst)
                instructions += [instr5, instr6]

                # END:
                instr7       :ta_instruction  = ta_Label(end_label)
                instructions.append(instr7)
                return dst

            # other binary ops
            else:
                tacky_op :ta_binary_operator      = _BinaryOp_to_TaBinaryOp[_type]()
                src1     :ta_val                  = emit_tacky(exp1, instructions)
                src2     :ta_val                  = emit_tacky(exp2, instructions)
                dst      :ta_val                  = ta_Var(ta_identifier(f'tmp.{make_temporary()}'))
                instructions.append(ta_Binary(tacky_op, src1, src2, dst))
                return dst
        # error
        case _:
            global e 
            e = node
            _type = type(node)
            msg = f'convert_block_item: Unknown type: {_type}'
            error(msg)

def convert_block_item(node:block_item) -> List[ta_instruction]:
    match node:
        # goto 
        case Goto(label=label):
            instrs = [] 
            instrs.append(ta_Jump(ta_identifier(label.str_))) # instruction: jump to label
            return instrs
        case Label(label=label, stmnt=stmnt):
            instrs = []
            instrs.append(ta_Label(ta_identifier(label.str_))) # add label instruction
            instrs += convert_block_item(stmnt) # convert the actual statement after it
            return instrs
        # block_item
        case S(stmnt=stmnt):
            return convert_block_item(stmnt)
        case D(decl=decl):
            return convert_block_item(decl)
        # declaration
        case Declaration(name=name,init=init):
            instrs = []
            # if there is initializer expression, process it like assignment
            if init is not None:
                emit_tacky(Assignment(RegularAssignment(), Var(name), init), instrs)
            return instrs
        # statement
        case If(condition=condition, then_=then_, else_=else_): # :exp, :statement, :statement
            if else_ is None: # no else clause 
                instrs = []                
                end_label :ta_identifier   = ta_identifier(f'END_{make_temporary()}')

                c         :ta_val          = emit_tacky(condition, instrs)
                instrs                     . append(ta_JumpIfZero(c, end_label)) # if cond == 0, jump to END
                instrs                    += convert_block_item(then_)
                instrs                     . append(ta_Label(end_label))         # END:
            else: # else clause is present 
                instrs = []
                else_label:ta_identifier   = ta_identifier(f'ELSE_{make_temporary()}')
                end_label :ta_identifier   = ta_identifier(f'END_{make_temporary()}')

                c         :ta_val          = emit_tacky(condition, instrs)
                instrs                     . append(ta_JumpIfZero(c, else_label)) # if cond == 0, jump to ELSE
                instrs                    += convert_block_item(then_)            # <statement1>
                instrs                     . append(ta_Jump(end_label))           # Jump(END) 
                instrs                     . append(ta_Label(else_label))         # ELSE:
                instrs                    += convert_block_item(else_)            # <statement2>
                instrs                     . append(ta_Label(end_label))          # END:
            return instrs
        case Return(exp_=exp_):
            instrs = []
            src      :ta_val                  = emit_tacky(exp_, instrs)
            instrs.append(ta_Return(src))
            return instrs
        case Expression(exp_=exp_):
            instrs = []
            src      :ta_val                  = emit_tacky(exp_, instrs)
            return instrs
        case Null():
            return []
        case Block(list_=list_): # list_:List[block_item]
            instrs = []
            for i in list_:
                instrs += convert_block_item(i) # block_item -> list[instr]
            return instrs 
        case Compound(block_=block_):
            return convert_block_item(block_)
        # error
        case _:
            global e 
            e = node
            _type = type(node)
            msg = f'convert_block_item: Unknown type: {_type}'
            error(msg)

# convert AST nodes (except epr, which have separate function) to Tacky
def convert_ast(node:AstNode) -> TaNode:
    match node:
        # same structure
        case identifier(str_=str_):
            return ta_identifier(str_)
        case integer(int_=int_):
            return ta_integer(int_)
        case Program(fd=fd):
            ta_fd    :ta_function_definition  = convert_ast(fd)
            return ta_Program(ta_fd)
        # Function: body *block* -> List[ta_instr]
        case Function(name=name, body=body):
            ta_name  :ta_identifier           = convert_ast(name)
            instrs   :List[ta_instruction]    = convert_block_item(body)
            instrs.append(ta_Return(ta_Constant(ta_integer(0)))) # add return 0 to all functions
            return ta_Function(ta_name, instrs)
        # unary_op and binary_op are inside Unary() and Binary() nodes, handled in emit_tacky
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
            pretty_print_tacky(fd, depth+4) if fd is not None else None
        case ta_Function(name=name,body=body,):
            print(depth*" " + "Function")
            pretty_print_tacky(name, depth+4) if name is not None else None
            for i in body:
                pretty_print_tacky(i, depth+4) if body is not None else None
        case ta_Return(v=v,):
            print(depth*" " + "Return")
            pretty_print_tacky(v, depth+4) if v is not None else None
        case ta_Unary(op=op,src=src,dst=dst,):
            print(depth*" " + "Unary")
            pretty_print_tacky(op, depth+4) if op is not None else None
            pretty_print_tacky(src, depth+4) if src is not None else None
            pretty_print_tacky(dst, depth+4) if dst is not None else None
        case ta_Binary(binop =binop ,src1  =src1  ,src2  =src2  ,dst   =dst   ,):
            print(depth*" " + "Binary")
            pretty_print_tacky(binop , depth+4) if binop  is not None else None
            pretty_print_tacky(src1  , depth+4) if src1   is not None else None
            pretty_print_tacky(src2  , depth+4) if src2   is not None else None
            pretty_print_tacky(dst   , depth+4) if dst    is not None else None
        case ta_Copy(src   =src   ,dst   =dst   ,):
            print(depth*" " + "Copy")
            pretty_print_tacky(src   , depth+4) if src    is not None else None
            pretty_print_tacky(dst   , depth+4) if dst    is not None else None
        case ta_Jump(target =target ,):
            print(depth*" " + "Jump")
            pretty_print_tacky(target , depth+4) if target  is not None else None
        case ta_JumpIfZero(condition =condition ,target    =target    ,):
            print(depth*" " + "JumpIfZero")
            pretty_print_tacky(condition , depth+4) if condition  is not None else None
            pretty_print_tacky(target    , depth+4) if target     is not None else None
        case ta_JumpIfNotZero(condition=condition,target =target ,):
            print(depth*" " + "JumpIfNotZero")
            pretty_print_tacky(condition, depth+4) if condition is not None else None
            pretty_print_tacky(target , depth+4) if target  is not None else None
        case ta_Label(ident      =ident      ,):
            print(depth*" " + "Label")
            pretty_print_tacky(ident      , depth+4) if ident       is not None else None
        case ta_Constant(integer=integer,):
            print(depth*" " + "Constant")
            pretty_print_tacky(integer, depth+4) if integer is not None else None
        case ta_Var(ident=ident,):
            print(depth*" " + "Var")
            pretty_print_tacky(ident, depth+4) if ident is not None else None
        case ta_Complement():
            print(depth*" " + "Complement")
        case ta_Negate():
            print(depth*" " + "Negate")
        case ta_Not():
            print(depth*" " + "Not")
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
        case ta_Equal():
            print(depth*" " + "Equal")
        case ta_NotEqual():
            print(depth*" " + "NotEqual")
        case ta_LessThan():
            print(depth*" " + "LessThan")
        case ta_LessOrEqual():
            print(depth*" " + "LessOrEqual")
        case ta_GreaterThan():
            print(depth*" " + "GreaterThan")
        case ta_GreaterOrEqual():
            print(depth*" " + "GreaterOrEqual")
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

    variable_map = {}
    ast2 = resolve(ast, variable_map)
    pretty_print(ast2)

    labels = {}
    resolve_labels(ast2, labels)

    tacky = convert_ast(ast2)
    pretty_print_tacky(tacky)






