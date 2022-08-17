import csv 
import math
import matplotlib.pyplot as plt

# Create a Stratey
class DataPreProcessing():
    def dataCollect():
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
            
        return pearsonCorrelationValues    


        
returnValues = DataPreProcessing.dataCollect()
pearsonValues = DataPreProcessing.incrementalPearsonCorrelationCalculator(returnValues[0], returnValues[1], 20)

xValues = []
yValues = []
medianCorrelation = 0
for key in pearsonValues:
    xValues.append(key)
    yValues.append(pearsonValues[key])
    medianCorrelation += pearsonValues[key]
    

print(medianCorrelation/len(yValues))
plt.plot(xValues[10:], yValues[10:])
plt.xlabel('Date/Time')
plt.ylabel('Pearson Coefficient')
plt.title('WCP vs SGY Pearson Coeff.')
plt.xticks([1, 20, 40, 60, 80, 100, 120 ])
plt.show()
        