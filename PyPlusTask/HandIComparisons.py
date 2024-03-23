import os
from pylsl import local_clock
import pandas as pd



def compare(n, metric, distanceType):
    curDir = os.path.dirname(__file__)
    
    # collect existing data for I and H
    loadPathH = os.path.abspath(os.path.join(curDir, '..', 'topStimuli',  metric, 'H', distanceType, 'CSVs', 'Top', 'Top%d.csv'%n))
    loadPathI = os.path.abspath(os.path.join(curDir, '..', 'topStimuli',  metric, 'I', distanceType, 'CSVs', 'Top', 'Top%d.csv'%n))
    dfH = pd.read_csv(loadPathH).drop('metric', axis = 1)
    dfI = pd.read_csv(loadPathI).drop('metric', axis = 1)
    stimuliNumbersH = dfH['stimulusNumber'].tolist()
    stimuliNumbersI = dfI['stimulusNumber'].tolist()
    
    # collect comparison columns
    loadPathH = os.path.abspath(os.path.join(curDir, '..', 'statisticalResults',  metric, 'H', '%s.csv'%distanceType))
    loadPathI = os.path.abspath(os.path.join(curDir, '..', 'statisticalResults',  metric, 'I', '%s.csv'%distanceType))
    dfHComparisons = pd.read_csv(loadPathH)
    dfIComparisons = pd.read_csv(loadPathI)
    dfHFiltered = dfHComparisons[dfHComparisons['stimulusNumber'].isin(stimuliNumbersI)]
    dfIFiltered = dfIComparisons[dfIComparisons['stimulusNumber'].isin(stimuliNumbersH)]

    # add the new comparison column
    FinalH = pd.merge(dfH, dfIFiltered, on = 'stimulusNumber', how = 'inner')
    FinalI = pd.merge(dfI, dfHFiltered,on = 'stimulusNumber', how = 'inner')
    #dfI['H r'] = dfHFiltered
    
    # make the new save locations
    savePathH = os.path.abspath(os.path.join(curDir, '..', 'H_vs_I', metric, 'H', distanceType))
    savePathI = os.path.abspath(os.path.join(curDir, '..', 'H_vs_I', metric, 'I', distanceType))
    os.makedirs(savePathH, exist_ok = True)
    os.makedirs(savePathI, exist_ok = True)

    # save the new CSVs
    FinalH.to_csv(os.path.join(savePathH, 'Top%sH.csv'%n), index = False)
    FinalI.to_csv(os.path.join(savePathI, 'Top%sI.csv'%n), index = False)

                                     
if __name__ == '__main__':
    startTime = local_clock()
    metrics = ['central', 'gaussian', 'linear', 'logarithmic', 'quadratic', 'unweighted']
    distanceTypes = ['fullStimulus', 'borders']


    for metric in metrics:
        for distanceType in distanceTypes:
            compare(10, metric, distanceType)
            compare(100, metric, distanceType)
            compare(1000, metric, distanceType)
    print('runtime: %f'%(local_clock() - startTime))

