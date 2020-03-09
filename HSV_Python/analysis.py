import csv
import numpy
import os
from pathlib import Path
from matplotlib import pyplot as plot

if __name__ == "__main__":
    traceDir = Path(os.curdir) / 'Traces/KNOWN'
    knownCSV = []
    count = 0
    for f in os.scandir(traceDir):
        print(count)
        knownCSV.append(numpy.loadtxt(f.path).astype('float'))
        count += 1
        if count >= 7:
            break

    traceDir = Path(os.curdir) / 'Traces/RANDOM'
    randomCSV = []
    count = 0
    for f in os.scandir(traceDir):
        print(count)
        randomCSV.append(numpy.loadtxt(f.path).astype('float'))
        count += 1
        if count >= 7:
            break

    zeroToFive = numpy.array(knownCSV)
    fiveToNine = numpy.array(randomCSV)



    mean1 = numpy.mean(zeroToFive, axis=0)
    mean2 = numpy.mean(fiveToNine, axis=0)
    stdDev1 = numpy.std(zeroToFive, axis=0)
    stdDev2 = numpy.std(fiveToNine, axis=0)

    tResult = []
    for i in range(100000):
        meanX = mean1[i]
        meanY = mean2[i]
        stdDevX = stdDev1[i]
        stdDevY = stdDev2[i]

        top = meanX - meanY
        bot1 = numpy.square(stdDevX)/len(zeroToFive)
        bot2 = numpy.square(stdDevY)/len(fiveToNine)
        bot = numpy.sqrt(bot1+bot2)
        t = top/bot
        tResult.append(t)

    plot.figure(1)
    plot.title('Known Trace')
    plot.xlabel('Time')
    plot.ylabel('Power')
    #for p in zeroToFive:
    plot.plot(zeroToFive[0])
    plot.show()

    plot.figure(2)
    plot.title('Random Trace')
    plot.xlabel('Time')
    plot.ylabel('Power')
    for p in fiveToNine:
        plot.plot(p)
    plot.show()

    plot.figure(3)
    plot.title('T-Test Trace')
    plot.xlabel('Trace #')
    plot.ylabel('Similarity')
    plot.plot(tResult)
    plot.show()

    #
    # print(tResult[2819])
    # print(mean1[2819])
    # print(mean2[2819])

    # for i in range(3):
    #     count = 0
    #     for trace in traces:
    #         count += trace[i]
    #     res = count / 10
    #     print("Averaged value {0}: {1}".format(i, res))