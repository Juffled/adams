from os import listdir
import pandas as pd
import matplotlib.pyplot as plt
from python.traj_plotter import TrajectoryPlotter

# Variables
trajectory_start_time = 2.5  # start time for trajectory plotting
num_trajectory_rotations = 5  # number of rotations to plot
rotating_speed_rpm = 5000
rotating_hz = rotating_speed_rpm / 60
rotation_time = 1 / rotating_hz
trajectory_end_time = trajectory_start_time + rotation_time * num_trajectory_rotations

# Code
list_of_files = listdir(path='4_data_results_formatted')

#Create an empty database
all_traj = pd.DataFrame()

# Add all the results to it
for formatted_file in list_of_files:
    my_trajectory = TrajectoryPlotter(filepath=f'4_data_results_formatted/{formatted_file}', separator='    ')
    all_traj = pd.concat([all_traj, my_trajectory.formatted_df])

# Take a slice of time
filtered_df = all_traj[all_traj['time'].between(trajectory_start_time, trajectory_end_time)]

# Open a plot window
plt.clf()

# Draw lines on the plot
for sim_id in filtered_df['sim_id'].unique():
    sim_df = filtered_df[(filtered_df['sim_id'] == sim_id)]

    r_x = sim_df['rotorspline_dx']
    r_y = sim_df['rotorspline_dy']

    i_x = sim_df['inputspline_dx']
    i_y = sim_df['inputspline_dy']

    plt.plot(r_x, r_y, label=f'{sim_id}: Rotor Shaft Spline')
    plt.plot(i_x, i_y, label=f'{sim_id}: Input Shaft Spline')

# Plot formatting and save
plt.title(f'Spline Trajectory' )
plt.xlabel("X [mm]")
plt.ylabel("Y [mm]")
plt.legend(loc="upper left", fancybox=True)
plt.gca().set_aspect('equal')
plt.savefig(f"./8_trajectory_plots/all_trajectory.png")