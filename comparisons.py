import numpy as np
from csv import writer
from createImages import imageWidth, imageHeight, imageSize
import os
from pylsl import local_clock


sigma = 1
imageCenter = imageWidth // 2 # assumes a square image

# true widths are doubled plus one
widths = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# template names for csv file
templateNames = ['temp2', 'temp4', 'temp6', 'temp8', 'temp10', \
                'temp12', 'temp14', 'temp16', 'temp18', 'temp20']
header = ['stimulus number'] + templateNames

# array, templates and results save paths
def getPaths():
    curDir = os.path.dirname(__file__)
    
    # where to find stimulus arrays
    stimArraysPath = os.path.join(curDir, 'stimuli')
    stimArraysPath = os.path.join(stimArraysPath, 'arrays')
    
    # where to find template arrays
    tempArraysPath = os.path.join(curDir, 'templates')
    tempArraysPath = os.path.join(tempArraysPath, 'arrays')
    
    # paths for storing results
    resultsPath = os.path.join(curDir, 'statisticalResults')
    linearPath = os.path.join(resultsPath, 'linear.csv')
    quadraticPath = os.path.join(resultsPath, 'quadratic.csv')
    centralPath = os.path.join(resultsPath, 'central.csv')
    logPath = os.path.join(resultsPath, 'logarithmic.csv')
    gaussianPath = os.path.join(resultsPath, 'gaussian.csv')
    unweightedPath = os.path.join(resultsPath, 'unweighted.csv')
    
    # store csv names as a list
    resultFilesList = [linearPath, quadraticPath, centralPath, \
            logPath, unweightedPath, gaussianPath]
    
    # create save folder if necessary
    if not os.path.exists(resultsPath):
        os.mkdir(resultsPath)
        
    return stimArraysPath, tempArraysPath, resultFilesList


def split(string):
    return string.split('.')[0]

# get the weighted mean of the image data
def weightedMean(array, weightMatrix):
    weightedSum = np.sum(weightMatrix * array)
    totalWeight = np.sum(weightMatrix)
    
    if totalWeight > 0:
        return weightedSum / totalWeight
    
    return 0

# calculates the weighted or unweighted pearsons depending on type
def pearsons(stimulus, template, stimulusMean, templateMean, weightMatrix):

    baseStim = stimulus - stimulusMean
    baseTemp = template - templateMean
    
    numerator = np.sum(weightMatrix * baseStim * baseTemp)
    denomStim = np.sqrt(np.sum(weightMatrix * np.square(baseStim)))
    denomTemp = np.sqrt(np.sum(weightMatrix * np.square(baseTemp)))
    
    return numerator / (denomStim * denomTemp)

# Define a key function to extract the numerical part of the filename
def extractNumber(filename):
    # Extract the number from the filename and convert it to an integer
    return int(filename.split('.')[0].replace('temp', ''))
    
# calculates a distance matrix
def distances(filename, folder, width):
    # Load the file
    filepath = os.path.join(folder, filename)
    file = np.load(filepath)

    # Create a grid of row and column indices
    rowIndices, colIndices = np.indices(file.shape)

    # Calculate vertical and horizontal distances from the image center
    vertDistances = np.abs(rowIndices - imageHeight / 2) - width
    horizDistances = np.abs(colIndices - imageWidth / 2) - width

    # Calculate the minimum distance from the center for each pixel
    # and set it to 0 if within the width of the cross
    distanceMatrix = np.minimum(vertDistances, horizDistances)
    distanceMatrix = np.where((vertDistances <= width) | (horizDistances <= width), 0, distanceMatrix)

    return distanceMatrix.flatten()

