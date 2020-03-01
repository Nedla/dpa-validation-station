import csv
import numpy
import os
from pathlib import Path
from matplotlib import pyplot as plot

def aes_ecb():

    traceDir = Path(os.curdir) / 'Traces'
    traces = []
    mySet = []
    mySet2 = []

    for f in os.scandir(traceDir):
        traces.append(numpy.loadtxt(f.path).astype('float'))

    for t in traces:
        mySet.append(t[n])

    x1 = numpy.mean(mySet)
    x2 = numpy.mean(mySet2)
    stddev1 = numpy.std(mySet)
    stddev2 = numpy.std(mySet2)

    alpha = x1-x2 / (numpy.sqrt())
        
aes_ecb()