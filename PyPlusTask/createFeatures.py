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
    templateImagePathLeft = os.path.join(curDir, '..', 'templates', 'LeftFeature', 'images')
    templateArrayPathLeft = os.path.join(curDir, '..', 'templates', 'LeftFeature','arrays')
    templateImagePathRight = os.path.join(curDir, '..', 'templates', 'RightFeature', 'images')
    templateArrayPathRight = os.path.join(curDir, '..', 'templates', 'RightFeature','arrays')
    templateImagePathTop = os.path.join(curDir, '..', 'templates', 'TopFeature', 'images')
    templateArrayPathTop = os.path.join(curDir, '..', 'templates', 'TopFeature','arrays')
    templateImagePathBottom = os.path.join(curDir, '..', 'templates', 'BottomFeature', 'images')
    templateArrayPathBottom = os.path.join(curDir, '..', 'templates', 'BottomFeature','arrays')
    templateImagePathHorizontalMiddle = os.path.join(curDir, '..', 'templates', 'HorizontalMiddleFeature', 'images')
    templateArrayPathHorizontalMiddle = os.path.join(curDir, '..', 'templates', 'HorizontalMiddleFeature','arrays')
    templateImagePathVerticalMiddle = os.path.join(curDir, '..', 'templates', 'VerticalMiddleFeature', 'images')
    templateArrayPathVerticalMiddle = os.path.join(curDir, '..', 'templates', 'VerticalMiddleFeature','arrays')
    templatePaths = [templateImagePathLeft, templateArrayPathLeft, templateImagePathRight, templateArrayPathRight,
                     templateImagePathTop, templateArrayPathTop, templateImagePathBottom, templateArrayPathBottom,
                     templateImagePathHorizontalMiddle, templateArrayPathHorizontalMiddle, 
                     templateImagePathVerticalMiddle, templateArrayPathVerticalMiddle]

    # paths to the stimuli folders

    # create the directory for each of the stimlus/template paths defined above
    for path in templatePaths:
        os.makedirs(name = path, exist_ok = True)
    
    # return all of the various paths
    return templatePaths

# creates the full screen template images for comparison
def createFeaturesTemplates(templateImagePath, templateArrayPath, feature):

    # create empty array (white)
    array = np.ones((imageHeight, imageWidth)) * 255
    
    middleBarHeight = 2
    sideBarsWidths = 2
    for i, row in enumerate(array):
        for j, _ in enumerate(row):
            if feature == 'Left' or feature == 'Top':
                if ((imageWidth / 4) - 1 <=  j <= ((imageWidth / 4)  + (2 * sideBarsWidths))) and (abs(i - (imageHeight / 2)) <= imageHeight / 4):
                    array[i][j] = 0
            elif feature == 'Right' or feature == 'Bottom':
                if ((3 * imageWidth / 4) - (2 * sideBarsWidths) - 2) <  j < (3 * imageWidth / 4) - 1 and (abs(i - (imageHeight / 2)) <= imageHeight / 4):
                    array[i][j] = 0
            elif feature == 'HorizontalMiddle' or feature == 'VerticalMiddle':
                if (abs(i - (imageHeight / 2)) <= middleBarHeight and abs(j - (imageWidth / 2)) < (imageWidth / 4) - 1):
                    array[i][j] = 0 # handles the middle bar of the "H"
    
    if feature == 'Top' or feature == 'Bottom' or feature == 'VerticalMiddle':
        print('here')
        arrayNew = array.T
    else:
        arrayNew = array.copy()
    
    # create image and save
    imageName = os.path.join(templateImagePath, '%s.png'%feature)
    image = Image.fromarray(arrayNew.astype(np.uint8), 'L')
    image.save(imageName)
    image.close()
    
    # save array
    arrayName = os.path.join(templateArrayPath, '%s.npy'%feature)
    np.save(arrayName, np.ceil(arrayNew / 255))

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
    templateImagePathLeft, templateArrayPathLeft, templateImagePathRight, templateArrayPathRight, \
    templateImagePathTop, templateArrayPathTop, templateImagePathBottom, templateArrayPathBottom, \
    templateImagePathHorizontalMiddle, templateArrayPathHorizontalMiddle, \
    templateImagePathVerticalMiddle, templateArrayPathVerticalMiddle = createSavePaths()
    
    createFeaturesTemplates(templateImagePathLeft, templateArrayPathLeft, 'Left')
    createFeaturesTemplates(templateImagePathRight, templateArrayPathRight, 'Right')
    createFeaturesTemplates(templateImagePathTop, templateArrayPathTop, 'Top')
    createFeaturesTemplates(templateImagePathBottom, templateArrayPathBottom, 'Bottom')
    createFeaturesTemplates(templateImagePathHorizontalMiddle, templateArrayPathHorizontalMiddle, 'HorizontalMiddle')
    createFeaturesTemplates(templateImagePathVerticalMiddle, templateArrayPathVerticalMiddle, 'VerticalMiddle')


    # print the total time to estimate overall runtime
    totalTime = local_clock() - startTime
    print('\n\n\nTotal Runtime: %f'%totalTime)