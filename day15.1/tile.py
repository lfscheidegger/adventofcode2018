from OpenGL.GL import *

from texture import Texture

class Tile:
    _wall_texture = None
    _floor_texture = None
    _elf_texture = None
    _goblin_texture = None
    _skull_texture = None
    
    def __init__(self, type, position, state, dead=False):
        self.type = type
        self.dead = dead
        self.position = position
        self.state = state

    def draw(self):
        if self.dead:
            self._draw_skull()
        elif self.type == '#':
            self._draw_wall()
        elif self.type == '.':
            self._draw_floor()
        elif self.type == 'E':
            self._draw_elf()
        elif self.type == 'G':
            self._draw_goblin()
        else:
            raise Exception('Unknown tile type %s' % self.type)

    def _draw_skull(self):
        if Tile._skull_texture is None:
            Tile._skull_texture = Texture('D')
        self._draw_with_texture(Tile._skull_texture)
        
    def _draw_wall(self):
        if Tile._wall_texture is None:
            Tile._wall_texture = Texture('#')
        self._draw_with_texture(Tile._wall_texture)

    def _draw_floor(self):
        if Tile._floor_texture is None:
            Tile._floor_texture = Texture('.')
        self._draw_with_texture(Tile._floor_texture)

    def _draw_elf(self):
        if Tile._elf_texture is None:
            Tile._elf_texture = Texture('E')
        self._draw_with_texture(Tile._elf_texture)

    def _draw_goblin(self):
        if Tile._goblin_texture is None:
            Tile._goblin_texture = Texture('G')
        self._draw_with_texture(Tile._goblin_texture)

    def _draw_with_texture(self, texture):
        x = self.position[0]
        y = self.state.height - self.position[1] - 1

        texture.bind()

        glBegin(GL_TRIANGLES)
        glTexCoord2f(0, 1)
        glVertex2f(x, y)
        
        glTexCoord2f(1, 1)        
        glVertex2f(x+1, y)

        glTexCoord2f(1, 0)        
        glVertex2f(x+1, y+1)


        glTexCoord2f(0, 1)        
        glVertex2f(x, y)

        glTexCoord2f(1, 0)        
        glVertex2f(x+1, y+1)

        glTexCoord2f(0, 0)                
        glVertex2f(x, y+1)
        glEnd()

        glBindTexture(GL_TEXTURE_2D, 0)
