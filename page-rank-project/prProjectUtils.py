# -*- coding: utf-8 -*-
"""
Utility functions - do not modify these functions!

If you find errors post to class piazza page.

"""
import time
import os
#useful structure to build dictionaries of lists
from collections import defaultdict

########################################
#IO and Util functions  

#returns sorted version of l, and idx order of sort
def getSortResIDXs(l, rev=True):
    from operator import itemgetter  
    return zip(*sorted([(i,e) for i,e in enumerate(l)], 
                        key=itemgetter(1),reverse=rev))


#read srcFile into list of ints 
def readIntFileDat(srcFile):
    strs = readFileDat(srcFile)
    res = [int(s.strip()) for s in strs]
    return res

#read srcFile into list of floats 
def readFloatFileDat(srcFile):
    strs = readFileDat(srcFile)
    res = [float(s.strip()) for s in strs]
    return res

#read srcFile into list of strings
def readFileDat(srcFile):
    try:
        f = open(srcFile, 'r')
    except IOError:
        #file doesn't exist, return empty list
        print('Note : {} does not exist in current dir : {}'.format(srcFile, os.getcwd()))
        return []
    src_lines = f.readlines()
    f.close()
    return src_lines

#write datList into fName file
def writeFileDat(fName, datList):
    f = open(fName, 'w')
    for item in datList:
        print>>f, item
    f.close()
    
#append record to existing file
def appendFileDat(fName, dat):
    f = open(fName, 'a+')
    print>>f, dat
    f.close()

########################################
#Page Rank Functions  

    
#get file values for particular object and alpha value 
#results are list of nodes, list of rank values and dictionary matching node to rank value
#list of nodes and list of rank values are sorted
def getResForPlots(prObj, alpha):
    outFileName = makeResOutFileName(prObj.inFileName, alpha, prObj.selfLoops) 
    vNodeIDs_unsr, vRankVec_unsr = loadRankVectorData(outFileName, isTest=False)
    #build dictionary that links node id to rank value
    vNodeDict = buildValidationDict(vNodeIDs_unsr,vRankVec_unsr) 
    
    #build sorted list          
    vNodeIDs, vRankVec = getSortResIDXs(vRankVec_unsr)    
    return vNodeIDs, vRankVec, vNodeDict

#build appropriate results file name based on passed input name, alpha and sink handling flag
def makeResOutFileName(inFileName,alpha,selfLoops):
    nameList = inFileName.strip().split('.')
    namePrefix = '.'.join(nameList[:-1])
    #build base output file name based on input file name and whether or not using selfloops to handle sinks
    outFileName = "{}_{}_{}.{}".format(namePrefix,("SL" if selfLoops else "T3"), alpha,nameList[-1])
    return outFileName     

#builds output file names given passed file name
def buildOutFNames(fName, getVerifyNames=False):
    #list of file name suffixes used in pagerank project to denote file type :
    # output : file holding rank vector values (floats)
    # rank : file holding node id (ints) in order of rank
    # verifyRVec : verification file provided to student to check rank vector values (may not match because of float errors)
    # verifyRanks : verification file provided to student to check node order of rank vector    
    _fileNameSfxs=['outputPR', 'rankingsPR', 'verifyRVec', 'verifyRanks']
    
    #construct ouput file names based on fName (which is input file name : i.e. 'inputstuff.txt')
    #builds 'inputstuff-ranks.txt' for rank ordering and 'inputstuff-output.txt' for rank vector values
    nameList = fName.strip().split('.')
    #name without extension
    namePrefix = '.'.join(nameList[:-1])
    if getVerifyNames :
        #get names for verification files
        #file holding node ids in order of rank
        vrankFName = '{}-{}.{}'.format(namePrefix, _fileNameSfxs[3],nameList[-1])
        #file holding rank vector values
        voutFName = '{}-{}.{}'.format(namePrefix, _fileNameSfxs[2],nameList[-1])
        return vrankFName, voutFName
    else :
        #names for saving results or accessing saved results
        #file holding node ids in order of rank
        rankFName = '{}-{}.{}'.format(namePrefix, _fileNameSfxs[1],nameList[-1])
        #file holding rank vector values
        outFName = '{}-{}.{}'.format(namePrefix, _fileNameSfxs[0],nameList[-1])
        return rankFName, outFName

    
