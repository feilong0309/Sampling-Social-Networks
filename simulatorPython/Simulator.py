import sys
import cPickle
import random
import os
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import pylab 
"""
Loads a graph from file, pickles it and returns the 
graph as an adjacency list
"""
def populateGraph(fp):
  Graph = {}
  for line in fp:
    first, second = line.split("\t")
    Graph.setdefault(int(first), []).append(int(second))
  cPickle.dump(Graph, open("graph.pkl","w"))
  print "ok"
  return Graph

"""
Loads and returns a pickled graph object
"""
def loadGraph():
  print "Loading pickled graph..."
  Graph = cPickle.load(open("graph.pkl"))
  print "Graph loaded..."  
  return Graph

"""
Loads a graph from file; adjacency list
"""
def getGraph(fp):
  print "Loading graph... "
  Graph = {}
  for line in fp:
    try:
      first, second = line.rstrip("\n").split("\t")
      Graph.setdefault(int(first), []).append(int(second))
    except: print line #pass
  print "Graph loaded!"
  return Graph  

"""
'Heart' of the code
Performs:
1) Naive random walk from a random seed node
2) Generates a uniform sample (rejection based)
3) BFS
"""
def analyzeGraph(fp, numHops):
  os.system("clear")
  Graph = getGraph(fp)
  #Graph = loadGraph()
  graphNodes = Graph.keys()
  startIdx = random.randint(0, len(graphNodes))   #FIXME start node should be explicit 
  startNode = graphNodes[startIdx]
  print "startIdx = %s, startNode = %s"%(startIdx, startNode)

  print "Random Walk"
  RWalk = runRW(startNode, numHops, Graph)
  print RWalk

  print "Uniform sample:"
  UNI = getUniformSample(numHops, Graph)
  print UNI

  print "BFS"
  BFSWalk = runBFS(startNode, numHops, Graph)
  print BFSWalk
  
  #N = max(max(RWalk.values()), max(UNI.values()), max(BFSWalk.values())) 
  N = 0  #plots all graphs with same scale
  plotGraph(RWalk, "RandomWalk", numHops, N)
  plotGraph(UNI, "UniformSample", numHops, N)
  plotGraph(BFSWalk, "BFS", numHops, N)
  Graph2 = {}
  for node in Graph.keys(): Graph2[node] = len(Graph[node])
  plotGraph(Graph2, "FullGraph", len(Graph2.keys()), max(Graph2.values()))
  #plotScatter(Graph2, "FullGraph2", len(Graph2.keys()), max(Graph2.values()))


def runRW(startNode, numHops, Graph):
  walkedNodes = []
  distDict = {} #creating the distribution dictionary for plotting(RW)
  currNode = startNode
  #print "Starting walk..."
  while (len(walkedNodes) < numHops + 1):
    walkedNodes.append(currNode)
    currNeighbors = Graph[currNode]
    currNode = currNeighbors[random.randint(0, len(currNeighbors)) - 1]
  print "Random Walk done. Walked nodes: %s"%walkedNodes
  print "Number of nodes walked: %s Number of unique nodes: %s"\
  %(len(walkedNodes), len(set(walkedNodes)))
  for node in set(walkedNodes): 
    distDict[node] = len(Graph[node])   
    #print node, len(Graph[node])
  return distDict

"""
def runBFS(Graph, startNode, numHops):
  walkedNodes = []
  currNode = startNode
  while len(walkedNodes < numHops):
    walkedNodes.append(currNode)
    currNeighbors = Graph[currNode]
    for node in currNeighbors: walkedNodes.append(node)
  pass
"""

def runBFS(startNode, numHops, Graph, path=[]):
  q=[startNode]
  while q:
    v=q.pop(0)
    if not v in path:
      path=path+[v]
      q=q+Graph[v]
    if len(path) > numHops:
      distDict = {}
      for node in path: 
        distDict[node] = len(Graph[node])
      return distDict

def getUniformSample(numHops, Graph):
  uniformSample = []
  UNIDict = {}
  nodes = Graph.keys()
  for i in range(numHops):
    uniformSample.append(random.choice(nodes))
  print "%s samples, %s unique samples"%(len(uniformSample), \
  len(set(uniformSample)))
  for node in uniformSample: UNIDict[node] = len(Graph[node])
  #print UNIDict
  return UNIDict

def plotGraph(distDict, walkType, numHops, N):
  #mu, sigma = 100, 15#
  fileName = "walk_%s_%s.png"%(walkType, numHops)
  fig = plt.figure()
  #ax = fig.add_subplot(111)#
  print "Plotting %s distribution..."%walkType
  #nodes = distDict.keys()
  neighbors = distDict.values()
  if (N == 0): N = max(neighbors)
  samples = np.array(neighbors)
  n, bins, patches  = plt.hist( samples, N, facecolor="green",\
                                  range=[1,N], normed=True )
  plt.title('Plot of %s with size %s'%(walkType, numHops))
  plt.xlabel('Degree')
  plt.ylabel('Probability')  
  #fig.set_size_inches(18.5,10.5)
  fig.savefig(fileName)#, dpi=300)
  print "plot saved at %s"%fileName

def plotScatter(distDict, walkType, numHops, N):
  def log_10_product(x, pos): return '%1i' % (x)
  ax = pylab.subplot(111)
  ax.set_xscale('log')
  ax.set_yscale('log')
  formatter = pylab.FuncFormatter(log_10_product)
  ax.xaxis.set_major_formatter(formatter)
  ax.yaxis.set_major_formatter(formatter)
  xVals = distDict.keys()
  yVals = distDict.values()
  ax.scatter(xVals, yVals, s=40, c='b', marker='s', faceted=False)
  ax.set_xlim(1e-1, 1e4)
  ax.set_ylim(1e-1, 1e4)
  pylab.grid(True)
  pylab.xlabel(r"Degree", fontsize = 12)
  pylab.ylabel(r"Frequency", fontsize = 12)

def main():
  try:
    fileName, numHops = sys.argv[1], sys.argv[2]
    fp = open(fileName)
  except:
    print "usage: python Simulator.py <input filename> <number of hops>\
          \n\tTry again..."
    sys.exit(1)
#  populateGraph(fp)
  analyzeGraph(fp, int(numHops))
   
if __name__ == "__main__":
  main()

