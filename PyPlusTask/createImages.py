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
    templateImagePathFull = os.path.join(curDir, '..', 'templates', 'full', 'images')
    templateArrayPathFull = os.path.join(curDir, '..', 'templates', 'full', 'arrays')
    templateImagePathHalf = os.path.join(curDir, '..', 'templates', 'half', 'images')
    templateArrayPathHalf = os.path.join(curDir, '..', 'templates', 'half','arrays')
    templateImagePathS = os.path.join(curDir, '..', 'templates', 'S', 'images')
    templateArrayPathS = os.path.join(curDir, '..', 'templates', 'S', 'arrays')
    templatePaths = [templateImagePathFull, templateArrayPathFull, 
                     templateImagePathHalf, templateArrayPathHalf,
                     templateImagePathS, templateArrayPathS]

    # paths to the stimuli folders
    stimulusImagePath = os.path.join(curDir, '..', 'stimuli', 'images')
    stimulusArrayPath = os.path.join(curDir, '..', 'stimuli', 'arrays')
    stimulusPaths = [stimulusImagePath, stimulusArrayPath]

    # create the directory for each of the stimlus/template paths defined above
    for path in templatePaths + stimulusPaths:
        os.makedirs(name = path, exist_ok = True)
    
    # return all of the various paths
    return tuple(templatePaths + stimulusPaths)

# creates the full screen template images for comparison
def createFullScreenTemplates(templateImagePath, templateArrayPath):
    
    # find screen center
    widthCenter = imageWidth // 2
    heightCenter = imageHeight // 2

    # make template images for all widths
    for i, width in enumerate(widths):
        
         # create empty array (black)
        array = np.ones((imageHeight, imageWidth)) * 255
        
        for j, row in enumerate(array):
            for k, _ in enumerate(row):
                # Note: heightCenter is the horizontal line across the center and
                # widthCenter is the vertical line through the center
                if abs(j - heightCenter) < width or abs(k - widthCenter) < width:
                    array[j][k] = 0
    
        # create image and save
        imageName = os.path.join(templateImagePath, 'temp%d.png'%(width * 2))
        image = Image.fromarray(array.astype(np.uint8), 'L')
        image.save(imageName)
        image.close()
        
        # save array
        arrayName = os.path.join(templateArrayPath, 'temp%d.npy'%(width * 2))
        np.save(arrayName, np.ceil(array / 255))

# creates the full screen template images for comparison
def createHalfScreenTemplates(templateImagePath, templateArrayPath):
    
    # find screen center
    widthCenter = imageWidth // 2
    heightCenter = imageHeight // 2

    # make template images for all widths
    for i, width in enumerate(widths):
        
         # create empty array (black)
        array = np.ones((imageHeight, imageWidth)) * 255
        
        for j, row in enumerate(array):
            for k, _ in enumerate(row):
                if (abs(j - heightCenter) < width and abs(k - widthCenter) < imageWidth / 4) or \
                    (abs(k - widthCenter) < width and abs(j - heightCenter) < imageHeight / 4):
                    array[j][k] = 0
    
        # create image and save
        imageName = os.path.join(templateImagePath, 'temp%d.png'%(width * 2))
        image = Image.fromarray(array.astype(np.uint8), 'L')
        image.save(imageName)
        image.close()
        
        # save array
        arrayName = os.path.join(templateArrayPath, 'temp%d.npy'%(width * 2))
        np.save(arrayName, np.ceil(array / 255))

# add the template S image and create the array
def addSTemplate(templateImagePathS, templateArrayPathS):
    
    # path to the template S used by Shannon and co.
    curDir = os.path.dirname(__file__)
    OGImagePath = os.path.join(curDir, 'tempS.png')

    # create the array and then save it
    image = Image.open(OGImagePath)
    array = np.ceil(np.array(image) / 255)
    arraySavePath = os.path.join(templateArrayPathS, 'tempS.npy')
    np.save(arraySavePath, array)

    # copy the image to the image directory
    copy(OGImagePath, templateImagePathS)

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
    templateImagePathFull, templateArrayPathFull, \
    templateImagePathHalf, templateArrayPathHalf, \
    templateImagePathS, templateArrayPathS, \
    stimulusImagePath, stimulusArrayPath= createSavePaths()

    # Use ProcessPoolExecutor to parallelize image creation
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Create a list of tasks for each image to be generated
        tasks = [executor.submit(createAndSaveImage, i + 1, stimulusImagePath, stimulusArrayPath) for i in range(numImages)]
        
        # Wait for all tasks to complete
        for task in concurrent.futures.as_completed(tasks):
            task.result()
    
    # create the template crosses that span the full screen
    createFullScreenTemplates(templateImagePathFull, templateArrayPathFull)

    # create the template crosses that span half of the screen
    createHalfScreenTemplates(templateImagePathHalf, templateArrayPathHalf)

    # add the template and its array
    addSTemplate(templateImagePathS, templateArrayPathS)

    # print the total time to estimate overall runtime
    totalTime = local_clock() - startTime
    print('\n\n\nTotal Runtime: %f'%totalTime)