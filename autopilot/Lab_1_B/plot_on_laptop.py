import numpy as np
import matplotlib.pyplot as plt

# Replace 'path_to_grid.txt' with the path to the transferred file on your desktop
# grid = np.loadtxt('/Users/jo6109072/Desktop/grid_2.txt')
grid = np.loadtxt('/Users/jo6109072/Downloads/grid_1.txt')
grid[grid == 3] = 0
grid[[len(grid)//2, 0]] = 3
grid = np.transpose(grid)
plt.figure(figsize=(8, 8))
plt.title("Advanced Mapping")
plt.imshow(grid, cmap='gray', origin='lower')
plt.colorbar()
plt.show()
