import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import time

# Streamlit setup
st.title("2D Thermal Simulation on Mars")

# Geometry definitions (in km)
domain_size_x_km = 8  # Domain width in km
domain_size_y_km = 8  # Domain depth in km
vertical_body_width_km = 0.1  # Vertical hot body width in km
horizontal_body_length_km = 2  # Horizontal hot body length in km
horizontal_body_depth_km = 0.5  # Horizontal hot body depth in km

# Initial temperature distribution
T_hot = 1300
T_surface = -63  # Surface temperature (°C)

steps = 200  # Number of steps for simulation

# Physical and numerical parameters
dx = dy = 50  # Grid spacing (meters)
alpha = 1e-6   # Thermal diffusivity (m^2/s)

# Stability criterion
dt = 2 * (dx ** 2) / (4 * alpha) * 0.5  # Stable time step

size_x = int(domain_size_x_km * 1000 / dx)  # Convert domain width to nodes
size_y = int(domain_size_y_km * 1000 / dy)  # Convert domain depth to nodes

temperature = np.zeros((size_x, size_y))

# Set temperature gradient vertically (10°C per km)
depth = np.linspace(0, 8, size_y)
for j in range(size_y):
    temperature[:, j] = T_surface + 10 * depth[j]

# Central vertical rectangle 
x_center = size_x // 2
width = int(vertical_body_width_km * 1000 / dx)  # Convert width to nodes
temperature[x_center - width//2:x_center + width//2, :] = T_hot

# Horizontal hot body at top (0-1 km depth, x_center to x_center+2 km)
x_start = x_center
x_end = x_start + int(horizontal_body_length_km * 1000 / dx)  # Convert to nodes
y_start = 0
y_end = int(horizontal_body_depth_km * 1000 / dy)  # Convert to nodes
temperature[x_start:x_end, y_start:y_end] = T_hot  # Set hot region

# Ensure top boundary remains at T_surface
temperature[:, 0] = T_surface

# Streamlit progress bar
progress_bar = st.progress(0)
plot_placeholder = st.empty()

# Time stepping loop
for frame in range(steps):
    new_temperature = temperature.copy()

    for i in range(1, size_x - 1):
        for j in range(1, size_y - 1):
            new_temperature[i, j] = temperature[i, j] + alpha * dt / dx**2 * (
                temperature[i + 1, j] + temperature[i - 1, j] + temperature[i, j + 1] + temperature[i, j - 1] - 4 * temperature[i, j])

    temperature[:] = new_temperature  # Ensure update persists
    progress_bar.progress((frame + 1) / steps)
    
    # Update plot
    fig, ax = plt.subplots()
    im = ax.imshow(temperature.T, cmap='hot', origin='upper', extent=[-4, 4, -8, 0], vmin=-70, vmax=10)
    cbar = plt.colorbar(im, ax=ax, label='Temperature (°C)')
    ax.set_xlabel('X (km)')
    ax.set_ylabel('Depth (km)')
    time_years = (frame + 1) * dt / 86400 / 365.24  # Convert time to years
    ax.set_title(f'Time: {time_years/1e3:.2f} ky, Step: {frame+1}/{steps}')
    
    # Add contours for specific temperatures
    contour_0 = ax.contour(X, Y[::-1], temperature.T, levels=[0], colors='blue', linewidths=2)
    contour_100 = ax.contour(X, Y[::-1], temperature.T, levels=[100], colors='green', linewidths=2)
    ax.clabel(contour_0, fmt='T=0', colors='blue', fontsize=10)
    ax.clabel(contour_100, fmt='T=100', colors='green', fontsize=10)

        plot_placeholder.pyplot(fig)
        plt.close(fig)
        time.sleep(0.1)  # Adjust for animation speed

# Final plot with contours
fig, ax = plt.subplots()
X = np.linspace(-4, 4, size_x)
Y = np.linspace(-8, 0, size_y)
X, Y = np.meshgrid(X, Y)
im = ax.imshow(temperature.T, cmap='hot', origin='upper', extent=[-4, 4, -8, 0], vmin=-70, vmax=10)
cbar = plt.colorbar(im, ax=ax, label='Temperature (°C)')
ax.set_xlabel('X (km)')
ax.set_ylabel('Depth (km)')
ax.set_title(f'Final Temperature Distribution\nTime: {time_years/1e3:.2f} ky, Steps: {steps}')

# Add contours for specific temperatures
        contour_0 = ax.contour(X, Y[::-1], temperature.T, levels=[0], colors='blue', linewidths=2)
        contour_100 = ax.contour(X, Y[::-1], temperature.T, levels=[100], colors='green', linewidths=2)
        ax.clabel(contour_0, fmt='T=0', colors='blue', fontsize=10)

# Add contours for specific temperatures
        contour_0 = ax.contour(X, Y[::-1], temperature.T, levels=[0], colors='blue', linewidths=2)
        contour_100 = ax.contour(X, Y[::-1], temperature.T, levels=[100], colors='green', linewidths=2)
        ax.clabel(contour_0, fmt='T=0', colors='blue', fontsize=10)
        ax.clabel(contour_100, fmt='T=100', colors='green', fontsize=10)

plot_placeholder.pyplot(fig)
plt.close(fig)
