from PIL import Image
import os
import numpy as np
import concurrent.futures
from pylsl import local_clock

numImages = 15
imageWidth, imageHeight = 50, 50
imageSize = (imageHeight, imageWidth)
WHITE = (255, 255, 255)


# true widths are doubled plus one
widths = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# creates/returns the path to where we save the images and the arrays (within a "stimuli" folder).
def createSavePaths():
    
    # create the path
    curDir = os.path.dirname(__file__)
    stimulusPath = os.path.join(curDir, 'stimuli')
    templatePath = os.path.join(curDir, 'templates')
    stimImagePath = os.path.join(stimulusPath, 'images')
    stimArrayPath = os.path.join(stimulusPath, 'arrays')
    tempImagePath = os.path.join(templatePath, 'images')
    tempArrayPath = os.path.join(templatePath, 'arrays')
    
    # check if folder exists, create it if necessary
    if not os.path.exists(stimulusPath):
        os.mkdir(stimulusPath)
    
    # check if folder exists, create it if necessary
    if not os.path.exists(templatePath):
        os.mkdir(templatePath)
        
    # check if folder exists, create it if necessary
    if not os.path.exists(stimImagePath):
        os.mkdir(stimImagePath)
    
    # check if folder exists, create it if necessary
    if not os.path.exists(stimArrayPath):
        os.mkdir(stimArrayPath)
    
    # check if folder exists, create it if necessary
    if not os.path.exists(tempImagePath):
        os.mkdir(tempImagePath)
    
    # check if folder exists, create it if necessary
    if not os.path.exists(tempArrayPath):
        os.mkdir(tempArrayPath)
        
    return stimImagePath, stimArrayPath, \
        tempImagePath, tempArrayPath

# creates the template images for comparison
def createTemplates(tempImagePath, tempArrayPath):
    
    # find screen center
    horizCenter = imageWidth // 2
    vertCenter = imageHeight // 2

    # make template images for all widths
    for i, width in enumerate(widths):
        
         # create empty array (black)
        array = np.zeros((imageHeight, imageWidth))
        
        for j, row in enumerate(array):
            for k, _ in enumerate(row):
                if abs(j - vertCenter) < width or \
                    abs(k - horizCenter) < width:
                    array[j][k] = 255
    
        # create image and save
        imageName = os.path.join(tempImagePath, 'temp%d.png'%(width * 2))
        image = Image.fromarray(array.astype(np.uint8), 'L')
        image.save(imageName)
        image.close()
        
        # save array
        arrayName = os.path.join(tempArrayPath, 'temp%d.npy'%(width * 2))
        np.save(arrayName, np.ceil(array / 255))

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
    startTime = local_clock()

    stimImagePath, stimArrayPath, tempImagePath, tempArrayPath = createSavePaths()

    # Use ProcessPoolExecutor to parallelize image creation
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Create a list of tasks for each image to be generated
        tasks = [executor.submit(createAndSaveImage, i + 1, stimImagePath, stimArrayPath) for i in range(numImages)]
        
        # Wait for all tasks to complete
        for task in concurrent.futures.as_completed(tasks):
            task.result()
    
    # create the template crosses 
    createTemplates(tempImagePath, tempArrayPath)

    # print the total time to estimate overall runtime
    totalTime = local_clock() - startTime
    print('\n\n\nTotal Runtime: %f'%totalTime)