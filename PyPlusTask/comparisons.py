import numpy as np
from csv import writer
from createImages import imageWidth, imageHeight, imageSize
import concurrent.futures
import os
from pylsl import local_clock

# Defining some global variables
# ===============================================================================
# ===============================================================================

# two types of distance measures we may want to check
# distance from stimuli returns 0 distance if pixel is within the stimuli
# distance from border returns the pixel's distance from the nearest border
distanceTypes = ['fullStimulus', 'borders']

sigma = 1 # constant for gaussian measure
imageCenter = imageWidth // 2 # assumes a square image

# true widths are doubled plus one
widths = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# template names for csv file
templateNames = ['2 r', '4 r', '6 r', '8 r', '10 r', \
                '12 r', '14 r', '16 r', '18 r', '20 r']
header = ['stimulusNumber'] + templateNames + ['metric']

# ===============================================================================
# ===============================================================================



# String/Path Helper Functions
# ===============================================================================
# ===============================================================================

def split(string):
    return string.split('.')[0]

# Define a key function to extract the numerical part of the filename
def extractNumber(filename):
    # Extract the number from the filename and convert it to an integer
    return int(filename.split('.')[0].replace('temp', ''))

# ===============================================================================
# ===============================================================================



# Writing, Saving, and Loading Functions
# ===============================================================================
# ===============================================================================

# array, templates and results save paths
def getPaths():
    curDir = os.path.dirname(__file__)
    
    # where to find stimulus arrays
    stimulusArraysPath = os.path.join(curDir, '..', 'stimuli', 'arrays')
    
    # where to find template arrays
    templateArraysPathFull = os.path.join(curDir, '..', 'templates', 'full', 'arrays')
    templateArraysPathHalf = os.path.join(curDir, '..', 'templates', 'half','arrays')
    templateArraysSPath = os.path.join(curDir, '..', 'templates', 'S', 'arrays')

    # paths for storing results
    resultsPath = os.path.join(curDir, '..', 'statisticalResults')
    linearPath = os.path.join(resultsPath, '..', 'linear')
    quadraticPath = os.path.join(resultsPath, '..', 'quadratic')
    centralPath = os.path.join(resultsPath, '..', 'central')
    logPath = os.path.join(resultsPath, '..', 'logarithmic')
    gaussianPath = os.path.join(resultsPath, '..', 'gaussian')
    unweightedPath = os.path.join(resultsPath, '..', 'unweighted')
    
    # store csv names as a list
    resultPathsList = [linearPath, quadraticPath, centralPath, \
           logPath, unweightedPath, gaussianPath]
    
    # create folders for each of the statistical weighting conditions
    for path in resultPathsList:
        if not os.path.exists(path):

            # directory of the subfolder paths (half and full)
            subDirectories = [os.path.join(path, 'half'), os.path.join(path, 'full'), os.path.join(path, 'S')]

            # make the overall directory (statistical measure name) and subdirectories
            os.makedirs(path, exist_ok = True) 
            for subPath in subDirectories:
                os.mkdir(subPath)
            
    return stimulusArraysPath, templateArraysPathFull, templateArraysPathHalf, templateArraysSPath, resultPathsList

# get one line of results for a given stimulus and metric over all of the templates
def getLine(stimulusFilename, templates, tempArraysPath, meanDict, metric, weightsMatrices, metricName, widths, stimulus, distanceType):

    # prep the results list
    results = [split(stimulusFilename)]

    for i, templateFilename in enumerate(templates):
    
        # load the template and its mean
        templatePath = os.path.join(tempArraysPath, templateFilename)
        template = np.load(templatePath) 
        templateMean = meanDict[templateFilename + metricName]
        weightMatrix = weightsMatrices[templateFilename + metricName]

        # calculate stimulus mean
        stimulusMean = weightedMean(stimulus, weightMatrix)

        result = pearsons(stimulus, template, stimulusMean, templateMean, weightMatrix)
        results.append(str(result))
    
    return results + [str(os.path.basename(metric)).replace('.csv', '')], metric

# ===============================================================================
# ===============================================================================



# Calculation Helper Functions
# ===============================================================================
# ===============================================================================

# returns the minimum distance of a point from any of the relevant point in the stimuli
def getDistance(array, relevantPoints):

    # Convert relevantPoints to a NumPy array for efficient computations
    relevantPoints = np.array(relevantPoints)

    # Extract all row indices and column indices from the array
    i_indices, j_indices = np.indices(array.shape)

    # Calculate the difference in rows and columns between each element in array and each relevant point
    # Using broadcasting, this will generate arrays of differences in dimensions [array_shape x num_relevant_points]
    row_diffs = i_indices[:, :, None] - relevantPoints[:, 0]
    col_diffs = j_indices[:, :, None] - relevantPoints[:, 1]

    # Calculate squared distances using the differences
    squared_distances = row_diffs**2 + col_diffs**2

    # Find the minimum squared distance for each element in array
    min_squared_distances = squared_distances.min(axis=2)

    # Take the square root to get the actual distances
    distances = np.sqrt(min_squared_distances)

    return distances

