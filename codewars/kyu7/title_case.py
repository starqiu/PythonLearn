import Test
def title_case(title, minor_words=''):
    minor_set = set(minor_words.lower().split(' '))
    if len(title) <= 0:
        return title
    title_arr = title.lower().split(' ')
    title_case_arr = []
    for t in title_arr:
        if t not in minor_set:
            title_case_arr.append(t.capitalize())
        else:
            title_case_arr.append(t)
    # title_case_arr[0] = title_case_arr[0].capitalize()
    return ' '.join(title_case_arr)

def title_case_best(title, minor_words=''):
    minor_set = set(minor_words.lower().split(' '))
    title_arr = title.capitalize().split(' ')
    return ' '.join([t if t in minor_set else t.capitalize() for t in title_arr])

print title_case_best('THE WIND IN THE WILLOWS', 'The In')
# Test.assert_equals(title_case(''), '')
# Test.assert_equals(title_case('a clash of KINGS', 'a an the of'), 'A Clash of Kings')
# Test.assert_equals(title_case('THE WIND IN THE WILLOWS', 'The In'), 'The Wind in the Willows')
# Test.assert_equals(title_case('the quick brown fox'), 'The Quick Brown Fox')