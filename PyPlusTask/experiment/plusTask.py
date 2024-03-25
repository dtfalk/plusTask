# tests have been run and there is no overlapping stimuli
from psychopy import visual, core
from random import randint
from helperFunctions import *
    
showTempEveryConstant = 1.7

# The experiment itself
def experiment(gametype, dataSavePath, outlet, win, metric, distanceType, letter, templateShowType):
    win.color = altBackgroundColor

    # get images for stimuli and preps their paths
    curDir = os.path.dirname(__file__)
    Himages, Iimages = getImages(metric, distanceType, gametype)
    images = Himages + Iimages
    imagesDir = os.path.join(curDir, '..', '..', 'stimuli', 'images')
    extension = '.png'

    # various variables for handling the game
    reset = False
    startTime = core.Clock()
    firstWrite = True # check to make sure that we are not overwriting an existing file

    # initialize a starting image
    while True:
        randomIndex = randint(1, len(images))
        stimulusNumber = images[randomIndex - 1]
        imagePath = os.path.join(imagesDir, str(stimulusNumber) + extension)
        if templateShowType == 'every':
            image = visual.ImageStim(win = win, image = imagePath, size = (scaledImageSize[0] / showTempEveryConstant, scaledImageSize[1] / showTempEveryConstant), units = 'pix', pos = ((screenWidth / 10) - scaledImageSize[0] / 2, 0))
            templateImagePath = os.path.join(os.path.dirname(__file__), 'templates', '%s.png'%letter)
            templateImage = visual.ImageStim(win = win, image = templateImagePath, size = (scaledImageSize[0] / showTempEveryConstant, scaledImageSize[1] / showTempEveryConstant), units = 'pix', pos = ((scaledImageSize[0] / 2) - (screenWidth / 10), 0))
        else: 
            image = visual.ImageStim(win = win, image = imagePath, size = scaledImageSize, units = 'pix')
        images.remove(stimulusNumber)
        break
    
    # Loop for handling events
    while True:
        
        # handling key presses
        for key in event.getKeys():
            if key == 'escape':
                win.close()
                core.quit()
            elif key == 'y' or key == 'n':
                reset = True # indicates we will reset the experiment

                # user's response to a stimulus
                if key == 'y':
                    response = True
                else:
                    response = False

                # saves user's response
                if gametype == 'real':
                    responseTime = startTime.getTime()
                    pushSample(outlet, str(response))
                    recordResponse(dataSavePath, response, responseTime, stimulusNumber, firstWrite, letter)
                    firstWrite = False
            
        # while the trial continues on
        if not reset:
            if templateShowType == 'every':
                templateImage.draw()
            image.draw()
            win.flip()
            
        # end of a trial
        else:
            reset = False
            win.flip()
            event.clearEvents()
            
            # end trial if we have shown all of the images
            if (len(images) == 0):
                return
            
            # get a new image
            randomIndex = randint(1, len(images))
            stimulusNumber = images[randomIndex - 1]
            imagePath = os.path.join(imagesDir, str(stimulusNumber) + extension)
            if templateShowType == 'every':
                image = visual.ImageStim(win = win, image = imagePath, size = (scaledImageSize[0] / showTempEveryConstant, scaledImageSize[1] / showTempEveryConstant), units = 'pix', pos = ((screenWidth / 10) - scaledImageSize[0] / 2, 0))
                templateImagePath = os.path.join(os.path.dirname(__file__), 'templates', '%s.png'%letter)
                templateImage = visual.ImageStim(win = win, image = templateImagePath, size = (scaledImageSize[0] / showTempEveryConstant, scaledImageSize[1] / showTempEveryConstant), units = 'pix', pos = ((scaledImageSize[0] / 2) - (screenWidth / 10), 0))
            else:
                image = visual.ImageStim(win = win, image = imagePath, size = scaledImageSize, units = 'pix')
            images.remove(stimulusNumber)
            
            # reset the trial timer
            startTime.reset()
            win.callOnFlip(pushSample, outlet = outlet, tag = 'STRT')

# handles the overall experiment flow
if __name__ == '__main__':
    
    # Create LSL outlet
    outlet = initializeOutlet()
    
    # initialize window and mouse object (set mouse to invisible)
    win = visual.Window(size = screenSize, fullscr = True, color = backgroundColor)
    mouse = event.Mouse(win = win)
    mouse.setVisible(False)
    
    # get user info and where to store their results
    subjectName, subjectNumber, metric, distanceType, templateShowType, dataSavePath = openingScreen(win)

    # determines whether we ask for them to search for the "H"s or "I"s first
    letterList = ['H', 'I']
    randomInt = randint(0,1)
    if randomInt == 1:
        letterList = ['I', 'H']
    
    firstIteration = True
    for letter in letterList:

        # keeps track of the first letter the subjects were asked to look for
        if firstIteration:
            firstLetter = letter
            firstIteration = False
        
        # explain the experiment to the subject
        experimentExplanation(win, letter)

        # gives the subject some practice trials.
        practiceInstructions(win, letter, templateShowType)
        experiment('practice', dataSavePath, outlet, win, metric, distanceType, letter, templateShowType)
        win.color = backgroundColor
    
        # move onto the real experiment
        realInstructions(win, letter, templateShowType)
        experiment('real', dataSavePath, outlet, win, metric, distanceType, letter, templateShowType)
        win.color = backgroundColor

    # exit screen thanking participant
    exitScreen(win)