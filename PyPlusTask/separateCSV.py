import csv
import pandas as pd
import os
from pylsl import local_clock

def getSavePaths(templateType, distanceType):
    curDir = os.path.dirname(__file__)

    central = os.path.abspath(os.path.join(curDir, '..', 'statisticalResults', 'central', templateType, '%s.csv'%distanceType))
    print(central)
    gaussian = os.path.abspath(os.path.join(curDir, '..', 'statisticalResults', 'gaussian', templateType, '%s.csv'%distanceType))
    linear = os.path.abspath(os.path.join(curDir, '..', 'statisticalResults', 'linear', templateType, '%s.csv'%distanceType))
    logarithmic = os.path.abspath(os.path.join(curDir, '..', 'statisticalResults', 'logarithmic', templateType, '%s.csv'%distanceType))
    quadratic = os.path.abspath(os.path.join(curDir, '..', 'statisticalResults', 'quadratic', templateType, '%s.csv'%distanceType))
    unweighted = os.path.abspath(os.path.join(curDir, '..', 'statisticalResults', 'unweighted', templateType, '%s.csv'%distanceType))

    return central, gaussian, linear, logarithmic, quadratic, unweighted

def extractAndSave(metric, distanceType, templateType, savePath):
    # Step 2: Load the CSV file into a DataFrame
    curDir = os.path.dirname(__file__)
    loadPath = os.path.join(curDir, 'results.csv')
    df = pd.read_csv(loadPath)
    headerTemplateType = '%s r'%(templateType.replace('.npy', ''))
    df.columns = ['stimulusNumber', headerTemplateType, 'metric', 'templateType', 'distanceType'] 

    # Step 3: Filter the DataFrame
    filtered_df = df[(df['metric'] == metric) & (df['templateType'] == templateType) & (df['distanceType'] == distanceType)]

    # Step 4: Drop the 'stimulusType' and 'distanceType' columns
    filtered_df = filtered_df.drop(['templateType', 'distanceType'], axis=1)

    # Step 5: Write the filtered DataFrame to a new CSV file, without the index
    
    filtered_df.to_csv(savePath, index=False)

if __name__ == '__main__':

    startTime = local_clock()

    instanceTime = local_clock()
    central, gaussian, linear, logarithmic, quadratic, unweighted = getSavePaths('H', 'fullStimulus')
    extractAndSave('central', 'fullStimulus', 'H.npy', central)
    print('done central H full')
    extractAndSave('gaussian', 'fullStimulus', 'H.npy', gaussian)
    print('done gaussian H full')
    extractAndSave('linear', 'fullStimulus', 'H.npy', linear)
    print('done linear H full')
    extractAndSave('logarithmic', 'fullStimulus', 'H.npy', logarithmic)
    print('done logarithmic H full')
    extractAndSave('quadratic', 'fullStimulus', 'H.npy', quadratic)
    print('done quadratic H full')
    extractAndSave('unweighted', 'fullStimulus', 'H.npy', unweighted)
    print('done unweighted H full')
    print('H full runtime: %f'%(local_clock() - instanceTime))

    instanceTime = local_clock()
    central, gaussian, linear, logarithmic, quadratic, unweighted = getSavePaths('H', 'borders')
    extractAndSave('central', 'borders', 'H.npy', central)
    print('done central H borders')
    extractAndSave('gaussian', 'borders', 'H.npy', gaussian)
    print('done gaussian H borders')
    extractAndSave('linear', 'borders', 'H.npy', linear)
    print('done linear H borders')
    extractAndSave('logarithmic', 'borders', 'H.npy', logarithmic)
    print('done logarithmic H borders')
    extractAndSave('quadratic', 'borders', 'H.npy', quadratic)
    print('done quadratic H borders')
    extractAndSave('unweighted', 'borders', 'H.npy', unweighted)
    print('done unweighted H borders')
    print('H borders runtime: %f'%(local_clock() - instanceTime))

    instanceTime = local_clock()
    central, gaussian, linear, logarithmic, quadratic, unweighted = getSavePaths('I', 'fullStimulus')
    extractAndSave('central', 'fullStimulus', 'I.npy', central)
    print('done central I full')
    extractAndSave('gaussian', 'fullStimulus', 'I.npy', gaussian)
    print('done gaussian I full')
    extractAndSave('linear', 'fullStimulus', 'I.npy', linear)
    print('done linear I full')
    extractAndSave('logarithmic', 'fullStimulus', 'I.npy', logarithmic)
    print('done logarithmic I full')
    extractAndSave('quadratic', 'fullStimulus', 'I.npy', quadratic)
    print('done quadratic I full')
    extractAndSave('unweighted', 'fullStimulus', 'I.npy', unweighted)
    print('done unweighted I full')
    print('I full runtime: %f'%(local_clock() - instanceTime))

    instanceTime = local_clock()
    central, gaussian, linear, logarithmic, quadratic, unweighted = getSavePaths('I', 'borders')
    extractAndSave('central', 'borders', 'I.npy', central)
    print('done central I borders')
    extractAndSave('gaussian', 'borders', 'I.npy', gaussian)
    print('done gaussian I borders')
    extractAndSave('linear', 'borders', 'I.npy', linear)
    print('done linear I borders')
    extractAndSave('logarithmic', 'borders', 'I.npy', logarithmic)
    print('done logarithmic I borders')
    extractAndSave('quadratic', 'borders', 'I.npy', quadratic)
    print('done quadratic I borders')
    extractAndSave('unweighted', 'borders', 'I.npy', unweighted)
    print('done unweighted I borders')
    print('I borders runtime: %f'%(local_clock() - instanceTime))

    print('total runtime: %f'%(local_clock() - startTime))


    


    
    

