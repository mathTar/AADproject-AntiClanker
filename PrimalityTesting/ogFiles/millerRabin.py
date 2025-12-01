import math
import random
import time
import sys
from trialDiv import eGcd

#implementaion caveat: test is defined only for co-prime a (bases)
# if a is not co-prime to num, num is composite - we can use this for practical purposes!

# ANALYZE SYSRANDOM - cryptographic security for bases? + uniform randomness

def isPrime(num, k):
    startTime = time.time()
    if num <= 1:
        return False, 0
    if num <= 3:
        return True, 0
    if num % 2 == 0:
        return False, 0
    #n-1 = t * 2**s 
    s,t = 0, num-1
    while t%2 == 0:
        s+=1
        t//=2
    for _ in range(k):
        a = random.SystemRandom().randint(2, num - 2)
        if eGcd(num, a) != 1:
            return False, time.time() - startTime #composite number so not co-prime with a
        x = pow(a, t, num)
        #series of x: a^t, a^(2t), a^(4t), ..., a^(2^s * t) (mod num)
        if x == 1 or x == num-1: #if a^t = 1 or -1 (mod num), then all terms will be 1 or -1 - prime for sure
           continue
        for _ in range(s-1):
            x = (x*x)%num
            if x == num-1: #if any term is -1 (mod num), then num is probably prime - all terms after are square - so 1 at a^(n-1)
                break
        else: #if we dont reach -1 at some point at all - composite (last term is a^(n-1) was not -1)
            return False, time.time() - startTime
    return True, time.time() - startTime

print(isPrime(741, 190))