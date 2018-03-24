import pyglet
import numpy as np
from pyglet.gl import *

window = pyglet.window.Window()

label = pyglet.text.Label("Hello world", font_name='Times New Roman',
                          font_size=36,
                          x=window.width//2, y=window.height//2,
                          anchor_x='center', anchor_y='center')

class Wave():
    def __init__(self):
        self.xpos = window.width
        self.ypos = window.height/2
        self.xstep = 3
        self.reflected = np.zeros(window.width//self.xstep)
        self.array = np.zeros(3*window.width//self.xstep)
        self.t = 0

    def draw(self):
        for i in range(0, window.width//self.xstep):
            total = self.array[-window.width//self.xstep:-1] + self.reflected
            glBegin(GL_LINES)
            if i >= len(self.array)-1:
                glVertex2f(self.xpos - self.xstep*i, self.ypos)
                glVertex2f(0, self.ypos)
                glEnd()
                break
            glVertex2f(self.xpos - self.xstep*i, total[-i+1] + self.ypos)
            glVertex2f(self.xpos - self.xstep*(i+1), total[-i] + self.ypos)
            glEnd()

    def tick(self, dt):
        self.t += self.xstep/window.width*np.pi
        self.array = np.append(self.array, np.sin(self.t)*100)
        if len(self.array) > window.width//self.xstep:
            self.reflected = -self.array[-2*window.width//self.xstep:-window.width//self.xstep]
            self.reflected = self.reflected[::-1]
        



@window.event
def on_key_press(symbol, modifiers):
    print("a key was pressed")
    
wave = Wave()
fps_display = pyglet.clock.ClockDisplay()
@window.event
def on_draw():
    window.clear()
    fps_display.draw()
    wave.draw()

def update(dt):
    wave.tick(dt)

pyglet.clock.schedule_interval(update, 1/60.0)

pyglet.app.run()