# extracts the relevant points that we decide to have distance = 0 based on distance type
def getRelevantPoints(file, rowIndices, colIndices, distanceType):
    relevantPoints = []
    for i, _ in enumerate(rowIndices):
        for j, _ in enumerate(colIndices):
            if distanceType == 'fullStimulus':
                if int(file[i][j]) == 0:
                    relevantPoints.append((i,j))
            else:
                # gotta fix this
                if (0 < i < 49 and 0 < j < 49):
                    if int(file[i][j]) == 0 and \
                    (file[i-1][j] == 1 or file[i+1][j] == 1 or
                    file[i][j-1] == 1 or file[i][j+1] == 1 or \
                    file[i+1][j+1] == 1 or file[i+1][j-1] == 1 or \
                    file[i-1][j+1] == 1 or file[i-1][j-1] == 1):
                        relevantPoints.append((i,j))
    return relevantPoints

# get the weighted mean of the image data 
def weightedMean(array, weightMatrix):
    weightedSum = np.sum(weightMatrix * array)
    totalWeight = np.sum(weightMatrix)
    
    if totalWeight > 0:
        return weightedSum / totalWeight
    
    return 0

# ===============================================================================
# ===============================================================================



# Main Calculation Functions
# ===============================================================================
# ===============================================================================

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
        weightsMatrix[nonZeroDistances] = np.log(1 + (1 / distanceMatrix[nonZeroDistances]))
    elif 'gaussian' in metric:
        weightsMatrix[nonZeroDistances] = np.exp(-1 * np.square(distanceMatrix[nonZeroDistances]) / (2 * np.square(sigma)))
    elif 'central' in metric:
        weightsMatrix = np.ones(imageSize)
        rowIndices, colIndices = np.indices(weightsMatrix.shape)
        distanceToCenter = np.sqrt(np.square(rowIndices - imageCenter) + np.square(colIndices - imageCenter))
        distanceToCenter[distanceToCenter == 0] = 0
        distanceToCenter = np.where(np.sqrt(np.square(rowIndices - imageCenter) + np.square(colIndices - imageCenter)) == 0, 1, distanceToCenter)
    
    return weightsMatrix.reshape(imageSize).copy()

# calculates a distance matrix
def distances(filename, folder, distanceType):
    # Load the file
    filepath = os.path.join(folder, filename)
    file = np.load(filepath)

    # Create a grid of row and column indices
    rowIndices, colIndices = np.indices(file.shape)

    relevantPoints = getRelevantPoints(file, rowIndices, colIndices, distanceType)
    distanceMatrix = getDistance(file, relevantPoints)

    return distanceMatrix.flatten()

# calculates the weighted or unweighted pearsons depending on type
def pearsons(stimulus, template, stimulusMean, templateMean, weightMatrix):

    baseStim = stimulus - stimulusMean
    baseTemp = template - templateMean

    numerator = np.sum(weightMatrix * baseStim * baseTemp)
    denomStim = np.sqrt(np.sum(weightMatrix * np.square(baseStim)))
    denomTemp = np.sqrt(np.sum(weightMatrix * np.square(baseTemp)))
    
    return (numerator / (denomStim * denomTemp))

# ===============================================================================
# ===============================================================================



