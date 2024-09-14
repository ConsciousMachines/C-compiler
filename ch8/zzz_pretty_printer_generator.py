
from common import _counter, make_temporary

# ---------- P R E T T Y   P R I N T E R   G E N E R A T O R
# exception: integer
# exception: identifier
# exception: Function body


# text = '''
# '''

# read file and get the text which describes the classes
def read_class_definition(file_path):

    # read the file 
    with open(file_path, 'r') as f:
        content = f.read()

    # the class definitions we want to pretty-print are between these two lines:
    # --- BEGIN CLASS DEFINITION
    # --- END CLASS DEFINITION
    text = content.split('# --- BEGIN CLASS DEFINITION')[1].split('# --- END CLASS DEFINITION')[0]
    return text

# get the class names and members, from the text
def get_class_names_and_members(text):
        
    lines = text.split('\n')

    i = 0 
    results = []
    while i < len(lines):
        line = lines[i]
        j = i # use j to check out the lines ahead
        # state 0: we are in a class definition
        if line[:5] == 'class':
            members = []
            class_name = line[6:].split(':')[0].split('(')[0]
            # get next line
            j += 1 
            line = lines[j]
            # state 1: we are in def __init__
            if line.strip()[:12] == 'def __init__':
                # collect all the members that start with self.<member>
                while True:
                    # get next line
                    j += 1        
                    line = lines[j]
                    if line[:13] != '        self.':
                        break
                    else:
                        member = line[13:].split('=')[0].split(':')[0]
                        members.append(member)
            results.append((class_name, members))
        i += 1
    return results 

# generate pretty printer from list of classes and their members
def generate_pretty_printer(results):

    _prologue = '''
def pretty_print(node:_IN_TYPE_, depth=0) -> None:
    match node:'''
    _epilogue = '''        case _:
            global e 
            e = node
            _type = type(node)
            msg = f'pretty_print: Unknown type: {_type}'
            error(msg)
'''

    all_lines = []
    for i, (class_name, members) in enumerate(results):

        # print prologue
        if i == 0:
            all_lines.append(_prologue)

        # remove prefix from class name, if any
        if '_' in class_name: # remove cg_ prefix, not in AST
            _class_name = class_name.split('_')[1]
        else:                 # if no prefix, leave as is, we are in AST
            _class_name = class_name

        # print the code
        args = ''
        for member in members:
            args += f'{member}={member},'
        line1 = f'        case {class_name}({args}):'
        line2 = f'            print(depth*" " + "{_class_name}")'
        lines = [line1, line2]
        for member in members:
            line = f'            pretty_print({member}, depth+4) if {member} is not None else None'
            lines.append(line)

        # exception: identifier / integer types
        if _class_name in ['identifier', 'integer']:
            line1 = f'            print(depth*" " + f"{_class_name}({{{members[0]}}})")'
            lines = [lines[0], line1] # keep only the 'case' line

        if _class_name in ['Block']:
            line3 = f'            for i in {members[0]}:'
            line4 = f'                pretty_print(i, depth+4) if i is not None else None'
            lines = [lines[0], lines[1], line3, line4]

        for line in lines:
            all_lines.append(line)

        # print epilogue
        if i == len(results)-1:
            all_lines.append(_epilogue)

    result = '\n'.join(all_lines)
    return result

# wrapper to make pp
def file_2_pp(file_path):

    text      = read_class_definition(file_path)
    results   = get_class_names_and_members(text)

    # for _class, _members in results:
    #     print(_class)
    #     for _member in _members:
    #         print('\t', _member)

    pp = generate_pretty_printer(results)
    return pp


# file_path = '/home/chad/Desktop/_backups/notes/projects/nora_compiler/ch3/parser.py'
# pp = file_2_pp(file_path)
# print(pp)







# ---------- R E C U R S I V E   W A L K   G E N E R A T O R
# exception: integer
# exception: identifier
# exception: Function body




# generate pretty printer from list of classes and their members
def generate_recursive_walk(results):

    _prologue = '''
def recurse(node:_IN_TYPE_) -> _OUT_TYPE_:
    match node:'''
    _epilogue = '''        case _:
            global e 
            e = node
            _type = type(node)
            msg = f'recurse: Unknown type: {_type}'
            error(msg)
'''

    all_lines = []
    for i, (class_name, members) in enumerate(results):

        # print prologue
        if i == 0:
            all_lines.append(_prologue)

        # remove prefix from class name, if any
        if '_' in class_name: # remove cg_ prefix, not in AST
            _class_name = class_name.split('_')[1]
        else:                 # if no prefix, leave as is, we are in AST
            _class_name = class_name

        # print the code
        _counter.reset()
        args = ''
        arguments = []
        for member in members:
            args += f'{member}={member},'
        line1 = f'        case {class_name}({args}):'
        lines = [line1]
        for member in members:
            argument = f'x{make_temporary()}'
            line = f'            {argument} = recurse({member}) if {member} is not None else None'
            lines.append(line)
            arguments.append(argument)
        line_last = f'            return {class_name}({",".join(arguments)})'
        lines.append(line_last)

        # exception: identifier / integer types
        if _class_name in ['identifier', 'integer']:
            lines = [lines[0]] # keep only the 'case' line
            line = f'            return {class_name}({members[0]})'
            lines.append(line)

        # Function
        if _class_name in ['Function']:
            line1 = f'            x1 = [recurse(i) for i in instructions]'
            _ = lines.pop(-2)
            lines.insert(-1, line1)

        for line in lines:
            all_lines.append(line)

        # print epilogue
        if i == len(results)-1:
            all_lines.append(_epilogue)

    result = '\n'.join(all_lines)
    return result


# wrapper to make recurse
def file_2_recurse(file_path):

    text      = read_class_definition(file_path)
    results   = get_class_names_and_members(text)
    recurse   = generate_recursive_walk(results)
    return recurse



# file_path = '/home/chad/Desktop/_backups/notes/projects/nora_compiler/ch3/parser.py'
# pp = file_2_recurse(results)
# print(pp)


