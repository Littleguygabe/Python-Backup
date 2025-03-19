lowerBandThresh = 25
upperBandThresh = 25
lowerATRThresh = 25 #threshold to classify stock as stable based on atr
upperATRThresh = 25 #threshold to classify stock as volatile/risky
highMACDSIGdif = 72

postPeakGradient = 1 #the gradient for 'peakLength' No days before and after a given point must be less than this to classify as a peak
    #decreasing gradient threshold and decreasing peak length will get a larger number of short sharp peaks
prePeakGradient = 1
peakLength = 2
prePeakLength = 2

postTroughGradient = -1
preTroughGradient = -1
troughLength = 2
preTroughLength = 2



highRSI = 60
goodRSI = 50
lowRSI = 40
rsiDif = 3 #the threshold of difference in RSI between the current and previous day that means a high or low difference
highMACDSIGavg = 10 #divide the value by 10 when evalutating -> changes how high the average of the MACD and signal line needs to be in order to constitute a sell point



# could make a window to change the threshold values with sliders then once im happy 
# with changes run the data creation files again to generate new indicator
# dataframes with the adjusted threshold values
