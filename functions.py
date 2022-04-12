"""
"""
import numpy as np
import pandas as pd

def thermal_diffusivity(temp_z, z, interfaces, H, dt, dz, kappa, ccapacity):
    """
    Apply the thermal diffusivity
    """
    cond = (z < interfaces["litho"][0]) | (temp_z == 0)
    temp_aux = np.copy(temp_z)
    t = 0
    dt_sec = dt * 365 * 24 * 3600
    while t < 500.0e6:
        temp_z[1:-1] += (
            kappa * dt_sec * ((temp_z[2:] + temp_z[:-2] - 2 * temp_z[1:-1]) / dz ** 2)
            + H[1:-1] * dt_sec / ccapacity
        )
        temp_z[cond] = temp_aux[cond]
        t = t + dt
    return temp_z
    
def load_time(filename):
    time = np.loadtxt(filename, dtype="str")
    time = time[:, 2:]
    return time.astype("float")

def load_data(filename, nx, nz):
    """
    rho, strain, temp, 
    """
    data = pd.read_csv(
        filename,
        delimiter=" ",
        comment="P",
        skiprows=2,
        header=None,
    )
    data = data.to_numpy()
    data[np.abs(data) < 1.0e-200] = 0
    data = np.reshape(data, (nx, nz), order="F")
    return np.transpose(data)

def load_velocity(filename, nx, nz):
    veloc = pd.read_csv(
        filename,
        delimiter=" ",
        comment="P",
        skiprows=2,
        header=None,
    )
    veloc = veloc.to_numpy()
    veloc_x = np.reshape(veloc[0::2], (nx, nz), order="F")
    veloc_z = np.reshape(veloc[1::2], (nx, nz), order="F")
    return veloc_x, veloc_z

# Create the colors to plot the density
cr = 255.0
color_upper_crust = (228.0 / cr, 156.0 / cr, 124.0 / cr)
color_lower_crust = (240.0 / cr, 209.0 / cr, 188.0 / cr)
color_lithosphere = (155.0 / cr, 194.0 / cr, 155.0 / cr)
color_asthenosphere = (207.0 / cr, 226.0 / cr, 205.0 / cr)
colors = [
    color_upper_crust, 
    color_lower_crust, 
    color_lithosphere, 
    color_asthenosphere
]