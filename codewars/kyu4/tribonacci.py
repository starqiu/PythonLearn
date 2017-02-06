def tribonacci(signature, n):
    if n <= 0:
        return []
    else:
        while len(signature) < n:
            print signature[-3:]
            signature.append(reduce(lambda x, y: x + y, signature[-3:], 0))
        return signature[0:n]


print tribonacci([1, 2, 3], 5)
