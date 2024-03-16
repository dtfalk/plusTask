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
    if templateType == 'full' or templateType == 'half':
        topNLoadPath = os.path.join(curDir, 'topStimuli', metric, templateType, distanceType, 'CSVs', templateNumber, 'Top%d.csv'%n)
    else:
        topNLoadPath = os.path.join(curDir, 'topStimuli', metric, templateType, distanceType, 'CSVs', 'Top%d.csv'%n)

    with open(topNLoadPath, 'r', newline = '') as f:
        reader = csv.reader(f)
        lines = list(reader)
        for i, line in enumerate(lines):
            if i == 0:
                continue
            topNStimuliNumbers.append(line[0]) # append the stimuli number
        
    
    # load the relevant arrays into a list
    topNStimuli = []
    for stimulusNumber in topNStimuliNumbers:
        loadPath = os.path.join(curDir, 'stimuli', 'arrays', '%s.npy'%stimulusNumber)
        stimuliArray = np.load(loadPath)
        topNStimuli.append(stimuliArray.copy()) 
        
    
    # add the arrays from topNSTimuli List
    compositeArray = np.zeros((imageHeight, imageWidth))
    for array in topNStimuli:
        compositeArray += array
    compositeArray = (compositeArray / n) * 255
    
    # save composite arrays to relevant folders
    if templateType == 'full' or templateType == 'half':
        compositeArraySavePath = os.path.join(curDir, 'topStimuli', metric, templateType, distanceType, 'arrays', templateNumber, 'Composite%d.npy'%n)
    else:
        compositeArraySavePath = os.path.join(curDir, 'topStimuli', metric, templateType, distanceType, 'arrays', 'Composite%d.npy'%n)
    np.save(compositeArraySavePath, compositeArray)

    # save composite images to relevant folders
    if templateType == 'full' or templateType == 'half':
        compositeImageSavePath = os.path.join(curDir, 'topStimuli', metric, templateType, distanceType, 'images', templateNumber, 'Composite%d.png'%n)
    else:
        compositeImageSavePath = os.path.join(curDir, 'topStimuli', metric, templateType, distanceType, 'images', 'Composite%d.png'%n)
    compositeImage = Image.fromarray(compositeArray.astype(np.uint8), 'L')
    compositeImage.save(compositeImageSavePath)
    compositeImage.close()

    
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