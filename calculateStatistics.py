import csv
import os
import pandas as pd
from pylsl import local_clock


def statistics(n, metric, templateType, distanceType, templateNumber):
    curDir = os.path.dirname(__file__)

    if templateType == 'full' or templateType == 'half':
        loadPathBottom = os.path.join(curDir, 'topStimuli', metric, templateType, distanceType, 'CSVs', templateNumber, 'Bottom', 'Bottom%d.csv'%n)
        loadPathTop = os.path.join(curDir, 'topStimuli', metric, templateType, distanceType, 'CSVs', templateNumber, 'Top', 'Top%d.csv'%n)
        savePathBottom = os.path.join(curDir, 'topStimuli', metric, templateType, distanceType, 'CSVs', templateNumber, 'Bottom', 'Bottom%dStats.csv'%n)
        savePathTop = os.path.join(curDir, 'topStimuli', metric, templateType, distanceType, 'CSVs', templateNumber, 'Top', 'Top%dStats.csv'%n)
        columnName = '%s r'%templateNumber
    else:
        loadPathBottom = os.path.join(curDir, 'topStimuli', metric, templateType, distanceType, 'CSVs', 'Bottom', 'Bottom%d.csv'%n)
        loadPathTop = os.path.join(curDir, 'topStimuli', metric, templateType, distanceType, 'CSVs', 'Top', 'Top%d.csv'%n)
        savePathBottom = os.path.join(curDir, 'topStimuli', metric, templateType, distanceType, 'CSVs', 'Bottom', 'Bottom%dStats.csv'%n)
        savePathTop = os.path.join(curDir, 'topStimuli', metric, templateType, distanceType, 'CSVs', 'Top', 'Top%dStats.csv'%n)
        columnName = 'S r'

    dfBottom = pd.read_csv(loadPathBottom)
    dataColumn = dfBottom[columnName]
    bottomMin = dataColumn.min()
    bottomMax = dataColumn.max()
    bottomMean = dataColumn.mean()
    bottomStd = dataColumn.std()
    bottomRange = bottomMax - bottomMin
    bottomData = [str(bottomMean), str(bottomStd), str(bottomRange), str(bottomMax), str(bottomMin)]

    dfTop = pd.read_csv(loadPathTop)
    dataColumn = dfTop[columnName]
    topMin = dataColumn.min()
    topMax = dataColumn.max()
    topMean = dataColumn.mean()
    topStd = dataColumn.std()
    topRange = topMax - topMin
    topData = [str(topMean), str(topStd), str(topRange), str(topMax), str(topMin)]

    header = ['Mean', 'STD', 'Range', 'Max', 'Min']

    with open(savePathBottom, 'w', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerow(bottomData)

    with open(savePathTop, 'w', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerow(topData)

if __name__ == '__main__':
    startTime = local_clock()
    metrics = ['central', 'gaussian', 'linear', 'logarithmic', 'quadratic', 'unweighted']
    templateTypes = ['full', 'half', 'S']
    distanceTypes = ['fullStimulus', 'borders']
    templateNumbers = ['2', '4', '6', '8', '10', '12', '14', '16', '18', '20']


    for metric in metrics:
        for templateType in templateTypes:
            for distanceType in distanceTypes:
                for templateNumber in templateNumbers:
                    statistics(10, metric, templateType, distanceType, templateNumber)
                    statistics(100, metric, templateType, distanceType, templateNumber)
                    statistics(1000, metric, templateType, distanceType, templateNumber)

    
    print('runtime: %f'%(local_clock() - startTime))