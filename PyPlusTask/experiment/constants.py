from screeninfo import get_monitors

backgroundColor = (1,1,1) # background color for screen
altBackgroundColor = (int((253 * 2/ 255)) - 1 , int((253 * 2/ 255)) - 1, int((150 * 2/ 255)) - 1)
textColor = (0, 0, 0) # text color



# This block of code gets info about the subject's monitor
# =======================================================================
# =======================================================================

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

# =======================================================================
# =======================================================================

# This block of code defines the valid characters and numbers for text entry
# =======================================================================
# =======================================================================

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

# =======================================================================
# =======================================================================


# This block of code contains the text for explanation screens
# =======================================================================
# =======================================================================

def explanationText(letter):
    return 'You will be shown a series of images.\n\n'\
            'In some of these images there is a hidden "%s" sign in the middle '\
            'of the image on the screen.\n\nPlease press "Y" if you believe that '\
            'you see a "%s" hidden in the middle of the image.\n\n' \
            'Please press "N" if you do not believe that you see a "%s" hidden in the middle '\
            'of the image.\n\n\n'\
            'Please let your experimenter know if you encounter any issues or if you would '\
            'like to terminate your participation in the experiment.\n\n\n\n'\
            'Press the spacebar to continue.\n\n\n'%(letter, letter, letter)
                
def realText(letter, templateShowType):
    if templateShowType == 'never':
        return 'You will now participate in the real experiment\n\n\n\n'\
            'Remember to press "Y" if you believe that you see a hidden "%s" sign.\n\n\n\n'\
            'Remember to press "N" if you do not believe that you see a hidden "%s" sign.\n\n\n\n'\
            'Press the spacebar to continue.'%(letter, letter)
    elif templateShowType == 'once':
        return 'You will now participate in the real experiment\n\n\n\n'\
            'Remember to press "Y" if you believe that you see a hidden "%s" sign.\n\n\n\n'\
            'Remember to press "N" if you do not believe that you see a hidden "%s" sign.\n\n\n\n'\
            'You will now see the "%s" that will be hidden in some of the stimuli.\n\n\n\n'\
            'Press the spacebar to continue.'%(letter, letter, letter)
    else: 
        return 'You will now participate in the real experiment\n\n\n\n'\
            'Remember to press "Y" if you believe that you see a hidden "%s" sign.\n\n\n\n'\
            'Remember to press "N" if you do not believe that you see a hidden "%s" sign.\n\n\n\n'\
            'The "%s" that may or may not be hidden in the image will appear next to each image that you are shown.\n\n\n\n'\
            'Press the spacebar to continue.'%(letter, letter, letter)


def practiceText(letter, templateShowType):
    if templateShowType == 'never':
        return 'You will now be given a set of practice stimuli.\n\n\n\n'\
            'Remember to press "Y" if you believe that you see a hidden "%s" sign.\n\n\n\n'\
            'Remember to press "N" if you do not believe that you see a hidden "%s" sign.\n\n\n\n'\
            'Press the spacebar to continue.'%(letter, letter)
    elif templateShowType == 'once':
        return 'You will now be given a set of practice stimuli.\n\n\n\n'\
            'Remember to press "Y" if you believe that you see a hidden "%s" sign.\n\n\n\n'\
            'Remember to press "N" if you do not believe that you see a hidden "%s" sign.\n\n\n\n'\
            'You will now see the "%s" that will be hidden in some of the stimuli.\n\n\n\n'\
            'Press the spacebar to continue.'%(letter, letter, letter)
    else:
        return 'You will now be given a set of practice stimuli.\n\n\n\n'\
            'Remember to press "Y" if you believe that you see a hidden "%s" sign.\n\n\n\n'\
            'Remember to press "N" if you do not believe that you see a hidden "%s" sign.\n\n\n\n'\
            'The "%s" that may or may not be hidden in the image will appear next to each image that you are shown.\n\n\n\n'\
            'Press the spacebar to continue.'%(letter, letter, letter)


exitScreenText = 'Thank you for participating in this study!\n\n\n\n'\
                'Please notify the experimenter that you have completed the study.\n\n\n\n'\
                'For the experimenter: Press the spacebar to terminate the experiment.'
# =======================================================================
# =======================================================================



                        
    

 