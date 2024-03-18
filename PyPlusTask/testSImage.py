import os
import numpy as np
from PIL import Image

if __name__ == '__main__':
    curDir = os.path.dirname(__file__)
    imagePath = os.path.join(curDir, 'tempS.png')
    image = Image.open(imagePath)
    array = np.array(image)
    print(array.shape)