import os
import numpy as np
from PIL import Image

if __name__ == '__main__':
    curDir = os.path.dirname(__file__)
    arrayPath = os.path.abspath(os.path.join(curDir, '..', 'templates', 'I', 'arrays', 'I.npy'))
    array = np.load(arrayPath) * 255
    image = Image.fromarray(array.astype(np.uint8), 'L')
    image.save(os.path.join(os.path.dirname(__file__), 'I.png'))