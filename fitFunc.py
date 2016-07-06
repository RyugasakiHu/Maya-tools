def fit(input,fitRange,outputRange):    
    if input >= fitRange[0] and float(input) <= fitRange[1]:
        k = (fitRange[1]-fitRange[0])/(outputRange[1]-outputRange[0])
        b = fitRange[0] - k * outputRange[0]
        outPutValue = (input - b) / k
        return outPutValue
    else:
        print 'input value ' +str(input) + ' not in range ' +str(fitRange)
        outPutValue = 1
        return outPutValue
