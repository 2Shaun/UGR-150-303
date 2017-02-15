#import pdb
#pdb.set_trace()

from pyparsing import Literal,CaselessLiteral,Word,Combine,Group,Optional,ZeroOrMore,Forward,nums,alphas

import timeit
import tkinter
import gmpy2
import math
import operator

start = timeit.default_timer()
exprStack = []
period = []

# BEGIN GUI
class MyGUI:
    def __init__(self):
        self.main_window = tkinter.Tk()
        self.preimage_frame = tkinter.Frame(self.main_window)
        self.generator_frame = tkinter.Frame(self.main_window)
        self.divisor_frame = tkinter.Frame(self.main_window)

        self.preimage_label = tkinter.Label(self.preimage_frame, \
                text='Pre-Image(x):')
        self.preimage_entry = tkinter.Entry(self.preimage_frame)

        self.generator_label = tkinter.Label(self.generator_frame, \
                text='Generator(phi):')
        self.generator_entry = tkinter.Entry(self.generator_frame)

        self.divisor_label = tkinter.Label(self.divisor_frame, \
                text='Divisor:')
        self.divisor_entry = tkinter.Entry(self.divisor_frame)

        self.generate_button = tkinter.Button(text='Generate')
        
        self.preimage_frame.pack()
        self.preimage_label.pack(side='left')
        self.preimage_entry.pack(side='right')
        self.generator_frame.pack()
        self.generator_label.pack(side='left')
        self.generator_entry.pack(side='right')
        self.divisor_frame.pack()
        self.divisor_label.pack(side='left')
        self.divisor_entry.pack(side='right')
        self.generate_button.pack(side='bottom')

        tkinter.mainloop()
# END GUI

# BEGIN PARSER
def pushFirst(strg, loc, toks):
    exprStack.append(toks[0])

def pushUMinus(strg, loc, toks):
    if toks and toks[0] == '-':
        exprStack.append('unary -')

bnf = None

def BNF():
    """
    expop   :: '^'
    multop  :: '*' | '/'
    addop   :: '+' | '-'
    integer :: ['+' | '-'] '0'..'9'+
    atom    :: PI | E | X | real | fn '(' expr ')' | expr ')'
    factor  :: atom [ expop factor ]*
    term    :: factor [ multop factor ]*
    expr    :: term [ addop term ]*
    """
    global bnf
    global image
    if not bnf:
        point   = Literal(".")
        e       = CaselessLiteral("E")
        x       = CaselessLiteral("X")
        fnumber = Combine(Word("+-" + nums, nums) +
                Optional(point + Optional(Word(nums))) +
                Optional(e + Word("+-" + nums, nums)))
        ident = Word(alphas, alphas + nums + "_$")

        plus    = Literal("+")
        minus   = Literal("-")
        mult    = Literal("*")
        div     = Literal("/")
        lpar    = Literal("(").suppress()
        rpar    = Literal(")").suppress()
        addop   = plus | minus
        multop  = mult | div
        expop   = Literal("^")
        pi      = CaselessLiteral("PI")

        expr    = Forward()
        atom    = (Optional("-") + (pi | e | x | fnumber | ident + lpar + expr + rpar).setParseAction(pushFirst) | (lpar + expr.suppress() + rpar)).setParseAction(pushUMinus)

        factor = Forward()
        factor << atom + ZeroOrMore((expop + factor).setParseAction(pushFirst))

        term = factor + ZeroOrMore((multop + factor).setParseAction(pushFirst))
        expr << term + ZeroOrMore((addop + term).setParseAction(pushFirst))
        bnf = expr
    return bnf

epsilon = 1e-12
opn = {
        "+" :   gmpy2.add,
        "-" :   operator.sub,
        "*" :   gmpy2.mul,
        "/" :   operator.truediv,
        "^" :   operator.pow
}

