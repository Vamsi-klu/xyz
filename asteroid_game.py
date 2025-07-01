import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Wave parameters
num_waves = 3  # Number of wave components
amplitude = [0.5, 0.3, 0.2]  # Wave heights
wavelength = [2.0, 1.5, 1.0]  # Wave lengths
direction = [0, np.pi/4, -np.pi/6]  # Wave directions (radians)
phase = [0.0, 0.5, 1.0]  # Phase offsets
speed = [1.0, 0.8, 1.2]  # Wave speeds

# Simulation parameters
x = np.linspace(-10, 10, 500)  # X-axis coordinates
t = 0  # Time variable

# Set up figure
fig, ax = plt.subplots(figsize=(10, 4))
ax.set_xlim(-10, 10)
ax.set_ylim(-1, 1)
ax.set_facecolor('navy')
line, = ax.plot([], [], lw=2, color='cyan')

# Initialization function
def init():
    line.set_data([], [])
    return line,

# Update function for animation
def update(frame):
    global t
    t += 0.1
    
    # Calculate Gerstner wave components
    y = np.zeros_like(x)
    for i in range(num_waves):
        k = 2 * np.pi / wavelength[i]  # Wave number
        omega = np.sqrt(9.81 * k)  # Angular frequency
        angle = k * x * np.cos(direction[i]) - omega * t + phase[i]
        
        # Gerstner wave displacement
        y += amplitude[i] * np.sin(angle)
        
        # Add directional component
        x_steepness = 0.5 * amplitude[i] * k
        dx = x_steepness * np.cos(angle)
        x_disp = np.cumsum(dx) * (x[1] - x[0])
        x_disp -= x_disp.mean()
        
        line.set_data(x + x_disp, y)
    
    # Add additional wave components
    line.set_data(x + x_disp, y + 0.2 * np.sin(2 * x + 0.5 * t))
    
    return line,

# Create animation
ani = FuncAnimation(fig, update, frames=200, init_func=init, blit=True, interval=50)

plt.show()