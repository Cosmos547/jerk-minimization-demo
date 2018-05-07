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
p1.a = 30
p2 = Point(600.0, 600.0)
p2.v = 400
p2.a = 50
path = Path([p1, p2])
agent = Agent('car_agent.png')
agent.setAtri(path.plist)
frame = 0

jmagent = JMAgent('car_agent.png')
jmagent.setAtri(path.plist)
# print(jmagent.poly_a)

jmagent.make_plot()

@window.event
def on_draw():
    window.clear()
    path.render()
    agent.render()
    jmagent.render()
    # print(pyglet.clock.get_fps())

def update(dt):
    global frame
    jmagent.update(dt)
    agent.update(dt)
    # if (jmagent.end and agent.end):
        # return
    # file_num = str(frame).zfill(5)
    # filename="frame"+file_num+'.png'
    # pyglet.image.get_buffer_manager().get_color_buffer().save(filename)
    # frame+=1
    # agent.sprite.x += dt*10
    # print(dt)
    return

pyglet.clock.schedule_interval(update, 1/60.0)

pyglet.app.run()