# runs the main portion of the code
def runInstance(stimulusArraysPath, tempArraysPath, distanceType, metricList, widths):
    strrttime = local_clock()
    print('start instance')
    # list the file names in the array and template folders
    stims = sorted(os.listdir(stimulusArraysPath), key = extractNumber)
    print('sorted stims and templates: %f'%(local_clock() - strrttime))

    if 'full' in tempArraysPath or 'half' in tempArraysPath:
        templates = sorted(os.listdir(tempArraysPath), key = extractNumber)
    else:
        templates = os.listdir(tempArraysPath)
    print('sorted stims and templates: %f'%(local_clock() - strrttime))

    # calculate a set of weight and distance matrices
    distanceMatrices = {}
    weightsMatrices = {}
    for i, template in enumerate(templates):
        distanceMatrices[template] = distances(template, tempArraysPath, distanceType)
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
            meanDict[template + metricName] = weightedMean(file, weightMatrix)
    print('means distances and weights calculated: %f'%(local_clock() - strrttime))


    # write the headers for each file
    for metric in metricList:

        # different save paths for different stimulus types (half crosses vs full crosses)
        if 'full' in tempArraysPath:
            savePath = os.path.join(metric, 'full')
        elif 'half' in tempArraysPath: 
            savePath = os.path.join(metric, 'half')
        else:
            savePath = os.path.join(metric, 'S')
        
        if distanceType == 'borders': # different csv files for different distance types
            savePath = os.path.join(savePath, 'borders.csv')
        else:
            savePath = os.path.join(savePath, 'fullStimulus.csv')

        # open the metric-specific csv file for writing
        with open(savePath, 'w', newline = '') as f:
        
            # setup a writer/header and write the header
            write = writer(f)
            if 'full' in tempArraysPath or 'half' in tempArraysPath:
                write.writerow(header)
            else:
                write.writerow(['stimulusNumber', 'S r', 'metric'])
    print('headers written: %f'%(local_clock() - strrttime))


    #  collect all of the tasks for future parallel execution
    taskCounter = 0
    taskTimer = local_clock()
    tasks = []
    i = 0
    for stimulusFilename in stims:
        stimulusNum = os.path.basename(stimulusFilename)
        stimulusNumber = int(stimulusNum.replace('.npy', ''))
        if i % 10000 == 0:
            print(i)
            print('runtime for %d stimuli: %f'%(i, local_clock()- strrttime))
        i += 1
        
        metricName = os.path.basename(split(metric))

        # for each array, perform the analysis on all of the templates
        for metric in metricList:

            # delete all of this
            # ----------------------------------
            # ----------------------------------
            # if not 'linear' in metric:
            #     if stimulusNumber <= 998433:
            #         continue
            # else:
            #     if stimulusNumber <= 998434:
            #         continue
            # ----------------------------------
            # ----------------------------------

            metricName = os.path.basename(split(metric))

            # load the stimulus
            stimulusPath = os.path.join(stimulusArraysPath, stimulusFilename)
            stimulus = np.load(stimulusPath)

            tasks.append([stimulusFilename, templates, tempArraysPath, meanDict, metric, weightsMatrices, metricName, widths, stimulus, distanceType])
            if len(tasks) >= 10000:
                print('execute')
                executeTasks(tasks)
                tasks = []
                taskCounter += 10000
                print('%d tasks completed in %f seconds: '%(taskCounter, local_clock() - taskTimer))

    #executeTasks(tasks) # delete meeeeeeeee
    print('tasks collected: %f'%(local_clock() - strrttime))

# executes tasks in parallel
def executeTasks(tasks):

    i = 0
    with concurrent.futures.ProcessPoolExecutor() as executor:
        time = local_clock()
        future_to_task = {executor.submit(getLine, *task): task for task in tasks}

        for future in concurrent.futures.as_completed(future_to_task):
            results, metric = future.result()
            stimulusFilename, templates, tempArraysPath, meanDict, metric, weightsMatrices, metricName, widths, stimulus, distanceType = future_to_task[future]

            # different save paths for different stimulus types (half crosses vs full crosses)
            if 'full' in tempArraysPath:
                savePath = os.path.join(metric, 'full')
            elif 'half' in tempArraysPath: 
                savePath = os.path.join(metric, 'half')
            else:
                savePath = os.path.join(metric, 'S')
        
            if distanceType == 'borders': # different csv files for different distance types
                savePath = os.path.join(savePath, 'borders.csv')
            else:
                savePath = os.path.join(savePath, 'fullStimulus.csv')
            with open(savePath, 'a', newline = '') as f:
                # setup a writer/header and write the header
                write = writer(f)
                write.writerow(results)        
            i += 1
            if i % 1000 == 0:
                print('%d runtime: %f'%(i, local_clock() - time))


if __name__ == '__main__':
    
    # clock for keeping track of program runtime
    startTime = local_clock()
   
    # various save and load paths
    stimulusArraysPath, templateArraysPathFull, templateArraysPathHalf, templateArraysSPath, metricList = getPaths()
    
    # list and for loop to let me iterate over the stimuli n times for each of n types of templates
    # because I am lazy and dont want to refactor the code
    templateList = [templateArraysPathFull, templateArraysPathHalf, templateArraysSPath]

    for tempArraysPath in templateList:
        for distanceType in distanceTypes:
            # if distanceType == 'fullStimulus' and \
            #     not ('full' in tempArraysPath):
            #     print(tempArraysPath)
            #     print(distanceType)
            #     continue
            iterationStart = local_clock()
            runInstance(stimulusArraysPath, tempArraysPath, distanceType, metricList, widths)
            print('Iteration Runtime: %f'%(local_clock() - iterationStart))
    
    # print the runtime
    print('runtime: %f'%(local_clock() - startTime))  