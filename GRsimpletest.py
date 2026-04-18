import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Black hole mass (supermassive scale)
M = 1.0   # mass parameter (G=c=1)

def geodesic(lam, y):
    t, r, phi, pt, pr, pphi = y
    
    # Metric terms
    f = 1 - 2*M/r
    
    # Geodesic equations (Schwarzschild, equatorial plane)
    dt = pt / f
    dr = pr * f
    dphi = pphi / r**2
    
    # Momentum derivatives
    dpt = 0
    dpphi = 0
    
    dpr = (
        -M/(r**2*f)*pt**2
        + M/(r**2*f)*pr**2
        + (r - 3*M)/r**4 * pphi**2
    )
    
    return [dt, dr, dphi, dpt, dpr, dpphi]


# Initial conditions (incoming photon)
r0 = 20
phi0 = 0
t0 = 0

impact = 6.0     # impact parameter

pt0 = 1.0
pphi0 = impact

# Null condition (lightlike)
pr0 = -np.sqrt(pt0**2 - (1 - 2*M/r0)*(pphi0**2 / r0**2))

y0 = [t0, r0, phi0, pt0, pr0, pphi0]

# Integrate
sol = solve_ivp(
    geodesic,
    [0, 200],
    y0,
    max_step=0.1,
    rtol=1e-8
)

r = sol.y[1]
phi = sol.y[2]

# Convert to Cartesian
x = r * np.cos(phi)
y = r * np.sin(phi)

# Plot
plt.figure(figsize=(6,6))
plt.plot(x, y, label="Light path")
plt.scatter([0],[0], s=200, label="Black Hole")
plt.gca().set_aspect('equal')
plt.legend()
plt.xlabel("x")
plt.ylabel("y")
plt.title("Photon Geodesic Around Supermassive Object")
plt.show()


r_s = 1
x = np.arange(0,10,0.1)
y = np.arange(0,2*np.pi, 0.1)
x,y = np.meshgrid(x,y)


z = 2 * np.sqrt(r_s * (x - r_s))
# plt.plot(x,y)
# plt.show()
x,y = x * np.cos(y), x * np.sin(y)
fig = plt.figure()
ax = fig.add_subplot(projection = '3d')
ax.plot_surface(x,y,z)
plt.show()
