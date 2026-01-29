import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

theta = np.deg2rad(70)
v = 20
y = [5]
x = [5]
g = -9.81
dt = 0.01
t = [0]
bounces = 0
e = 0.6

#horizontal
vh = [v * np.cos(theta)]

#vertical
vv = [v * np.sin(theta)]

while t[-1] < 10:
    vv.append(vv[-1] + g * dt)
    y.append(y[-1] + vv[-1] * dt)
    vh.append(vh[-1])
    x.append(x[-1] + vh[-1] * dt)
    t.append(t[-1] + dt)

    if y[-1] < 0:
        y[-1] = 0
        vv[-1] = -vv[-1] * e
        bounces += 1

    
# plt.plot(t, vv, label = "y velocity")
# plt.plot(t, y, label = "y displacement")
# plt.plot(t, x, label = 'x displacement')
# plt.plot(t, vh, label = 'x velocity')
# plt.legend()
# plt.figtext(0.75,0.6,"{} bounces".format(bounces))
# plt.grid()
# plt.show()

fig, ax = plt.subplots()
ax.set_xlim(0, max(x)+5)
ax.set_ylim(0, max(y)+5)
ax.set_aspect("equal")

ball = plt.Circle((x[0], y[0]), 1)
ax.add_patch(ball)

def update(frame):
    ball.center = (x[frame], y[frame])
    return ball,

ani = FuncAnimation(
    fig,
    update,
    frames = len(t),
    interval = dt*1000,
    blit = True
)

plt.show()