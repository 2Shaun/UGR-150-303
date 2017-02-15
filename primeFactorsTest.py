def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:                           # the largest prime factor will never be greater than the square root
        if n % i:                               # if there is a remainder 
            i += 1                              # increment i
        else:                                   # if not, divide by the found factor and continue to factor the number
            n //= i                             # n floor divided by i then reassign value to n
            factors.append(i)                   # save the found factor into the array

    if n > 1:                                   # if n is still larger than 1
        factors.append(n)                       # it is prime, so it's only prime factor is itself 
    
    factorPowers = []

    j = 0
    savedFactor = 0
    for q in factors:
        if q == savedFactor:
            j -= 1
            factorPowers[j][1] += 1
            j += 1
            continue
        else:
            factorPowers.append([])
            factorPowers[j].append(q)
            factorPowers[j].append(1)
            j += 1
            savedFactor = q
    for d in factorPowers:
        print d

prime_factors(28224)

#ALGORITHM FOR 2D LIST
# j = 0                                  iterator
# savedFactor                            variable to hold previous loop's factor, this works because duplicate factors are grouped in output
# for q in factors
#   if q == saved                        if current factor is the same as last loop's factor
#       factorPowers[j][1]++             the power that the factor must be raised to is contained in the 1st index of the inner list
#       continue                         check next factor without appending anything
#   else
#       factorPowers.append([])          add a new list to hold factor and powers
#       factorPowers[j][0].append(q)     must be a new factor so it must be appended to the 0th index of the inner list
#       factorPowers[j][1] = 1           raised to the 1st power
