

if __name__ == '__main__':
    import sys, getopt, parser
    lowerBound = 0
    upperBound = 0
    lowerBound = sys.argv[1]
    upperBound = sys.argv[2]
    function = sys.argv[3]

    function = parser.expr(function)
    function = parser.st2list(function)
    print function
    print 'lower bound: ', lowerBound, 'upper bound: ', upperBound
    
    print 'Number of Arguments: ', len(sys.argv), 'arguments.'
    print 'Argument List:', str(sys.argv)
    
# getopt.getopt(args, options, [long_options])
# args - list of arguments
# options - option characters 
# long options - option strings