fn = {
        "sin"   : math.sin,
        "cos"   : math.cos,
        "tan"   : math.tan,
        "abs"   : abs,
        "trunc" : lambda a: int(a),
        "round" : round,
        "sgn"   : lambda a: abs(a) > epsilon and cmp(a,0) or 0
}

def evaluateStack(s, image):
    op = s.pop()
    if op == 'unary -':
        return evaluateStack(s, image)
    if op in "+-*/^":
        op2 = evaluateStack(s, image)
        op1 = evaluateStack(s, image)
        return opn[op](op1, op2)
    elif op == "PI":
        return math.pi
    elif op == "E":
        return math.e
    elif op == "X":
        return int(image)
    elif op in fn:
        return fn[op](evaluateStack(s, image))
    elif op[0].isalpha():
        return 0
    else:
        return int(op)
# END PARSER

# BEGIN LINKED LIST
class Node(object):
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node

    def __str__(self):
        return str(self.data)

    def get_data(self):
        return self.data

    def get_next(self):
        return self.next_node

    def set_next(self, new_next):
        self.next_node = new_next

class LinkedList(object):
    def __init__(self, head=None, tail=None):
        self.head = head
        self.tail = tail

    def __iter__(self):
        return self

    def next(self):
        current = self.head
        while current.get_next() != None:
            yield current
            current = current.get_next()

    def insert(self, data):
        new_node = Node(data)
        if self.head == None:
            self.head = new_node
        if self.tail != None:
            self.tail.next_node = new_node
        
        self.tail = new_node

    def tostring(self):
        current = self.head
        while current:
            print(current)
            current = current.get_next()

    def printList(self, iterations):
        current = self.head
        i = 0

        while current != None and i <= iterations:
            print(("{}").format(current.data), " ", end="") # end="" specifies no newline char
            current = current.get_next()
            i += 1
        print()
# END LINKED LIST

def generate(linkedlist, preimage, divisor, phi, iterations):
    #phi = preimage
    global exprStack
    exprstack = []
    results = BNF().parseString(phi)
    print(("first pre-image: {} divisor: {}").format(preimage, divisor))
    for i in range(iterations):
        #preimage = preimage**2
       #preimage = int(preimage % divisor)
       #preimage = int(gmpy2.powmod(preimage,2,divisor))
       moddedPreimage = int(gmpy2.f_mod(preimage, divisor))
       linkedlist.insert(moddedPreimage)
       preimage = int(evaluateStack(exprStack[:], preimage))

# BEGIN TORTOISE AND HARE
def findAndPrintPeriodicValues(linkedlist):
    tortoise = linkedlist.head.get_next()
    hare = linkedlist.head.get_next().get_next()
    while tortoise.get_data() != hare.get_data():
        tortoise = tortoise.get_next()
        hare = hare.get_next().get_next()
    preperiodicNodes = 0
    tortoise = linkedlist.head
    while tortoise.get_data() != hare.get_data():
        tortoise = tortoise.get_next()
        hare = hare.get_next()
        preperiodicNodes += 1
    print(("first periodic node: {} ").format(tortoise.get_data()))
    periodicity = 1
    hare = tortoise.get_next()
    while tortoise.get_data() != hare.get_data():
        hare = hare.get_next()
        periodicity += 1
    print(("pre-periodic nodes: {} periodicity: {}").format(preperiodicNodes, periodicity))
    linkedlist.printList(periodicity+preperiodicNodes);
    print(("pre-periodic nodes: {} periodicity: {}").format(preperiodicNodes, periodicity))
# END TORTOISE AND HARE

if __name__ == "__main__":
    import sys
    my_gui = MyGUI()
    modImageNodes = LinkedList()
    generate(modImageNodes, int(sys.argv[1]), int(sys.argv[2]), str(sys.argv[3]), int(sys.argv[4])) 
    # python program preimage divisor phi
    # modPhiNodes.printList()
    findAndPrintPeriodicValues(modImageNodes)

stop = timeit.default_timer()

print(("time: {0:.2f} s").format(stop - start ))
