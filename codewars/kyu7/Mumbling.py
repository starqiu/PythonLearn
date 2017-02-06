import Test


def accum(s):
    arr = []
    if len(s) <= 0:
        return s
    else:
        for i, c in zip(range(1, len(s) + 1), s):
            arr.append((c * i).capitalize())
    return '-'.join(arr)


def disemvowel(s):
    for x in 'aoeiuAOEIU':
        s = s.replace(x, '')
    return s


def to_weird_case(s):
    return ' '.join(''.join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(x)) for x in s.split(' '))


def longest_consec(strarr, k):
    n = len(strarr)
    if n == 0 or k > n or k <= 0:
        return ""
    len_arr = [len(x) for x in strarr]
    len_sum_with_index_arr = []
    for i in range(0, n - k + 1):
        len_sum_with_index_arr.append((i,sum(len_arr[i:i+k])))
    len_sum_with_index_arr = sorted(len_sum_with_index_arr, key= lambda x: x[1], reverse=True)
    start_index = len_sum_with_index_arr[0][0]
    return ''.join(strarr[start_index:start_index + k])

def is_triangle(a, b, c):
    if a <=0 or b<=0 or c<=0:
        return False
    else:
        sorted_arr = sorted([a,b,c])
        return a+b>c

def digital_root(n):
    while(len(str(n))>1):
        n = sum(int(x) for x in str(n))
    return n


def longest_palindrome(s):
    if s is None or len(s)==0:
        return 0
    longest_count = 1

    l = len(s)
    for i, c in enumerate(s):# longest_palindrome is odd
        cur_count = 1
        loop = 1
        while i-loop >= 0 and i+loop < l:
            if s[i-loop] == s[i+loop]:
                cur_count += 2
                loop += 1
            else:
                break
        longest_count = cur_count if cur_count>longest_count else longest_count
    for i, c in enumerate(s):# longest_palindrome is even
        cur_count = 0
        loop = 1
        while i-loop+1 >= 0 and i+loop < l:
            if s[i-loop+1] == s[i+loop]:
                cur_count += 2
                loop += 1
            else:
                break
        longest_count = cur_count if cur_count>longest_count else longest_count
    return longest_count

def sum_pairs(ints, s):
    res = None
    l = len(ints)
    if l <= 2:
        return res

    ints_map ={}
    ints_rm_dup = []
    for m in ints:
        if ints_map.has_key(m):
            if ints_map[m] < 2:
                ints_rm_dup.append(m)
                ints_map[m] += 1
        else:
            ints_map[m] = 1
            ints_rm_dup.append(m)
    ints = ints_rm_dup

    for i, a in enumerate(ints):
        diff = s - a
        for li, x in enumerate(ints[i+1::], i+1):
            if diff == x:
                res = sum_pairs(ints[i+1:li], s)
                if res is None:
                    return [a, x]
                else:
                    return res
    return res

l5 = [10, 5, 2, 3, 7, 5]
print sum_pairs(l5, 10)
# print is_triangle(7, 2, 2)
#
# print longest_consec(["zone", "abigail", "theta", "form", "libe", "zas"], 2)
#
# print 'aadb'.replace(r'[a]+', 'A')