#this will build a dictionary with :
#   keys == graph nodes and 
#   values == list of pages accessible from key
#   and will also return a list of all node ids
#   using terminology from lecture, this builds the "out list" for each node in 
#   file, and a list of all node ids
def loadGraphADJList(fName):
    #defaultDict has 0/empty list entry for non-present keys,  
    #does not return invalid key error
    resDict = defaultdict(list)
    filedat = readFileDat(fName)
    allNodesSet = set()
    #each line has a single number, followed by a colon, followed by a list of 
    #1 or more numbers spearated by commas
    #these represent node x : reachable nodes from node x
    for line in filedat:
        vals = line.strip().split(':')
        adjValStrs = vals[1].strip().split(',')
        #convert list of strings to list of ints           
        adjVals = [int(s.strip()) for s in adjValStrs]
        key = int(vals[0].strip())
        allNodesSet.add(key)
        allNodesSet.update(adjVals)  
        resDict[key] = adjVals  
    return resDict, list(allNodesSet)

#given the base input file name
#this will return a list of nodes in order of rank (if rankName file exists)
#and a vector of rank values as floats (if outputName file exists)
#using either base file extensions or the verification file names
def loadRankVectorData(fName, isTest=False):
    rankFName, outFName = buildOutFNames(fName, isTest)
    #read node ids as list of ints in order of rank - will be size 0 list if doesn't exist
    rankedIDS = readIntFileDat(rankFName)
    #read rank vector as list of floats, expected to be in order of node ids
    rankVec = readFloatFileDat(outFName)
    #if rankedIDS doesn't exist, then assume rankVec is in ID order
    if((len(rankedIDS)==0) and (len(rankVec)!=0)):
        rankedIDS = list(xrange(len(rankVec)))       
    #either output, or both, might be empty list(s) if files don't exist
    return rankedIDS, rankVec   

#will save a list of nodes in order of rank, and rank values (the rank vector) for those nodes in same order
#in two separate files 
def saveRankData(fName, rankList=None, rankVec=None):
    rFName, outFName = buildOutFNames(fName)
    if(rankList != None):
        writeFileDat(rFName, rankList)
        print('Ranked node listing saved to file {}'.format(rFName))
    if(rankVec != None):
        writeFileDat(outFName, rankVec)        
        print('Rank vector saved to file {}'.format(outFName))
        

#build a dictionary that will have node id as key and rank vector value as value - used for verification since equal rank vector values might be in different order        
def buildValidationDict(nodeIDs, rankVec):
    vDict = {}
    for x in xrange(len(nodeIDs)):
        vDict[nodeIDs[x]] = rankVec[x]
    return vDict
     
"""
using provided output file, verify calculated page rank is the same as expected results
args used for autograder version
"""
def verifyResults(prObj, args=None, eps=.00001): 
    print('\nVerifying results for input file "{}" using alpha={} and {} sink handling :\n'.format(prObj.inFileName, prObj.alpha, ('self loop' if prObj.selfLoops else 'type 3')))
    #load derived values from run of page rank
    calcNodeIDs,calcRankVec = loadRankVectorData(prObj.outFileName, isTest=False)
    #load verification data
    vNodeIDs, vRankVec = loadRankVectorData(prObj.outFileName, isTest=True)
    if (len(vNodeIDs) == 0) or (len(vRankVec)==0) :
        print ('Validation data not found, cannot test results')
        return False
    
    
    #compare nodeID order
    if(len(calcNodeIDs) != len(vNodeIDs)) :
        print('!!!! Error : incorrect # of nodes in calculated page rank - yours has {}; validation has {}'.format(len(calcNodeIDs),len(vNodeIDs)))
        return False
    print('Calculated Rank vector is of appropriate length')
    
    #need to verify that rank vector sums to 1
    cRVecSum = sum(calcRankVec)
    if abs(cRVecSum - 1) > eps :
        print('!!!! Error : your calculated rank vector values do not sum to 1.0 : {} '.format(cRVecSum))
        return False
    print('Calculated Rank vector has appropriate magnitude of 1.0')
 
    #build dictionary of validation data and test data - doing this because order might be different for nodes with same rank value
    validDict = buildValidationDict(vNodeIDs,vRankVec)
    calcDict = buildValidationDict(calcNodeIDs,calcRankVec)

    
    #compare if matched - Note nodes with same rank value vector value might be out of order
    for x in xrange(len(vNodeIDs)):
        if abs(calcDict[vNodeIDs[x]] - validDict[vNodeIDs[x]]) > eps :
            print('!!!! Error : rank vector values do not match, starting at idx {}, node {}, in validation node id list'.format(x,vNodeIDs[x]))
            return False
    print('Rank Vector values match verification vector values')        

    return True    

#autograder code
def autogradePR(prObj, args, prMadeTime):
    print('Running autograder on {} for prObj with input file {}'.format(args.studentName, prObj.inFileName))
    
 
