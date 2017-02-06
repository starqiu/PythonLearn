from math import sqrt
import random
from Test import test

def is_square(n):
    if n < 0:
        return False
    sqrt_n = int(sqrt(n))
    return n == sqrt_n ** 2



test.describe("is_square")
# test.it("should work for some examples")
test.expect(not is_square(-1), "Negative numbers cannot be square numbers")
test.expect(not is_square( 3))
test.expect(    is_square( 4))
test.expect(    is_square(25))
test.expect(not is_square(26))

# test.it("should work for random square numbers")
for i in range(1,100):
    r = random.randint(0, 0xfff0)
    test.expect(is_square(r * r), "{number} is a square number".format(number=(r * r)))
