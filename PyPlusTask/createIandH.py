from PIL import Image
import os
import numpy as np
import concurrent.futures
from pylsl import local_clock
from shutil import copy

numImages = 10 ** 6
imageWidth, imageHeight = 50, 50
imageSize = (imageHeight, imageWidth)
WHITE = (255, 255, 255)


# true widths are doubled plus one
widths = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# creates/returns the path to where we save the images and the arrays (within a "stimuli" folder).
def createSavePaths():

    # current path to this file
    curDir = os.path.dirname(__file__)

    # paths to the various template folders
    templateImagePathH = os.path.join(curDir, '..', 'templates', 'H', 'images')
    templateArrayPathH = os.path.join(curDir, '..', 'templates', 'H','arrays')
    templateImagePathI = os.path.join(curDir, '..', 'templates', 'I', 'images')
    templateArrayPathI = os.path.join(curDir, '..', 'templates', 'I','arrays')
    templatePaths = [templateImagePathH, templateArrayPathH,
                     templateImagePathI, templateArrayPathI]

    # paths to the stimuli folders

    # create the directory for each of the stimlus/template paths defined above
    for path in templatePaths:
        os.makedirs(name = path, exist_ok = True)
    
    # return all of the various paths
    return templatePaths

# creates the full screen template images for comparison
def createHandITemplates(templateImagePathH, templateArrayPathH, templateImagePathI, templateArrayPathI):

    # create empty array (white)
    array = np.ones((imageHeight, imageWidth)) * 255
    
    middleBarHeight = 2
    sideBarsWidths = 2
    for i, row in enumerate(array):
        for j, _ in enumerate(row):
            # Note: heightCenter is the horizontal line across the center and
            # widthCenter is the vertical line through the center
            if (abs(i - (imageHeight / 2)) <= middleBarHeight and abs(j - (imageWidth / 2)) < (imageWidth / 4) - 1):
                array[i][j] = 0 # handles the middle bar of the "H"
            elif ((imageWidth / 4) - 1 <=  j <= ((imageWidth / 4)  + (2 * sideBarsWidths)) or ((3 * imageWidth / 4) - (2 * sideBarsWidths) - 2) <  j < (3 * imageWidth / 4) - 1) \
                and (abs(i - (imageHeight / 2)) <= imageHeight / 4):
                array[i][j] = 0 # handles the side bars of the "H"
    
    # create H image and save
    imageNameH = os.path.join(templateImagePathH, 'H.png')
    imageH = Image.fromarray(array.astype(np.uint8), 'L')
    imageH.save(imageNameH)
    imageH.close()
    
    # save H array
    arrayNameH = os.path.join(templateArrayPathH, 'H.npy')
    np.save(arrayNameH, np.ceil(array / 255))



    # create I image and save
    imageNameI = os.path.join(templateImagePathI, 'I.png')
    imageI = Image.fromarray(array.astype(np.uint8).T, 'L')
    imageI.save(imageNameI)
    imageI.close()
    
    # save array
    arrayNameI = os.path.join(templateArrayPathI, 'I.npy')
    np.save(arrayNameI, np.ceil(array.T / 255))

# Function to create and save a single image
def createAndSaveImage(stimuliNumber, imagesFolderPath, arraysFolderPath):
    imageName = os.path.join(imagesFolderPath, f'{stimuliNumber}.png')
    arrayName = os.path.join(arraysFolderPath, f'{stimuliNumber}.npy')
    
    # Creates a randomly assigned black and white image
    array = np.random.randint(2, size = imageSize, dtype = np.uint8)
    image = Image.fromarray(array * 255, 'L')
    
    # Save the new image and the array
    image.save(imageName)
    np.save(arrayName, array)
    image.close()

if __name__ == '__main__':

    # clock for checking runtime on the device running the code
    startTime = local_clock()

    # the various relevant paths for where to save images
    templateImagePathH, templateArrayPathH, \
    templateImagePathI, templateArrayPathI = createSavePaths()
    
    createHandITemplates(templateImagePathH, templateArrayPathH, templateImagePathI, templateArrayPathI)


    # print the total time to estimate overall runtime
    totalTime = local_clock() - startTime
    print('\n\n\nTotal Runtime: %f'%totalTime)