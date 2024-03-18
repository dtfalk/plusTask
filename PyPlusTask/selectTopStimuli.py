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
    savePath = os.path.join(curDir, '..', 'topStimuli')

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
    csvPath = os.path.join(curDir, '..', 'statisticalResults', metric, templateType, '%s.csv'%distanceType)

    # Load the CSV into a DataFrame
    df = pd.read_csv(csvPath)

    # Sort the DataFrame by your column of interest in descending order
    if templateType == 'full' or templateType == 'half':
        dfSorted = df.sort_values(by='%s r'%templateNumber, ascending=False)
    else:
        dfSorted = df.sort_values(by='S r', ascending=False)
    
    # Create a copy of dfSorted to sort by absolute values
    dfSortedAbs = dfSorted.copy()

    # Determine the column to sort by
    sort_column = '%s r' % templateNumber if templateType in ['full', 'half'] else 'S r'

    # Calculate the absolute values for the column of interest in the copied DataFrame
    dfSortedAbs[sort_column] = dfSortedAbs[sort_column].abs()

    # Sort the copied DataFrame based on the absolute values in descending order
    dfSortedAbs = dfSortedAbs.sort_values(by=sort_column, ascending=False)

    # Select the top n rows
    topThousand = dfSorted.head(1000)
    topHundred = topThousand.head(100)
    topTen = topHundred.head(10)
    bottomThousand = dfSortedAbs.tail(1000)
    bottomHundred = bottomThousand.tail(100)
    bottomTen = bottomHundred.tail(10)

    if templateType == 'full' or templateType == 'half':
        saveFolderTop = os.path.join(curDir, '..', 'topStimuli', metric, templateType, distanceType,  'CSVs', templateNumber, 'Top')
        saveFolderBottom = os.path.join(curDir, '..', 'topStimuli', metric, templateType, distanceType,  'CSVs', templateNumber, 'Bottom')
    else: 
        saveFolderTop = os.path.join(curDir, '..', 'topStimuli', metric, templateType, distanceType,  'CSVs', 'Top')
        saveFolderBottom = os.path.join(curDir, '..', 'topStimuli', metric, templateType, distanceType,  'CSVs', 'Bottom')
    os.makedirs(saveFolderTop, exist_ok = True)
    os.makedirs(saveFolderBottom, exist_ok = True)

    topThousandSave = os.path.join(saveFolderTop, 'Top1000.csv')
    topHundredSave = os.path.join(saveFolderTop, 'Top100.csv')
    topTenSave = os.path.join(saveFolderTop, 'Top10.csv')
    bottomThousandSave = os.path.join(saveFolderBottom, 'Bottom1000.csv')
    bottomHundredSave = os.path.join(saveFolderBottom, 'Bottom100.csv')
    bottomTenSave = os.path.join(saveFolderBottom, 'Bottom10.csv')
    if templateType == 'full' or templateType == 'half':
        saveDataFrame(topThousand, topThousandSave, 'stimulusNumber', '%s r'%templateNumber)
        saveDataFrame(topHundred, topHundredSave, 'stimulusNumber', '%s r'%templateNumber)
        saveDataFrame(topTen, topTenSave, 'stimulusNumber', '%s r'%templateNumber)
        saveDataFrame(bottomThousand, bottomThousandSave, 'stimulusNumber', '%s r'%templateNumber)
        saveDataFrame(bottomHundred, bottomHundredSave, 'stimulusNumber', '%s r'%templateNumber)
        saveDataFrame(bottomTen, bottomTenSave, 'stimulusNumber', '%s r'%templateNumber)
    else: 
        saveDataFrame(topThousand, topThousandSave, 'stimulusNumber', 'S r')
        saveDataFrame(topHundred, topHundredSave, 'stimulusNumber', 'S r')
        saveDataFrame(topTen, topTenSave, 'stimulusNumber', 'S r')
        saveDataFrame(bottomThousand, bottomThousandSave, 'stimulusNumber', 'S r')
        saveDataFrame(bottomHundred, bottomHundredSave, 'stimulusNumber', 'S r')
        saveDataFrame(bottomTen, bottomTenSave, 'stimulusNumber', 'S r')
    return


if __name__ == '__main__':
    startTime = local_clock()
    metrics = ['central', 'gaussian', 'linear', 'logarithmic', 'quadratic', 'unweighted']
    templateTypes = ['full', 'half', 'S']
    distanceTypes = ['fullStimulus', 'borders']
    templateNumbers = ['2', '4', '6', '8', '10', '12', '14', '16', '18', '20']

    createFolders()

    for metric in metrics:
        for templateType in templateTypes:
            for distanceType in distanceTypes:
                for templateNumber in templateNumbers:
                    findTopNStimuli(1000, metric, templateType, distanceType, templateNumber)
    
    print('runtime: %f'%(local_clock() - startTime))





    
