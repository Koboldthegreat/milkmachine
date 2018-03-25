import numpy as np
from pyglet.gl import *
import sound


class Sprite():
    def __init__(self, window):
        self.window_width = window.width
        self.window_height = window.height
        self.xpos = window.width
        self.ypos = window.height / 2

class Wave(Sprite):
    def __init__(self, window, xstep=4):
        super().__init__(window)
        self.xstep = xstep
        self.reflected = np.zeros(self.window_width // self.xstep)
        self.array = np.zeros(3 * self.window_width // self.xstep)
        self.t = 0
        self.last = self.t

    def draw(self):
        total = self.array[-self.window_width // self.xstep:] + self.reflected
        for i in range(0, len(total)-1):
            glBegin(GL_LINES)
            glVertex2f(self.xpos - self.xstep * i,
                       total[-i-1] + self.ypos)
            glVertex2f(self.xpos - self.xstep * (i + 1),
                       total[-i-2] + self.ypos)
            glEnd()

class StandingWave(Wave):
    def update(self, dt):
        self.t += self.xstep / self.window_width * np.pi
        self.array = np.append(self.array, np.sin(self.t) * 100)
        if len(self.array) > self.window_width // self.xstep:
            self.reflected = -self.array[-2 * self.window_width // self.xstep:
                                         -self.window_width // self.xstep]
            self.reflected = self.reflected[::-1]

class SoundStandWave(Wave):
    def __init__(self, window):
        super().__init__(window, xstep=1)

    def update(self, dt):
        dt = dt
        self.t += dt
        freq = 1
        w = 2*np.pi*freq
        self.array = np.append(self.array, 100*np.sin(w*np.linspace(self.last, self.t, num=dt*self.window_width//self.xstep, endpoint=False)))
        if len(self.array) > self.window_width // self.xstep:
            self.reflected[:] = -self.array[-2 * self.window_width//self.xstep-1:
                                         -self.window_width // self.xstep-1]
            self.reflected[:] = self.reflected[::-1]
        if len(self.array) > 2*self.window_width // self.xstep:
            self.reflected[:] -= self.array[-3 * self.window_width//self.xstep-1:
                                         -2*self.window_width//self.xstep-1]
            pass

        self.last = self.t


class SoundWave(Wave):
    def __init__(self, sound_data, *args):
        self.sound_data = sound_data
        self.last = 0
        self.playing = False
        super().__init__(*args)
        self.t = len(self.sound_data)
        self.last = self.t
        self.plast = 0

    def update(self, dt, keys):
        if self.t < len(self.sound_data):
            self.t += int(dt * sound.SAMPLE_FREQ)
            self.array = np.append(self.array, self.sound_data[self.last:self.t] * 100)
            self.last = self.t
        if self.plast < len(self.sound_data)-1:
            sound.play(self.sound_data[self.plast:])
            self.plast = len(self.sound_data)-1

    def play(self, tone):
        if self.t >= len(self.sound_data):
            print(tone % 25)
            self.sound_data = np.append(self.sound_data, sound.artone(np.array([tone % 25]*(sound.SAMPLE_FREQ//4)), sound.SAMPLE_FREQ))

class KeyWave(Wave):
    def update(self, dt, down):
        self.array = np.append(self.array, down * 100)


class MainWindow(pyglet.window.Window):
    def __init__(self):
        super().__init__()
        self.label = pyglet.text.Label("Milkmachine")
        self.label.x = 0
        self.label.y = self.height - 10
        self.fps_display = pyglet.clock.ClockDisplay()
        self.wave = SoundStandWave(self)
        self.pause = False
        self.d = False
        self.line = {"width": 1, "color": (1.0, 1.0, 1.0)}
        self.keys = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys)

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.P:
            self.pause = not self.pause
        #elif symbol == pyglet.window.key.R:
        #    pass
        #self.wave.play(symbol)
        pass

    def on_draw(self):
        glLineWidth(self.line["width"])
        glColor3f(*self.line["color"])
        self.clear()
        self.label.draw()
        self.fps_display.draw()
        self.wave.draw()

    def update(self, dt):
        if not self.pause:
            self.wave.update(dt)

    @staticmethod
    def start():
        window = MainWindow()
        pyglet.clock.schedule_interval(window.update, 1 / 60.0)
        pyglet.app.run()
        return window

    def on_resize(self,width, height):
        self.wave.__init__(self)
        glViewport(0, 0, width, height)
        glMatrixMode(gl.GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)
        glMatrixMode(gl.GL_MODELVIEW)



if __name__ == "__main__":
    mainwindow = MainWindow.start()
