import os
from pylsl import StreamOutlet, StreamInfo
from psychopy import visual, core, event
import csv
import pandas as pd
from constants import *
from pylsl import local_clock

imageWidth, imageHeight = 50, 50
imageSize = imageWidth * imageHeight
scaleFactor = screenHeight / imageHeight
scaledImageSize = (imageWidth * scaleFactor, imageHeight * scaleFactor)

# This block of code handles lab streaming layer functionality
# =======================================================================
# =======================================================================

# Initializes lab streaming layer outlet
def initializeOutlet():
    infoEvents = StreamInfo('eventStream', 'events', 1, 0, 'string')
    outlet = StreamOutlet(infoEvents)
    return outlet

# pushes a sample to the outlet
def pushSample(outlet, tag):
    outlet.push_sample([tag])

# =======================================================================
# =======================================================================



# These functions are for collecting/saving user/experiment data
# =======================================================================
# =======================================================================

# Returns user name, subject number, and path to where
# we will store their data.
def openingScreen(win):
        
    # current directory
    curDir = os.path.dirname(__file__)
    
    # get user's name and user's subject number
    subjectName, subjectNumber, experimentMetric, experimentDistanceType, templateShowType, win = getSubjectInfo(win)
    
    # create save folder if necessary and get the save path
    subjectDataFolder = os.path.join(curDir, 'subjectData')
    if not os.path.isdir(subjectDataFolder):
        os.mkdir(subjectDataFolder)
    
    # File to where we save the user's data
    dataSavePath = os.path.join(subjectDataFolder, experimentMetric, experimentDistanceType, templateShowType, subjectNumber)
    os.makedirs(dataSavePath, exist_ok = True)

    # add name and number to crosswalk
    addToCrosswalk(subjectNumber, subjectName)
    
    return subjectName, subjectNumber, experimentMetric, experimentDistanceType, templateShowType, dataSavePath

# gets the subject name, subject number, metric type and distance type
def getSubjectInfo(win):
    subjectName = getSubjectName(win)
    subjectNum = getSubjectNum(win)
    experimentMetric = getExperimentMetric(win)
    experimentDistanceType = getExperimentDistanceType(win)
    templateShowType = getTemplateShowType(win)
    
    return subjectName, subjectNum, experimentMetric, experimentDistanceType, templateShowType, win

# gets the subject's name
def getSubjectName(win):
    namePrompt = 'Subject Name: '
    subjectName = ''
    
    while True:
        keys = event.getKeys()
        for key in keys:
            if key == 'escape':
                win.close()
                core.quit()
                return
            elif key == 'return':
                return subjectName
            elif key == 'backspace':
                if subjectName != '':
                    subjectName = subjectName[:-1]
            elif key == 'space':
                subjectName = subjectName + ' '
            elif key in validLetters:
                subjectName = subjectName + key
        prompt = visual.TextStim(win = win, text = namePrompt + subjectName, height = 0.2, color = textColor)
        prompt.draw()
        win.flip()

# gets the subject number
def getSubjectNum(win):
    numPrompt = 'Subject Number: '
    subjectNum = ''
    
    while True:
        keys = event.getKeys()
        for key in keys:
            if key == 'escape':
                win.close()
                core.quit()
                return
            elif key == 'return':
                return subjectNum
            elif key == 'backspace':
                if subjectNum != '':
                    subjectNum = subjectNum[:-1]
            elif key in validNumbers:
                subjectNum = subjectNum + key
        prompt = visual.TextStim(win = win, text = numPrompt + subjectNum, height = 0.2, color = textColor)
        prompt.draw()
        win.flip()

# gets the metric we use for the experiment
def getExperimentMetric(win):
    validEntries = ['gaussian', 'unweighted', 'linear', 'logarithmic', 'quadratic']
    numPrompt = 'metric (gaussian, unweighted, linear, logarithmic, or quadratic): '
    experimentMetric = ''
    
    while True:
        keys = event.getKeys()
        for key in keys:
            if key == 'escape':
                win.close()
                core.quit()
                return
            elif key == 'return':
                if experimentMetric.lower() in validEntries:
                    return experimentMetric.lower()
                else:
                    experimentMetric = ''
            elif key == 'backspace':
                if experimentMetric != '':
                    experimentMetric = experimentMetric[:-1]
            elif key in validLetters:
                experimentMetric = experimentMetric + key
        prompt = visual.TextStim(win = win, text = numPrompt + experimentMetric, height = 0.1, color = textColor)
        prompt.draw()
        win.flip()

