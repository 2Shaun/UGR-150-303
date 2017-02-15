primes = [True for i in range(5000)]

primes[0] = primes[1] = False

for i in range(71):
    if primes[i] == True:
        for n in range(i*i, 5000, i):
             primes[n] = False

def primeFactors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)

    if n > 1:
        factors.append(n)

    factorPowers = []

    j = 0
    savedFactor = 0
    for q in factors:
        if q == savedFactor:
            j -= 1
            factorPowers[j][1] += 1
            j += 1                                                          # can't think of a better way to avoid OOB error right now
            continue
        else:
            factorPowers.append([])
            factorPowers[j].append(q)
            factorPowers[j].append(1)
            j += 1
            savedFactor = q
    print "k = ",
    for d in factorPowers:
        print d,
    print
             
for i, integer in enumerate(primes):
    if i >= 2 and integer == True:
        #if integer == True:
        j = 0
        q = 0
        while (2**j) < (i):
            j += 1
            if i % 2**j == 1:
                q = i / 2**j
            else:
                j -= 1
                break
        
        print "%d = %d * (2,%d) + 1 \t\t\t\t\t" % (i, q, j),                 # also print factors of q
        primeFactors(q)
        

def primeGenerator(n):
    i = j = 0
    while i < n:
        if primes[j] == True:
            i += 1
            yield j
            j += 1
        else:
            j += 1

class PrimeIterator(object):
    def __init__(self, low, high):
        self.current = low
        self.high = high

    def __iter__(self):
        return self

    def __next__(self):
        if self.current > self.high:
            raise StopIteration
        else:
            self.current += 1
            return self.current - 1

# List all possible k * 2^n + 1 equations for each prime
# List factors of k
# create a list of k's which contain similar factors
