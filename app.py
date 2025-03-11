import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
import time

# Streamlit sidebar controls
st.sidebar.header("Simulation Parameters")
domain_size_x_km = st.sidebar.number_input("Domain width (km)", min_value=4, max_value=16, value=8, step=1)
domain_size_y_km = st.sidebar.number_input("Domain depth (km)", min_value=4, max_value=16, value=8, step=1)
vertical_body_width_km = st.sidebar.number_input("Vertical body width (km)", min_value=0.05, max_value=0.5, value=0.1, step=0.05)
horizontal_body_length_km = st.sidebar.number_input("Horizontal body length (km)", min_value=1, max_value=4, value=2, step=1)
horizontal_body_depth_km = st.sidebar.number_input("Horizontal body width (km)", min_value=0.1, max_value=2.0, value=0.5, step=0.1)

# Temperature settings
T_hot = st.sidebar.number_input("Bodies' Temperature (°C)", min_value=500, max_value=1500, value=1300, step=50)
T_surface = st.sidebar.number_input("Surface Temperature (°C)", min_value=-100, max_value=0, value=-63, step=5)
Tgradient = st.sidebar.number_input("Temperature gradient (°C/km)", min_value=1, max_value=100, value=10, step=5)

# Simulation settings
steps = st.sidebar.number_input("Number of time steps", min_value=1, max_value=4000, value=200, step=50)


# Streamlit setup
st.title("2D Thermal Simulation on Mars")

# Physical and numerical parameters
dx = dy = 50  # Grid spacing (meters)
alpha = 1e-6   # Thermal diffusivity (m^2/s)

# Adaptive time step: Increase dt as the simulation progresses to optimize speed
# dt starts small for stability and increases over time as temperature gradients smooth out
dt_initial = 2 * (dx ** 2) / (4 * alpha) * 0.5
dt = dt_initial  # Initial stable time step  # Stable time step

size_x = int(domain_size_x_km * 1000 / dx)  # Convert domain width to nodes
size_y = int(domain_size_y_km * 1000 / dy)  # Convert domain depth to nodes

temperature = np.zeros((size_x, size_y))

# Set temperature gradient vertically (10°C per km)
depth = np.linspace(0, domain_size_y_km, size_y)
for j in range(size_y):
    temperature[:, j] = T_surface + Tgradient * depth[j]

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

# Define meshgrid for plotting
X = np.linspace(-domain_size_x_km / 2, domain_size_x_km / 2, size_x)
Y = np.linspace(-domain_size_y_km, 0, size_y)
X, Y = np.meshgrid(X, Y)

# Streamlit simulation button
run_simulation = st.sidebar.button("Run Simulation")
if run_simulation:
    progress_bar = st.progress(0)
    plot_placeholder = st.empty()

    # Time stepping loop
    for frame in range(steps):
        # Gradually increase time step as gradients smooth out
        dt = dt_initial * (1 + 0.00 * frame)  # Increase dt by 1% per step, ensuring gradual acceleration
        new_temperature = temperature.copy()

        for i in range(1, size_x - 1):
            for j in range(1, size_y - 1):
                new_temperature[i, j] = temperature[i, j] + alpha * dt / dx**2 * (
                    temperature[i + 1, j] + temperature[i - 1, j] + temperature[i, j + 1] + temperature[i, j - 1] - 4 * temperature[i, j])

        temperature[:] = new_temperature  # Ensure update persists
        progress_bar.progress((frame + 1) / steps)

        # Update plot
        fig, ax = plt.subplots()
        im = ax.imshow(np.flipud(temperature.T), cmap='hot', origin='lower', extent=[-domain_size_x_km/2, domain_size_x_km/2, -domain_size_y_km, 0], vmin=-65, vmax=110)
        cbar = plt.colorbar(im, ax=ax, label='Temperature (°C)', orientation='vertical', aspect=40)
        cbar.ax.invert_yaxis()  # Flip the color bar
        ax.set_xlabel('X (km)')
        ax.set_ylabel('Depth (km)')
        time_years = sum(dt_initial * (1 + 0.01 * i) for i in range(frame + 1)) / 86400 / 365.24  # Convert time to years
        ax.set_title(f'Time: {time_years/1e3:.2f} ky, Step: {frame+1}/{steps}')

        # Add contours for specific temperatures
        contour_0 = ax.contour(X, Y[::-1], temperature.T, levels=[0], colors='blue', linewidths=2)
        contour_100 = ax.contour(X, Y[::-1], temperature.T, levels=[100], colors='green', linewidths=2)
        ax.clabel(contour_0, fmt='T=0', colors='blue', fontsize=10)
        ax.clabel(contour_100, fmt='T=100', colors='green', fontsize=10)

        plot_placeholder.pyplot(fig)
        plt.close(fig)
        time.sleep(0.1)  # Adjust for animation speed
