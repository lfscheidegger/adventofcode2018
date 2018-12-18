from PIL import Image
from OpenGL.GL import *
import numpy as np


class Texture:
    _type_to_path = {
        '#': './assets/wall.png',
        'E': './assets/elf.png',
        'G': './assets/goblin.png',
        'D': './assets/skull.png',
    }
    
    def __init__(self, type):
        self.type = type

        self._texture_handle = glGenTextures(1)

        image = Image.open(Texture._type_to_path[self.type])
        imageData = np.array(list(image.getdata()), np.uint8)

        glBindTexture(GL_TEXTURE_2D, self._texture_handle)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.size[0], image.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, imageData)
        glBindTexture(GL_TEXTURE_2D, 0)

    def bind(self):
        glBindTexture(GL_TEXTURE_2D, self._texture_handle)
