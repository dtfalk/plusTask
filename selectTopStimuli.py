import csv
import os
import numpy
import pandas as pd
from pylsl import local_clock

# creates all of the necessary folders
def createFolders():

    metrics = ['central', 'gaussian', 'linear', 'logarithmic', 'quadratic', 'unweighted']
    templateTypes = ['full', 'half', 'S']
    distanceTypes = ['fullStimulus', 'borders']
    templateNumbers = ['2', '4', '6', '8', '10', '12', '14', '16', '18', '20']

    curDir = os.path.dirname(__file__)
    savePath = os.path.join(curDir, 'topStimuli')

    for metric in metrics:
        for templateType in templateTypes:
            for distanceType in distanceTypes:
                folderPath = os.path.join(savePath, metric, templateType, distanceType)
                imagesPath = os.path.join(folderPath, 'images')
                arraysPath = os.path.join(folderPath, 'arrays')
                CSVsPath = os.path.join(folderPath, 'CSVs')
            
                if templateType == 'S':
                    os.makedirs(imagesPath, exist_ok = True)
                    os.makedirs(arraysPath, exist_ok = True)
                    os.makedirs(CSVsPath, exist_ok = True)
                else:
                    for k, stimuliNumber in enumerate(templateNumbers):
                        imagesSubPath = os.path.join(imagesPath, stimuliNumber)
                        arraysSubPath = os.path.join(arraysPath, stimuliNumber)
                        CSVsSubPath = os.path.join(CSVsPath, stimuliNumber)
                        os.makedirs(imagesSubPath, exist_ok = True)
                        os.makedirs(arraysSubPath, exist_ok = True)
                        os.makedirs(CSVsSubPath, exist_ok = True)

                                
def saveDataFrame(df, path, first_col_name, filtered_col_name):
    df_to_save = df[[first_col_name, filtered_col_name, 'metric']]
    df_to_save.to_csv(path, index=False)

# returns the top n stimuli for a given metric, template type and template number
def findTopNStimuli(n, metric, templateType, distanceType, templateNumber):

    curDir = os.path.dirname(__file__)
    csvPath = os.path.join(curDir, 'statisticalResults', metric, templateType, '%s.csv'%distanceType)

    # Load the CSV into a DataFrame
    df = pd.read_csv(csvPath)

    # Sort the DataFrame by your column of interest in descending order
    if templateType == 'full' or templateType == 'half':
        dfSorted = df.sort_values(by='%s r'%templateNumber, ascending=False)
    else:
        dfSorted = df.sort_values(by='S r', ascending=False)

    # Select the top n rows
    topThousand = dfSorted.head(1000)
    topHundred = topThousand.head(100)
    topTen = topHundred.head(10)

    if templateType == 'full' or templateType == 'half':
        saveFolder = os.path.join(curDir, 'topStimuli', metric, templateType, distanceType,  'CSVs', templateNumber)
    else: 
        saveFolder = os.path.join(curDir, 'topStimuli', metric, templateType, distanceType,  'CSVs')
    topThousandSave = os.path.join(saveFolder, 'Top1000.csv')
    topHundredSave = os.path.join(saveFolder, 'Top100.csv')
    topTenSave = os.path.join(saveFolder, 'Top10.csv')
    if templateType == 'full' or templateType == 'half':
        saveDataFrame(topThousand, topThousandSave, 'stimulusNumber', '%s r'%templateNumber)
        saveDataFrame(topHundred, topHundredSave, 'stimulusNumber', '%s r'%templateNumber)
        saveDataFrame(topTen, topTenSave, 'stimulusNumber', '%s r'%templateNumber)
    else: 
        saveDataFrame(topThousand, topThousandSave, 'stimulusNumber', 'S r')
        saveDataFrame(topHundred, topHundredSave, 'stimulusNumber', 'S r')
        saveDataFrame(topTen, topTenSave, 'stimulusNumber', 'S r')

    return topTen, topHundred, topThousand

    
    


if __name__ == '__main__':
    startTime = local_clock()
    metrics = ['central', 'gaussian', 'linear', 'logarithmic', 'quadratic', 'unweighted']
    templateTypes = ['full', 'half', 'S']
    distanceTypes = ['fullStimulus', 'borders']
    templateNumbers = ['2', '4', '6', '8', '10', '12', '14', '16', '18', '20']

    curDir = os.path.dirname(__file__)
    saveFolder = os.path.join(curDir, 'topStimuli')
    createFolders()

    for metric in metrics:
        for templateType in templateTypes:
            for distanceType in distanceTypes:
                for templateNumber in templateNumbers:
                    topTen, topHundred, topThousand = findTopNStimuli(1000, metric, templateType, distanceType, templateNumber)
    
    print('runtime: %f'%(local_clock() - startTime))





    
