import pyglet
import math
from pyglet import image
from path import *
import matplotlib.pyplot as plt
import numpy as np

class Agent:
    def __init__(self, fstring):
        self.pic = image.load(fstring)
        self.pic.anchor_x = self.pic.width//2
        self.pic.anchor_y = self.pic.height//2
        self.posx = 0
        self.posy = 0
        self.sprite = pyglet.sprite.Sprite(self.pic)
        self.orientation = 0

    def set_location(self, x, y):
        self.posx = x
        self.posy = y

    def render(self):
        self.sprite.set_position(self.posx, self.posy)
        self.sprite.update(rotation=-math.degrees(self.orientation))
        self.sprite.draw()

    def update(self,dt):
        # print(self.posx, self.posy)
        # Hardcoded, for general purpose need to consider point location
        if (self.path[-1].x - self.posx + self.path[-1].y - self.posy < 0.001):
            return
        self.posx += (self.path[0].v+self.path[1].v)/2 * (math.cos(self.orientation)) * dt
        self.posy += (self.path[0].v+self.path[1].v)/2 * (math.sin(self.orientation)) * dt

    def setAtri(self, pts):
        self.path = pts
        if (len(pts) >= 2):
            self.posx = pts[0].x + 50
            self.posy = pts[0].y - 50
            self.orientation = math.atan2(pts[-1].y - pts[0].y, pts[-1].x - pts[0].x)

        return


class JMAgent(Agent):
    def __init__(self, fstring):
        Agent.__init__(self, fstring)
        self.t = 0

    def setAtri(self, pts):
        Agent.setAtri(self, pts)
        self.calculate_quintic_poly()

    def update(self, dt):
        if (self.t > self.time):
            return
        if self.moved_dis > self.total_dis :
            return
        self.t += dt
        self.moved_dis = self.calculate_moved_dist(self.t)
        self.posx = self.path[0].x + math.cos(self.orientation) * self.moved_dis
        self.posy = self.path[0].y + math.sin(self.orientation) * self.moved_dis

    def calculate_moved_dist(self, t):
        dist = 0
        for i in range(6):
            dist += self.poly_a[i] * t**i
        # print(dist)
        return dist

    def calculate_quintic_poly(self):
        p1 = self.path[0]
        p2 = self.path[-1]
        total_dis = math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)
        ave_speed = (p2.v + p1.v)/2
        time = total_dis / ave_speed
        # print(total_dis, ave_speed, time)
        x_dot = total_dis / time
        x_ddot = (p2.v - p1.v) / time
        x_dddot = (p2.a - p1.a) / time

        a_0 = 0
        a_1 = p1.v
        a_2 = p1.a/2.0

        a_3 = 10/(time**2)*(x_dot - p1.v - 0.5*p1.a*time) - 4/time*(x_ddot - p1.a) + 0.5*x_dddot
        a_4 = -15/(time**3)*(x_dot - p1.v - 0.5*p1.a*time) + 7/(time**2)*(x_ddot - p1.a) - 1/time*x_dddot
        a_5 = 6/(time**4)*(x_dot - p1.v - 0.5*p1.a*time) - 3/(time**3)*(x_ddot - p1.a) + 1/(2*(time**2))*x_dddot

        self.poly_a = [a_0, a_1, a_2, a_3, a_4, a_5]

        self.time = time
        self.total_dis = total_dis
        self.moved_dis = 0

    def make_plot(self):
        N = self.time / 0.01
        samples = np.arange(N)*0.01
        fnc = np.vectorize(self.calculate_moved_dist)
        dists = fnc(samples)
        fnc = np.vectorize(lambda x: self.poly_a[1]+ 2*self.poly_a[2]*x + 3*self.poly_a[3]*x**2 + 4 * self.poly_a[4]*x**3 + 5*self.poly_a[5]*x**4)
        vels = fnc(samples)
        fnc = np.vectorize(lambda x: 2*self.poly_a[2] + 6*self.poly_a[3]*x + 12*self.poly_a[4]*x**2 + 20*self.poly_a[5]*x**3)
        accels = fnc(samples)
        fnc = np.vectorize(lambda x: 6*self.poly_a[3] + 24*self.poly_a[4]*x + 60*self.poly_a[5]*x**2)
        jerk = fnc(samples)
        # plt.plot(samples, dists)
        # plt.plot(samples, ((self.path[-1].v + self.path[0].v)/2)*samples)
        # plt.show()

        f, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2,2)
        ax1.plot(samples, dists)
        ax1.set_title("time(s) vs displacement(px)")
        ax1.plot(samples, ((self.path[-1].v + self.path[0].v)/2)*samples)
        ax2.set_title("time(s) vs velocity(px/s)")
        ax2.plot(samples, vels)
        ax3.plot(samples, accels)
        ax3.set_title("time(s) vs acceleration(px/s^2)")
        ax4.plot(samples, jerk)
        ax4.set_title("time(s) vs jerk(px/s^3)")

        plt.show()



