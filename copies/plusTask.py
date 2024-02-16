from psychopy import visual, core
from random import randint
from createImages import numImages, imageWidth, imageHeight
from helperFunctions import *

# factor by which to scale each of the stimuli
imageSize = imageWidth * imageHeight
scaleFactor = screenHeight / imageHeight
scaledImageSize = (imageWidth * scaleFactor, imageHeight * scaleFactor)

# The experiment itself
def experiment(gametype, dataSavePath, outlet, win, subjectName, subjectNumber):
    
    # path for images folder and image extension label
    curDir = os.path.dirname(__file__)
    imagesDir = os.path.join(curDir, 'stimuli', 'images')
    extension = '.png'

    # various variables for handling the game
    imagesShown = 0
    reset = False
    startTime = core.Clock()
    firstWrite = True # check to make sure that we are not overwriting an existing file

    # initialize a starting image
    while True:
        stimulusNumber = randint(1, numImages)
        imagePath = os.path.join(imagesDir, str(stimulusNumber) + extension)
        if not stimulusNumber in usedImages:
            image = visual.ImageStim(win = win, image = imagePath, 
                                     size = scaledImageSize, units = 'pix')
            break
    
    # Loop for handling events
    while True:
        
        # break loop if we have shown the specified number of images
        if (imagesShown >= numReal and gametype == 'real') \
        or (imagesShown >= numPractice and gametype == 'practice'):
            return
        
        # handling key presses
        for key in event.getKeys():
            if key == 'escape':
                win.close()
                core.quit()
            elif key == 'y':
                reset = True
                if gametype == 'real':
                    responseTime = startTime.getTime()
                    pushSample(outlet, 'YEySS')
                    recordResponse(dataSavePath, True, responseTime, subjectName, 
                                    subjectNumber, stimulusNumber, firstWrite)
                    firstWrite = False
            elif key == 'n':
                reset = True
                if gametype == 'real':
                    responseTime = startTime.getTime()
                    pushSample(outlet, 'NOOO')
                    recordResponse(dataSavePath, False, responseTime, subjectName,
                                    subjectNumber, stimulusNumber, firstWrite)
                    firstWrite = False
            
        # while the trial continues on
        if not reset:
            # define the image and put it on the screen
            image.draw()
            win.flip()
            
        # end of a trial
        else:
            
            # increment/reset variables for next trial
            imagesShown += 1
            reset = False
            win.flip()
            event.clearEvents()
    
            # add the current stimuli number 
            usedImages.append(stimulusNumber)
            
            # get a new iymage
            while True:
                if len(usedImages) == numImages:
                    break
                stimulusNumber = randint(1, numImages)
                imagePath = os.path.join(imagesDir, str(stimulusNumber) + extension)
                if not stimulusNumber in usedImages:
                    image = visual.ImageStim(win = win, image = imagePath,
                                             size = scaledImageSize, units = 'pix')
                    break
            
            # reset the trial timer
            startTime.reset()
            win.callOnFlip(pushSample, outlet = outlet, tag = 'STRT')

if __name__ == '__main__':
    
    # Create LSL outlet
    outlet = initializeOutlet()
    
    # initialize window and mouse object (set mouse to invisible)
    win = visual.Window(size = screenSize, fullscr = True, color = backgroundColor)
    mouse = event.Mouse(win = win)
    mouse.setVisible(False)
    
    # get user info and where to store their results
    subjectName, subjectNumber, dataSavePath = openingScreen(win)
    
    # explain the experiment to the subject
    experimentExplanation(win)
    
    # global variable to keep track of which stimuli we have used
    # so we don't have to keep passing and returning it.
    # Will be referenced in the "experiment" function.
    usedImages = [] 
    
    # gives the subject some practice trials.
    practiceInstructions(win)
    experiment('practice', dataSavePath, outlet, win, subjectName, subjectNumber)
    
    # move onto the real experiment
    realInstructions(win)
    experiment('real', dataSavePath, outlet, win, subjectName, subjectNumber)