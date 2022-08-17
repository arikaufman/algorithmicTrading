import csv 
import math
import matplotlib.pyplot as plt
import statsmodels.api as stat
import statsmodels.tsa.stattools as ts
import pandas as pd
import yfinance as yf

# Create a Stratey
class DataPreProcessing():
    def dataCollect(pearson):
        if pearson:
            f = open('C:/Development/algorithmicTrading/datas/WCP.csv')
            f2 = open('C:/Development/algorithmicTrading/datas/SGY.csv')
            csv_reader = csv.reader(f)
            csv_reader2 = csv.reader(f2)
            #data to store data -> price mappings, and average price for pearson formula
            dict1 = {}
            dict2 = {}
            next(csv_reader)
            next(csv_reader2)
            for line in csv_reader:
                # High + Low/2 is price
                price = float((float(line[2]) + float(line[3])) / 2)
                dict1[line[0]] = price
            for line in csv_reader2:
                price = float((float(line[2]) + float(line[3])) / 2)
                dict2[line[0]] = price
            return (dict1, dict2)
        else:
            # Define list of tickers
            tickers_list = ['WTI', 'BRNT.L']

            # Store the list in a Dataframe
            data = pd.DataFrame(columns=tickers_list)

            # Fetch the data
            for ticker in tickers_list:
                data[ticker] = yf.download(ticker,'2010-02-22','2022-02-22')['Adj Close']
            return data



    def incrementalPearsonCorrelationCalculator(dict1, dict2, xCorrelationDays):
        #incrementally calculate correlation every x days
        #r = Σi [(xi - xmean)(yi - ymean] / √Σi(xi - xmean)2 √Σi(yi - ymean)2
        pearsonCorrelationValues = {}
        count = 0
        tempXY = 0
        tempX = 0
        tempY = 0
        tempX2 = 0
        tempY2 = 0
        for key in dict1:
            if count % xCorrelationDays == 0 and count != 0:
                #Tracked at last index
                denominator = math.sqrt(math.fabs(((xCorrelationDays*tempX2)-(tempX*tempX))*((xCorrelationDays*tempY2)-(tempY*tempY))))
                pearsonCorrelationValues[key] = ((xCorrelationDays*tempXY) - (tempX * tempY)) / denominator
                tempXY = 0
                tempX = 0
                tempY = 0
                tempX2 = 0
                tempY2 = 0
            else:
                #iterate until x then store
                tempXY += (dict1[key] * dict2[key])
                tempX += dict1[key]
                tempY += dict2[key]
                tempX2 += (dict1[key] * dict1[key])
                tempY2 += (dict2[key] * dict2[key])
            count += 1

        xValues = []
        yValues = []
        medianCorrelation = 0
        for key in pearsonCorrelationValues:
            xValues.append(key)
            yValues.append(pearsonCorrelationValues[key])
            medianCorrelation += pearsonCorrelationValues[key]

        print(medianCorrelation/len(yValues))
        plt.plot(xValues[10:], yValues[10:])
        plt.xlabel('Date/Time')
        plt.ylabel('Pearson Coefficient')
        plt.title('WCP vs SGY Pearson Coeff.')
        plt.xticks([1, 20, 40, 60, 80, 100, 120 ])
        plt.show()

    def ADFTest(data):
        #store result of OLS regression on closing prices of fetched data
        data = data.dropna()
        print(data)
        result = stat.OLS(data['WTI'], data['BRNT.L']).fit()
        #run the adfuller test by passing residuals of the regression as the input, store the result in computation
        computationResults = ts.adfuller(result.resid)

        print ("Significance Level:", computationResults[0] )
        print ("pValue is:", computationResults[1] )
        print ("Critical Value Parameters", computationResults[4] )

        if computationResults[0] <= computationResults[4]['10%']  and computationResults[1]<= 0.1:
            print ("Co-integrated")





data = DataPreProcessing.dataCollect(False)
DataPreProcessing.ADFTest(data)
#DataPreProcessing.incrementalPearsonCorrelationCalculator(returnValues[0], returnValues[1], 20)


