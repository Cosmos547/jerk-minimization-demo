import pyglet
import numpy

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.v = 0
        self.a = 0


class Path:
    def __init__(self, plist):
        self.plist = plist
        self.len = len(plist)
        self.relax()

    def relax(self):
        r = []
        for i in self.plist:
            r.append(i.x)
            r.append(i.y)
        self.vlist = pyglet.graphics.vertex_list(self.len,('v2f', r))
        if (self.len >= 2):
            self.selist = pyglet.graphics.vertex_list(2, ('v2f', (r[0],r[1], r[-2], r[-1])))

    def render(self):
        if (self.len >= 2):
            pyglet.gl.glPointSize(10.0)
            self.selist.draw(pyglet.gl.GL_POINTS)
            pyglet.gl.glPointSize(1.0)
        pyglet.gl.glLineWidth(2.0)
        self.vlist.draw(pyglet.gl.GL_LINES)
        pyglet.gl.glLineWidth(1.0)

