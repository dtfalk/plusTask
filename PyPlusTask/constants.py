from screeninfo import get_monitors

# number of practice and real stimuli the subject will be shown
numPractice = 5
numReal = 10

backgroundColor = (1,1,1) # background color for screen
textColor = (0, 0, 0) # text color

# get screen size for each monitor in the system
def getScreenInfo():
    winInfo = []
    for m in get_monitors():
        winInfo.append((m.width, m.height))
    return winInfo

# get info for subject screen
winInfo = getScreenInfo()
screenSize = winInfo[0]
screenWidth = winInfo[0][0]
screenHeight = winInfo[0][1]

# getting the valid letters and numbers for user info.
def getValidChars():
    validLetters = []
    validNumbers = []
    
    # valid digits (0 - 9)
    for i in range(48, 58):
        validNumbers.append(chr(i))
        
    # valid lowercase letters (a - z)
    for i in range(97, 123):
        validLetters.append(chr(i))
        
    # valid uppercase letters (A - Z)
    for i in range(65, 91):
        validLetters.append(chr(i))
    
    return validLetters, validNumbers

validLetters, validNumbers = getValidChars()

explanationText = 'You will be shown a series of images.\n\n'\
                    'In some of these images there is a hidden "+" sign in the middle '\
                    'of the image on the screen.\n\nPlease press "Y" if you believe that '\
                    'you see a cross hidden in the middle of the image.\n\n' \
                    'Please press "N" if you do not believe that you see a cross hidden in the middle '\
                    'of the image.\n\n\n'\
                    'Please let your experimenter know if you encounter any issues or if you would '\
                    'like to terminate your participation in the experiment.\n\n\n\n'\
                    'Press the spacebar to continue.\n\n\n'\

practiceText = 'You will now be given %d practice stimuli.\n\n\n\n'\
                'Remember to press "Y" if you believe that you see a hidden "+" sign.\n\n\n\n'\
                'Remember to press "N" if you do not believe that you see a hidden "+" sign.\n\n\n\n'\
                'Press the spacebar to continue.'%numPractice
                
realText = 'You will now participate in the real experiment\n\n\n\n'\
            'Remember to press "Y" if you believe that you see a hidden "+" sign.\n\n\n\n'\
            'Remember to press "N" if you do not believe that you see a hidden "+" sign.\n\n\n\n'\
            'Press the spacebar to continue.'


                        
    

 