import os
from pylsl import StreamOutlet, StreamInfo
from psychopy import visual, core, event
import csv
from constants import *

# Initializes lab streaming layer outlet
def initializeOutlet():
    infoEvents = StreamInfo('eventStream', 'events', 1, 0, 'string')
    outlet = StreamOutlet(infoEvents)
    return outlet

# pushes a sample to the outlet
def pushSample(outlet, tag):
    outlet.push_sample([tag])
    
# gets the subject's name
# need to check if letter or alpha.
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
                
# gets the subject's name and subject number
def getSubjectInfo(win):
    
    # get subject name and subject number
    subjectName = getSubjectName(win)
    subjectNum = getSubjectNum(win)
    
    return subjectName, subjectNum, win

# Returns user name, subject number, and path to where
# we will store their data.
def openingScreen(win):
    
    # file extenstion where we save data to
    extension = '.csv'
    
    # current directory
    curDir = os.path.dirname(__file__)
    
    # get user's name and user's subject number
    subjectName, subjectNumber, win = getSubjectInfo(win)
    
    # create save folder if necessary and get the save path
    subjectDataFolder = os.path.join(curDir, 'subjectData')
    if not os.path.isdir(subjectDataFolder):
        os.mkdir(subjectDataFolder)
    
    # File to where we save the user's data
    dataSavePath = os.path.join(subjectDataFolder, subjectNumber + extension)
    print('data save path: ' + dataSavePath)
    
    return subjectName, subjectNumber, dataSavePath

# explains the experiment to the subject
def experimentExplanation(win):
    
    # text height and preparing the explanation text
    height = 0.07
    prompt = visual.TextStim(win = win, text = explanationText, height = height,
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

def practiceInstructions(win):
    
    # text height and preparing the explanation text
    height = 0.07
    prompt = visual.TextStim(win = win, text = practiceText, height = height,
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

def realInstructions(win):
    
    # text height and preparing the explanation text
    height = 0.07
    prompt = visual.TextStim(win = win, text = realText, height = height,
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

def recordResponse(dataSavePath, response, responseTime, subjectName,
                    subjectNumber, stimulusNumber, firstWrite):
    data = [str(subjectName), str(subjectNumber), str(stimulusNumber), str(response), str(responseTime)]
    
    # if csv file does not exist, then write the header and the data
    if not os.path.exists(dataSavePath):
        header = ['subjectName', 'subjectNumber', 'stimulusNumber', 'response', 'responseTime']
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

# draw black borders while stimuli being presented?
def drawBorders(win, scaledImageSize):
    win.flip()
    
    