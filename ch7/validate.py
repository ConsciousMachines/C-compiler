

from parse import *
from collections import namedtuple # similar to C struct


_VarMapEntry:Tuple[str,bool] = namedtuple('VarMapEntry', ['unique_name', 'from_current_block'])

def copy_variable_map(variable_map:dict):

    # create new dictionary
    new_variable_map = {}
    
    # for each key / value pair
    for k, v in variable_map.items():

        # create a new entry with the same name, and FALSE for "from_current_block"
        new_v = _VarMapEntry(v.unique_name, False)
        new_variable_map[k] = new_v
    
    return new_variable_map


# semantic analysis: variables
def resolve(node:AstNode, variable_map:dict) -> AstNode:
    match node:
        case Compound(block_=block_):
            new_variable_map = copy_variable_map(variable_map)
            x0 = resolve(block_, new_variable_map)
            return Compound(x0)
        case Declaration(name=name,init=init,):
            name_:str = name.str_

            # if name in variable_map, and was added in the current block, then duplicate declaration
            if (name_ in variable_map.keys()) and (variable_map[name_].from_current_block):
                msg = f'resolve: Declaration: duplicate variable declaration: {name_}'
                error(msg)

            # otherwise, create unique name, and say it was created in this scope / block
            unique_name_:str = f'{name_}.{make_temporary()}'
            variable_map[name_] = _VarMapEntry(identifier(unique_name_), True)
            if init is not None:
                init = resolve(init, variable_map) 
            return Declaration(variable_map[name_].unique_name, init)

        case Var(ident=ident):
            name_:str = ident.str_
            if name_ in variable_map.keys():
                return Var(variable_map[name_].unique_name)
            else:
                msg = f'resolve: Var: undeclared variable: {name_}'
                error(msg)
        case Assignment(kind=kind, exp1=exp1, exp2=exp2):
            if type(exp1) != Var:
                msg = f'resolve: Assignment: invalid lvalue: {type(exp1)}'
                error(msg)
            return Assignment(kind, resolve(exp1, variable_map), resolve(exp2, variable_map))

        case Block(list_=list_):
            x0 = [resolve(i, variable_map) for i in list_]
            return Block(x0)
        case Goto(label=label):
            x0 = resolve(label, variable_map)
            return Goto(x0)
        case Label(label=label, stmnt=stmnt):
            x0 = resolve(label, variable_map)
            x1 = resolve(stmnt, variable_map)
            return Label(x0, x1)
        case Conditional(condition=condition,exp1=exp1,exp2=exp2,):
            x0 = resolve(condition, variable_map)
            x1 = resolve(exp1, variable_map)
            x2 = resolve(exp2, variable_map)
            return Conditional(x0,x1,x2)
        case If(condition=condition,then_     =then_     ,else_     =else_     ,):
            x0 = resolve(condition , variable_map)
            x1 = resolve(then_     , variable_map)
            x2 = None 
            if else_ is not None:
                x2 = resolve(else_     , variable_map)
            return If(x0,x1,x2)
        # everything else is just recursive
        case Return(exp_=exp_):
            return Return(resolve(exp_, variable_map))
        case Expression(exp_=exp_):
            return Expression(resolve(exp_, variable_map))
        case identifier(str_=str_,):
            return identifier(str_)
        case integer(int_=int_,):
            return integer(int_)
        case Program(fd=fd,):
            x0 = resolve(fd, variable_map)
            return Program(x0)
        case Function(name=name,body=body,):
            x0 = resolve(name, variable_map)
            x1 = resolve(body, variable_map)
            return Function(x0,x1)
        case Null():
            return Null()
        case Constant(integer_=integer_,):
            x0 = resolve(integer_, variable_map)
            return Constant(x0)
        case Unary(unary_operator_=unary_operator_,exp_=exp_,):
            if (type(unary_operator_) in [Increment,IncrementPost,Decrement,DecrementPost]):
                if (type(exp_) != Var):
                    msg = f'resolve: Unary: invalid lvalue: {type(exp_)}'
                    error(msg)
            x0 = resolve(unary_operator_, variable_map)
            x1 = resolve(exp_, variable_map)
            return Unary(x0,x1)
        case Binary(binary_operator_=binary_operator_,exp1=exp1,exp2=exp2,):
            x0 = resolve(binary_operator_, variable_map)
            x1 = resolve(exp1, variable_map)
            x2 = resolve(exp2, variable_map)
            return Binary(x0,x1,x2)
        case Complement():
            return Complement()
        case Negate():
            return Negate()
        case Not():
            return Not()
        case Add():
            return Add()
        case Subtract():
            return Subtract()
        case Multiply():
            return Multiply()
        case Divide():
            return Divide()
        case Remainder():
            return Remainder()
        case BitwiseAnd():
            return BitwiseAnd()
        case BitwiseOr():
            return BitwiseOr()
        case BitwiseXor():
            return BitwiseXor()
        case LeftShift():
            return LeftShift()
        case RightShift():
            return RightShift()
        case And():
            return And()
        case Or():
            return Or()
        case Equal():
            return Equal()
        case NotEqual():
            return NotEqual()
        case LessThan():
            return LessThan()
        case LessOrEqual():
            return LessOrEqual()
        case GreaterThan():
            return GreaterThan()
        case GreaterOrEqual():
            return GreaterOrEqual()
        case S(stmnt=stmnt,):
            x0 = resolve(stmnt, variable_map)
            return S(x0)
        case D(decl=decl,):
            x0 = resolve(decl, variable_map)
            return D(x0)
        case Increment():
            return Increment()
        case Decrement():
            return Decrement()
        case IncrementPost():
            return IncrementPost()
        case DecrementPost():
            return DecrementPost()
        case _:
            global e 
            e = node
            _type = type(node)
            msg = f'resolve: Unknown type: {_type}'
            error(msg)



