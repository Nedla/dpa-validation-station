from matplotlib import pyplot as plot
import numpy
import pandas

filename200 = "Plots/KNOWN_200_2020-03-26_22-02-41.csv"
filename500 = "Plots/KNOWN_500_2020-03-26_22-03-18.csv"
filename1000 = "Plots/KNOWN_1000_2020-03-26_22-04-46.csv"
filename2500 = "Plots/KNOWN_2500_2020-03-26_22-08-09.csv"
filename5000 = "Plots/KNOWN_5000_2020-03-26_22-16-08.csv"
filename40000 = "Plots/KNOWN_40000_10000_2020-03-27_02-43-39.csv"
filename5Masked = "Plots/KNOWN_MASKED_5000_90000_2020-03-27_01-40-31.csv"


fiveMasked = pandas.read_csv(filename5Masked).to_numpy().astype('float')
traces200 = pandas.read_csv(filename200).to_numpy().astype('float')
traces500 = pandas.read_csv(filename500).to_numpy().astype('float')
traces1000 = pandas.read_csv(filename1000).to_numpy().astype('float')
traces2500 = pandas.read_csv(filename2500).to_numpy().astype('float')
traces5000 = pandas.read_csv(filename5000).to_numpy().astype('float')
traces40000 = pandas.read_csv(filename40000).to_numpy().astype('float')

maxIndex = numpy.where(traces40000 == numpy.amax(traces40000))[0][0]
xFit = numpy.linspace(200, 40000, 38000)
xScatter = 200, 500, 1000, 2500, 5000, 40000
y = traces200[maxIndex], traces500[maxIndex], traces1000[maxIndex], traces2500[maxIndex], traces5000[maxIndex], \
    traces40000[maxIndex]
eq = numpy.poly1d(numpy.squeeze(numpy.polyfit(xScatter, y, 1)))

fourPos = numpy.zeros(90000)
fourPos += 4.5
fourNeg = numpy.zeros(90000)
fourNeg -= 4.5

plot.figure(1)
plot.title('T-Test: 5k UnMasked vs 5k Masked')
plot.ylabel("Similarity")
plot.xlabel("Time (Row of Trace)")
# plot.scatter(xScatter, y, color='green')
# plot.plot(xFit, eq(xFit), '--', color= 'orange')
# plot.plot(traces200)
# plot.plot(traces500)
# plot.plot(traces1000)
# plot.plot(traces2500)
plot.plot(traces5000)
# plot.plot(traces40000)
plot.plot(fiveMasked)
plot.plot(fourPos, 'k--')
plot.plot(fourNeg, 'k--')
plot.show()
