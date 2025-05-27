import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
#%%
df = pd.read_csv("../Data/RawLiftingData.csv")
#%%
#Creating a figure with a width and height of 10 and 7
fig = plt.figure(figsize=(10,7))
#Forcing 3D projection, creating only 1 plot
chart = fig.add_subplot(111, projection='3d')

#Creating the xyz variables
x = df['Time']
y = df['PR']
z = df['BodyWeight']

#Creating scatter plot, using the xyz variables, with the plasma color gradient and a dot size of 60
scatter = chart.scatter(x,y,z, c=z, cmap='Blues', s=60)

#Creating the axes labels
chart.set_xlabel('Time')
chart.set_ylabel('PR')
chart.set_zlabel('Body Weight')

#Showing the plotting
#Adding a legend to show color
fig.colorbar(scatter, label='Bench PR')
#Showing data
plt.show()
#%%
#Creating independent and dependant variables
#Independent
x1 = df['Time']
x2 = df['BodyWeight']

#Dependent
y = df['PR']

#Creating the 2D array.
xMatrix = np.column_stack((x1, x2))

#Printing the 2D array.
print("xMatrix shape:", xMatrix.shape)
print("xMatrix:\n", xMatrix[:49])
#%%
#Creating the empty model
model = LinearRegression()

#Calculating regression, just like the m = n∑(xy) - ∑(x)∑(y) / n∑x^2 - ∑x^2, then the b portion as well. Using that formula, to calculate our regression formula.
#However with a third variable added. Using the normal equation and matricies instead. With the matrix X being xMatrix and y being our y column of data in the CSV
# β̂ = (XᵗX)⁻¹ Xᵗy
model.fit(xMatrix, y)

#Getting our intercept from the model, b0 of y = b0 + b1(x1) + b2(x2)
b0 = model.intercept_
#Getting our slopes from the model
b1, b2 = model.coef_

#Printing our regression equation
print(f"Equation: BenchPressPR = {b0:.2f} + {b1:.2f} * Time + {b2:.2f} * BodyWeight")
#Along with our R score, with model.predict being the above equation implemented in code form
#r2 being the regression coeffecient
yHat = model.predict(xMatrix)
r2 = r2_score(y, yHat)
print(f"R² Score: {r2:.4f}")
#%%
#Creating the regression plane

#Creating the dimensions of the plane, via bounds of each column
xRange = np.linspace(x.min(), x.max(), 49)
zRange = np.linspace(z.min(), z.max(), 49)

#Creating a grid of all values
xGrid, zGrid = np.meshgrid(xRange, zRange)

#Compressing both grids into a 1D array
xFlat = xGrid.ravel()
zFlat = zGrid.ravel()

#Making both into a new matrix, like, time1,time1,time1,time1,infinity... weight1,weight2,weight3,weight4, etc.
#Until time2,time2,time2,infinity, weight1,weight2,weight3, etc.
gridInput = np.column_stack((xFlat, zFlat))

#New yHat! Because now were using the new matrix created from flattening the xGrid and zGrid,
#and using that as the matrix for the normal equation, gridInput is now our X in β̂ = (XᵗX)⁻¹ Xᵗy
finalYHat = model.predict(gridInput)

#Creating the regression plane. We are using the shape of xGrid to make sure
#That Y grid has the same dimensions as the xGrid
yGrid = finalYHat.reshape(xGrid.shape)
#%%
#Plotting Regression Plane

#Creating a figure with a width and height of 10 and 7
fig = plt.figure(figsize=(10,7))
#Forcing 3D projection, creating only 1 plot
chart = fig.add_subplot(111, projection='3d')

#Creating the xyz variables
x = df['Time']
y = df['PR']
z = df['BodyWeight']

#Creating scatter plot, using the xyz variables, with the plasma color gradient and a dot size of 60
scatter = chart.scatter(x,y,z, c=z, cmap='Blues', s=60)

#Plotting the regression plane
chart.plot_surface(xGrid, yGrid, zGrid, alpha=0.9, color='red')


#Creating the axes labels
chart.set_xlabel('Time')
chart.set_ylabel('PR')
chart.set_zlabel('Body Weight')

#Adjusting view
chart.view_init(elev=40, azim=195)

#Showing the plotting
#Adding a legend to show color
fig.subplots_adjust(right=0.85)
cbar = fig.colorbar(scatter, pad=0.1)
cbar.set_label('Bench PR')
#Showing data
plt.show()