# semantic analysis: labels
def resolve_labels(node:exp, labels:list) -> exp:
    match node:
        case Compound(block_=block_):
            x0 = resolve_labels(block_, labels)
            return Compound(x0)
        case Goto(label=label,):
            label_:str = label.str_
            # if it is not in dict, add it
            if label_ not in labels.keys():  
                # 1 occurence of GOTO, 0 occurence of label 
                labels[label_] = (1, 0)      
            # otherwise, it i in the dict, update the entry
            else:                            
                curr_gotos, curr_labels = labels[label_]
                labels[label_] = (curr_gotos + 1, curr_labels)

            x0 = resolve_labels(label, labels)
            return Goto(x0)
        case Label(label=label,stmnt=stmnt,):
            label_:str = label.str_
            # if it is not in dict, add it
            if label_ not in labels.keys():  
                # 0 occurence of GOTO, 1 occurence of label 
                labels[label_] = (0, 1)      
            # otherwise, it i in the dict, update the entry
            else:                            
                curr_gotos, curr_labels = labels[label_]
                labels[label_] = (curr_gotos, curr_labels + 1)
            x0 = resolve_labels(label, labels)
            x1 = resolve_labels(stmnt, labels)
            return Label(x0,x1)

        case Block(list_=list_):

            # fn_labels = {} # the labels that will be inside this function
            x0 = [resolve_labels(i, labels) for i in list_]
            return Block(x0)

        case Function(name=name,body=body,):
            x0 = resolve_labels(name, labels)
            x1 = resolve_labels(body, labels)
            return Function(x0,x1)
        case identifier(str_=str_,):
            return identifier(str_)
        case integer(int_=int_,):
            return integer(int_)
        case Program(fd=fd,):
            x0 = resolve_labels(fd, labels)

            # make sure each label has 1 goto and 1 label-stmnt 
            for label in labels.keys():
                num_gotos, num_labels = labels[label]
                # ERROR: num_labels > 1
                if num_labels > 1:
                    msg = f'resolve_labels: Function: label "{label}" occurs more than once'
                    error(msg)
                # ERROR: num_labels == 0
                if num_labels == 0:
                    msg = f'resolve_labels: Function: label "{label}" has a GOTO, but zero label-statements'
                    error(msg)
                # # error: num_gotos == 0
                # if num_gotos == 0:
                #     msg = f'resolve_labels: Function: label "{label}" has 0 gotos'
                #     error(msg)

            return Program(x0)
        case Return(exp_=exp_,):
            x0 = resolve_labels(exp_, labels)
            return Return(x0)
        case Expression(exp_=exp_,):
            x0 = resolve_labels(exp_, labels)
            return Expression(x0)
        case If(condition=condition,then_     =then_     ,else_     =else_     ,):
            x0 = resolve_labels(condition, labels)
            x1 = resolve_labels(then_    , labels)
            x2 = resolve_labels(else_    , labels) if else_ is not None else None
            return If(x0,x1,x2)
        case Null():
            return Null()
        case Declaration(name=name,init=init,):
            x0 = resolve_labels(name, labels)
            x1 = resolve_labels(init, labels) if init is not None else None
            return Declaration(x0,x1)
        case Constant(integer_=integer_,):
            x0 = resolve_labels(integer_, labels)
            return Constant(x0)
        case Unary(unary_operator_=unary_operator_,exp_=exp_,):
            x0 = resolve_labels(unary_operator_, labels)
            x1 = resolve_labels(exp_, labels)
            return Unary(x0,x1)
        case Binary(binary_operator_=binary_operator_,exp1=exp1,exp2=exp2,):
            x0 = resolve_labels(binary_operator_, labels)
            x1 = resolve_labels(exp1, labels)
            x2 = resolve_labels(exp2, labels)
            return Binary(x0,x1,x2)
        case Var(ident=ident,):
            x0 = resolve_labels(ident, labels)
            return Var(x0)
        case Assignment(kind=kind,exp1=exp1,exp2=exp2,):
            x0 = resolve_labels(kind, labels)
            x1 = resolve_labels(exp1, labels)
            x2 = resolve_labels(exp2, labels)
            return Assignment(x0,x1,x2)
        case Conditional(condition=condition,exp1=exp1,exp2=exp2,):
            x0 = resolve_labels(condition, labels)
            x1 = resolve_labels(exp1, labels)
            x2 = resolve_labels(exp2, labels)
            return Conditional(x0,x1,x2)
        case Complement():
            return Complement()
        case Negate():
            return Negate()
        case Not():
            return Not()
        case Increment():
            return Increment()
        case Decrement():
            return Decrement()
        case IncrementPost():
            return IncrementPost()
        case DecrementPost():
            return DecrementPost()
        case Add():
            return Add()
        case Subtract():
            return Subtract()
        case Multiply():
            return Multiply()
        case Divide():
            return Divide()
        case Remainder():
            return Remainder()
        case BitwiseAnd():
            return BitwiseAnd()
        case BitwiseOr():
            return BitwiseOr()
        case BitwiseXor():
            return BitwiseXor()
        case LeftShift():
            return LeftShift()
        case RightShift():
            return RightShift()
        case And():
            return And()
        case Or():
            return Or()
        case Equal():
            return Equal()
        case NotEqual():
            return NotEqual()
        case LessThan():
            return LessThan()
        case LessOrEqual():
            return LessOrEqual()
        case GreaterThan():
            return GreaterThan()
        case GreaterOrEqual():
            return GreaterOrEqual()
        case RegularAssignment():
            return RegularAssignment()
        case CompoundAssPlusEq():
            return CompoundAssPlusEq()
        case CompoundAssMinusEq():
            return CompoundAssMinusEq()
        case CompoundAssMultEq():
            return CompoundAssMultEq()
        case CompoundAssDivEq():
            return CompoundAssDivEq()
        case CompoundAssModEq():
            return CompoundAssModEq()
        case CompoundAssAndEq():
            return CompoundAssAndEq()
        case CompoundAssOrEq():
            return CompoundAssOrEq()
        case CompoundAssXorEq():
            return CompoundAssXorEq()
        case CompoundAssShlEq():
            return CompoundAssShlEq()
        case CompoundAssShrEq():
            return CompoundAssShrEq()
        case S(stmnt=stmnt,):
            x0 = resolve_labels(stmnt, labels)
            return S(x0)
        case D(decl=decl,):
            x0 = resolve_labels(decl, labels)
            return D(x0)
        case _:
            global e 
            e = node
            _type = type(node)
            msg = f'resolve_labels: Unknown type: {_type}'
            error(msg)





# # automatically generate replace_pseud
# # -----------------------------------------------------------------------------
# from zzz_pretty_printer_generator import file_2_recurse
# recurse = file_2_recurse(__file__)
# recurse = recurse.replace('recurse', 'resolve_labels')
# recurse = recurse.replace('_IN_TYPE_', 'exp')
# recurse = recurse.replace('_OUT_TYPE_', 'exp')
# print(recurse)





if __name__ == "__main__":
    l = lexer()
    my_exit_code = l.lex(source_)
    l.print()

    ast = parse_program(l.tokens)
    pretty_print(ast)

    _variable_map = {}
    ast2 = resolve(ast, _variable_map)
    pretty_print(ast2)

    resolve_labels(ast2, {})