#End Page Rank Functions
########################################
    
    
########################################
#Bloom Filter Project functions
    
#this will compare the contents of the resList with the data in baseFile
#and display performance
def compareResults(resList, configData):
    baseFileName = configData['valFileName']
    baseRes = readFileDat(baseFileName)
    if(len(baseRes) != len(resList) ):
        print('compareFiles : Failure : Attempting to compare different size lists')
        return None
    numFail = 0
    numFTrueRes = 0
    numFFalseRes = 0
    for i in range(len(resList)):
        if (resList[i].strip().lower() != baseRes[i].strip().lower()):
            resVal = resList[i].strip().lower()
            baseResVal = baseRes[i].strip().lower()
            #uncomment this to see inconsistencies
            #print('i : ' + str(i) + ': reslist : ' + resVal + ' | baseres : ' + baseResVal)
            numFail += 1
            if resVal == 'true' :
                numFTrueRes += 1
            else :
                numFFalseRes += 1
    if(numFail == 0):
        print('compareResults : Your bloom filter performs as expected')        
    else:
        print('compareResults : Number of mismatches in bloomfilter compared to validation file : ' + str(numFail) + '| # of incorrect true results : ' + str(numFTrueRes) + '| # of incorrect False results : ' + str(numFFalseRes))
    if((configData['studentName'] != '') and (configData['autograde'] == 2)):
        gradeRes = configData['studentName'] + ', ' + str(numFail) + ', ' + str(numFTrueRes) + ', ' + str(numFFalseRes)
        print('saving results for ' + gradeRes + ' to autogradeResult.txt')
        appendFileDat('autogradeResult.txt', gradeRes)
        

#this will process input configuration and return a dictionary holding the relevant info
def buildBFConfigStruct(args):
    bfConfigData = readFileDat(args.configFileName)
    configData = dict()
    for line in bfConfigData:
        #build dictionary on non-list elements
        if (line[0]=='#') or ('_' in line):
            continue
        elems = line.split('=')
        if('name' in elems[0]):
            configData[elems[0]]=elems[1].strip()
        else :
            configData[elems[0]]=int(elems[1])
    
    if ('Type 1' in configData['name']):   
        configData['type'] = 1
        configData['seeds'] = buildSeedList(bfConfigData, int(configData['k']))
        
    elif ('Type 2' in configData['name']):
        configData['type'] = 2
        aListData = []
        bListData = []
        listToAppend = aListData
        for line in bfConfigData:
            if (line[0]=='#'):
                if ('b() seeds' in line):
                    listToAppend = bListData
                continue
            listToAppend.append(line)
        
        configData['a']= buildSeedList(aListData, int(configData['k']))
        configData['b']= buildSeedList(bListData, int(configData['k']))   
    else :
        configData['type'] = -1
        print('unknown hash function specified in config file')
    
    configData['task'] = int(args.taskToDo)
    if configData['task'] != 2 :
        configData['genSeed'] =  int(time.time()*1000.0) & 0x7FFFFFFF  #(int)(tOffLong & 0x7FFFFFFF);
        print('Random Time Seed is : ' + str(configData['genSeed']))

    configData['inFileName'] = args.inFileName
    configData['outFileName'] = args.outFileName
    configData['configFileName'] = args.configFileName
    configData['valFileName'] = args.valFileName
    configData['studentName'] = args.studentName
    configData['autograde'] = int(args.autograde)
    
    for k,v in configData.iteritems():
        print('Key = ' + k + ': Val = '),
        print(v)
        
    return configData
    
def buildSeedList(stringList, k):
    res = [0 for x in range(k)]
    for line in stringList:
        if ('_' not in line) or (line[0]=='#'):
            continue
        elems = line.split('=')        
        araElems = elems[0].split('_')
        res[int(araElems[1])]=int(elems[1])
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
    if (n%2==0):	
        n+=1      
    #n is odd here; 336 is larger than largest gap between 2 consequtive 32 bit primes
    for i in range (n,(n + 336), 2):
        if checkIfPrime(i):
            return i            
    #error no prime found returns -1
    return -1
	
"""
    check if value is prime, return true/false
    n value to check
"""
def checkIfPrime(n):
    if (n < 2) : return False
    if (n < 4) : return True
    if ((n % 2 == 0) or (n % 3 == 0)): return False
    sqrtN = n**(.5)
    i = 5
    w = 2
    while (i <= sqrtN):
        if (n % i == 0): return False	  
        i += w
        #addresses mod2 and mod3 above, flip flops between looking ahead 2 and 4 (every other odd is divisible by 3)
        w = 6-w
    return True

## end bloom filter functions
######################################
