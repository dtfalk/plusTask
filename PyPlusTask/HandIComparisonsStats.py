import os
from pylsl import local_clock
import pandas as pd



def calcStats(n, metric, distanceType, templateType):
    curDir = os.path.dirname(__file__)
    
    loadPath = os.path.abspath(os.path.join(curDir, '..', 'H_vs_I', metric, templateType, distanceType, 'Top%d%s.csv'%(n, templateType)))
    savePath = os.path.abspath(os.path.join(curDir, '..', 'H_vs_I', metric, templateType, distanceType, 'Top%dStats.csv'%n))
    
    df = pd.read_csv(loadPath)

    dataColumnH = df['H r']
    dataColumnI = df['I r']

    MinH = dataColumnH.min()
    MinI = dataColumnI.min()

    MaxH = dataColumnH.max()
    MaxI = dataColumnI.max()

    MeanH = dataColumnH.mean()
    MeanI = dataColumnI.mean()

    StdH = dataColumnH.std()
    StdI = dataColumnI.std()

    RangeH = MaxH - MinH
    RangeI = MaxI - MinI

    dataH = ['H' ,str(MeanH), str(StdH), str(RangeH), str(MaxH), str(MinH)]
    dataI = ['I', str(MeanI), str(StdI), str(RangeI), str(MaxI), str(MinI)]

    header = ['Template Type', 'Mean', 'STD', 'Range', 'Max', 'Min']
    if templateType == 'H':
        finalDF = pd.DataFrame([dataH, dataI], columns = header)
    else:
        finalDF = pd.DataFrame([dataI, dataH], columns = header)

    finalDF.to_csv(savePath, index = False)
                                     
if __name__ == '__main__':
    startTime = local_clock()
    metrics = ['central', 'gaussian', 'linear', 'logarithmic', 'quadratic', 'unweighted']
    distanceTypes = ['fullStimulus', 'borders']
    templateTypes = ['H', 'I']


    for metric in metrics:
        for distanceType in distanceTypes:
            for templateType in templateTypes:
                calcStats(10, metric, distanceType, templateType)
                calcStats(100, metric, distanceType, templateType)
                calcStats(1000, metric, distanceType, templateType)
    print('runtime: %f'%(local_clock() - startTime))

