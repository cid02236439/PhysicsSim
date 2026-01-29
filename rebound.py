# import pandas as pd
# import statsmodels.api as sm

# data = pd.read_csv("/Users/praneshdara/Documents/simspractice/Startups.csv")

# y = data['Profit']
# x = sm.add_constant(data['R&D Expenditure'])

# results = sm.OLS(y,x).fit()
# print(results.summary())

# prediction = results.predict([1,125000])
# print(prediction)

import rebound
import matplotlib.pyplot as plt

sim = rebound.Simulation()
sim.add(m=1.0)

n= 10
for i in range(n):
    sim.add(m=1.0e-3, a=1.0 + i * 0.1)

sim.move_to_com()

sim.integrate(10.0)
rebound.OrbitPlot(sim)
plt.show()
