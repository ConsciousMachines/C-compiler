
if False:
    pass

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


    # 1 + 2 * 3 / 4 + 5
    # ((1 + ((2 * 3) / 4)) + 5)
    # first call: left = parse_factor parses 1
    #   right = parse_factor(prec+1)
    # second call: left = parse_factor parses 2
    #   right = parse_factor(prec+2)
    #       does not find a highe rprecedence, stops at 3
    #   left = package(2,3)
    #   loop checks next thing is /
    #   right = parse_factor(prec+2) parses 4
    #   left = package((2,3),4)
    #   return left 
    # back to first call:
    #   left = package(1, ((2,3).4))
    #   loop
    #   right = parse_factor(prec) parses 5


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



# NOTE: precedence climbing
# NOTE: nested expressions only contain a source. 
#   translating them to TACKY, for each nested expression we generate a new tmp variable. 
#   this is the dst of that expression, becomes the src of the next expression. 
# we take the nested subepressions and output them to a memory register
#   that memory is the input to the parent expression
#   thus we removed nesting, and every input / output is now a register (or constant)
# instead of parent exp being connected to child exp, now the middle man is the register
# connected nested subexpressions were output into a register, and that register is now the input


# NOTE: emit_tacky returns a new ta_Var, destination register / address, 
#   for each expression. so a nested expression returns a ta_Var 
#   as the source. the dst is also a ta_Var because all dst become
#   variables. variables -> pseudo-registers -> stack locations.  


# NOTE: Tacky converts expression trees into List[instr], which is a 
#   list of instructions with NO NESTING!
#   so we can just loop over the instructions.


# NOTE: assembly programs usually store important things on the stack,
#   not in registers. so its ok to overwrite whatever is in EAX 



# shitty code 
if False:
    pass

    # def _insert_sublists_into_list(items, replace):

    #     # 'replace' is a list matching 'items', at each 
    #     # position has either None or a list of things 
    #     # to insert into 'items' at that position. 
    #     # we iterate backwards because the list grows 
    #     # as we insert items. 
            
    #     # items = list(range(11))

    #     # replace = []
    #     # for i, item in enumerate(items): 
    #     #     if i % 2 == 1:
    #     #         replace.append((item + 0.25, item + 0.5))
    #     #     else:
    #     #         replace.append(None) # dont replace anything

    #     # walk list backwards 
    #     for i in range(len(items)-1,-1,-1):
    #         item = items[i]
    #         # print(i, item, replace[i])
    #         to_insert = replace[i] # things to insert into list
    #         if to_insert is not None:
    #             _ = items.pop(i) # drop the element already there 
    #             for j in range(len(to_insert)-1,-1,-1): # iterate backwards
    #                 items.insert(i, to_insert[j])


# chapter 4

# the reason we need a copy instr is because in && or || we evaluate one expression,
#   and depending on its value, we take that result to another register/variable. ex:
#   r0 <- e1
#       if e1 != 0 jump to SHORTCIRCUIT
# SHORTCIRCUIT:
#   copy r1, r0
# also e1 may not be 1, but we need to return 1 anyways


# chapter 5
# in the new precedence parsing algorithm, for right-associativity, 
#   we want the right-most nodes to be the deepest, so the right-most 
#   assignment nodes should be evaluated first, then attached as children
#   to their left-most neighbors. this makes it right-associative
# if a sub-expression becomes the right child, then this is right-associative
# we parse everything to the right of "=" into a subtree, and attach it as 
#   the right child, making it right-associative
#   so everything to the right is included in the right-hand sub-tree

# the new updated parser collects sub-expressions of equal precedence using
#   recursive calls to the right. the previous one collected them in a loop,
#   where a + b + c would become (a + b) + c since the recursive call only
#   returns b as the right side to "a", and then the loop with precedence = 0
#   continues collecting the other expressions. 
# but this new one, a = b = c, the second call to parse_exp will grab "b" and 
#   conitnue parsing "=" after it, since the precedence is the same. so each
#   sub-expression to the right of "a" is collected using a recursive call, 
#   instead of a loop. this way the recursive calls return sub-trees, which 
#   are attached to the right side of the original node, making the whole 
#   thing right-associative. 
# WRONG: hypothetically, you could make the original code right-associative by making 
#   right = Node(left, right) in the loop body. 


# chapter 5 - extra credit
# why do assignments need to be their own AST node and not a binary expression?
#   does it have to do with associativity? 
#   since assignments are right-ass, binary is left-ass


# chapter 6
# (remember we are not using braces for if statements here)
# once we parse the deepest nested if statement, the next token is an else-clause. 
#   but we are currently parsing the deepest if statement. so the else-clause will 
#   be parsed into the deepest IF node. 

# conditional operator: higher prec than assignment, lower than anything else 
#   the ?: tokens act as parentheses, anything between them is their own world

# when we parse an exp with precedence level 0, that means a fresh exp, 
#   not a sub-expression (for example, consisting of only multiplication factors)

# label is basically going to be a wrapper for a statement. when someone calls parse_statement
#   and it parses a label, that is basically a wrapper for the real statement after it, so 
#   the Label node should have a child node for the real statement following it. 




# TODO ???
# a function body is literally a compound statement, so why do we implement it as a list S|D