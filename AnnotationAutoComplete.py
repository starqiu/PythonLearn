# coding=utf-8

import sys

reload(sys)  # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')
from optparse import OptionParser


class Trie1:
    root = {}
    END = '/'

    def add(self, word):
        # 从根节点遍历单词,char by char,如果不存在则新增,最后加上一个单词结束标志
        node = self.root
        for c in word:
            node = node.setdefault(c, {})
        node[self.END] = None

    def find(self, word):
        node = self.root
        for c in word:
            if c not in node:
                return False
            node = node[c]
        return self.END in node

def nomalizeWord(word):
    if word is None:
        return None
    word = word.strip().upper()

    # 去掉前缀，如R_SFZH => SFZH
    ind = word.find('_')
    if ind >= 0:
        word = word[ind+1:]

    if word == '':
        word = None

    return word


class Trie:
    root = {}
    END = '/'
    outputSep = '\t'

    def add(self, word, desc):
        word = nomalizeWord(word)
        # 从根节点遍历单词,char by char,如果不存在则新增,最后加上一个单词结束标志
        node = self.root
        for c in word:
            node = node.setdefault(c, {})
        if not node.has_key(self.END):
            node[self.END] = set()
        node[self.END].add(desc)

    def find(self, word, depth=0):
        if word is None:
            return None
        node = self.root
        for c in word:
            if c not in node:
                return None
            node = node[c]
        if depth == 0:
            annotation = node.get(self.END)
            if annotation is None:
                return None
            else:
                return self.outputSep.join(annotation)
        else:
            node.keys()

    def addResource(self, path):
        arr = []
        f = open(path)
        for line in f.readlines():
            try:
                arr = line.strip().split("\t", 2)
                self.add(arr[0], arr[1])
            except Exception, e:
                print e
                print "Error: " + line
        f.close()

    def __init__(self, sep='\t', *paths):
        self.outputSep = sep
        for path in paths:
            self.addResource(path)

def main():
    parser = OptionParser()
    parser.add_option("-t", "--inputType", dest="inputType", action="store", type="string", default=0,
                      help="输入类型 0为字符串，1表示文件")
    parser.add_option("-i", "--inputValue", dest="inputValue", action="store", type="string", metavar="FILE",
                      help="输入值，字符串或是文件，跟输入类型保持一致")
    parser.add_option("-s", "--outputSep", dest="outputSep", action="store", type="string", default="\001",
                      help="多条输出的连接符")
    parser.add_option("-f", "--trainFiles", dest="trainFiles", action="store", type="string",
                      help="一个或多个训练文件，以;连接")
    parser.add_option("-o", "--outputPath", dest="outputPath", action="store", type="string", metavar="FILE",
                      help="结果输出文件")

    if len(sys.argv) <= 1:  # 没有参数时
        parser.print_help()
        return
    options, args = parser.parse_args()
    print options
    inputType = int(options.inputType)
    inputValue = options.inputValue
    trainFiles = options.trainFiles.split(";")
    outputPath = options.outputPath
    outputSep = options.outputSep

    trie = Trie(outputSep, *trainFiles)

    outputValue = getAnnotation(trie, inputType, inputValue)

    saveOrPrintAnnotation(outputValue, outputPath)


def saveOrPrintAnnotation(outputValue, outputPath=None):
    if len(outputValue) > 0:
        if outputPath is None:
            print outputValue
        else:
            outputFile = open(outputPath, 'w')
            for line in outputValue:
                outputFile.write(line)
                outputFile.write('\n')
            outputFile.close()
    else:
        print "no annotation matches"


def getAnnotation(trie, inputType, inputValue):
    outputValue = []
    if inputType == 0:
        nomalizeValue = nomalizeWord(inputValue)
        tmpRes = trie.find(nomalizeValue)
        if tmpRes is None:
            print "Error: can't find annotation, inputVaule = " + inputValue
        else:
            outputValue.append(tmpRes)
    elif inputType == 1:
        inputFile = open(inputValue)
        for line in inputFile:
            nomalizeValue = nomalizeWord(line)
            if line is None:
                pass
            tmpRes = trie.find(nomalizeValue)
            if tmpRes is None:
                print "Error: can't find annotation, inputVaule = " + line
            else:
                outputValue.append(line + "\002" + tmpRes)
        inputFile.close()
    else:
        print "Error input type, exit"
        exit(-1)
    return outputValue


if __name__ == '__main__':
    # w = nomalizeWord('R_DD_SS')
    #
    # print w
    main()
    # OUTPUT_SPLIT = "\001"
    # trie = Trie("E:\\test\dictionary.csv", "E:\\test\other.csv")
    # # trie.addResource("E:\\test\other.csv")
    # # trie = Trie()
    #
    # # f = open("E:\\test\dictionary.csv")
    # #
    # # arr = []
    # # for line in f.readlines():
    # #     try:
    # #         arr = line.strip().split("\t", 2)
    # #         trie.add(arr[0], arr[1])
    # #     except Exception, e:
    # #         print e
    # #         print "Error: " + line
    #
    # results = trie.find("SFZH")
    # if results is None:
    #     print "Error: can't find annotation"
    # else:
    #     print OUTPUT_SPLIT.join(results)