# calculates a weight matrix
def weights(metric, distanceMatrix):
    # creates a matrix of all ones (helps handles divsion by zero)
    weightsMatrix = np.ones_like(distanceMatrix, 'float32')
    
    nonZeroDistances = distanceMatrix != 0
    if 'linear' in metric:
        weightsMatrix[nonZeroDistances] = 1 / distanceMatrix[nonZeroDistances]
    elif 'quadratic' in metric:
        weightsMatrix[nonZeroDistances] = 1 / np.square(distanceMatrix[nonZeroDistances])
    elif 'logarithmic' in metric:
        weightsMatrix[nonZeroDistances] = 1 / np.log(distanceMatrix[nonZeroDistances])
    elif 'gaussian' in metric:
        weightsMatrix[nonZeroDistances] = np.exp(-1 * np.square(distanceMatrix[nonZeroDistances]) / (2 * np.square(sigma)))
    elif 'central' in metric:
        weightsMatrix = np.ones(imageSize)
        rowIndices, colIndices = np.indices(weightsMatrix.shape)
        distanceToCenter = np.sqrt(np.square(rowIndices - imageCenter) + np.square(colIndices - imageCenter))
        distanceToCenter[distanceToCenter == 0] = 0
        distanceToCenter = np.where(np.sqrt(np.square(rowIndices - imageCenter) + np.square(colIndices - imageCenter)) == 0, 1, distanceToCenter)
        
    return weightsMatrix.reshape(imageSize).copy()
    
if __name__ == '__main__':
    startTime = local_clock()
    # various save and load paths
    stimArraysPath, tempArraysPath, metricList = getPaths()
    
    # list the file names in the array and template folders
    stims = sorted(os.listdir(stimArraysPath), key = extractNumber)
    templates = sorted(os.listdir(tempArraysPath), key = extractNumber)

    # calculate a set of weight and distance matrices
    distanceMatrices = {}
    weightsMatrices = {}
    for i, template in enumerate(templates):
        distanceMatrices[template] = distances(template, tempArraysPath, widths[i])
    for matrixName, distanceMatrix in distanceMatrices.items():
        for metric in metricList:
            metricName = os.path.basename(split(metric))
            weightsMatrices[matrixName + metricName] = weights(metric, distanceMatrix)

    # weighted means of templates as a dictionary
    meanDict = {}
    for template in templates:
        for metric in metricList:
            filepath = os.path.join(tempArraysPath, template)
            file = np.load(filepath)
            metricName = os.path.basename(split(metric))
            weightMatrix = weightsMatrices[template + metricName]
            meanDict[template + metric] = weightedMean(file, weightMatrix)
    print('mean calc time: %f'%(local_clock() - startTime))
    
    # perform the weighted vs unweighted pearson tests and save results
    # go over each metric (each metric is stored in a unqiue csv file)
    for metric in metricList:
        metricName = os.path.basename(split(metric))
        
        # open the metric-specific csv file for writing
        with open(metric, 'w', newline = '') as f:
                
            # setup a writer/header and write the header
            write = writer(f)
            write.writerow(header)
            
            # for each array, perform the analysis on all of the templates
            for stimulusFilename in stims:
                
                # load the stimulus
                stimulusPath = os.path.join(stimArraysPath, stimulusFilename)
                stimulus = np.load(stimulusPath)
                
                # prep the results list
                results = [split(stimulusFilename)]
                
                for i, templateFilename in enumerate(templates):
                    
                    # load the template and its mean
                    templatePath = os.path.join(tempArraysPath, templateFilename)
                    template = np.load(templatePath) 
                    templateMean = meanDict[templateFilename + str(metric)]
                    
                    # load stimulus mean if already calculated, otherwise calculate it
                    try:
                        stimulusMean = meanDict[stimulusFilename + metric + str(widths[i])]
                    except KeyError:
                        stimulusMean = weightedMean(stimulus, weightsMatrices[templateFilename + metricName])
                        meanDict[stimulusFilename + metric + str(widths[i])] = stimulusMean
                    
                    result = pearsons(stimulus, template, stimulusMean, templateMean, weightsMatrices[templateFilename + metricName])
                    results.append(str(result))
                write.writerow(results)
            f.close()
    print('runtime: %f'%(local_clock() - startTime))