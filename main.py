import pyglet
import numpy as np
import scipy
from path import *
from agent import *

pyglet.options['debug_gl']=False

config = pyglet.gl.Config(sample_buffers=1, samples=4)
window = pyglet.window.Window(width=640, height=640, config=config)
p1 = Point(40.0, 40.0)
p1.v = 200
p2 = Point(600.0, 600.0)
p2.v = 400
path = Path([p1, p2])
agent = Agent('car_agent.png')
agent.setAtri(path.plist)

jmagent = JMAgent('car_agent.png')
jmagent.setAtri(path.plist)
# print(jmagent.poly_a)

# jmagent.make_plot()

@window.event
def on_draw():
    window.clear()
    path.render()
    # agent.render()
    jmagent.render()
    # print(pyglet.clock.get_fps())

def update(dt):
    jmagent.update(dt)
    agent.update(dt)
    # agent.sprite.x += dt*10
    # print(dt)
    return

pyglet.clock.schedule_interval(update, 1/60.0)

pyglet.app.run()