# gets the distance type we use for the experiment
def getExperimentDistanceType(win):
    validEntries = ['full stimulus', 'borders']
    numPrompt = 'distance type ("full stimulus" or "borders"): '
    experimentDistanceType = ''
    
    while True:
        keys = event.getKeys()
        for key in keys:
            if key == 'escape':
                win.close()
                core.quit()
                return
            elif key == 'return':
                if experimentDistanceType.lower() in validEntries:
                    if experimentDistanceType == 'full stimulus':
                        return "fullStimulus"
                    else:
                        return "borders"
                else:
                    experimentDistanceType = ''
            elif key == 'backspace':
                if experimentDistanceType != '':
                    experimentDistanceType = experimentDistanceType[:-1]
            elif key == 'space':
                experimentDistanceType = experimentDistanceType + ' '
            elif key in validLetters:
                experimentDistanceType = experimentDistanceType + key
        prompt = visual.TextStim(win = win, text = numPrompt + experimentDistanceType, height = 0.1, color = textColor)
        prompt.draw()
        win.flip()

# gets the manner in which we show the template to the subject ('never', 'once', or 'every' trial)
def getTemplateShowType(win):
    validEntries = ['never', 'once', 'every']
    numPrompt = 'template show type ("never", "once", or "every"): '
    templateShowType = ''
    
    while True:
        keys = event.getKeys()
        for key in keys:
            if key == 'escape':
                win.close()
                core.quit()
                return
            elif key == 'return':
                if templateShowType.lower() in validEntries:
                    return templateShowType
                else:
                    templateShowType = ''
            elif key == 'backspace':
                if templateShowType != '':
                    templateShowType = templateShowType[:-1]
            elif key == 'space':
                templateShowType = templateShowType + ' '
            elif key in validLetters:
                templateShowType = templateShowType + key
        prompt = visual.TextStim(win = win, text = numPrompt + templateShowType, height = 0.1, color = textColor)
        prompt.draw()
        win.flip()

# adds the user's info to the crosswalk
def addToCrosswalk(subjectNumber, subjectName):
    curDir = os.path.dirname(__file__)
    crosswalkPath = os.path.join(curDir, 'subjectData', 'crosswalk.csv')
    fileExists = os.path.isfile(crosswalkPath)

    with open(crosswalkPath, mode = 'a', newline = '') as f:
        writer = csv.writer(f)
        
        # write header if cross walk does not exist yet
        if not fileExists:
            header = ['subject Number', 'Subject Name']
            writer.writerow(header)
        
        # write subject number and subject name as a row
        writer.writerow([subjectNumber, subjectName])

# records a user's response to a given trial
def recordResponse(dataSavePath, response, responseTime, stimulusNumber, firstWrite, letter):
    data = [str(stimulusNumber), str(response), str(responseTime)]
    dataSavePath = os.path.join(dataSavePath, '%s.csv'%letter)
    # if csv file does not exist, then write the header and the data
    if not os.path.exists(dataSavePath):
        header = ['stimulusNumber', 'response', 'responseTime']
        with open(dataSavePath, 'w', newline = '') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerow(data)
            file.close()
    # otherwise just write the data
    else:
        if firstWrite:
            print('\n\n\nYou tried to overwrite an existing file. '\
                  'Please delete the file or pick a new subject number.\n\n\n')
            raise(FileExistsError)
        # check that we are not overwriting an existing file
        with open(dataSavePath, 'a', newline = '') as file:
            writer = csv.writer(file)
            writer.writerow(data)
            file.close()
    return

# =======================================================================
# =======================================================================
        



# This code is for showing various message screens (e.g. experiment explanation)
# =======================================================================
# =======================================================================

# explains the experiment to the subject
def experimentExplanation(win, letter):
    
    # text height and preparing the explanation text
    height = 0.07
    prompt = visual.TextStim(win = win, text = explanationText(letter), height = height,
                            color = textColor, wrapWidth = 1.9, alignText = 'left')
    
    # wait for the user to press spacebar before the experiment continues
    while True:
        keys = event.getKeys()
        for key in keys:
            if key == 'escape':
                win.close()
                core.quit()
            if key == 'space':
                return
        prompt.draw()
        win.flip()

