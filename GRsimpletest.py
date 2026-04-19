import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# -----------------------
# Parameters
# -----------------------
M = 1.0
impact = 6.0  # impact parameter b

# Energy normalization (for photons, only ratio matters)
E = 1.0
L = impact

# -----------------------
# System: first-order form
# y = [u, du/dphi]
# -----------------------
def geodesic(phi, y):
    u, up = y  # u = 1/r

    dudphi = up
    duphi = -u + 3 * M * u**2

    return [dudphi, duphi]

# -----------------------
# Initial conditions
# r0 large => nearly straight line
# -----------------------
r0 = 30.0
u0 = 1 / r0

# initial slope from impact parameter
up0 = -np.sqrt((1 / impact**2) - u0**2)

y0 = [u0, up0]

# integrate
sol = solve_ivp(
    geodesic,
    [0, 10 * np.pi],
    y0,
    max_step=0.01,
    rtol=1e-9
)

phi = sol.t
u = sol.y[0]
r = 1 / u

# -----------------------
# Convert to Cartesian
# -----------------------
x = r * np.cos(phi)
y = r * np.sin(phi)

# -----------------------
# Plot
# -----------------------
plt.figure(figsize=(6, 6))
plt.plot(x, y, label="Photon path")
plt.scatter([0], [0], s=200, label="Black Hole")
plt.gca().set_aspect("equal")
plt.xlabel("x")
plt.ylabel("y")
plt.title("Schwarzschild Photon Geodesic")
plt.legend()
plt.show()

r_s = 100
r = np.arange(0,1000,1)
theta = np.arange(0,2*np.pi, 0.1)

r,theta = np.meshgrid(r,theta)
z = 2 * np.sqrt(r_s * (r + 1))
x,y = r * np.cos(theta), r * np.sin(theta)

fig = plt.figure()
ax = fig.add_subplot(projection = '3d')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

ax.plot_surface(x,y,z)



