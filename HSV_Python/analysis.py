import csv
import numpy
import pandas
import os
from pathlib import Path
from datetime import datetime

STARTROW = 10000
TOTALROW = 100000
NUMROWS = 90000
NUMTRACES = 5000
KNOWN_FOLDERNAME = "KNOWN"
RANDOM_FOLDERNAME = "RANDOM"

if __name__ == "__main__":
    filename = "Plots/{}_{}_{}_{}.csv".format(KNOWN_FOLDERNAME, NUMTRACES, NUMROWS, datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))


    while STARTROW <= TOTALROW - NUMROWS: # STARTROW == 10000:
        # Loads CSVs into an array, uses pandas to read as it's fastest
        traceDir = Path(os.curdir) / 'Traces/{}'.format(KNOWN_FOLDERNAME)
        knownCSV = []
        count = 0
        for f in os.scandir(traceDir):
            print(count)
            knownCSV.append(pandas.read_csv(f.path, nrows=NUMROWS, skiprows=STARTROW).to_numpy().astype('float'))
            count += 1
            if count >= NUMTRACES:
                break

        # Loads CSVs into an array, uses pandas to read as it's fastest
            traceDir = Path(os.curdir) / 'Traces/{}'.format(RANDOM_FOLDERNAME)
            randomCSV = []
            count = 0
            for f in os.scandir(traceDir):
                print(count)
                randomCSV.append(pandas.read_csv(f.path, nrows=NUMROWS, skiprows=STARTROW).to_numpy().astype('float'))
                count += 1
                if count >= NUMTRACES:
                    break
        STARTROW += NUMROWS
        #print(knownCSV[0])

    # Turns all the regular arrays into numpy arrays for processing
    knownTraces = numpy.array(knownCSV)
    print("Loaded Known")
    randomTraces = numpy.array(randomCSV)
    print("Loaded Random")

    # Get the means and standard deviations at the same point across all traces
    knownMean = knownTraces.mean(axis=0)
    meanArray = []
    print("Known Mean")
    randomMean = randomTraces.mean(axis=0)
    print("Random Mean")
    knownStdDev = knownTraces.std(axis=0)
    print("Known StdDev")
    randomStdDev = randomTraces.std(axis=0)
    print("Random StdDev")

    tResult = []
    for i in range(min(len(knownMean), len(knownStdDev), len(randomMean), len(randomStdDev))):
        print(i)
        meanX = knownMean[i]
        meanY = randomMean[i]
        stdDevX = knownStdDev[i]
        stdDevY = randomStdDev[i]

        top = meanX - meanY
        bot1 = numpy.square(stdDevX)/len(knownTraces)
        bot2 = numpy.square(stdDevY)/len(randomTraces)
        bot = numpy.sqrt(bot1+bot2)
        t = top/bot
        tResult.append(t[0])

    with open(filename, 'a', newline='') as csvfile:
            csvWriter = csv.writer(csvfile)
            for result in tResult:
                csvWriter.writerow(["{0:.4f}".format(result)])
