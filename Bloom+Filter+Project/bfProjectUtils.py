# -*- coding: utf-8 -*-
"""
Bloom Filter Project utility functions - do not modify these functions!

If you find errors post to class piazza page.

"""
import time

# read srcFile into list of ints


def readIntFileDat(srcFile):
    strs = readFileDat(srcFile)
    res = []
    for line in strs:
        res.append((int)(line.strip()))
    return res

# read srcFile into list of strings


def readFileDat(srcFile):
    f = open(srcFile, 'r')
    src_lines = f.readlines()
    f.close()
    return src_lines

# write datList into fName file


def writeFileDat(fName, datList):
    f = open(fName, 'w')
    for item in datList:
        print>>f, item
    f.close()

# append record to existing file


def appendFileDat(fName, dat):
    f = open(fName, 'a+')
    print>>f, dat
    f.close()
# this will compare the contents of the resList with the data in baseFile
# and display performance


def compareResults(resList, configData):
    baseFileName = configData['valFileName']
    baseRes = readFileDat(baseFileName)
    if(len(baseRes) != len(resList)):
        print('compareFiles : Failure : Attempting to compare different size lists')
        return None
    numFail = 0
    numFTrueRes = 0
    numFFalseRes = 0
    for i in range(len(resList)):
        if (resList[i].strip().lower() != baseRes[i].strip().lower()):
            resVal = resList[i].strip().lower()
            baseResVal = baseRes[i].strip().lower()
            # uncomment this to see inconsistencies
            #print('i : ' + str(i) + ': reslist : ' + resVal + ' | baseres : ' + baseResVal)
            numFail += 1
            if resVal == 'true':
                numFTrueRes += 1
            else:
                numFFalseRes += 1
    if(numFail == 0):
        print('compareResults : Your bloom filter performs as expected')
    else:
        print(
            'compareResults : Number of mismatches in bloomfilter comared to validation file : ' +
            str(numFail) +
            '| # of incorrect true results : ' +
            str(numFTrueRes) +
            '| # of incorrect False results : ' +
            str(numFFalseRes))
    if((configData['studentName'] != '') and (configData['autograde'] == 2)):
        gradeRes = configData['studentName'] + ', ' + str(
            numFail) + ', ' + str(numFTrueRes) + ', ' + str(numFFalseRes)
        print('saving results for ' + gradeRes + ' to autogradeResult.txt')
        appendFileDat('autogradeResult.txt', gradeRes)


# this will process input configuration and return a dictionary holding
# the relevant info
def buildBFConfigStruct(args):
    bfConfigData = readFileDat(args.configFileName)
    configData = dict()
    for line in bfConfigData:
        # build dictionary on non-list elements
        if (line[0] == '#') or ('_' in line):
            continue
        elems = line.split('=')
        if('name' in elems[0]):
            configData[elems[0]] = elems[1].strip()
        else:
            configData[elems[0]] = int(elems[1])

    if ('Type 1' in configData['name']):
        configData['type'] = 1
        configData['seeds'] = buildSeedList(bfConfigData, int(configData['k']))

    elif ('Type 2' in configData['name']):
        configData['type'] = 2
        aListData = []
        bListData = []
        listToAppend = aListData
        for line in bfConfigData:
            if (line[0] == '#'):
                if ('b() seeds' in line):
                    listToAppend = bListData
                continue
            listToAppend.append(line)

        configData['a'] = buildSeedList(aListData, int(configData['k']))
        configData['b'] = buildSeedList(bListData, int(configData['k']))
    else:
        configData['type'] = -1
        print('unknown hash function specified in config file')

    configData['task'] = int(args.taskToDo)
    if configData['task'] != 2:
        # (int)(tOffLong & 0x7FFFFFFF);
        configData['genSeed'] = int(time.time()*1000.0) & 0x7FFFFFFF
        print('Random Time Seed is : ' + str(configData['genSeed']))

    configData['inFileName'] = args.inFileName
    configData['outFileName'] = args.outFileName
    configData['configFileName'] = args.configFileName
    configData['valFileName'] = args.valFileName
    configData['studentName'] = args.studentName
    configData['autograde'] = int(args.autograde)

    for k, v in configData.iteritems():
        print('Key = ' + k + ': Val = '),
        print(v)

    return configData


def buildSeedList(stringList, k):
    res = [0 for x in range(k)]
    for line in stringList:
        if ('_' not in line) or (line[0] == '#'):
            continue
        elems = line.split('=')
        araElems = elems[0].split('_')
        res[int(araElems[1])] = int(elems[1])
    return res


"""
    Function provided for convenience, to find next prime value from passed value
    Use this to find an appropriate prime size for type 2 hashes.

    Finds next prime value larger than n via brute force.  Checks subsequent numbers
    until prime is found - should be much less than 160 checks for any values
    seen in this project since largest gap g between two primes for any 32 bit
    signed int is going to be g < 336, and only have to check at most every
    other value in gap. For more, see this article :
        https://en.wikipedia.org/wiki/Prime_gap

    n  : some value
    return next largest prime
"""


def findNextPrime(n):
    if (n % 2 == 0):
        n += 1
    # n is odd here; 336 is larger than largest gap between 2 consequtive 32
    # bit primes
    for i in range(n, (n + 336), 2):
        if checkIfPrime(i):
            return i
    # error no prime found returns -1
    return -1


"""
    check if value is prime, return true/false
    n value to check
"""


def checkIfPrime(n):
    if (n < 2):
        return False
    if (n < 4):
        return True
    if ((n % 2 == 0) or (n % 3 == 0)):
        return False
    sqrtN = n**(.5)
    i = 5
    w = 2
    while (i <= sqrtN):
        if (n % i == 0):
            return False
        i += w
        # addresses mod2 and mod3 above, flip flops between looking ahead 2 and
        # 4 (every other odd is divisible by 3)
        w = 6-w
    return True
