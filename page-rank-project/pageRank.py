# -*- coding: utf-8 -*-
"""
Created on Wed Jan 03 14:40:02 2018

@author: Magahet Mendiola
"""

import time
#argparse allows the parsing of command line arguments
import argparse
#utility functions for the PageRank project
import prProjectUtils as util
#useful structure to build dictionaries of lists - provides 
#a default entry for keys that don't exist in map
from collections import defaultdict
#to build a dictionary that will have a list as its value
#use : mydict = defaultdict(list)


#PageRank object to hold graph representation and code to solve for algorithm
class PageRank(object):     
    #this object will build a page rank vector on a map of nodes
    def __init__(self, inFileName, alpha=.85, selfLoops=False):
        """        
        Args:
            inFileName : the name of the file describing the graph to be 
                        ranked using the page rank algorithm
        """
        self.inFileName = inFileName
        #set alpha value
        self.alpha = alpha
        #whether using self loops or using alpha==0 for sinks
        self.selfLoops = selfLoops
        #make output file name
        self.outFileName = util.makeResOutFileName(self.inFileName, self.alpha, self.selfLoops)   

        #this is only placed here to prevent errors when running empty template code
        self.rankVec = []        
        #dictionary of every node and its outlist and list of all node ids
        self.adjList, self.nodeIDs = util.loadGraphADJList(self.inFileName)
        #number of nodes total in map
        self.N = len(self.nodeIDs)
        
        #Task 1 : initialize data structures you will use
        self.initAllStructs()   
    
    """
    Task 1 : using self.adjList, do the following, in this order :
    1. conditionally add self loops to self.adjList : for type 1 sink handling only
    2. build in-list structure to relate a node to all the nodes pointing to it
    3. build out-degree structure to hold reference to the out degree of all nodes
    4. conditionally build list of all sink nodes, for type 3 sink handling only)
    5. initialize self.rankVec : pagerank vector -> initialize properly(uniformly)
    """
    def initAllStructs(self):
        # 1. conditionally add self loops to self.adjList : for type 1 sink handling only
        if self.selfLoops:
            for id_ in self.nodeIDs:
                if id_ not in self.adjList.get(id_, []):
                    self.adjList[id_].append(id_)
                    
        # 2. build in-list structure to relate a node to all the nodes pointing to it
        self.inList = defaultdict(set)
        for source, outList in self.adjList.iteritems():
            for destination in outList:
                self.inList[destination].add(source)
                
        # 3. build out-degree structure to hold reference to the out degree of all nodes
        self.outDegree = {k:len(v) for k, v in self.adjList.iteritems()}
        
        # 4. conditionally build list of all sink nodes, for type 3 sink handling only)
        if not self.selfLoops:
            self.sinkNodes = [bool(self.adjList.get(n)) for n in self.nodeIDs]
        
        # 5. initialize self.rankVec : pagerank vector -> initialize properly(uniformly)
        self.rankVec = [1.0 / len(self.nodeIDs) for _ in self.nodeIDs]
        
    """
    Task 2 : using in-list structure, out-degree structure, (and sink-related 
    structure if appropriate for current sink handling strategy) :
    
    Perform single iteration of PageRank algorithm and return resultant vector
    """
    def solveRankIter(self, oldRankVec):
        def get_idx(id_):
            return self.nodeIDs.index(id_)
            
        def get_alpha(id_):
            if self.selfLoops:
                return self.alpha
            else:
                return 0 if id_ in self.sinkNodes else self.alpha
                
        def prob(y, x):
            alpha = get_alpha(y)
            if y in self.inList[x]:
                return ((1 - alpha) / self.N) + (alpha / self.outDegree[y])
            else:
                return (1 - alpha) / self.N
            
        #need to make copy of old rank vector 
        return [
            sum([oldRankVec[i] * prob(y, x) for i, y in enumerate(self.nodeIDs)])
            for x in self.nodeIDs
        ]
    
    """
    Task 3 : Find page rank vector by iterating through solveRankIter calls  
    until rank vector updates are within eps.
    """
    def solveRankToEps(self, eps):
        #copy current page rank vector
        rankVec = self.rankVec[:]
        newRankVec = [r + eps for r in self.rankVec]
        last_update = time.time() - 10
        eps_delta = eps
        
        while eps_delta >= eps:
            if time.time() - last_update > 10:
                print eps_delta
                last_update = time.time()
            rankVec = newRankVec[:]
            newRankVec = self.solveRankIter(rankVec)
            # print rankVec
            # print newRankVec
            # print eps_delta
            # print
            eps_delta = sum([
                newRankVec[i] - rankVec[i]
                for i in xrange(self.N)
            ])
        return newRankVec
    
    
    """
        find page rank vector, save results.  Optionally sort results, although
        unnecessary for proper verification.
    """
    def solvePageRank(self, eps, sortRes=False, saveVals=True):
        #DO NOT MODIFY THIS FUNCTION -add any extra functions you want to use
        #in solveRankToEps
        
        self.rankVec = self.solveRankToEps(eps)
                
        if(len(self.rankVec)>0):
            if(sortRes):
                #when converges, to sort self.rankVec also need to sort self.nodeIDs 
                #so that rankvec is descending and node ids still aligns with it 
                sortedIDXs, self.rankVec = util.getSortResIDXs(self.rankVec)
                newIDVec = [self.nodeIDs[i] for i in sortedIDXs]
                self.nodeIDs = newIDVec
            else:
                #don't save node id list if rank vec not sorted - node ids are
                #just idxs in order
                newIDVec = None                
        else : 
            print('Zero-size PageRank vector Error.')
            newIDVec = None
            
        if(saveVals):
            print('Saving results')
            util.saveRankData(self.outFileName, newIDVec, self.rankVec)
            print('Results saved')           
            
        return self.rankVec, self.nodeIDs    

    
