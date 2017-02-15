from pyparsing import Literal,CaselessLiteral,Word,Combine,Group,Optional,ZeroOrMore,Forward,nums,alphas

import timeit
import gmpy2
import math
import operator

start = timeit.default_timer()
exprStack = []

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
        return long(image)
    elif op in fn:
        return fn[op](evaluateStack(s, image))
    elif op[0].isalpha():
        return 0
    else:
        return long(op)
# END PARSER

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
            print current
            current = current.get_next()

    def printList(self, iterations):
        current = self.head
        i = 0

        while current != None and i <= iterations:
            print "%d" % current.data,
            current = current.get_next()
            i += 1
        print

def generate(linkedlist, preimage, divisor, phi, iterations):
    #phi = preimage
    global exprStack
    exprstack = []
    results = BNF().parseString(phi)
    print "first pre-image: %d divisor: %d" % (preimage, divisor)
    for i in range(iterations):
        #preimage = preimage**2
       #preimage = long(preimage % divisor)
       #preimage = long(gmpy2.powmod(preimage,2,divisor))
       moddedPreimage = long(gmpy2.f_mod(preimage, divisor))
       linkedlist.insert(moddedPreimage)
       preimage = long(evaluateStack(exprStack[:], preimage))

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
    print "first periodic node: %d " % tortoise.get_data(),
    periodicity = 1
    hare = tortoise.get_next()
    while tortoise.get_data() != hare.get_data():
        hare = hare.get_next()
        periodicity += 1
    print "pre-periodic nodes: %d periodicity: %d" % (preperiodicNodes, periodicity)
    linkedlist.printList(periodicity+preperiodicNodes);
    print "pre-periodic nodes: %d periodicity: %d" % (preperiodicNodes, periodicity)

if __name__ == "__main__":
    import sys
    modImageNodes = LinkedList()
    generate(modImageNodes, long(sys.argv[1]), long(sys.argv[2]), str(sys.argv[3]), int(sys.argv[4])) 
    # python program preimage divisor phi
    #modPhiNodes.printList()
    findAndPrintPeriodicValues(modImageNodes)

stop = timeit.default_timer()

print "time: %.2f s" % (stop - start )