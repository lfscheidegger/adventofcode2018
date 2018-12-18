from PIL import Image
from OpenGL.GL import *
import numpy as np

class Number:
    _digit_textures = [None] * 10
    _digit_to_path = [
        './assets/digit_0.png',
        './assets/digit_1.png',
        './assets/digit_2.png',
        './assets/digit_3.png',
        './assets/digit_4.png',
        './assets/digit_5.png',
        './assets/digit_6.png',
        './assets/digit_7.png',
        './assets/digit_8.png',
        './assets/digit_9.png',
    ]
    
    @staticmethod
    def draw(number, position, height):
        number_str = str(number)

        y = height - position[1] - 1
        x = position[0]
        
        for digit_in_str_idx in range(len(number_str)):
            digit = number_str[digit_in_str_idx]
            digit_idx = ord(digit) - ord('0')
            if Number._digit_textures[digit_idx] is None:
                Number._init_texture(digit_idx)

            glBindTexture(GL_TEXTURE_2D, Number._digit_textures[digit_idx])
            digit_x = x + digit_in_str_idx * 0.4

            glBegin(GL_TRIANGLES)
            glTexCoord2f(0, 1)
            glVertex2f(digit_x, y)
        
            glTexCoord2f(1, 1)        
            glVertex2f(digit_x+0.4, y)

            glTexCoord2f(1, 0)        
            glVertex2f(digit_x+0.4, y+0.4)


            glTexCoord2f(0, 1)        
            glVertex2f(digit_x, y)

            glTexCoord2f(1, 0)        
            glVertex2f(digit_x+0.4, y+0.4)

            glTexCoord2f(0, 0)                
            glVertex2f(digit_x, y+0.4)
            glEnd()

            glBindTexture(GL_TEXTURE_2D, 0)
            


    @staticmethod
    def _init_texture(idx):
        Number._digit_textures[idx] = glGenTextures(1)

        image = Image.open(Number._digit_to_path[idx])
        imageData = np.array(list(image.getdata()), np.uint8)

        glBindTexture(GL_TEXTURE_2D, Number._digit_textures[idx])
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.size[0], image.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, imageData)
        glBindTexture(GL_TEXTURE_2D, 0)