#once the appropriate runs have been performed, plot results
#alpha specified in prObj is ignored - .75,.85 and .95 alphas are tested
def plotRes(prObj):
    #for graphs you may wish to code
    #import matplotlib as plt
    import matplotlib.pyplot as plt
    #for plotting
    import numpy as np    
    
    stSiteLoc = 0
    endSiteLoc = 20
    # use results for .75, .85 and .95 alphas to build plots - vNodeIDxx and 
    # vRankVecXX results come back sorted in descending rank order  
    vNodeID75, vRankVec75, dictRV75 = util.getResForPlots(prObj, .75)
    vNodeID85, vRankVec85, dictRV85 = util.getResForPlots(prObj, .85)    
    vNodeID95, vRankVec95, dictRV95 = util.getResForPlots(prObj, .95)
    
    #find union of all top x sites' site ids
    allNodesSet = set()
    allNodesSet.update(vNodeID75[stSiteLoc:endSiteLoc])
    allNodesSet.update(vNodeID85[stSiteLoc:endSiteLoc])
    allNodesSet.update(vNodeID95[stSiteLoc:endSiteLoc])
    #all nodes in top 20 for any of the 3 alpha settings - unsorted
    allTopNodes = list(allNodesSet)
    
    #list of values in allTopNodes order
    pltPRVals85tmp = [dictRV85[x] for x in allTopNodes] 
    #find appropriate order  - use idxs to find actual node IDS in allTopNodes      
    srtdIDXsInATNlst, pltPRVals85 = util.getSortResIDXs(pltPRVals85tmp)
    allTopNodes2 = [allTopNodes[x] for x in srtdIDXsInATNlst]    
    #comparing alpha of .75 and .95 to alpha of .85
   
    pltPRVals75 = [dictRV75[x] for x in allTopNodes2]
    pltPRVals95 = [dictRV95[x] for x in allTopNodes2]
    
    # data to plot
    n_groups = len(allTopNodes2)
     
    # create plot
    fig, ax = plt.subplots()
    #index = np.asarray(allTopNodes)#np.arange(n_groups)
    index = np.arange(n_groups)
    bar_width = 0.30
    opacity = 0.8
     
    r1 = plt.bar(index, pltPRVals75, bar_width,
                     alpha=opacity,
                     color='b',
                     label='alpha=.75')
     
    r2 = plt.bar(index + bar_width, pltPRVals85, bar_width,
                     alpha=opacity,
                     color='r',
                     label='alpha=.85')
    r3 = plt.bar(index + 2*bar_width, pltPRVals95, bar_width,
                     alpha=opacity,
                     color='g',
                     label='alpha=.95')
     
    plt.xlabel('Site Rank')
    plt.ylabel('Score')
    ttlStr = 'Scores for dataset {} for sites ranked {} through {}\n'.format(prObj.inFileName,(stSiteLoc+1),endSiteLoc) \
                  + 'for 3 alpha values using {} sink handling'.format('self-loop' if prObj.selfLoops else 'Type 3')
    plt.title(ttlStr)
    plt.legend()
     
    plt.tight_layout()
    plt.show()


