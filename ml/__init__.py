#-*- coding=utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

"""Count words."""

def count_words(s, n):
    """Return the n most frequently occuring words in s."""

    # TODO: Count the number of occurences of each word in s
    items = s.split(" ")
    counter = {}
    for word in items:
        if counter.has_key(word):
            counter[word] = counter[word] + 1
        else:
            counter[word] = 1
    # TODO: Sort the occurences in descending order (alphabetically in case of ties)
    wordAndCount = sorted(counter.items(),cmp=lambda x,y: cmp(y[1],x[1]) or cmp(x[0],y[0]))
    # TODO: Return the top n words as a list of tuples (<word>, <count>)
    return wordAndCount[0:n]


def test_run():
    """Test count_words() with some inputs."""
    print count_words("cat bat mat cat bat cat", 3)
    print count_words("betty bought a bit of butter but the butter was bitter", 3)


if __name__ == '__main__':
    test_run()
