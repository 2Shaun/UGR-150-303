#import pdb
#pdb.set_trace()

from pyparsing import Literal,CaselessLiteral,Word,Combine,Group,Optional,ZeroOrMore,Forward,nums,alphas

import timeit
import gmpy2
import math
import operator
import numpy as np
import matplotlib.pyplot as plt

global exprStack
global start
global periodic
global preperiodic
global tortoise
global hare
global elements
start = timeit.default_timer()
global results
periodic = []
elements = []
preperiodic = []

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

class Node(object):
    def __init__(self, data=None, next_node=None, position=0):
        self.data = data
        self.next_node = next_node
        self.position = position

    def __str__(self):
        return str(self.data)

    def get_data(self):
        return self.data

    def get_next(self):
        return self.next_node

    def get_position(self):
        return self.position

    def set_next(self, new_next):
        self.next_node = new_next

    def set_position(self, new_position):
        self.position = new_position

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
            self.tail.next_node.set_position(self.tail.get_position()+1)

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
            print(("{}").format(current.data), " ", end="")
            current = current.get_next()
            i += 1
        print()

def generate(linkedlist, preimage, divisor):
    #phi = preimage
    global tortoise
    global hare

    elements.append(preimage)
    moddedPreimage = int(gmpy2.f_mod(preimage, divisor))
    linkedlist.insert(moddedPreimage)
    preimage = int(evaluateStack(exprStack[:], preimage))   # iteration
    elements.append(preimage)
    moddedPreimage = int(gmpy2.f_mod(preimage, divisor))    # image
    linkedlist.insert(moddedPreimage)
    tortoise = linkedlist.head.get_next()
    preimage = int(evaluateStack(exprStack[:], preimage))
    elements.append(preimage)
    moddedPreimage = int(gmpy2.f_mod(preimage, divisor))
    linkedlist.insert(moddedPreimage)
    hare = linkedlist.head.get_next().get_next()
    for i in range(divisor*2):
        #preimage = preimage**2
        #preimage = int(preimage % divisor)
        #preimage = int(gmpy2.powmod(preimage,2,divisor))
        preimage = int(evaluateStack(exprStack[:], preimage))
        elements.append(preimage)
        moddedPreimage = int(gmpy2.f_mod(preimage, divisor))
        linkedlist.insert(moddedPreimage)
        if i > 1 and i % 9 == 0 and findPeriod(linkedlist) == True:
            periodFound = True
            return True
    return False

def findStrictlyPrePeriodicNodes(divisor, periodic):
    # if image is in periodic list, then it is preperiodic
    # if it is not, then period finder needs to be ran again
    possiblyPrePeriodic = []
    for i in range(divisor):
        if i in periodic:
            continue
        possiblyPrePeriodic.append(i)

    for i in possiblyPrePeriodic:
        image = int(evaluateStack(exprStack[:], i))
        moddedImage = int(gmpy2.f_mod(image, divisor))
        if moddedImage in periodic:
            preperiodic.append(i)


def findPeriod(linkedlist):
    # find period
    # go back to find first occurrence of period
    # shift periodic array so that it reflects correct order
    # get position, find associated element
    # for loop
    #   plot(periodic(i), element(position))
    global tortoise
    global hare
    while tortoise.get_data() != hare.get_data():
        if hare.get_next().get_next() == None or tortoise.get_next() == None:
            tortoise = linkedlist.head.get_next()
            hare = linkedlist.head.get_next().get_next()
            return False
        tortoise = tortoise.get_next()
        hare = hare.get_next().get_next()
    tortoise = linkedlist.head
    while tortoise.get_data() != hare.get_data():
        if hare.get_next() == None or tortoise.get_next() == None:
            tortoise = linkedlist.head.get_next()
            hare = linkedlist.head.get_next().get_next()
            return False
        tortoise = tortoise.get_next()
        hare = hare.get_next()
    periodic.append(tortoise.get_data())
    plt.plot(periodic[len(periodic)-1],elements[tortoise.get_position()])
    hare = tortoise.get_next()
    while tortoise.get_data() != hare.get_data():
        periodic.append(hare.get_data())
        plt.plot(periodic[len(periodic)-1],elements[hare.get_position()], 'bo')
        hare = hare.get_next()
    periodic.append(hare.get_data())
    return True

if __name__ == "__main__":
    import sys
    modImageNodes = LinkedList()
    exprStack = []
    results = BNF().parseString(str(sys.argv[3]))
    print(("first pre-image: {} divisor: {}").format(sys.argv[1], sys.argv[2]))
    print('Periodic: ')
    if (generate(modImageNodes, int(sys.argv[1]), int(sys.argv[2]))) == True:
        print(periodic)
    print('Strictly PrePeriodic: ')
    findStrictlyPrePeriodicNodes(int(sys.argv[2]), periodic)
    print(preperiodic)
    plt.show()
    # python program preimage divisor phi
    # modPhiNodes.printList()

stop = timeit.default_timer()                   # time 

print(("time: {0:.2f} s").format(stop - start )) # print time