# instructions for the practice trials
def practiceInstructions(win, letter, templateShowType):
    
    # text height and preparing the explanation text
    height = 0.07
    prompt = visual.TextStim(win = win, text = practiceText(letter, templateShowType), height = height,
                            color = textColor, wrapWidth = 1.9, alignText = 'left')
    
    # wait for the user to press spacebar before the experiment continues
    while True:
        keys = event.getKeys()
        for key in keys:
            if key == 'escape':
                win.close()
                core.quit()
                return
            if key == 'space':
                if templateShowType == 'once':
                    showTemplate(win, letter)
                return
        prompt.draw()
        win.flip()

# instructions for the real trials
def realInstructions(win, letter, templateShowType):
    
    # text height and preparing the instructions text
    height = 0.07
    prompt = visual.TextStim(win = win, text = realText(letter, templateShowType), height = height,
                            color = textColor, wrapWidth = 1.9, alignText = 'left')
    
    # wait for the user to press spacebar before the experiment continues
    while True:
        keys = event.getKeys()
        for key in keys:
            if key == 'escape':
                win.close()
                core.quit()
                return
            if key == 'space':
                if templateShowType == 'once':
                    showTemplate(win, letter)
                return
        prompt.draw()
        win.flip()

# shows the stimulus in the "show template once" condition
def showTemplate(win, letter):
    startTime = local_clock()
    curDir = os.path.dirname(__file__)
    templateImagePath = os.path.join(curDir, 'templates', '%s.png'%letter)
    image = visual.ImageStim(win = win, image = templateImagePath, size = scaledImageSize, units = 'pix')

    # wait for the user to press spacebar before the experiment continues
    while local_clock() - startTime < 5:
        keys = event.getKeys()
        for key in keys:
            if key == 'escape':
                win.close()
                core.quit()
                return
            if key == 'space':
                return
        image.draw()
        win.flip()
    return
    
# exit screen thanking the participant
def exitScreen(win):
    # text height and preparing the exit screen text
    height = 0.07
    prompt = visual.TextStim(win = win, text = exitScreenText, height = height,
                            color = textColor, wrapWidth = 1.9, alignText = 'left')
    
    # wait for the user to press spacebar before the experiment continues
    while True:
        keys = event.getKeys()
        for key in keys:
            if key == 'escape':
                win.close()
                core.quit()
                return
            if key == 'space':
                return
        prompt.draw()
        win.flip()

# draw black borders while stimuli being presented
def drawBorders(win, scaledImageSize):
    win.flip()

# =======================================================================
# =======================================================================
    



# Other functions
# =======================================================================
# =======================================================================
    
# gets the images that we will use for the stimuli
def getImages(metric, distanceType, gameType):
    curDir = os.path.dirname(__file__)

    if gameType == 'real':
        HImagesLoad = os.path.abspath(os.path.join(curDir, '..', '..', 'topStimuli', metric, 'H', distanceType, 'CSVs', 'Top', 'Top100.csv'))
        IImagesLoad = os.path.abspath(os.path.join(curDir, '..', '..', 'topStimuli', metric, 'I', distanceType, 'CSVs', 'Top', 'Top100.csv'))
        HImages = pd.read_csv(HImagesLoad)['stimulusNumber'].tolist()
        IImages = pd.read_csv(IImagesLoad)['stimulusNumber'].tolist()
    else:
        HImagesLoad = os.path.abspath(os.path.join(curDir, '..', '..', 'topStimuli', metric, 'H', distanceType, 'CSVs', 'Top', 'Top1000.csv'))
        IImagesLoad = os.path.abspath(os.path.join(curDir, '..', '..', 'topStimuli', metric, 'I', distanceType, 'CSVs', 'Top', 'Top1000.csv'))
        HImages = pd.read_csv(HImagesLoad)['stimulusNumber'].tolist()[100:110]
        IImages = pd.read_csv(IImagesLoad)['stimulusNumber'].tolist()[100:110]

    return HImages, IImages

# =======================================================================
# =======================================================================
    
    