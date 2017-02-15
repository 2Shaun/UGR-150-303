print "Sophie Germain Periods:"
for q in range(1,12):
    print "MOD ",
    print q,
    print ": ",
    for i in 1,4,10,3,4,12,20,10,3,12:
        print i % q,
    print


print "Safe Prime Periods:"
for q in range(1,28):
    print "MOD ",
    print q,
    print ": ",
    for i in 4,10,11,28,20,52,82,11,28,130:
        print i % q,
    print
