

# global compiler variables
# -----------------------------------------------------------------------------
my_exit_code = 0
# -----------------------------------------------------------------------------

# --- E R R O R 
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def error(msg:str):
    print(msg)
    # global my_exit_code
    my_exit_code = 1 
    raise Exception(msg)

# --- C O U N T E R
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

class counter:
    def __init__(self):
        self.v = 0
    def increment(self):
        ret = self.v
        self.v += 1
        return ret
    def reset(self):
        self.v = 0

_counter = counter()
_counter.reset()
make_temporary = lambda: str(_counter.increment())

# --- S O U R C E 
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------



source_ = '''
int main(void) {
    int sum = 0;
    int counter;
    for (int i = 0; i <= 10; i = i + 1) {
        counter = i;
        if (i % 2 == 0)
            continue;
        sum = sum + 1;
    }

    return sum == 5 && counter == 10;
}

'''

source_ = '''
int main(void) {
    int a = 420;
    do 
    {
        a = a - 1;
    }
    while (a > 0);
    return a;
}

'''
