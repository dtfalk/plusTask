import csv
import os
import numpy as np
from PIL import Image
from pylsl import local_clock
from createImages import imageWidth, imageHeight

def compose(n, metric, templateType, distanceType, templateNumber):
    curDir = os.path.dirname(__file__)
    
    # read the relevant CSV file and collect all of the stimuli numbers
    topNStimuliNumbers = []
    bottomNStimuliNumbers = []
    if templateType == 'full' or templateType == 'half':
        topNLoadPath = os.path.join(curDir, 'topStimuli', metric, templateType, distanceType, 'CSVs', templateNumber, 'Top', 'Top%d.csv'%n)
        bottomNLoadPath = os.path.join(curDir, 'topStimuli', metric, templateType, distanceType, 'CSVs', templateNumber, 'Bottom', 'Bottom%d.csv'%n)
    else:
        topNLoadPath = os.path.join(curDir, 'topStimuli', metric, templateType, distanceType, 'CSVs', 'Top', 'Top%d.csv'%n)
        bottomNLoadPath = os.path.join(curDir, 'topStimuli', metric, templateType, distanceType, 'CSVs', 'Bottom', 'Bottom%d.csv'%n)

    with open(topNLoadPath, 'r', newline = '') as f:
        reader = csv.reader(f)
        lines = list(reader)
        for i, line in enumerate(lines):
            if i == 0:
                continue
            topNStimuliNumbers.append(line[0]) # append the stimuli number
    
    with open(bottomNLoadPath, 'r', newline = '') as f:
        reader = csv.reader(f)
        lines = list(reader)
        for i, line in enumerate(lines):
            if i == 0:
                continue
            bottomNStimuliNumbers.append(line[0]) # append the stimuli number
    
    # load the relevant arrays into a list
    topNStimuli = []
    for stimulusNumber in topNStimuliNumbers:
        loadPath = os.path.join(curDir, 'stimuli', 'arrays', '%s.npy'%stimulusNumber)
        stimuliArray = np.load(loadPath)
        topNStimuli.append(stimuliArray.copy()) 
    
    bottomNStimuli = []
    for stimulusNumber in bottomNStimuliNumbers:
        loadPath = os.path.join(curDir, 'stimuli', 'arrays', '%s.npy'%stimulusNumber)
        stimuliArray = np.load(loadPath)
        bottomNStimuli.append(stimuliArray.copy()) 
        
    
    # add the arrays from topNSTimuli List
    compositeArrayTopN = np.zeros((imageHeight, imageWidth))
    for array in topNStimuli:
        compositeArrayTopN += array
    compositeArrayTopN = (compositeArrayTopN / n) * 255

    # add the arrays from topNSTimuli List
    compositeArrayBottomN = np.zeros((imageHeight, imageWidth))
    for array in bottomNStimuli:
        compositeArrayBottomN += array
    compositeArrayBottomN = (compositeArrayBottomN / n) * 255
    
    # save composite arrays to relevant folders
    if templateType == 'full' or templateType == 'half':
        compositeArraySavePathTopN = os.path.join(curDir, 'topStimuli', metric, templateType, distanceType, 'arrays', templateNumber, 'Top', 'Composite%d.npy'%n)
        compositeArraySavePathBottomN = os.path.join(curDir, 'topStimuli', metric, templateType, distanceType, 'arrays', templateNumber, 'Bottom', 'Composite%d.npy'%n)
    else:
        compositeArraySavePathTopN = os.path.join(curDir, 'topStimuli', metric, templateType, distanceType, 'arrays', 'Top', 'Composite%d.npy'%n)
        compositeArraySavePathBottomN = os.path.join(curDir, 'topStimuli', metric, templateType, distanceType, 'arrays', 'Bottom', 'Composite%d.npy'%n)
    os.makedirs(os.path.dirname(compositeArraySavePathBottomN), exist_ok = True)    
    os.makedirs(os.path.dirname(compositeArraySavePathTopN), exist_ok = True)

    np.save(compositeArraySavePathBottomN, compositeArrayBottomN)
    np.save(compositeArraySavePathTopN, compositeArrayTopN)

    # save composite images to relevant folders
    if templateType == 'full' or templateType == 'half':
        compositeImageSavePathTopN = os.path.join(curDir, 'topStimuli', metric, templateType, distanceType, 'images', templateNumber, 'Top', 'Composite%d.png'%n)
        compositeImageSavePathBottomN = os.path.join(curDir, 'topStimuli', metric, templateType, distanceType, 'images', templateNumber, 'Bottom', 'Composite%d.png'%n)
    else:
        compositeImageSavePathTopN = os.path.join(curDir, 'topStimuli', metric, templateType, distanceType, 'images', 'Top', 'Composite%d.png'%n)
        compositeImageSavePathBottomN = os.path.join(curDir, 'topStimuli', metric, templateType, distanceType, 'images', 'Bottom', 'Composite%d.png'%n)
    os.makedirs(os.path.dirname(compositeImageSavePathTopN), exist_ok = True)
    os.makedirs(os.path.dirname(compositeImageSavePathBottomN), exist_ok = True)

    compositeImageTopN = Image.fromarray(compositeArrayTopN.astype(np.uint8), 'L')
    compositeImageTopN.save(compositeImageSavePathTopN)
    compositeImageTopN.close()

    compositeImageBottomN = Image.fromarray(compositeArrayBottomN.astype(np.uint8), 'L')
    compositeImageBottomN.save(compositeImageSavePathBottomN)
    compositeImageBottomN.close()
            

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
                    compose(10, metric, templateType, distanceType, templateNumber)
                    compose(100, metric, templateType, distanceType, templateNumber)
                    compose(1000, metric, templateType, distanceType, templateNumber)
    
    print('runtime: %f'%(local_clock() - startTime))