#calculate page rank vector
def calcRes(prObj, args, prMadeTime):
    #calculate page rank vector for passed arguments   
    print('\nCalculating PageRank vector')
    rankVec, nodeIDsInRankOrder = prObj.solvePageRank(float(args.eps))
    rvDoneTime = time.time()
    print('\nPageRank vector calculated.  Elapsed time : {} seconds'.format(rvDoneTime - prMadeTime))
    print('\nVerifying PageRank vector')
    compareRes = util.verifyResults(prObj)  
    resStr = 'matches' if compareRes else 'does not match'
    print('\nYour calculated PageRank vector {} the validation file'.format(resStr))


"""     
main
"""     
def main():	
    #DO NOT REMOVE ANY ARGUMENTS FROM THE ARGPARSER BELOW
    parser = argparse.ArgumentParser(description='Page Rank Project')
    parser.add_argument('-i', '--infile',  help='Input file adjacency information of graph', default='testCaseSmall.txt', dest='inFileName')
    parser.add_argument('-a', '--alpha', help='Alpha Value', type=float, default=.85, dest='alpha')
    parser.add_argument('-e', '--epsilon', help='Epsilon Value for convergence test.', type=float, default=1e-10, dest='eps')
    parser.add_argument('-p', '--plot', help='Plot pregenerated results instead of executing algorithm', action='store_true', default=False, dest='plot')
    parser.add_argument('-s', '--selfloop', help='Use Self Loops to handle sinks.', action='store_true', default=False, dest='selfLoops')
    #args for autograder, DO NOT MODIFY
    parser.add_argument('-n', '--sName',  help='Student name, used by autograder', default='GT', dest='studentName')	
    parser.add_argument('-z', '--autograde',  help='Autograder-called (2) or not (1=default)', type=int, choices=[1, 2], default=1, dest='autograde')	
    args = parser.parse_args()   
    
    #DO NOT MODIFY ANY OF THIS CODE :     
    
    #input file name is used to build names for output files to save rank vector and ranked ordering of nodes  
    startTime = time.time()
    print('\nMaking pagerank object using input file {} and alpha {} and {} sink handling.'.format(args.inFileName, args.alpha, 'self-loop' if args.selfLoops else 'Type 3'))
    prObj = PageRank(args.inFileName, alpha=float(args.alpha), selfLoops=args.selfLoops)
    prMadeTime = time.time()
    print('\nPageRank object made.  Elapsed time : {} seconds'.format(prMadeTime - startTime))

    if (args.autograde == 2):
        util.autogradePR(prObj, args, prMadeTime)
        return   
    elif (args.plot) :
        #make sure you have .75, .85 and .95 alpha results generated for a 
        #particular input file before calling plotRes.  Args-specified alpha value 
        #is ignored in plotRes, but file name and self-loop method is used
        plotRes(prObj)
        return
    else:   
        calcRes(prObj, args, prMadeTime)    
    
if __name__ == '__main__':
    main()
    